import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'line_all.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Group by 'User' and get the maximum values for each user in other columns
df_max = df.groupby('User').max().reset_index()

# Plot each column against 'User' with color-coded value labels
plt.figure(figsize=(10, 6))
colors = plt.cm.tab10.colors  # Use a colormap for distinct colors

# Adicionar o valor no ponto de interseção
for i, column in enumerate(df_max.columns[1:]):  # Exclude 'User' for y-axis data
    plt.plot(df_max['User'], df_max[column], label=column, color=colors[i])
    for x, y in zip(df_max['User'], df_max[column]):
        plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', color=colors[i])  # Add color-coded labels

# Add labels and legend
plt.xlabel('User')
plt.ylabel('Metrics')
plt.title('Metrics by User (Maximum Values)')

# Coloca a legenda fora do gráfico, no lado direito
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Ajuste o layout para não cortar a legenda externa
plt.tight_layout()

plt.grid(True)

# Save the plot as a PNG image
plt.savefig('line_allH.png', bbox_inches='tight')  # Save as an image file
#plt.show()
