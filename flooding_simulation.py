import subprocess
import multiprocessing
from datetime import datetime, timedelta, timezone
import re
import os
import matplotlib.pyplot as plt
import time
import csv
from threading import Lock
import yaml

from random_generator import *
from restart_core import creation_phase,termination_phase
from utils import *
from flooding_context_input import run_default_experiment
import prometheus_data_collector


coreSelector = 'free5gc'
gnbSelector = 'ueransim-gnb'
ueGeneralSelector = 'ueransim-ue'
ueGeneralManifest = f'../5g-manifests/{ueGeneralSelector}/' 
ueBenignSelector = 'ueransim-ue-benign'
ueBenignManifest = f'../5g-manifests/{ueBenignSelector}/' 
ueAttackerSelector = 'ueransim-ue-attacker'
ueAttackerManifest = f'../5g-manifests/{ueAttackerSelector}/'


# Markers needed to read the logs
REGISTRATION_REQUEST = 'Sending Initial Registration'
REGISTRATION_ACCEPT = 'Registration accept received'
PDU_SESSION_EST_REQUEST = 'Sending PDU Session Establishment Request'
PDU_SESSION_EST_ACCEPT = 'PDU Session Establishment Accept received'
DEREGISTRATION_REQUEST = 'Starting de-registration procedure'
DEREGISTRATION_ACCEPT = 'De-registration accept received'

COMMAND_GET_GENERAL = "kubectl get pods -n paul | awk '/ueransim-ue1/ {print $1;exit}'"
COMMAND_DELETE_GENERAL = f'kubectl delete -k ./{ueGeneralManifest} -n paul'
COMMAND_CREATE_GENERAL = f'kubectl apply -k ./{ueGeneralManifest} -n paul'
COMMAND_GET_BENIGN = "kubectl get pods -n paul | awk '/ueransim-ue1-benign/ {print $1;exit}'"
COMMAND_DELETE_BENIGN = f'kubectl delete -k ./{ueBenignManifest} -n paul'
COMMAND_CREATE_BENIGN = f'kubectl apply -k ./{ueBenignManifest} -n paul'
COMMAND_GET_ATTACKER = "kubectl get pods -n paul | awk '/ueransim-ue1-attacker/ {print $1;exit}'"
COMMAND_DELETE_ATTACKER = f'kubectl delete -k ./{ueAttackerManifest} -n paul'
COMMAND_CREATE_ATTACKER = f'kubectl apply -k ./{ueAttackerManifest} -n paul'

_commands = {'getBenign':COMMAND_GET_BENIGN, 'getAttacker':COMMAND_GET_ATTACKER, 'deleteBenign':COMMAND_DELETE_BENIGN, 'deleteAttacker':COMMAND_DELETE_ATTACKER}



class LatestDataQueue:
    def __init__(self):
        self.queue = multiprocessing.Queue(maxsize=1)
        self.lock = multiprocessing.Lock()

    def put(self, data):
        with self.lock:
            while not self.queue.empty():
                self.queue.get()
            self.queue.put(data)

    def get(self):
        with self.lock:
            if self.queue.empty():
                return [[],[]], [[],[]], [[],[]]
            return self.queue.get()



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
    general_existing_pod = exec_command("kubectl get pods -n paul | awk '/ueransim-ue1/ {print $1;exit}'")
    benign_existing_pod = exec_command(COMMAND_GET_BENIGN)
    attacker_existing_pod = exec_command(COMMAND_GET_ATTACKER)
            
    # Create pod
    print("Creating pods...")
    if deployments > 1:
        exec_command(COMMAND_CREATE_ATTACKER)
        exec_command(COMMAND_CREATE_BENIGN)
    else:
        exec_command(f'kubectl apply -k ./{ueBenignManifest} -n paul')
        exec_command(f'kubectl apply -k ./{ueAttackerManifest} -n paul')


    benign_pod = exec_command(COMMAND_GET_BENIGN)
    attacker_pod = exec_command(COMMAND_GET_ATTACKER)

    while (exec_command(f"kubectl get pod {benign_pod} -n paul -o json | jq -r '.status.phase'") != 'Running'
           or exec_command(f"kubectl get pod {attacker_pod} -n paul -o json | jq -r '.status.phase'") != 'Running'):
        time.sleep(1)
    time.sleep(5)


