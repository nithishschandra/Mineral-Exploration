import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter

# Ultra HD resolution
lat = np.linspace(8.0, 35.0, 500)
lon = np.linspace(68.0, 97.0, 500)
LON, LAT = np.meshgrid(lon, lat)

# Indian subcontinent terrain: Himalayas (north), Deccan Plateau (central), Coastal plains (south)
elevation = 6000 * np.exp(-((LAT - 32)**2 / 40 + (LON - 80)**2 / 150))  # Himalayas
elevation += 1200 * np.exp(-((LAT - 20)**2 / 80 + (LON - 78)**2 / 100))  # Deccan Plateau
elevation += 400 * np.sin((LAT - 18) / 4) * np.cos((LON - 82) / 5)  # Western Ghats
elevation += 300 * np.sin((LAT - 22) / 3) * np.sin((LON - 85) / 4)  # Eastern Ghats
elevation = gaussian_filter(elevation, sigma=2.5)
elevation = np.maximum(elevation, 0)

# Neon gradient: cyan -> magenta -> yellow -> electric green
cmap = LinearSegmentedColormap.from_list('neon', 
    ['#001a33', '#00ffff', '#ff00ff', '#ffff00', '#00ff88'], N=512)

# Mineral deposits
minerals = {
    'Coal': [(23.5, 86.0), (23.0, 82.0), (18.0, 79.0)],
    'Iron Ore': [(15.5, 75.5), (22.0, 84.0), (15.0, 76.0)],
    'Bauxite': [(23.0, 82.0), (17.0, 82.0)],
    'Copper': [(24.5, 72.5), (22.5, 78.5)],
    'Gold': [(12.5, 78.0), (25.0, 85.0)],
    'Manganese': [(21.0, 79.0), (15.5, 74.5)]
}

colors = {'Coal': '#ffffff', 'Iron Ore': '#ff0066', 'Bauxite': '#ff9900',
          'Copper': '#ffcc00', 'Gold': '#ffff00', 'Manganese': '#cc00ff'}

# Create figure
fig = plt.figure(figsize=(24, 18), facecolor='#0a1628')
ax = fig.add_subplot(111, projection='3d', facecolor='#0a1628')

# Plot terrain with glow
surf = ax.plot_surface(LON, LAT, elevation, cmap=cmap, alpha=0.95,
                       linewidth=0, antialiased=True, shade=True,
                       vmin=0, vmax=elevation.max(), rcount=400, ccount=400)

# Glass base platform
ax.plot_surface(LON, LAT, np.full_like(elevation, -200),
                color='#00ffff', alpha=0.08, linewidth=0)

# Transparent grid
ax.plot_wireframe(LON, LAT, elevation, color='#00ffff', alpha=0.12,
                  linewidth=0.25, rcount=25, ccount=25)

# Glowing mineral markers
for mineral, locs in minerals.items():
    for lat_m, lon_m in locs:
        lat_idx = np.argmin(np.abs(lat - lat_m))
        lon_idx = np.argmin(np.abs(lon - lon_m))
        elev = elevation[lat_idx, lon_idx]
        
        ax.scatter(lon_m, lat_m, elev + 300, c=colors[mineral], s=500,
                  marker='o', edgecolors='white', linewidths=3.5, alpha=1.0, label=mineral)
        ax.plot([lon_m, lon_m], [lat_m, lat_m], [-200, elev + 300],
               color=colors[mineral], linewidth=2.5, alpha=0.7)

# Styling
ax.set_xlabel('Longitude', fontsize=16, color='#00ffff', labelpad=20)
ax.set_ylabel('Latitude', fontsize=16, color='#00ffff', labelpad=20)
ax.set_zlabel('Elevation (m)', fontsize=16, color='#00ffff', labelpad=20)
ax.set_title('ADVANCED 3D TERRAIN MODEL\nMineral Distribution Visualization',
             fontsize=26, color='#00ffff', fontweight='bold', pad=40)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('#00ffff')
ax.yaxis.pane.set_edgecolor('#00ffff')
ax.zaxis.pane.set_edgecolor('#00ffff')
ax.xaxis.pane.set_alpha(0.08)
ax.yaxis.pane.set_alpha(0.08)
ax.zaxis.pane.set_alpha(0.08)

ax.grid(True, color='#00ffff', alpha=0.15, linewidth=0.4)
ax.tick_params(colors='#00ffff', labelsize=11)
ax.view_init(elev=35, azim=45)

# Legend
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='upper left',
          fontsize=13, framealpha=0.25, facecolor='#0a1628',
          edgecolor='#00ffff', labelcolor='#00ffff')

# Colorbar
cbar = plt.colorbar(surf, ax=ax, shrink=0.45, aspect=12, pad=0.08)
cbar.set_label('Elevation (m)', color='#00ffff', fontsize=13)
cbar.ax.tick_params(colors='#00ffff', labelsize=11)
cbar.outline.set_edgecolor('#00ffff')

plt.tight_layout()
plt.savefig('cinematic_terrain_ultra_hd.png', dpi=400, bbox_inches='tight',
            facecolor='#0a1628', edgecolor='none')
print("✨ Ultra HD cinematic terrain generated!")
print("📊 Saved as 'cinematic_terrain_ultra_hd.png'")
plt.show()
