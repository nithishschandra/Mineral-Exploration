import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

# Find and load the mineralization data
mineralization_path = None
for root, dirs, files in os.walk('geo_data'):
    for file in files:
        if 'mineralization' in file and file.endswith('.shp'):
            mineralization_path = os.path.join(root, file)
            break

if mineralization_path:
    print(f"Loading data from: {mineralization_path}")
    gdf = gpd.read_file(mineralization_path)
    
    # Extract coordinates
    gdf['x'] = gdf.geometry.x
    gdf['y'] = gdf.geometry.y
    
    # Create a simple z-coordinate (you can modify this based on actual elevation data)
    gdf['z'] = np.random.uniform(0, 100, len(gdf))  # Random elevation for demonstration
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot points
    scatter = ax.scatter(gdf['x'], gdf['y'], gdf['z'], 
                        c=range(len(gdf)), cmap='viridis', 
                        marker='o', s=50, alpha=0.6)
    
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Elevation (arbitrary)')
    ax.set_title('3D Visualization of Mineral Locations')
    
    plt.colorbar(scatter, label='Point Index')
    plt.savefig('mineral_3d_visualization.png', dpi=300, bbox_inches='tight')
    print("3D visualization saved as 'mineral_3d_visualization.png'")
    plt.show()
else:
    print("Mineralization shapefile not found!")