def kill_pod(): 
    # Get running ue pod
    running_benign_pod = exec_command(COMMAND_GET_BENIGN)
    running_attacker_pod = exec_command(COMMAND_GET_ATTACKER)

    if running_benign_pod:
        # Delete existing pod
        exec_command(COMMAND_DELETE_BENIGN)

        # Wait for the pod to terminate
        print(f'Benign pod(s) {running_benign_pod} terminating...')

        while(exec_command(COMMAND_GET_BENIGN)):
            time.sleep(2)
        
        print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Pod {running_benign_pod} terminated.')

    if running_attacker_pod:
        # Delete existing pod
        exec_command(COMMAND_DELETE_ATTACKER)

        # Wait for the pod to terminate
        print(f'Attacker pod(s) {running_attacker_pod} terminating...')

        while(exec_command(COMMAND_GET_ATTACKER)):
            time.sleep(2)
        
        print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Pod {running_attacker_pod} terminated.')

def complete_params(simulation_params):
    default_deployments_path = {
        'udm': f'../5g-manifests/{coreSelector}/nf/udm/udm-deployment.yaml',
        'ausf': f'../5g-manifests/{coreSelector}/nf/ausf/ausf-deployment.yaml',
        'udr': f'../5g-manifests/{coreSelector}/nf/udr/udr-deployment.yaml',
        'ue1-benign': f'../5g-manifests/{ueBenignSelector}/ue1/ue-deployment.yaml',
        'ue1-attacker': f'../5g-manifests/{ueAttackerSelector}/ue1/ue-deployment.yaml',
        'gnb1': f'../5g-manifests/{gnbSelector}/gnb1/gnb-deployment.yaml',
        'amf1': f'../5g-manifests/{coreSelector}/nf/amf1/amf-deployment.yaml'
    }

    additional_deployments_path = {
        'ue2': f'../5g-manifests/{ueBenignSelector}/ue2/ue-deployment.yaml',
        'ue2': f'../5g-manifests/{ueAttackerSelector}/ue2/ue-deployment.yaml',
        'gnb2': f'../5g-manifests/{gnbSelector}/gnb2/gnb-deployment.yaml',
        'amf2': f'../5g-manifests/{coreSelector}/nf/amf2/amf-deployment.yaml'       
        }

    with open(f'../5g-manifests/{coreSelector}/nf/kustomization.yaml', 'r') as file:
        data = yaml.safe_load(file)
        if data['resources'][0] == 'amf1':
            mode = 'default'
        elif data['resources'][0] == 'amf1-storm':
            mode = 'signalling_storm_patch'
        simulation_params['amf_mode'] = mode

    for function, path in default_deployments_path.items():
        # Load the YAML file
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
            data = data['spec']['template']['spec']['containers'][0]['resources']
        simulation_params[f'{function}_cpu_requests'] = data['requests']['cpu']
        simulation_params[f'{function}_cpu_limits'] = data['limits']['cpu']

    if simulation_params['deployments'] > 1:
        for function, path in additional_deployments_path.items():
            # Load the YAML file
            with open(path, 'r') as file:
                data = yaml.safe_load(file)
                data = data['spec']['template']['spec']['containers'][0]['resources']
            simulation_params[f'{function}_cpu_requests'] = data['requests']['cpu']
            simulation_params[f'{function}_cpu_limits'] = data['limits']['cpu']

    return simulation_params



