#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author: Niloy Saha
# Email: niloysaha.ns@gmail.com
# version ='2.0.0'
# ---------------------------------------------------------------------------
"""
Exporter which exports UPF PDR statistics from Free5gc UPF and writes them to /var/log/upf_stats.json
Depends on the libgtp5gnl project.
"""
import subprocess as subproc
import re
import time
import datetime
import json
import logging
from logging.handlers import RotatingFileHandler


UPF_STATS_FILE = "/var/log/upf_stats.log"
UPDATE_PERIOD = 1  # seconds
CURRENT_STATS = []  # hold current (one update period) stats for **all** PDRs


# setup logger for console output
console_logger = logging.getLogger(__name__)
console_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] [%(filename)s] %(message)s'))
console_logger.addHandler(console_handler)

# setup logger for writing UPF stats to file
stats_logger = logging.getLogger('stats_logger')
stats_logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler(UPF_STATS_FILE, maxBytes=2*10**6, backupCount=3)
stats_logger.addHandler(file_handler)


def get_active_pdrs():
    """
    Returns list of dictionaries, each containing pdrid and seid.
    """
    try:

        completed_proc = subproc.run(["/free5gc/libgtp5gnl/tools/gtp5g-tunnel", "list", "pdr"], capture_output=True)
        stdout = completed_proc.stdout.decode("utf-8")

        pdr_info_line_matcher = re.compile(r"\[PDR No.[0-9]+ SEID [0-9]+ Info\]")
        matches = pdr_info_line_matcher.findall(stdout)

        active_pdrs = []  # hold active PDRs

        # each match is a separate PDR
        for match in matches:
            pdrid_match = re.search('PDR No.(\d+)', match)
            seid_match = re.search('SEID (\d+)', match)
            if pdrid_match:
                pdrid = int(pdrid_match.group(1))
            if seid_match:
                seid = int(seid_match.group(1))

            pdr = {'pdrid': pdrid, 'seid': seid}
            active_pdrs.append(pdr)


        active_pdrs_sorted = sorted(active_pdrs, key=lambda d: d['pdrid']) 
        return active_pdrs_sorted

    except:
        console_logger.exception("Error in getting active PDRs")

def get_pdr_stats(pdr):
    """
    Returns statistics for a given PDR
    """

    # try:
    #     # write PDR ID and interface name to proc file
    #     # cmd = "echo 'upfgtp %d %d' > /proc/gtp5g/pdr" % (pdr['seid'], pdr['pdrid'])
    #     cmd = ["/bin/echo", "'", "upfgtp",  "%d %d" % (pdr['seid'], pdr['pdrid']), "'", ">", "/proc/gtp5g/pdr"]
    #     # subproc.run(cmd, shell=True)
    #     out = subproc.run(cmd, capture_output=True)
    #     stdout = out.stdout.decode('utf-8', errors='replace')
    #     console_logger.debug(stdout)
    # except:
    #     console_logger.exception("Error in writing SEID, PDRID and interface to proc file!")

    try:
        with open("/proc/gtp5g/pdr", "w") as f:
            f.write("upfgtp %d %d\n" % (pdr['seid'], pdr['pdrid']))
    except:
        console_logger.exception("Error in writing SEID, PDRID and interface to proc file!")

    try:
        # read the proc file
        console_logger.debug("Trying to read proc file ...")
        cmd = ["cat", "/proc/gtp5g/pdr"]
        out = subproc.run(cmd, capture_output=True)
        stdout = out.stdout.decode('utf-8', errors='replace')
        console_logger.debug(f"stdout={stdout}")
    except:
        console_logger.exception("Error in reading proc file!")
        return


    ul_pkt_cnt_match = re.compile(r"UL Packet Count: (?P<count>[0-9]+)")
    dl_pkt_cnt_match = re.compile(r"DL Packet Count: (?P<count>[0-9]+)")
    ul_byte_cnt_match = re.compile(r"UL Byte Count: (?P<count>[0-9]+)")
    dl_byte_cnt_match = re.compile(r"DL Byte Count: (?P<count>[0-9]+)")

    ul_pkt_cnt = 0
    dl_pkt_cnt = 0
    ul_byte_cnt = 0
    dl_byte_cnt = 0

    try:
        ul_pkt_cnt = ul_pkt_cnt_match.search(stdout).group("count")
        dl_pkt_cnt = dl_pkt_cnt_match.search(stdout).group("count")
        ul_byte_cnt = ul_byte_cnt_match.search(stdout).group("count")
        dl_byte_cnt = dl_byte_cnt_match.search(stdout).group("count")
    except:
        console_logger.exception("Error in getting packet and byte counts!")

    timestamp = datetime.datetime.now()

    try:
        n3_ipaddr = get_upf_ip_addr("n3")
        n4_ipaddr = get_upf_ip_addr("n4")
    except: 
        console_logger.exception("Error in getting interface IP addresses!")


    data = {
        "timestamp" : str(timestamp),
        "pdrid": pdr['pdrid'],
        "seid": pdr['seid'],
        "upf_n3_ipaddr": n3_ipaddr,
        "upf_n4_ipaddr": n4_ipaddr,
        "pkt_count" : [ul_pkt_cnt, dl_pkt_cnt],
        "byte_count": [ul_byte_cnt, dl_byte_cnt]
    }

    # print(data)
    CURRENT_STATS.append(data)


def get_upf_ip_addr(iface):
    """
    get_upf_ip_addr: str -> str
    Returns the IP address of the interface. 
    """
    cmd = ["ip" ,"addr", "show", "%s" % iface]
    completed_proc = subproc.run(cmd, capture_output=True)
    stdout = completed_proc.stdout.decode("utf-8")
    ipv4_addr = stdout.split("inet ")[1].split("/")[0]
    return ipv4_addr


def write_stats_to_file():
    if CURRENT_STATS:
        CURRENT_STATS_json = json.dumps(CURRENT_STATS)
        stats_logger.info(CURRENT_STATS_json + "\n")

# get metrics for all the active PDRs
def get_metrics():

    active_pdrs = get_active_pdrs()
    console_logger.debug(active_pdrs)

    # get_pdr_stats(active_pdrs[0])

    for pdr in active_pdrs:
        get_pdr_stats(pdr)

    # write_stats_to_file()

    # clear current stats for next round of collection
    del CURRENT_STATS[:]
    
def main():
    console_logger.info("Starting UPF stats collector")
    get_metrics()

    # while True:
    #     try:
    #         get_metrics()
    #     except:
    #         console_logger.exception("Exception in getting metrics")
    #     time.sleep(UPDATE_PERIOD)


if __name__ == "__main__":
    main()
