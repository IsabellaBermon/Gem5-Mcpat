"""
Bot that runs Gem5 simulations and extracts the metric CPI of the stat.txt generated
Authors: 
    Isabella Bermón Rojas
    Jonathan Alexis Valencia
"""
import os
import itertools
from concurrent.futures import ThreadPoolExecutor

# Memory Options
l1i_size = ['64kB', '128kB']
l1i_lat = [2,4]
l1d_size = ['64kB', '256kB']
l1d_lat = [2,4]
l2_size = ['1MB', '2MB']
l2_lat = [9, 12]
# CPU Options
fetch_width = [8,12]
decode_width = [8]
fb_entries = [16,64]
fq_entries = [16]
num_fu_intALU = [2,4]

# Paths for the configuration
gem5_cmd = "build/ARM/gem5.fast"
config_file = "configs/CortexA76/CortexA76.py"
workload_path = "workloads/mp3_dec/mp3_dec"
resources = "-w workloads/mp3_dec/mp3dec_outfile.wav workloads/mp3_dec/mp3dec_testfile.mp3"

# Compute all combinations using itertools.product
combinations = list(itertools.product(l1i_size, l1i_lat, l1d_size, l1d_lat, l2_size,l2_lat,fetch_width,decode_width, fb_entries,fq_entries,num_fu_intALU))

# Function to run all possible combinations
def run_combination(combo, index_combination):
    # Construct the full command
    command = f"{gem5_cmd} --stats-file=stats_sim_{index_combination}.txt --json-config=config_sim_{index_combination}.json {config_file} --cmd={workload_path} --options='{resources}' --l1i_size={combo[0]} --l1i_lat={combo[1]} --l1d_size={combo[2]} --l1d_lat={combo[3]} --l2_size={combo[4]} --l2_lat={combo[5]} --fetch_width={combo[6]} --decode_width={combo[6]} --fb_entries={combo[8]} --fq_entries={combo[9]} --num_fu_intALU={combo[10]}"
    # print("COMANDO= ", command)
    # Execute the command
    os.system(command)
    # After running the command, extract the desired metric from stats.txt
    extracted_metrics = []
    with open(f"m5out/stats_sim_{index_combination}.txt", 'r') as stats_file:
        for line in stats_file:
            if "system.cpu.cpi" in line:
                extracted_metrics.append(line.strip())
                break
    # Create destination path if dosen´t exisit
    os.makedirs("m5out/extracted_metrics", exist_ok=True)
    # Write the extracted metrics to a text file
    with open(f"m5out/extracted_metrics/sim_{index_combination}.txt", 'w') as output_file:
        output_file.write(f"l1i_size: {combo[0]}\n")
        output_file.write(f"l1i_lat: {combo[1]}\n")
        output_file.write(f"l1d_size: {combo[2]}\n")
        output_file.write(f"l1d_lat: {combo[3]}\n")
        output_file.write(f"l2_size: {combo[4]}\n")
        output_file.write(f"l2_lat: {combo[5]}\n")
        output_file.write(f"fetch_width: {combo[6]}\n")
        output_file.write(f"decode_width: {combo[6]}\n")
        output_file.write(f"fb_entries: {combo[8]}\n")
        output_file.write(f"fq_entries: {combo[9]}\n")
        output_file.write(f"num_fu_intALU: {combo[10]}\n")
        for metric in extracted_metrics:
            output_file.write(f"Metric: {metric}\n")
        output_file.write("\n")
    print("Metrics saved to extracted_metrics.txt")

# Total num of simulations
total_simulations = 512
# Batch size (how many simulations to run simultaneously)
batch_size = 12

# Use ThreadPoolExecutor to execute combinations in batches
with ThreadPoolExecutor(max_workers=batch_size) as executor:
    for batch_start in range(0, total_simulations, batch_size):
        # Get the simulations for this batch
        batch_combinations = combinations[batch_start:batch_start + batch_size]
        # Enumerate combinations and run them in concurrent threads
        for index, combo in enumerate(batch_combinations):
            executor.submit(run_combination, combo, index + batch_start)
