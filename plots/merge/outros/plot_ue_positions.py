import pandas as pd
import matplotlib.pyplot as plt

def plot_ue_positions_with_distances(csv_file, output_file='ue_positions.png'):
    # Load data from CSV
    data = pd.read_csv(csv_file)

    # Filter data for UE and gNB nodes
    ue_data = data[data['NodeType'] == 'UE']
    gnb_data = data[data['NodeType'] == 'gNB']

    # Extract gNB position
    gnb_x, gnb_y = gnb_data['X'].values[0], gnb_data['Y'].values[0]

    # Create plot
    plt.figure(figsize=(10, 6))

    # Scatter plot for UE positions with color intensity based on distance from the gNB
    sc = plt.scatter(ue_data['X'], ue_data['Y'], c=ue_data['DistanceFromBSS'], cmap='viridis', s=100, alpha=0.7)
    plt.colorbar(sc, label='Distance from gNB (meters)')
    plt.xlabel('X Position (meters)')
    plt.ylabel('Y Position (meters)')
    plt.title('UE Positioning and Distance from gNB with Distance Labels')
    plt.grid(True)

    # Highlight the position of the gNB
    plt.scatter(gnb_x, gnb_y, color='red', label='gNB Position', s=150, marker='X')

    # Draw lines between gNB and each UE, and add distance labels
    for _, row in ue_data.iterrows():
        plt.plot([gnb_x, row['X']], [gnb_y, row['Y']], color='gray', linestyle='--', linewidth=1)
        plt.text((gnb_x + row['X']) / 2, (gnb_y + row['Y']) / 2, f"{row['DistanceFromBSS']:.2f}m",
                 fontsize=11, ha='center', color='blue')

    # Save the plot as a PNG file
    plt.savefig(output_file, format='png', dpi=300)
    print(f"Plot saved as {output_file}")

    plt.legend()
    plt.show()

# Usage example
plot_ue_positions_with_distances('positions.csv', 'ue_positions.png')