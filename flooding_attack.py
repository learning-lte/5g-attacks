import subprocess
from datetime import datetime, timedelta, timezone
import re
import os
import matplotlib.pyplot as plt
from datetime import datetime
import time
import csv
from threading import Lock
import yaml
from prometheus_data_collector import *

"""
Manifest files
kubectl apply -f ./../5gc-manifests/free5gc-v3.2.0/ --recursive -n paul
kubectl apply -f ./../5gc-manifests/ueransim-v3.2.6-gnb/ --recursive -n paul
kubectl apply -f ./../5g-manifests/ueransim-v3.2.6-ue/ue-attacker/ --recursive -n paul
"""

coreSelector = 'free5gc-v3.2.0-duplicate'
gnbSelector = 'ueransim-v3.2.6-gnb-duplicate'
ueSelector = 'ueransim-v3.2.6-ue-duplicate'
ueManifest = f'../5g-manifests/{ueSelector}/' # '../5gc-manifests/ueransim-v3.2.6-ue-slice-x3/ue-attacker/'


"""
shell on container udm
ifconfig eth0
busypolling
linux tc
"""

# Markers needed to read the logs
REGISTRATION_REQUEST = 'Sending Initial Registration'
REGISTRATION_ACCEPT = 'Registration accept received'
PDU_SESSION_EST_REQUEST = 'Sending PDU Session Establishment Request'
PDU_SESSION_EST_ACCEPT = 'PDU Session Establishment Accept received'
DEREGISTRATION_REQUEST = 'Starting de-registration procedure'
DEREGISTRATION_ACCEPT = 'De-registration accept received'

command_get_ue = "kubectl get pods -n paul | awk '/ueransim-ue1/ {print $1;exit}'"
command_delete = f'kubectl delete -f ./{ueManifest} --recursive -n paul'
command_create = f'kubectl apply -f ./{ueManifest} --recursive -n paul'


def exec_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode().strip()  # Decode and remove leading/trailing whitespace

    return output


def delete_files_in_folder(folder_path, key=''):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    if key:
        files = [filename for filename in files if key in filename]

    # Iterate over the files and delete each one
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            #print(f"Deleted file: {file_path}")


def init_pod(deployments):  
    # Try to get existing ue pod
    existing_pod = exec_command(command_get_ue)
            
    if existing_pod:
        # There is a running ue pod
        print("Existing pod to be terminated:", existing_pod)

        # Delete existing pod
        exec_command(command_delete)

        # Wait for the pod to terminate
        print('Waiting for the existing pod to terminate...')
        while(exec_command(command_get_ue)):
            time.sleep(2)

    # Create pod
    print("Creating pod...")
    if deployments > 1:
        exec_command(command_create)
    else:
        exec_command(f'kubectl apply -f ./{ueManifest} --recursive -n paul')

    pod = exec_command(f"kubectl get pods -n paul | awk '/ueransim-ue1" + "/ {print $1;exit}'")
    while exec_command(f"kubectl get pod {pod} -n paul -o json | jq -r '.status.phase'") != 'Running':
        time.sleep(1)
    time.sleep(5)


def kill_pod():
    # Get nunning ue pod
    running_pod = exec_command(command_get_ue)

    if running_pod:
        # There is a running ue pod

        # Delete existing pod
        exec_command(command_delete)

        # Wait for the pod to terminate
        print(f'Pod {running_pod} terminating...')

        while(exec_command(command_get_ue)):
            time.sleep(2)
        
        print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Pod {running_pod} terminated.')


def get_params_from_yaml_file(yaml_file_path, params):
    # Load the YAML file
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    output = {}
    fields = data['data']['amfcfg.yaml']
    for param, key_string in params.items():
        value = None
        key_chain = fields.split('\n')
        for i in range (len(key_chain)):
            if key_string in key_chain[i]:
                value = key_chain[i+1].split('- ')[1]
                #print(value)
        output[param] = value
        
    return output