def run_flooding_attack(atk_params, log_folder, output_charts_folder, shared_memory_benign):
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

    ghostStr = '-i imsi-208930000005000 ' if atk_params['ghost'] else ''

    # Keep the script running until end time
    while datetime.now(timezone.utc).timestamp() < end_time:
        wave_time = datetime.now(timezone.utc)
        wave_num = len(wave_times[0])
        next_wave_time = (wave_time + timedelta(seconds=atk_params['wave_freq']))

        prc = []
        # Create new nodes and store logs in a separate file
        if wave_num == 0 or atk_params['ghost']:
            for ue_pod in range(atk_params['deployments']):
                my_ue = f"$(kubectl get pods -n paul | awk '/ueransim-ue{ue_pod+1}-attacker" + "/ {print $1;exit}')"

                log_file_path = f'{log_folder}ueransim-ue{pod+1}.txt'
                if atk_params['ghost']:
                    log_file_path = f'{log_folder}ueransim-ue{pod+1}-wave{wave_num}.txt'
                    if wave_num>0:
                        attacker_pod = exec_command(COMMAND_GET_ATTACKER)
                        print(f'{COLOR_INFO}[STORM][INFO]{COLOR_RESET} Storm pod is {attacker_pod}')
                        while (exec_command(f"kubectl get pod {attacker_pod} -n paul -o json | jq -r '.status.phase'") != 'Running'):
                            time.sleep(0.01)

                with Lock():
                    prc.append(subprocess.Popen(f'kubectl exec {my_ue} -n paul -- ./nr-ue -c config/free5gc-ue.yaml -n {str(atk_params["nb_ues"])} {ghostStr}> {log_file_path}', shell=True, stdout=subprocess.PIPE))

            time.sleep(1)

        # Save wave time
        with open('logs/atk_params.txt', 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([f'Wave{wave_num}', wave_time])

        # Perform the attack on multiple ueransim-ue pods in parallel
        processes, output_queues = [], []

        for pod in range(atk_params['deployments']):
            log_file_path = f'{log_folder}ueransim-ue{pod+1}.txt'
            if atk_params['restart_pod'] or atk_params['ghost']:
                log_file_path = f'{log_folder}ueransim-ue{pod+1}-wave{wave_num}.txt'

            output_queues.append(multiprocessing.Queue())

            registration_duration, pdu_establishment_duration, deregistration_duration = results[pod].values()
            process = multiprocessing.Process(target=one_round_atk, args=(atk_params,registration_duration, pdu_establishment_duration, deregistration_duration, wave_times, log_file_path, wave_time, pod+1, output_queues[pod]))
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        time.sleep(atk_params['cooldown'])


        if atk_params['restart_pod'] or atk_params['ghost']:
            running_attacker_pod = exec_command(COMMAND_GET_ATTACKER)

            if running_attacker_pod:
                # Delete existing pod
                exec_command(COMMAND_DELETE_ATTACKER)

                # Wait for the pod to terminate
                print(f'Attacker pod(s) for wave {wave_num} terminating...')

                while(exec_command(COMMAND_GET_ATTACKER)):
                    time.sleep(1)
                
                print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Pod {running_attacker_pod} terminated.')

 
                exec_command(COMMAND_CREATE_ATTACKER)

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

            # Plot the chart
            output_charts_path = f'{output_charts_folder}ue{i+1}_simulation_processing_times.png'
            registration_duration_benign, pdu_establishment_duration_benign, deregistration_duration_benign = shared_memory_benign.get()
            #print(registration_duration_benign, pdu_establishment_duration_benign, deregistration_duration_benign)
            plot_time_charts(
                [registration_duration, registration_duration_benign], 
                [pdu_establishment_duration, pdu_establishment_duration_benign], 
                [deregistration_duration, deregistration_duration_benign], 
                wave_times, 
                output_charts_path
                )
            plot_time_charts(
                [registration_duration, registration_duration_benign], 
                [pdu_establishment_duration, pdu_establishment_duration_benign], 
                [deregistration_duration, deregistration_duration_benign], 
                wave_times, 
                f'{output_charts_folder}ue{i+1}-benign_simulation_processing_times.png',
                one_color=True
            )


        # Sleep until next wave
        time.sleep(max(0,(next_wave_time - datetime.now(timezone.utc)).total_seconds()))


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


    leave = False
    registration_start_times = {}
    pdu_session_start_times = {}
    deregistration_start_times = {}
    deregistrations_count = 0
    deregistrations_started = False
    deregistrations_completed = False
    line_counter = 0
    my_pod = exec_command("kubectl get pods -n paul | awk '/ueransim-ue" + str(ue_pod) + "-attacker/ {print $1;exit}'")
    typeOfDeregistration = atk_params["deregistration"]

    if atk_params['ghost']:
        """       
        my_gnb = f"$(kubectl get pods -n paul | awk '/ueransim-gnb{ue_pod+1}" + "/ {print $1;exit}')"
        my_ue = f"$(kubectl get pods -n paul | awk '/ueransim-ue{ue_pod+1}-attacker" + "/ {print $1;exit}')" 
        ue_dump = exec_command(f'kubectl exec {my_ue} -n paul -- ./nr-cli --dump')
        ue_nodes = ue_dump.split('\n')
        gnb_dump = exec_command(f'kubectl exec {my_gnb} -n paul -- ./nr-cli --dump')
        gnb_nodes = gnb_dump.split('\n')
        for num in range(atk_params['nb_ues']+1):
            ue_id = f'imsi-208930000010{str(num).zfill(3)}'
            exec_command(f'kubectl exec {my_gnb} -n paul -- ./nr-cli {gnb_nodes[0]} --exec "ue-release {ue_id}"')
        """
        leave = True


    while (datetime.now(timezone.utc).timestamp() < max_end_time) and not leave:
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
                    print(f'{COLOR_ERROR}[ERROR]{COLOR_RESET}{timestamp}', line, time_for_procedure)
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
                exec_command(f'kubectl exec {my_pod} -n paul -- ./nr-cli {ue_id} --exec "deregister {typeOfDeregistration}"')
            deregistrations_started = True
        #elif atk_params['restart_pod'] and registrations_completed and pdu_session_est_completed:


        
        if deregistrations_started and deregistrations_completed and registrations_completed and pdu_session_est_completed:
            break


    if atk_params['ghost']:
        print(f'{COLOR_INFO}[STORM][INFO]{COLOR_RESET} {atk_params["nb_ues"]} ghost UE(s) trying to register')
    elif atk_params['amf_mode'] == 'signalling_storm_patch':
        if len(registration_start_times) == atk_params['nb_ues']:
            print(f'{COLOR_SUCCESS}[STORM][SUCCESS]{COLOR_RESET} {len(registration_start_times)} storm UE(s) successfully rejected')
        else:
            print(f'{COLOR_ERROR}[STORM][ERROR]{COLOR_RESET} {atk_params["nb_ues"]-len(registration_start_times)} storm UE(s) registered')
    elif atk_params['amf_mode'] == 'default':
        print(f'{COLOR_ERROR}[STORM][ERROR]{COLOR_RESET} {len(registration_start_times)} storm UE(s) not registered')
              
    if not leave and not deregistrations_completed:
        if len(deregistration_start_times) == 0:
            print(f'{COLOR_WARNING}[STORM][WARNING]{COLOR_RESET} Deregistration procedure has encountered errors but has now completed.')
        else:
            print(f'{COLOR_ERROR}[STORM][ERROR]{COLOR_RESET} {len(deregistration_start_times)} UE(s) not deregistered')


    if output_queue != None:
        output_queue.put((registration_duration, pdu_establishment_duration, deregistration_duration, wave_times))

    return registration_duration, pdu_establishment_duration, deregistration_duration, wave_times


def benign_flow(ue_pod_md, csv_times, offset):

    my_pod = exec_command("kubectl get pods -n paul | awk '/ueransim-ue" + str(ue_pod_md) + "-benign/ {print $1;exit}'")

    with open(csv_times, 'r') as file:
        reader = csv.reader(file)
        header_row = next(reader)  # Read the header row

        # Find the element in the header row that starts with 'Time:'
        time_element = next((element for element in header_row if element.startswith('Time:')), None)
        # Extract the time value using regular expressions
        time_start_generation = float(re.search(r'Time:(.*)', time_element).group(1).strip())

        imsi = 0
        for row in reader:
            imsi += 1
            time_value = float(row[0])
            log_file_path = f'logs/ueransim-ue{ue_pod_md}-benign_imsi-208930000001{str(imsi).zfill(3)}.txt'

            # Get current time
            current_time = datetime.now(timezone.utc).timestamp()

            # Wait until the specified time is reached
            while current_time < time_value + offset:
                current_time = datetime.now(timezone.utc).timestamp()
                #print(f'Current time:  {current_time}     |    Time for next benign UE:  {time_value}')
                

            # Execute the command
            process = multiprocessing.Process(target=exec_command, args=(f'kubectl exec {my_pod} -n paul -- ./nr-ue -c config/free5gc-ue.yaml -i imsi-208930000001{str(imsi).zfill(3)} > {log_file_path}', ))
            process.start()


def analyze_benign_flow(benign_params, log_key_prefix, output_queue=None):

    absolute_time_start = benign_params['start']

    registration_duration, pdu_establishment_duration, deregistration_duration = [[],[]], [[],[]], [[],[]]
    registration_start_times = {}
    pdu_session_start_times = {}
    deregistration_start_times = {}
    deregistrations_count = 0
    deregistrations_completed = False

    logs = parse_log_with_prefix(log_key_prefix)
    for ue_id, ue_log_file in logs.items():
        for timestamp, line in ue_log_file:
            #print(line)
            match = re.search(r'\[nas\]', line)
            if match:
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
        

        registrations_completed = not bool(registration_start_times) # Is True if the dictionary is empty, i.e. there is no registration ongoing
        pdu_session_est_completed = not bool(pdu_session_start_times) # Is True if the dictionary is empty, i.e. there is no PDU session establishment ongoing
        deregistrations_completed = not bool(deregistration_start_times)

        # In case procedures went wrong
        if not registrations_completed:
            ue_string = ue_id.split('_')[-1].split('.')[0]
            #print(f'[ERROR-BENIGN]  {ue_string} has not been registered')
            #print(f'[ERROR-BENIGN]  {ue_string} has not established a PDU session')
        if not deregistrations_completed:
            if len(deregistration_start_times) == 0:
                print(f'[WARNING-BENIGN] Deregistration procedure has encountered errors but has now completed.')
            else:
                print(f'[ERROR-BENIGN]  {len(deregistration_start_times)} UEs have not been deregistered')

    if output_queue != None:
        output_queue.put((registration_duration, pdu_establishment_duration, deregistration_duration))
    
    return registration_duration, pdu_establishment_duration, deregistration_duration


def run_benign_users(benign_params, log_folder, output_charts_folder, csv_times, shared_memory_blocks, printRegistrations = False):
    end_time = (benign_params['start'] + timedelta(minutes=benign_params['duration'])).timestamp()

    
    benign_params = complete_params(benign_params)


    # Save attack parameters
    with open('logs/benign_params.txt', 'w', newline="") as file:
        writer = csv.writer(file)
        # Write each parameter as a row in the CSV file
        for key, value in benign_params.items():
            writer.writerow([key, value])

    results = []
    for pod in range(benign_params['deployments']):
        dictionary = {'registration_duration':[[],[]], 'pdu_establishment_duration':[[],[]], 'deregistration_duration':[[],[]]}
        results.append(dictionary)


    # Create new nodes and store logs in a separate file
    prc = []
    processes = []

    for ue_pod in range(benign_params['deployments']):
        log_file_path = f'{log_folder}ueransim-ue{ue_pod+1}-benign.txt'
        my_pod = f"$(kubectl get pods -n paul | awk '/ueransim-ue{ue_pod+1}-benign" + "/ {print $1;exit}')"
        with Lock():
            prc.append(subprocess.Popen(f'kubectl exec {my_pod} -n paul -- ./nr-ue -c config/free5gc-ue.yaml > {log_file_path}', shell=True, stdout=subprocess.PIPE))
    
        process = multiprocessing.Process(target=benign_flow, args=(ue_pod+1, csv_times[pod], benign_params['start'].timestamp() + benign_params['wave_freq']))

        processes.append(process)
    time.sleep(1)

    

    print("Processes benign starting")
    for process in processes:
        process.start()

    # Keep the script running until end time
    while datetime.now(timezone.utc).timestamp() < end_time:
        time.sleep(benign_params['wave_freq']-2)

        # Get results
        for ue_pod in range (benign_params['deployments']):
            registration_duration, pdu_establishment_duration, deregistration_duration = analyze_benign_flow(benign_params, f'ueransim-ue{ue_pod+1}-benign')
            shared_memory_blocks.put((registration_duration, pdu_establishment_duration, deregistration_duration))
            #print(registration_duration, pdu_establishment_duration, deregistration_duration)

            if printRegistrations:
                print(registration_duration)

            # Save the data to csv files
            save_data_points(registration_duration, f'ue-data/ue{ue_pod+1}-benign_registration_time.csv')
            save_data_points(pdu_establishment_duration, f'ue-data/ue{ue_pod+1}-benign_pdu_establishment_time.csv')

            # Plot the chart
            #output_charts_path = f'{output_charts_folder}ue{i+1}-benign_processing_times.png'
            #plot_time_charts(registration_duration, pdu_establishment_duration, deregistration_duration, output_charts_path)

    for process in processes:
        process.terminate()
        process.join()

    time.sleep(2)


def plot_time_charts(registration_duration, pdu_establishment_duration, deregistration_duration, wave_times, output_chart_path, one_color=False):
    # Plot attackers
    if len(registration_duration[0][0]) > 0 and not one_color:
        plt.plot(registration_duration[0][0],registration_duration[0][1], 'x', label='[ATK] Initial Registration', color='tab:red')
        plt.plot(deregistration_duration[0][0],deregistration_duration[0][1], '+', label='[ATK] Deregistration', color='tab:gray')
    elif one_color:
        plt.plot(registration_duration[0][0],registration_duration[0][1], 'x', label='Registrations', color='tab:green')

    # Plot benign UEs
    plt.plot(registration_duration[1][0],registration_duration[1][1], 'x', label='[Benign] Initial Registration', color='tab:green')
    #plt.plot(deregistration_duration[1][0],deregistration_duration[1], '+', label='[Benign] Deregistration', color='tab:gray')

    #plt.plot(pdu_establishment_duration[0][0],pdu_establishment_duration[1], '+', label='PDU Session Establishment', color='tab:orange')

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



if __name__ == "__main__":
    # Careful while modifying these!
    pod_representants = {
    'free5gc':['free5gc-nrf', 'free5gc-upf'],
    'ueransim-gnb':['ueransim-gnb1'],
    'ueransim-ue':['ueransim-ue1','ueransim-ue2']
    }

    deletion_order = ['ueransim-ue', 'ueransim-gnb', 'free5gc']
    creation_order = ['free5gc', 'ueransim-gnb']

    # Restart core
    termination_phase(_commands, pod_representants, deletion_order)
    time.sleep(2)
    creation_phase(pod_representants, creation_order)
    kill_pod()

    simulation_params = {
        'start': datetime.now(timezone.utc),
        'duration': 5,                  # in minutes
        'collection_extra_time': 2,     # in minutes
        'collection_step': 1,           # in seconds
        'wave_freq': 60,                # in seconds
        'cooldown': 1,                  # in seconds
        'nb_ues': 30,
        'nb_benign':220,
        'ghost':False,
        'deployments': 1,       
        'restart_pod': False,           
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
        #'udm_rate':1,                   # in mbit
        #'udm_burst':10,                 # in kb
        #'udm_latency':70,               # in ms
    }

    # Initialization
    init_pod(simulation_params['deployments'])
    delete_files_in_folder('logs/')
    delete_files_in_folder('ue-data/')

    # Time parameters
    start_now = simulation_params['start']
    start_time = start_now.timestamp()
    end_time = (start_now + timedelta(minutes=simulation_params['duration'])).timestamp()
    end_collection_time = (start_now + timedelta(minutes=simulation_params['duration']+simulation_params['collection_extra_time'])).timestamp()
    step = simulation_params['collection_step']


    # Plot charts every 5 seconds for real-time visualisation
    delete_files_in_folder('data/')
    
    #real_time_charts(metric_lists, labels_dict, start_time, end_time, step, source_folder_path, dest_folder_path, debug=True)
    real_time_charts_process = multiprocessing.Process(target=exec_command, args=('python3 prometheus_data_collector.py',))
    #real_time_charts_process = multiprocessing.Process(target=prometheus_data_collector.real_time_charts, args=(prometheus_data_collector.metric_lists, prometheus_data_collector.labels_dict, start_time, end_collection_time, step, 'data/', 'charts/',))
    real_time_charts_process.start()
    print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Real-time charts running in background.')


    csv_files = []
    # Generate random times for the benign users
    for i in range(2):#
        csv_files.append(f'random_times_{i+1}.csv')
        #random_times(simulation_params,csv_files[i])


    # Collect data from the testbed (Prometheus) in the background
    log_collection_process = multiprocessing.Process(target=prometheus_data_collector.generate_logs, args=('logs/', simulation_params['deployments'],))
    log_collection_process.start()
    print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Log collection running in background.')
    

    # Put lists in shared memory
    shared_memory_blocks = LatestDataQueue()
    context_process = multiprocessing.Process(target=run_benign_users, args=(simulation_params, 'logs/', 'charts/', csv_files, shared_memory_blocks))
    attack_process = multiprocessing.Process(target=run_flooding_attack, args=(simulation_params, 'logs/', 'charts/', shared_memory_blocks))

    # Perform simulation and save results
    print(f'[{datetime.now(timezone.utc).strftime("%H:%M:%S.%f")}]  Running simulation...')
    #run_flooding_attack(simulation_params, 'logs/', 'charts/', shared_memory_blocks)
    attack_process.start()
    #context_process.start()
    run_benign_users(simulation_params, 'logs/', 'charts/', csv_files, shared_memory_blocks)

    """
    context_process.join()
    attack_process.join()
    end = (start_now + timedelta(minutes=simulation_params['duration']))
    time.sleep((end - datetime.now(timezone.utc)).total_seconds())
    """
    end = (start_now + timedelta(minutes=simulation_params['duration']))
    end2 = (start_now + timedelta(minutes=simulation_params['duration']+simulation_params['collection_extra_time']))

    time.sleep(max(0,(end2 - datetime.now(timezone.utc)).total_seconds()))

    kill_pod()


    # Waiting for the background process to complete
    log_collection_process.terminate()
    real_time_charts_process.terminate()
    real_time_charts_process.join()

    time.sleep(5)



    # Restart core
    termination_phase(_commands, pod_representants, deletion_order)
    time.sleep(2)
    creation_phase(pod_representants, creation_order)
    print("\nWaiting for 60s before starting the default experiment...\n\n")
    time.sleep(60)
    run_default_experiment(simulation_params, start_time)

    # Commit the results to the remote Git repository
    prometheus_data_collector.git_commit_results('Simulation-'+str(int(start_time)), withDefault=True)   

