import pandas as pd
import os

# Step 1: Define directories and input files
base_dir = '../n3_p30_d30_l4'
seeds = ['seed1', 'seed2', 'seed3', 'seed4', 'seed5','seed6', 'seed7', 'seed8', 'seed9', 'seed10','seed11', 'seed12', 'seed13', 'seed14', 'seed15']
file_name = 'result_train_sync.csv'
input_files = [os.path.join(base_dir, seed, file_name) for seed in seeds]
name_output_file = "high_accuracy"  # low_loss medium_loss high_loss

# Print each file path to verify
for file in input_files:
    if os.path.exists(file):
        print(f"Found: {file}")
    else:
        print(f"Error: Not found: {file}")

# Print the total number of files
print(f"\nTotal number of files checked: {len(input_files)}")

# Step 2: Read and concatenate all input files
dfs = []
for file in input_files:
    if os.path.exists(file):
        df = pd.read_csv(file)
        dfs.append(df)

if len(dfs) == 0:
    print("\nError: No valid input files found.\n")
    exit()

# Step 3: Concatenate all dataframes into one
combined_df = pd.concat(dfs, ignore_index=True)

# Step 4: Sort combined dataframe by 'Client' column
combined_df_sorted = combined_df.sort_values(by=['Client']).reset_index(drop=True)

# Step 5: Drop unnecessary columns
columns_to_drop = ['Train Loss', 'Train Accuracy', 'Validation Loss', 'Processing Time', 'Comm Time', 'Comm Data Size', 'Timestamp']
combined_df_cleaned = combined_df_sorted.drop(columns=columns_to_drop)

# Step 6: Convert 'Validation Accuracy' from a list to a float
combined_df_cleaned['Validation Accuracy'] = combined_df_cleaned['Validation Accuracy'].apply(lambda x: float(x.strip('[]')) if isinstance(x, str) else float(x))

# Step 7: Ensure data types are preserved correctly
# Define columns with specific data types to maintain decimal precision
dtype_map = {
    'Client': int,             # Assuming 'client' is integer
    'Validation Accuracy': float,         # Assuming 'rx_packets' is integer
    #'dist_ap_radius': int      # Assuming 'dist_ap_radius' is integer    
}

# Convert all other columns to float to preserve decimal precision
for col in combined_df_cleaned.columns:
    if col not in dtype_map:
        combined_df_cleaned[col] = combined_df_cleaned[col].astype(float)

# Step 8: Save to output file
output_file = name_output_file + '.csv'

if not os.path.exists(output_file):
    combined_df_cleaned.to_csv(output_file, index=False, float_format='%.6f')
    print(f"\nSuccess: Cleaned and sorted data saved to {output_file}.\n")
else:
    print(f"\nError: {output_file} already exists.\n")

