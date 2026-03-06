import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# India geographical bounds
lat_min, lat_max = 8.0, 35.0
lon_min, lon_max = 68.0, 97.0

# Create terrain grid
lat = np.linspace(lat_min, lat_max, 200)
lon = np.linspace(lon_min, lon_max, 200)
LON, LAT = np.meshgrid(lon, lat)

# Simulate elevation (Himalayas in north, coastal plains in south)
elevation = 3000 * np.exp(-((LAT - 30)**2 / 100 + (LON - 80)**2 / 200))
elevation += 500 * np.sin((LAT - 15) / 5) * np.cos((LON - 80) / 5)
elevation = np.maximum(elevation, 0)

# Major mineral deposits in India (approximate locations)
minerals = {
    'Coal': [(23.5, 86.0), (23.0, 82.0), (18.0, 79.0)],  # Jharkhand, Chhattisgarh, Odisha
    'Iron Ore': [(15.5, 75.5), (22.0, 84.0), (15.0, 76.0)],  # Karnataka, Odisha, Goa
    'Bauxite': [(23.0, 82.0), (17.0, 82.0)],  # Chhattisgarh, Odisha
    'Copper': [(24.5, 72.5), (22.5, 78.5)],  # Rajasthan, Madhya Pradesh
    'Gold': [(12.5, 78.0), (25.0, 85.0)],  # Karnataka, Bihar
    'Manganese': [(21.0, 79.0), (15.5, 74.5)],  # Maharashtra, Karnataka
    'Limestone': [(23.0, 77.0), (26.0, 73.0)],  # Madhya Pradesh, Rajasthan
}

colors = {'Coal': 'black', 'Iron Ore': 'red', 'Bauxite': 'orange', 
          'Copper': 'brown', 'Gold': 'gold', 'Manganese': 'purple', 'Limestone': 'gray'}

# Create 3D plot
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111, projection='3d')

# Plot terrain
surf = ax.plot_surface(LON, LAT, elevation, cmap=cm.terrain, alpha=0.7, 
                       linewidth=0, antialiased=True)

# Plot mineral deposits
for mineral, locations in minerals.items():
    for lat_m, lon_m in locations:
        # Get elevation at mineral location
        lat_idx = np.argmin(np.abs(lat - lat_m))
        lon_idx = np.argmin(np.abs(lon - lon_m))
        elev = elevation[lat_idx, lon_idx]
        
        ax.scatter(lon_m, lat_m, elev + 200, c=colors[mineral], s=200, 
                  marker='o', edgecolors='black', linewidths=2, label=mineral)

# Remove duplicate labels
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize=10)

ax.set_xlabel('Longitude (°E)', fontsize=12)
ax.set_ylabel('Latitude (°N)', fontsize=12)
ax.set_zlabel('Elevation (m)', fontsize=12)
ax.set_title('3D Terrain Model of India with Mineral Deposits', fontsize=16, fontweight='bold')

# Set viewing angle
ax.view_init(elev=30, azim=45)

plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Elevation (m)')
plt.tight_layout()
plt.savefig('india_terrain_minerals_3d.png', dpi=300, bbox_inches='tight')
print("3D terrain model saved as 'india_terrain_minerals_3d.png'")
print(f"Plotted {sum(len(v) for v in minerals.values())} mineral deposits across India")
plt.show()
