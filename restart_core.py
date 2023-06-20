import subprocess
from datetime import datetime
import time


def exec_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode().strip()  # Decode and remove leading/trailing whitespace
    error = result.stderr.decode().strip()

    if error:
        print(f"Error occurred: {error}")
    return output


def termination_phase(pod_representants, order):

    # Terminate the pods one by one
    for pod_name in order:

        # Terminate the pod
        exec_command(f'kubectl delete -f ./../5g-manifests/{pod_name} --recursive -n paul')

        # Wait until the pod is no longer in the terminating status
        pods = []
        for pod in pod_representants[pod_name]:
            pods.append(exec_command(f"kubectl get pods -n paul | awk '/{pod}" + "/ {print $1;exit}'"))

        for pod in pods:
            if pod: 
                while(exec_command("kubectl get pods -n paul | awk '/" + pod + "/ {print $1;exit}'")):
                    time.sleep(1)

        print(f"Pod '{pod_name}' terminated successfully.")  


def creation_phase(pod_representants, order):

    # Terminate the pods one by one
    for pod_name in order:

        # Terminate the pod
        exec_command(f'kubectl apply -f ./../5g-manifests/{pod_name} --recursive -n paul')

        time.sleep(0.5)
        # Wait until the pod is no longer in the terminating status
        pods = []
        for pod in pod_representants[pod_name]:
            pods.append(exec_command(f"kubectl get pods -n paul | awk '/{pod}" + "/ {print $1;exit}'"))
            print(exec_command(f"kubectl get pods -n paul | awk '/{pod}" + "/ {print $1;exit}'"))

        for pod in pods:
            while exec_command(f"kubectl get pod {pod} -n paul -o json | jq -r '.status.phase'") != 'Running':
                if exec_command(f"kubectl get pod {pod} -n paul -o json | jq -r '.status.phase'") in ['CrashLoopBaskOff', 'error', 'Completed']:
                    print('Failed', pod)
                    return
                time.sleep(1)

        time.sleep(2)
        print(f"Pod '{pod_name}' up and running.")  

if __name__ == "__main__":

    # Careful while modifying these!
    pod_representants = {
    'free5gc-v3.2.0-duplicate':['free5gc-nrf', 'free5gc-upf'],
    'ueransim-v3.2.6-gnb-duplicate':['ueransim-gnb1'],
    'ueransim-v3.2.6-ue-duplicate':['ueransim-ue1','ueransim-ue2']
    }

    deletion_order = ['ueransim-v3.2.6-ue-duplicate', 'ueransim-v3.2.6-gnb-duplicate', 'free5gc-v3.2.0-duplicate']
    creation_order = ['free5gc-v3.2.0-duplicate', 'ueransim-v3.2.6-gnb-duplicate']

    termination_phase(pod_representants, deletion_order)
    time.sleep(2)
    creation_phase(pod_representants, creation_order)