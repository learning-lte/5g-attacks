import numpy as np
import pandas as pd
from utils import *
from re import search
import csv
import matplotlib.pyplot as plt


containers_color = {
    'amf1': 'tab:red',
    'amf2': 'tab:orange',
    'ausf':'tab:pink',
    'udm': 'tab:purple',
    'upf': 'tab:blue',
    'smf': 'tab:cyan',
    'gnb1': 'tab:green',
    'gnb2': 'tab:olive',
    'ue1':  'tab:gray',
    'ue2': 'tab:brown'
}


def data_processing(data, label, paths, withAttackers=False):
    raw_data1 = pd.read_csv(paths[0])
    values1 = raw_data1.iloc[:, -1].tolist()

    if len(paths)>1 and withAttackers:
        try:
            raw_data2 = pd.read_csv(paths[1])
            values2 = raw_data2.iloc[:, -1].tolist()
        except pd.errors.EmptyDataError:
            values2 = []
    else:
        values2 = []
    values = values1 + values2

    data[label] = {}
    data[label]['processing_times'] = values

    # Compute the quartiles
    first_quartile = np.percentile(values, 25)
    median = np.percentile(values, 50)
    ninetieth_quartile = np.percentile(values, 90)
    data[label]['quartiles'] = [first_quartile, median, ninetieth_quartile]

    return data


def get_quartiles_ue(results, output):
    suffix1 = '/ue-data/ue1-benign_registration_time.csv'
    suffix2 = '/ue-data/ue1_registration_time.csv'
    data = {}

    for path, label in results.items():
        paths = [path+suffix1, path+suffix2]
        """if 'Ghost' in label:
            paths = [path+'/ue-data_default/ue1-benign_registration_time.csv']
            data = data_processing(data, 'No storm', paths)"""
        data = data_processing(data, label, paths)

        print(f'--  UE ({label})  --\n', data[label]['quartiles'])

    dataKeys, dataValues = [],[]
    for key, value in data.items():
        dataKeys.append(key) 
        dataValues.append(value)

    plt.figure()
    scale = 2 if len(dataKeys)>4 else 1  
    positions = [scale*(i+1) for i in range(len(dataKeys))]
    plt.boxplot([values['processing_times'] for values in dataValues], positions=positions,showfliers=False)
    plt.title('Comparison of initial registration time')
    plt.ylabel('Registration processing time (s)')
    plt.xticks(positions, dataKeys)
    plt.savefig(f'{output}ue_rt_cmp.png')
    plt.close()


def get_quartiles_amf():
    data = get_amf_rt()
    quartiles = {}
    labels = []

    for label in data:
        labels.append(label)
        values = data[label][1]

        # Compute the quartiles
        first_quartile = np.percentile(values, 25)
        median = np.percentile(values, 50)
        sixtieth_quartile = np.percentile(values, 60)

        seventifiveth_quartile = np.percentile(values, 80)
        ninetieth_quartile = np.percentile(values, 90)
        quartiles[label] = [first_quartile, median, sixtieth_quartile, seventifiveth_quartile, ninetieth_quartile]
        print(f'--  AMF ({label})  --\n', quartiles[label])


    plt.figure()
    plt.boxplot([data[labels[0]][1], data[labels[1]][1]], labels=labels)
    plt.title('Comparison of RT at AMF')
    plt.ylabel('Initial registration processing time (s)')
    plt.xlabel('Context')
    plt.xticks([1, 2], ['No attackers', 'With attackers'])
    plt.savefig('amf_rt_cmp.png')
    plt.close()


