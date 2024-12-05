import pandas as pd

# Define the input and output file paths
input_file = "high_accuracy1.csv"  # Replace with your input file name
output_file = "high_accuracy.csv"  # Replace with your desired output file name

# Define the mapping for User column
mapping = {
   'user 1': 151.17,
   'user 2': 90.04,
   'user 3': 51.55,
   'user 4': 66.43,
   'user 5': 154.13,
   'user 6': 91.84
}

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Apply the mapping to the 'User' column
df['User'] = df['User'].map(mapping)

# Save the modified DataFrame back to a CSV file
df.to_csv(output_file, index=False)

print(f"File saved successfully to {output_file}")


# Define the input and output file paths
input_file = "low_accuracy1.csv"  # Replace with your input file name
output_file = "low_accuracy.csv"  # Replace with your desired output file name

# Define the mapping for User column
mapping = {
   'user 1': 151.17,
   'user 2': 90.04,
   'user 3': 51.55,
   'user 4': 66.43,
   'user 5': 154.13,
   'user 6': 91.84
}

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Apply the mapping to the 'User' column
df['User'] = df['User'].map(mapping)

# Save the modified DataFrame back to a CSV file
df.to_csv(output_file, index=False)

print(f"File saved successfully to {output_file}")

# Define the input and output file paths
input_file = "merge_accuracy1.csv"  # Replace with your input file name
output_file = "merge_accuracy.csv"  # Replace with your desired output file name

# Define the mapping for User column
mapping = {
   'user 1': 151.17,
   'user 2': 90.04,
   'user 3': 51.55,
   'user 4': 66.43,
   'user 5': 154.13,
   'user 6': 91.84
}

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Apply the mapping to the 'User' column
df['User'] = df['User'].map(mapping)

# Save the modified DataFrame back to a CSV file
df.to_csv(output_file, index=False)

print(f"File saved successfully to {output_file}")