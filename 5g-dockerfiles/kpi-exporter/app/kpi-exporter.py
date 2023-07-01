#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author: Niloy Saha
# Email: niloysaha.ns@gmail.com
# version ='1.1.0'
# ---------------------------------------------------------------------------
"""
Prometheus exporter which exports slice throughput KPI.
"""
import requests
import pandas as pd
import json
import prometheus_client as prom
# disable annoying warning message
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

import logging
import time

# setup logger for console output
console_logger = logging.getLogger(__name__)
console_logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] [%(filename)s] %(message)s'))
console_logger.addHandler(console_handler)

PROMETHEUS_URL = "http://129.97.168.51:30090"
ELASTICSEARCH_URL = "https://129.97.26.28:31920/"
ELASTIC_INDEX = "logstash-filebeat"  # this index stores slice information from the SMF
ELASTIC_QUERY_URL = ELASTICSEARCH_URL + ELASTIC_INDEX + "/_search?pretty=true&filter_path=hits.hits*"

# PARAMS = {'query': "pdr_packet_count"}  # get last data point (instant vector)
PROM_PARAMS = {'query': 'deriv(pdr_byte_count[10s]) > 0'}  # per-second derivative of range vector

ES_PARAMS = {   
    "size": 50,
    "sort": { "@timestamp": "desc"},
    "_source": "false",
    "query" : {
            "match_all" : {}
        },
        "fields": ["S-NSSAI", "slice-session-info.PFCPSession.PDRs.PDRId", "slice-session-info.PFCPSession.PDRs.Fteid.GTPIPAddress", "slice-session-info.PFCPSession.Fseid.LocalSEID","slice-session-info.PFCPSession.Fseid.IPAddress", "slice-session-info.PduSession.DataNetworkName"]
}

HEADERS = {'Content-type': 'application/json'}

# Prometheus variables
SLICE_THROUGHPUT = prom.Gauge('slice_throughput', 'Throughput (bytes) per slice', ['snssai', 'seid', 'direction'])
UP = False  # flag to track status

# get rid of bloat
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)

UPDATE_PERIOD = 1
EXPORTER_PORT = 9000


def sanitize_prometheus_response(data):
    """ Take a prometheus result and transform it into a pandas dataframe """
    result = data["data"]["result"]

    d_list = []  # list of dict, where each dict is a row in pandas dataframe
    for item in result:
        d = {}
        labels = item["metric"]
        d["direction"] = labels["direction"]
        d["pdrid"] = int(labels["pdrid"])
        d["seid"] = int(labels["seid"])
        d["value"] = float(item["value"][1])
        d["n3_ipaddr"] = labels["n3_ipaddr"]
        d["n4_ipaddr"] = labels["n4_ipaddr"]
        d_list.append(d)

    df = pd.DataFrame(d_list)
    return df

def sanitize_elastic_response(result):
    """ Sanitize Elasticsearch result and transform it into a Pandas dataframe """

    # drop useless columns
    df = pd.json_normalize(result["hits"]["hits"]).drop(columns=["_index", "_id", "_score", "_ignored", "sort"])

    # drop NaN values
    df = df.dropna()

    # rename columns to make them easier to work with
    df.columns = ["n3_ipaddr", "dnn", "seid", "n4_ipaddr", "snssai", "pdrid"]

    def sanitize_column(col):
        """ Each col is a list containting a single element. Extract the element """
        df[col] = df[col].apply(lambda x: next(s for s in x if s))

    sanitize_column("dnn")
    sanitize_column("n3_ipaddr")
    sanitize_column("seid")
    sanitize_column("n4_ipaddr")
    sanitize_column("snssai")

    df = df.explode("pdrid")
    return df

