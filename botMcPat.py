

import os




combinations = 512

# List to store extracted metrics
extracted_metrics = []
index_combination = 0


for index in range(combinations):  

    # Construct the full command
    command = f"python2 gem5toMcPAT_cortexA76.py stats_sim_{index}.txt config_sim_{index}.json"
    
    # Execute the command
    os.system(command)
    


for index in range(combinations):  

    # Construct the full command
    command = f"./mcpat -infile  config_sim_{index}.xml > powerdata/power_data_sim_{index}.log"
    
    # Execute the command
    os.system(command)
