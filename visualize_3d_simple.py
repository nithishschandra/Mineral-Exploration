import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Sample data - you'll need to extract actual coordinates from your shapefile
# For demonstration, I'll create sample mineral locations
np.random.seed(42)

# Generate sample coordinates (replace with actual data from your shapefile)
n_points = 100
longitude = np.random.uniform(76.4, 76.5, n_points)
latitude = np.random.uniform(14.0, 14.1, n_points)
elevation = np.random.uniform(0, 500, n_points)  # Elevation in meters

# Create 3D plot
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Create scatter plot
scatter = ax.scatter(longitude, latitude, elevation, 
                    c=elevation, cmap='terrain', 
                    marker='o', s=100, alpha=0.7, edgecolors='black')

# Labels and title
ax.set_xlabel('Longitude', fontsize=12, labelpad=10)
ax.set_ylabel('Latitude', fontsize=12, labelpad=10)
ax.set_zlabel('Elevation (m)', fontsize=12, labelpad=10)
ax.set_title('3D Visualization of Mineral Locations\nKarnataka and Andhra Pradesh Region', 
             fontsize=14, pad=20)

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
cbar.set_label('Elevation (m)', fontsize=10)

# Adjust viewing angle
ax.view_init(elev=20, azim=45)

# Save the figure
plt.savefig('mineral_3d_visualization.png', dpi=300, bbox_inches='tight')
print("3D visualization saved as 'mineral_3d_visualization.png'")
print(f"Visualized {n_points} mineral locations")
plt.show()
