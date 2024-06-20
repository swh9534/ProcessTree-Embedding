import pm4py
import numpy as np
import math
import os

# Load the event log
LOG_FILENAMES = [f'BPIC15_{i}_rev' for i in range(1, 6)]

for idx, LOG_FILENAME in enumerate(LOG_FILENAMES):
    # if there's no directory for the log, create one
    # if not os.path.exists(f'data/{LOG_FILENAME}'):
    #     os.makedirs(f'{LOG_FILENAME}')

    log = pm4py.read_xes(f'data/{LOG_FILENAME}.xes')

    # NUM_THRESHOLD = 100
    # noise_thresholds = []
    # for i in range(1, NUM_THRESHOLD):
    #     noise_thresholds.append(i/NUM_THRESHOLD)
    noise_threshold = 0.8
    
    case_sizes = [len(trace) for trace in log]

    # Define the number of intervals you want
    NUM_INTERVALS = 5

    # Calculate the quantiles
    quantiles = np.linspace(0, 1, NUM_INTERVALS+1)
    
    NUM_INTERVALS = len(quantiles)
    # Calculate the intervals
    intervals = [(np.quantile(case_sizes, q), np.quantile(case_sizes, q+1/NUM_INTERVALS)) for q in quantiles[:-1]]

    # create process_trees.txt
    # with open(f"{LOG_FILENAME}/0_metadata.txt", "w") as file:
    #     file.write("visualization_filename, serialization\n")

    serializations = set()

    # Loop through each combination of filtering and noise threshold
    for i, interval in enumerate(intervals):
        # filtered_log = pm4py.filter_variants_by_coverage_percentage(log, coverage, activity_key='concept:name', timestamp_key='time:timestamp', case_id_key='case:concept:name')
        lower_bound = math.floor(interval[0])
        upper_bound = math.ceil(interval[1])
        # lower_bound = 17
        # upper_bound = 22
        
        filtered_log = pm4py.filter_case_size(log, lower_bound, upper_bound, case_id_key='case:concept:name')
        # for noise_threshold in noise_thresholds:
        #     # Discover the process tree with the given noise threshold
        #     tree = pm4py.discover_process_tree_inductive(filtered_log, noise_threshold=noise_threshold,activity_key='activityNameEN', case_id_key='case:concept:name', timestamp_key='time:timestamp')
        #     filename = f"{LOG_FILENAME}/process_tree_case_size_betwee_{lower_bound}_and_{upper_bound}_noise_{int(noise_threshold*100)}.svg"
        #     serialization = tree.to_string()
        #     if serialization in serializations:
        #         continue
        #     serializations.add(serialization)
        #     # append to process_trees.txt
        #     with open(f"{LOG_FILENAME}/0_metadata.txt", "a") as file:
        #         file.write(f"{filename, serialization}\n")
        #     pm4py.save_vis_process_tree(tree, filename)
        #     print(f"Model saved: {filename}")
        # 노이즈 임계값을 5개씩 그룹화하여 처리
        # for i in range(0, 20):
        #     case_folder = f"{LOG_FILENAME}"
        #     os.makedirs(case_folder, exist_ok=True)
            
            # 현재 케이스에 해당하는 노이즈 임계값 범위
            # current_thresholds = noise_thresholds[i*5:(i+1)*5]
            
            
        tree = pm4py.discover_process_tree_inductive(filtered_log, noise_threshold=noise_threshold, activity_key='activityNameEN', case_id_key='case:concept:name', timestamp_key='time:timestamp')

        # 파일 이름 설정
        directory = f"20_80_interval5/80_interval5/{LOG_FILENAME}"
        filename = f"{directory}/process_tree_case_size_between_{lower_bound}_and_{upper_bound}_noise_{int(noise_threshold*100)}.svg"

        # 디렉토리가 존재하지 않으면 생성
        os.makedirs(directory, exist_ok=True)

        # 시리얼화된 트리를 문자열로 변환
        serialization = tree.to_string()

        # 시리얼화된 트리가 이미 존재하는 경우 건너뛰기
        if serialization in serializations:
            continue

        # 새로운 시리얼화된 트리를 세트에 추가
        serializations.add(serialization)

        # 메타데이터 파일에 추가
        metadata_filename = f"20_80_interval5/80_interval5/{LOG_FILENAME}/{i+1}_metadata.txt"
        os.makedirs(os.path.dirname(metadata_filename), exist_ok=True)
        with open(metadata_filename, "a") as file:
            file.write(f"{filename, serialization}\n")

        # 프로세스 트리 시각화를 파일로 저장
        pm4py.save_vis_process_tree(tree, filename)
        print(f"Model saved: {filename}")

    print("All models have been generated and saved.")