def send_queries():
    """ send queries to both Elastic and Prometheus to collect necessary data for slice throughput KPI computation """

    r = requests.get(url=PROMETHEUS_URL + '/api/v1/query', params=PROM_PARAMS)
    data = r.json()
    prom_df = sanitize_prometheus_response(data)
    console_logger.debug("Prometheus")
    console_logger.debug(prom_df)

    if prom_df.empty:
        console_logger.warning('Prometheus dataFrame is empty! Check if UFP exporter is running!')
        global UP
        if UP:
            console_logger.debug("Clearing stale values in Prometheus")
            SLICE_THROUGHPUT.clear()
            UP = False
        return




    es_json_params = json.dumps(ES_PARAMS)
    r = requests.get(ELASTIC_QUERY_URL, headers=HEADERS, auth=('n6saha', 'password'), data=es_json_params,  verify=False)
    data = r.json()
    es_df = sanitize_elastic_response(data)
    console_logger.debug("ElasticSearch")
    console_logger.debug(es_df)

    if es_df.empty:
        console_logger.warning('ES dataFrame is empty! Check if SMF exporter is running!')
        return

   

    try:
        # merge should get rid of old ES entries
        # since prom should only be collecting information about active series
        merged_df = prom_df.merge(es_df, on=["n3_ipaddr", "pdrid"])
        merged_df = merged_df.drop_duplicates() 
        console_logger.debug(merged_df)
        return merged_df
    except:
        console_logger.error('Merging dataframes from ES and Prometheus failed!')
        return

def get_slice_throughput(df):
    result = df.groupby(["snssai", "direction"])["value"].sum()
    console_logger.debug(result)  # prints dataframe

def get_slice_x1_throughput_downlink(df):
    """ 
    get slice throughput from slice with SNSSAI 1@010203 on downlink
    used to compare with iperf test
    """
    mask = (df["snssai"] == "1@010203") & (df["direction"] == "downlink")
    result = df[mask]["value"].sum()
    result_mbits = (float(result) * 8) / (10 ** 6)
    print("{} Mbits/sec".format(result_mbits))

def get_slice_x1_throughput_uplink(df):
    """ 
    get slice throughput from slice with SNSSAI 1@010203 on uplink
    used to compare with iperf test
    """
    mask = (df["snssai"] == "1@010203") & (df["direction"] == "uplink")
    result = df[mask]["value"].sum()
    result_mbits = (float(result) * 8) / (10 ** 6)
    console_logger.debug("{} Mbits/sec".format(result_mbits))

    


def get_per_session_throughput(df):
    """ get slice throughput per PDU session """
    result = df.groupby(["snssai", "seid_x", "direction"])["value"].sum()
    result_bits = result.multiply(8)
    result_mbits = result_bits.divide(10**6)
    # print(result_mbits)  # prints dataframe
    return result

def get_per_session_throughput_groups(df):
    """ get slice throughput per PDU session """
    groups = df.groupby(["snssai", "seid_x", "direction"])["value"]
    return groups


def run_kpi_computation():
    df = send_queries()
    if df is None:
        console_logger.warning("No data available!")
        return
    groups = get_per_session_throughput_groups(df)
    export_to_prometheus(groups)
    console_logger.info("Exporter is running ...")


def export_to_prometheus(groups):

    # set flag to indicate we are exporting metrics
    global UP
    UP = True

    for labels, group in groups:
        snssai, seid, direction = labels
        value = group.sum()
        value_bits = value * 8.0
        value_mbits = round(value_bits / 10 ** 6, 6)
        console_logger.info(f"SNSSAI={snssai} | SEID={seid:2d} | DIR={direction:8s} | RATE (Mbps)={value_mbits}")
        SLICE_THROUGHPUT.labels(snssai=snssai, seid=seid, direction=direction).set(value_mbits)

def main():
    console_logger.info("Starting Prometheus server on port {}".format(EXPORTER_PORT))
    console_logger.info(f"Update period: {UPDATE_PERIOD}")
    prom.start_http_server(EXPORTER_PORT)

    while True:
        run_kpi_computation()
        time.sleep(UPDATE_PERIOD)


if __name__ == "__main__":
    main()
    
    