def complete_params(atk_params):
    params_values_amf = get_params_from_yaml_file(
        '../5g-manifests/free5gc/nf/amf1/amf-configmap.yaml', 
        {
            'ciphering_algorithm': 'cipheringOrder',
            'integrity_protection': 'integrityOrder'
         }
    )
    for params in params_values_amf:
        atk_params[params] = params_values_amf[params]


    default_deployments_path = {
        'udm': f'../5g-manifests/{coreSelector}/nf/udm/udm-deployment.yaml',
        'ausf': f'../5g-manifests/{coreSelector}/nf/ausf/ausf-deployment.yaml',
        'udr': f'../5g-manifests/{coreSelector}/nf/udr/udr-deployment.yaml',
        'ue1': f'../5g-manifests/{ueSelector}/ue1/ue-deployment.yaml',
        'gnb1': f'../5g-manifests/{gnbSelector}/gnb1/gnb-deployment.yaml',
        'amf1': f'../5g-manifests/{coreSelector}/nf/amf1/amf-deployment.yaml'
    }

    additional_deployments_path = {
        'ue2': f'../5g-manifests/{ueSelector}/ue2/ue-deployment.yaml',
        'gnb2': f'../5g-manifests/{gnbSelector}/gnb2/gnb-deployment.yaml',
        'amf2': f'../5g-manifests/{coreSelector}/nf/amf2/amf-deployment.yaml'       
    }


    for function, path in default_deployments_path.items():
        # Load the YAML file
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
            data = data['spec']['template']['spec']['containers'][0]['resources']
        atk_params[f'{function}_cpu_requests'] = data['requests']['cpu']
        atk_params[f'{function}_cpu_limits'] = data['limits']['cpu']

    if atk_params['deployments'] > 1:
        for function, path in additional_deployments_path.items():
            # Load the YAML file
            with open(path, 'r') as file:
                data = yaml.safe_load(file)
                data = data['spec']['template']['spec']['containers'][0]['resources']
            atk_params[f'{function}_cpu_requests'] = data['requests']['cpu']
            atk_params[f'{function}_cpu_limits'] = data['limits']['cpu']

    return atk_params


