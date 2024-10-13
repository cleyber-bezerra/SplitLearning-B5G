import pandas as pd
import os

def split_csv_by_user(input_file, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Load the CSV file
    df = pd.read_csv(input_file)
    
    # Drop the unwanted columns
    df = df.drop(columns=["Train Accuracy", "Timestamp"])
    
    # Get unique users from the 'User' column
    users = df['User'].unique()

    # Create individual CSVs for each user
    for user in users:
        user_df = df[df['User'] == user]
        # Format the filename by replacing spaces in user name and creating the CSV file
        user_filename = os.path.join(output_directory, f'{user.strip().replace(" ", "_")}.csv')
        user_df.to_csv(user_filename, index=False)
        print(f'File created: {user_filename}')

# Example usage:
input_file = 'result_train_sync.csv'
output_directory = './'
split_csv_by_user(input_file, output_directory)
