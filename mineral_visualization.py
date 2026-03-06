import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter

# High-resolution terrain grid
lat = np.linspace(8.0, 35.0, 350)
lon = np.linspace(68.0, 97.0, 350)
LON, LAT = np.meshgrid(lon, lat)

# Indian terrain: Himalayas (north), Deccan Plateau (central), coastal plains
elevation = 6000 * np.exp(-((LAT - 32)**2 / 40 + (LON - 80)**2 / 150))
elevation += 1200 * np.exp(-((LAT - 20)**2 / 80 + (LON - 78)**2 / 100))
elevation += 400 * np.sin((LAT - 18) / 4) * np.cos((LON - 82) / 5)
elevation = gaussian_filter(elevation, sigma=2)
elevation = np.maximum(elevation, 0)

# Mineral deposits with actual India locations
minerals = {
    'Coal': [(23.5, 86.0), (23.0, 82.0), (18.0, 79.0)],
    'Iron Ore': [(15.5, 75.5), (22.0, 84.0), (15.0, 76.0)],
    'Bauxite': [(23.0, 82.0), (17.0, 82.0)],
    'Copper': [(24.5, 72.5), (22.5, 78.5)],
    'Gold': [(12.5, 78.0), (25.0, 85.0)],
    'Manganese': [(21.0, 79.0), (15.5, 74.5)]
}

colors = {
    'Coal': '#2d2d2d',
    'Iron Ore': '#ff4444',
    'Bauxite': '#ff8800',
    'Copper': '#cc7722',
    'Gold': '#ffd700',
    'Manganese': '#9933ff'
}

# Create figure with dark background
fig = plt.figure(figsize=(20, 14), facecolor='#0d1117')
ax = fig.add_subplot(111, projection='3d', facecolor='#0d1117')

# Plot smooth terrain with vibrant colormap
surf = ax.plot_surface(LON, LAT, elevation, cmap='turbo', 
                       linewidth=0, antialiased=True, alpha=0.9,
                       vmin=0, vmax=elevation.max(), 
                       rcount=300, ccount=300, shade=True)

# Remove axis box and grid for clean floating look
ax.set_axis_off()

# Plot glowing mineral markers
for mineral, locations in minerals.items():
    for lat_m, lon_m in locations:
        lat_idx = np.argmin(np.abs(lat - lat_m))
        lon_idx = np.argmin(np.abs(lon - lon_m))
        elev = elevation[lat_idx, lon_idx]
        
        # Glowing marker
        ax.scatter(lon_m, lat_m, elev + 400, c=colors[mineral], 
                  s=600, marker='o', edgecolors='white', 
                  linewidths=4, alpha=1.0, label=mineral, depthshade=False)
        
        # Vertical indicator line
        ax.plot([lon_m, lon_m], [lat_m, lat_m], [elev, elev + 400],
               color=colors[mineral], linewidth=3, alpha=0.8)

# Title
ax.text2D(0.5, 0.95, 'Mineral Distribution Visualization', 
          transform=ax.transAxes, fontsize=28, weight='bold',
          color='white', ha='center', va='top')

# Legend
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
legend = ax.legend(by_label.values(), by_label.keys(), 
                  loc='upper left', fontsize=14, framealpha=0.8,
                  facecolor='#1c1c1c', edgecolor='white', 
                  labelcolor='white', markerscale=0.8)

# Cinematic camera angle
ax.view_init(elev=30, azim=50)

# Colorbar
cbar = plt.colorbar(surf, ax=ax, shrink=0.5, aspect=15, pad=0.05)
cbar.set_label('Elevation (m)', color='white', fontsize=13)
cbar.ax.tick_params(colors='white', labelsize=11)
cbar.outline.set_edgecolor('white')

plt.tight_layout()
plt.savefig('mineral_distribution_visualization.png', dpi=300, 
            bbox_inches='tight', facecolor='#0d1117')
print("✅ Visualization created: mineral_distribution_visualization.png")
print(f"📍 Total mineral deposits plotted: {sum(len(v) for v in minerals.values())}")
plt.show()