def run_flooding_attack(atk_params, log_folder, output_charts_folder):
    end_time = (atk_params['start'] + timedelta(minutes=atk_params['duration'])).timestamp()
    next_wave_time = atk_params['start'].timestamp()

    delete_files_in_folder('logs/')
    delete_files_in_folder('ue-data/')
    delete_files_in_folder('charts/', key=f'ue{2 * (atk_params["deployments"]==1)}')


    atk_params = complete_params(atk_params)


    # Save attack parameters
    with open('logs/atk_params.txt', 'w', newline="") as file:
        writer = csv.writer(file)
        # Write each parameter as a row in the CSV file
        for key, value in atk_params.items():
            writer.writerow([key, value])

    wave_times = [[],[]]
    results = []
    for pod in range(atk_params['deployments']):
        dictionary = {'registration_duration':[[],[]], 'pdu_establishment_duration':[[],[]], 'deregistration_duration':[[],[]]}
        results.append(dictionary)


    # Keep the script running until end time
    while datetime.now(timezone.utc).timestamp() < end_time:

        wave_time = datetime.now(timezone.utc)
        wave_num = len(wave_times[0])
        next_wave_time = (wave_time + timedelta(seconds=atk_params['wave_freq']))

        # Create new nodes and store logs in a separate file
        prc = []
        if wave_num == 0:
            for ue_pod in range(atk_params['deployments']):
                log_file_path = f'{log_folder}ueransim-ue{ue_pod+1}.txt'
                my_pod = f"$(kubectl get pods -n paul | awk '/ueransim-ue{ue_pod+1}" + "/ {print $1;exit}')"

                with Lock():
                    prc.append(subprocess.Popen(f'kubectl exec {my_pod} -n paul -- ./nr-ue -c config/free5gc-ue.yaml -n {str(atk_params["nb_ues"])} > {log_file_path}', shell=True, stdout=subprocess.PIPE))
            
            time.sleep(1)

        # Save wave time
        with open('logs/atk_params.txt', 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([f'Wave{wave_num}', wave_time])

        # Perform the attack on multiple ueransim-ue pods in parallel
        processes, output_queues = [], []

        for pod in range(atk_params['deployments']):
            log_file_path = f'{log_folder}ueransim-ue{pod+1}.txt'
            output_queues.append(multiprocessing.Queue())

            registration_duration, pdu_establishment_duration, deregistration_duration = results[pod].values()
            process = multiprocessing.Process(target=one_round_atk, args=(atk_params,registration_duration, pdu_establishment_duration, deregistration_duration, wave_times, log_file_path, wave_time, pod+1, output_queues[pod]))
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        time.sleep(atk_params['cooldown'])

        # Get results
        for i in range (atk_params['deployments']):
            registration_duration, pdu_establishment_duration, deregistration_duration, wave_times = output_queues[i].get()
            results[i]['registration_duration'] = registration_duration
            results[i]['pdu_establishment_duration'] = pdu_establishment_duration
            results[i]['deregistration_duration'] = deregistration_duration

            # Save the data to csv files
            save_data_points(registration_duration, f'ue-data/ue{i+1}_registration_time.csv')
            save_data_points(pdu_establishment_duration, f'ue-data/ue{i+1}_pdu_establishment_time.csv')
            save_data_points(wave_times, f'ue-data/ue{i+1}_wave_time.csv')

            log_file_path = f'{log_folder}ueransim-ue{i+1}.txt'

            if atk_params['restart_pod']:
                with Lock():
                    shutil.copy(log_file_path, f'logs/ueransim-ue{i+1}-wave{wave_num}.txt')

            # Plot the chart
            output_charts_path = f'{output_charts_folder}ue{i+1}_processing_times.png'
            plot_time_charts(registration_duration, pdu_establishment_duration, deregistration_duration, wave_times, output_charts_path)


        # Sleep until next wave
        time.sleep((next_wave_time - datetime.now(timezone.utc)).total_seconds())

    time.sleep(2)


def one_round_atk(
        atk_params, 
        registration_duration, 
        pdu_establishment_duration, 
        deregistration_duration, 
        wave_times, 
        log_file_path, 
        wave_time, 
        ue_pod,
        output_queue=None,
        timer=30
    ):

    withDeregistration = atk_params['deregistration'] != None
    absolute_time_start = atk_params['start']
    wave_num = len(wave_times[0])
    max_end_time = (wave_time + timedelta(seconds=timer)).timestamp()


    formatted_wavetime = wave_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    relative_wave_time = (wave_time - absolute_time_start).total_seconds()
    

    print(f'[{formatted_wavetime.split(" ")[1]}]  Proceeding wave {wave_num}')
    wave_times[0].append(relative_wave_time)
    wave_times[1].append(wave_num)
    time_for_procedure = 0


    registration_start_times = {}
    pdu_session_start_times = {}
    deregistration_start_times = {}
    deregistrations_count = 0
    deregistrations_started = False
    regist_and_pdu_done = False
    deregistrations_completed = False
    wave_completed = False
    line_counter = 0
    my_pod = exec_command("kubectl get pods -n paul | awk '/ueransim-ue" + str(ue_pod) + "/ {print $1;exit}'")

    while datetime.now(timezone.utc).timestamp() < max_end_time:
        logs = parse_log(log_file_path)

        for i in range (line_counter, len(logs), 1):#timestamp, line in logs:
            timestamp, line = logs[i]
            match = re.search(r'\[(\d+)\|nas\]', line)
            if match:
                ue_id = match.group(1)
                if REGISTRATION_REQUEST in line:
                    registration_start_times[ue_id] = timestamp
                elif REGISTRATION_ACCEPT in line:
                    #print(REGISTRATION_ACCEPT)
                    if ue_id in registration_start_times:
                        registration_start_time = registration_start_times[ue_id]
                        time_for_procedure = (timestamp - registration_start_time).total_seconds()
                        relative_registration_start_time = (registration_start_time - absolute_time_start).total_seconds()
                        registration_duration[0].append(relative_registration_start_time)
                        registration_duration[1].append(time_for_procedure)
                        del registration_start_times[ue_id]

                elif PDU_SESSION_EST_REQUEST in line:
                    pdu_session_start_times[ue_id] = timestamp
                elif PDU_SESSION_EST_ACCEPT in line:
                    #print(PDU_SESSION_EST_ACCEPT)
                    if ue_id in pdu_session_start_times:
                        pdu_session_start_time = pdu_session_start_times[ue_id]
                        time_for_procedure = (timestamp - pdu_session_start_time).total_seconds()
                        relative_pdu_session_start_time = (pdu_session_start_time - absolute_time_start).total_seconds()
                        pdu_establishment_duration[0].append(relative_pdu_session_start_time)
                        pdu_establishment_duration[1].append(time_for_procedure)
                        del pdu_session_start_times[ue_id]

                elif DEREGISTRATION_REQUEST in line:
                    deregistration_start_times[ue_id] = timestamp
                elif DEREGISTRATION_ACCEPT in line:
                    #print(DEREGISTRATION_ACCEPT)
                    if ue_id in deregistration_start_times:
                        deregistration_start_time = deregistration_start_times[ue_id]
                        time_for_procedure = (timestamp - deregistration_start_time).total_seconds()
                        relative_deregistration_start_time = (deregistration_start_time - absolute_time_start).total_seconds()
                        deregistration_duration[0].append(relative_deregistration_start_time)
                        deregistration_duration[1].append(time_for_procedure)
                        del deregistration_start_times[ue_id]
                        deregistrations_count += 1

                # Debugging negative times bug due to access conflicts (?) to the log file
                if time_for_procedure < 0:
                    print(timestamp, line, time_for_procedure)
                    exit(1)
        
        line_counter = len(logs)

        registrations_completed = not bool(registration_start_times) # Is True if the dictionary is empty, i.e. there is no registration ongoing
        pdu_session_est_completed = not bool(pdu_session_start_times) # Is True if the dictionary is empty, i.e. there is no PDU session establishment ongoing
        deregistrations_completed = not bool(deregistration_start_times)

        #print(f'line {line_counter}, {len(registration_start_times)}  regstr,  {deregistrations_count} deregistrations, {deregistrations_completed}, {wave_num}')
        
        
        # Check if it's time to deregister ()
        if withDeregistration and (not deregistrations_started) and ((wave_num == 0 and registrations_completed and pdu_session_est_completed) or wave_num>0):
            ue_dump = exec_command(f'kubectl exec {my_pod} -n paul -- ./nr-cli --dump')
            ue_nodes = ue_dump.split('\n')
            for ue_id in ue_nodes:
                exec_command(f'kubectl exec {my_pod} -n paul -- ./nr-cli {ue_id} --exec "deregister {atk_params["deregistration"]}"')
            deregistrations_started = True
        #elif atk_params['restart_pod'] and registrations_completed and pdu_session_est_completed:


        
        if deregistrations_started and deregistrations_completed and registrations_completed and pdu_session_est_completed:
            break


    # In case procedures went wrong
    if not registrations_completed:
        print(f'[ERROR]  {len(registration_start_times)} UEs have not been registered')
        print(f'[ERROR]  {len(pdu_session_start_times)} UEs have not established a PDU session')
    if not deregistrations_completed:
        if len(deregistration_start_times) == 0:
            print(f'[WARNING] Deregistration procedure has encountered errors but has now completed.')
        else:
            print(f'[ERROR]  {len(deregistration_start_times)} UEs have not been deregistered')

    if output_queue != None:
        output_queue.put((registration_duration, pdu_establishment_duration, deregistration_duration, wave_times))
    
    return registration_duration, pdu_establishment_duration, deregistration_duration, wave_times


def read_subprocess(process):
    logs = []
    line_counter = 0
    line_limit = 200

    # Read the output of the subprocess line by line
    for line_raw in iter(process.stdout.readline, b''):
        line = line_raw.decode('utf-8')
        match = re.search(r'^\[(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\]', line)
        if match:
            #print(line)
            timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S.%f")

            # Ensure the timestamp is in UTC (offset-aware)
            timestamp_utc = timestamp.replace(tzinfo=timezone.utc)

            logs.append((timestamp_utc, line))
            line_counter += 1
        if line_counter > line_limit:
            break
    return logs



def save_data_points(data_points, filename):
    mode = "w"  # "w" for writing, "a" for appending
    x,y = data_points

    # Open the CSV file in the specified mode
    with open(filename, mode, newline="") as file:
        writer = csv.writer(file)
        
        # Write each point as a row in the CSV file
        for i in range (0,len(x),1):
            writer.writerow([x[i],y[i]])
    print(f'   Data saved as csv ({filename})')


def plot_time_charts(registration_duration, pdu_establishment_duration, deregistration_duration, wave_times, output_chart_path):
    plt.plot(registration_duration[0],registration_duration[1], 'x', label='Initial Registration', color='tab:green')
    plt.plot(pdu_establishment_duration[0],pdu_establishment_duration[1], '+', label='PDU Session Establishment', color='tab:orange')
    plt.plot(deregistration_duration[0],deregistration_duration[1], 'x', label='Deregistration', color='tab:red')

    plt.plot(wave_times[0], [0]*len(wave_times[0]), 'o', label="Waves", color='tab:blue')
    plt.xlabel('Time elapsed (s)',)
    plt.ylabel('Processing time (s)')
    plt.title('UE requests processing time')
    plt.legend()
    plt.grid(True)

    if output_chart_path:
        plt.savefig(output_chart_path)
        plt.close()
    else:
        plt.show()
    print(f'   Chart generated ({output_chart_path})')


def parse_log(log_file_path, start_at=None):
    logs = []
    time_window = start_at == None
    with open(log_file_path, 'r') as file:
        for line in file:
            match = re.search(r'^\[(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\]', line)
            if match:
                #print(line)
                timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S.%f")
                # Ensure the timestamp is in UTC (offset-aware)
                timestamp_utc = timestamp.replace(tzinfo=timezone.utc)

                if not time_window and timestamp_utc >= start_at:
                    time_window = True

                if time_window:
                    logs.append((timestamp_utc, line))
                    #print(line)
    return logs


def find_message(logs, ue_id, MESSAGE):
    for timestamp, line in logs:
        if f'[{ue_id}|nas]' in line and MESSAGE in line:
            return timestamp
    return None


if __name__ == "__main__":


    atk_params = {
        'start': datetime.now(timezone.utc),
        'duration': 5,                  # in minutes
        'collection_extra_time': 2,     # in minutes
        'collection_step': 1,           # in seconds
        'wave_freq': 60,                # in seconds
        'cooldown': 1,                  # in seconds
        'nb_ues': 100,
        'deployments': 1,       
        'restart_pod': True,           
        'deregistration': 'normal',
        'integrity_protection': '',
        'ciphering_algorithm': '',
        'gnb1_cpu_requests':'',
        'gnb1_cpu_limits':'',
        'ue1_cpu_requests':'',
        'ue1_cpu_limits':'',
        'amf1_cpu_requests':'',
        'amf1_cpu_limits':'',
        'gnb2_cpu_requests':'',
        'gnb2_cpu_limits':'',
        'ue2_cpu_requests':'',
        'ue2_cpu_limits':'',
        'amf2_cpu_requests':'',
        'amf2_cpu_limits':'',
        'ausf_cpu_requests': '',
        'ausf_cpu_limits': '',
        'udr_cpu_requests': '',
        'udr_cpu_limits': '',
        'udm_cpu_requests': '',
        'udm_cpu_limits': '',
        'udm_rate':1,                   # in mbit
        'udm_burst':10,                 # in kb
        'udm_latency':70,               # in ms
    }


    # Initialization
    init_pod(atk_params['deployments'])


    # Time parameters
    start_now = atk_params['start']
    start_time = start_now.timestamp()
    end_time = (start_now + timedelta(minutes=atk_params['duration'])).timestamp()
    end_collection_time = (start_now + timedelta(minutes=atk_params['duration']+atk_params['collection_extra_time'])).timestamp()
    #print(end_time)
    step = atk_params['collection_step']

    
    # Collect data from the testbed (Prometheus) in the background
    log_collection_process = multiprocessing.Process(target=generate_logs, args=(atk_params['deployments'],))
    log_collection_process.start()
    print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Log collection running in background.')
    

    # Plot charts every 5 seconds for real-time visualisation
    delete_files_in_folder('data/')
    real_time_charts_process = multiprocessing.Process(target=real_time_charts, args=(metric_lists, labels_dict, start_time, end_collection_time, step))
    real_time_charts_process.start()
    print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Real-time charts running in background.')


    # Perform attack and save results
    print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Performing the flooding attack...')
    run_flooding_attack(atk_params, 'logs/', 'charts/')
    kill_pod()


    # Waiting for the background process to complete
    log_collection_process.terminate()
    log_collection_process.join()
    real_time_charts_process.join()


    # Commit the results to the remote Git repository
    git_commit_results(str(int(start_time)))   