"""def compare_packet_rate():
    suffix1 = '/data/ue1-benign_registration_time.csv'
    suffix2 = '/data/ue1_registration_time.csv'
    data = {}

    for path, label in results.items():
        paths = [path+suffix1, path+suffix2]
        data = ?????(data, label, paths)


    for filename in paths:
        packets_file = filename + '/data/'
        filepaths = []
        data_file = []
        # Iterate over files in the folder
        for file in os.listdir(packets_file):
            file_path = os.path.join(packets_file, file)
            if os.path.isfile(file_path):
                file_metric = file.split('-')[-1].split('.')[0]
                if file_metric == 'irate(container_network_receive_packets_total':
                    filepaths.append(file_path)

        # Create a new figure for each metric group
        plt.figure()

        graphs[f'{paths[filename]}-{filename.split("/")[-1]}'][1]= [x_values, y_values]

        for file in filepaths:
            # Plotting the figure for the group of files
            X, Y = [],[]
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for data_point in reader:
                    x, y = map(float, data_point)
                    X.append(x - origin)
                    Y.append(y)
            data = X,Y

            values = data[1]
            container = file.split('/')[-1].split('-')[0]

            linestyle = '-'
            if container not in ['upf', 'smf']:
                plt.plot(data[0], values, label=container, color=containers_color[container], linestyle=linestyle)

                # Set the labels and title
                title, ylabel = 'Rate of packets received per NF', "Packets/s"
                plt.xlabel('Time (s)')
                plt.ylabel(ylabel)
                plt.title(title)
                plt.xlim(0, end-origin)  # Adjust the range as needed
                plt.legend(loc=1)

        # Save the chart as an image
        plt.savefig(f'{output}/{paths[filename]}-{filename.split("/")[-1]}_kpi')

        # Close the figure to free up resources
        plt.close()

        print(f'--  Packet rate ({label})  --\n', data[label]['quartiles'])

    dataKeys, dataValues = [],[]
    for key, value in data.items():
        dataKeys.append(key) 
        dataValues.append(value)

    plt.figure()
    plt.boxplot([values['packet_rate'] for values in dataValues], showfliers=False)
    plt.title('Comparison of packets received')
    plt.ylabel('Packets/s')
    plt.xticks([i+1 for i in range(len(dataKeys))], dataKeys)
    plt.savefig(f'{output}packets_cmp.png')
    plt.close()
"""

def get_amf_rt():
    START_EXPR = r"Handle Registration Request"
    END_EXPR = r"Handle InitialRegistration"
    pattern = r"\[AMF_UE_NGAP_ID:(\d+)\]"

    files = {
        'logs-default/free5gc-amf1.txt':'No attackers',
        'logs/free5gc-amf1.txt':'With attackers'
    }

    output = {}
    ngap_trace = {}
    for filename in files:
        registration_prc_times = [[],[]]
        logs = parse_log(filename,format='AMF')
        for timestamp, line in logs:
            match_start = search(START_EXPR, line)
            match_end = search(END_EXPR, line)
            # Define the pattern to match

            if match_start:
                # Search for a match and extract the NGAP number
                match = search(pattern, line)
                if match:
                    ngap_id = match.group(1)
                    ngap_trace[ngap_id] = timestamp

            elif match_end:
                # Search for a match and extract the NGAP number
                match = search(pattern, line)
                if match:
                    ngap_id = match.group(1)
                    start_time = ngap_trace[ngap_id]
                    time_for_procedure = (timestamp - start_time).total_seconds()
                    registration_prc_times[0].append(start_time)
                    registration_prc_times[1].append(time_for_procedure)
                    del ngap_trace[ngap_id]
        output[files[filename]] = registration_prc_times
    
    return output


def get_data(filename, offset):
    data_file = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Convert the data to float
            x = float(row[0]) - offset
            y = float(row[1])
            data_file.append((x, y))
    x_values = [row[0] for row in data_file]
    y_values = [row[1] for row in data_file]
    return x_values, y_values


