"""
3D Mineral Visualization Script
This script creates an interactive 3D visualization of mineral locations.

To use with your actual data:
1. Install required packages: pip install geopandas matplotlib numpy
2. Update the shapefile path below
3. Run the script
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def create_3d_visualization(longitude, latitude, elevation, mineral_types=None):
    """
    Create a 3D visualization of mineral locations
    
    Parameters:
    - longitude: array of longitude coordinates
    - latitude: array of latitude coordinates
    - elevation: array of elevation values
    - mineral_types: optional array of mineral type labels
    """
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create color map based on elevation or mineral type
    if mineral_types is not None:
        colors = mineral_types
        cmap = 'tab20'
    else:
        colors = elevation
        cmap = 'terrain'
    
    # Create scatter plot
    scatter = ax.scatter(longitude, latitude, elevation, 
                        c=colors, cmap=cmap, 
                        marker='o', s=150, alpha=0.8, 
                        edgecolors='black', linewidth=0.5)
    
    # Labels and title
    ax.set_xlabel('Longitude (°E)', fontsize=14, labelpad=15)
    ax.set_ylabel('Latitude (°N)', fontsize=14, labelpad=15)
    ax.set_zlabel('Elevation (m)', fontsize=14, labelpad=15)
    ax.set_title('3D Visualization of Mineral Deposits\nKarnataka and Andhra Pradesh Region', 
                 fontsize=16, pad=25, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.7)
    if mineral_types is not None:
        cbar.set_label('Mineral Type', fontsize=12)
    else:
        cbar.set_label('Elevation (m)', fontsize=12)
    
    # Adjust viewing angle for better perspective
    ax.view_init(elev=25, azim=45)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    return fig, ax

# Example usage with sample data
print("Creating 3D visualization...")

# Sample data (replace with actual data from your shapefile)
np.random.seed(42)
n_points = 150

# Generate sample coordinates
longitude = np.random.uniform(76.40, 76.50, n_points)
latitude = np.random.uniform(14.04, 14.08, n_points)
elevation = np.random.uniform(400, 700, n_points)

# Create visualization
fig, ax = create_3d_visualization(longitude, latitude, elevation)

# Save the figure
output_file = 'mineral_3d_advanced.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"[OK] 3D visualization saved as '{output_file}'")
print(f"[OK] Visualized {n_points} mineral locations")

# Create multiple views
angles = [(20, 45), (20, 135), (60, 45)]
for i, (elev, azim) in enumerate(angles):
    ax.view_init(elev=elev, azim=azim)
    plt.savefig(f'mineral_3d_view_{i+1}.png', dpi=300, bbox_inches='tight', facecolor='white')
    print(f"[OK] Saved view {i+1} (elevation={elev} degrees, azimuth={azim} degrees)")

print("\nVisualization complete!")
print("\nTo use with your actual data:")
print("1. Extract coordinates from your shapefile")
print("2. Replace the sample data with actual longitude, latitude, and elevation")
print("3. Optionally add mineral type information for color coding")

plt.show()