def plot_clear_graphs(paths, y_max, output):
    graphs = {}
    for filename in paths:
        one_filename = filename
        break

    x_waves = []
    with open(one_filename + '/ue-data/ue1_wave_time.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Convert the data to float
            x = float(row[0])
            x_waves.append(x)
    origin, end = x_waves[1]-10, x_waves[-1]+50

    for filename in paths:
        times_file_storm = filename + '/ue-data/ue1_registration_time.csv'
        x_values, y_values = get_data(times_file_storm, origin)
        graphs[f'{paths[filename]}-{filename.split("/")[-1]}']= [[x_values, y_values],[]]

        
        times_file_benign = filename + '/ue-data/ue1-benign_registration_time.csv'
        x_values, y_values = get_data(times_file_benign, origin)
        graphs[f'{paths[filename]}-{filename.split("/")[-1]}'][1]= [x_values, y_values]
        if 'Ghost' in paths[filename]:
            ghosts_x, ghosts_y = x_values, y_values

        #========================================
        packets_file = filename + '/data/'
        filepaths = []
        data_file = []
        # Iterate over files in the folder
        for file in os.listdir(packets_file):
            file_path = os.path.join(packets_file, file)
            if os.path.isfile(file_path):
                file_metric = file.split('-')[-1].split('.')[0]
                if file_metric == 'irate(container_network_receive_packets_total':
                    filepaths.append(file_path)

        # Create a new figure for each metric group
        plt.figure()

        graphs[f'{paths[filename]}-{filename.split("/")[-1]}'][1]= [x_values, y_values]

        for file in filepaths:
            # Plotting the figure for the group of files
            X, Y = [],[]
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for data_point in reader:
                    x, y = map(float, data_point)
                    X.append(x - origin)
                    Y.append(y)
            data = X,Y

            values = data[1]
            container = file.split('/')[-1].split('-')[0]

            linestyle = '-'
            if container not in ['upf', 'smf']:
                plt.plot(data[0], values, label=container, color=containers_color[container], linestyle=linestyle)

                # Set the labels and title
                title, ylabel = f'[{filename.split("/")[-1].split("-")[0]}] Rate of packets received per NF', "Packets/s"
                plt.xlabel('Time (s)')
                plt.ylabel(ylabel)
                plt.title(title)
                plt.xlim(0, end-origin)  # Adjust the range as needed
                plt.legend(loc=1)

        # Save the chart as an image
        plt.savefig(f'{output}/{paths[filename]}-{filename.split("/")[-1]}_kpi')

        # Close the figure to free up resources
        plt.close()
    


    for name, values in graphs.items():
        x_storm, y_storm = values[0]
        x_benign, y_benign = values[1]

        # Plot the data
        if len(x_storm)>0:
            plt.plot(x_storm, y_storm, 'x', label=f'Storm registrations', color='tab:red')
            #ghosts_x, ghosts_y = x_storm, y_storm
        #elif 'Ghost' in name:
        #    plt.plot(ghosts_x, ghosts_y, 'x', label=f'Ghosts from the default storm', color='tab:gray')

        plt.plot(x_benign, y_benign, 'x', label=f'Benign registrations', color='tab:green')
        #plt.plot(x_waves, [0]*len(x_waves), 'o', label="Waves", color='tab:blue')
        plt.xlabel('Time (s)',)
        plt.ylabel('Processing time (s)')
        plt.title(f'[{name.split("-")[0]}] UE requests processing time')
        plt.grid(True)
        plt.legend(loc=1)
        plt.xlim(0, end-origin)  # Adjust the range as needed
        plt.ylim(0, y_max)  # Adjust the range as needed

        plt.savefig(f'{output}{name}')
        plt.close()
        print(f'Chart generated.')


if __name__ == "__main__":
    prefix = '/home/paul/testbed/attack-data-collection/5g-attacks/'
    output = 'charts_paper/'

    selector = 60

    if selector == 30:
        results = {
            f'{prefix}Simulation-1688775784': 'No storm',
            f'{prefix}Simulation-1688764830': 'Default storm',
            f'{prefix}Simulation-1688771189': 'Ghost storm',
            f'{prefix}Simulation-1688763205': 'AMF-active storm'
        }
        max_time = 1

    elif selector == 60:
        results = {
            f'{prefix}Simulation-1688775784': 'No storm',
            f'{prefix}Simulation-1688777383': 'Default storm',
            f'{prefix}Simulation-1688781750': 'Ghost storm',
            f'{prefix}Simulation-1688783571': 'AMF-active storm'
        }
        max_time = 2
    
    else:
        print("ERROR\nPlease choose a valid selector")
    
    plot_clear_graphs(results, max_time, output)
    
    get_quartiles_ue(results, output)

    #get_quartiles_amf()