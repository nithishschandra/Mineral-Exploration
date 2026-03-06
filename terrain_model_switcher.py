import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter

# ========== CHANGE THIS TO SWITCH MODELS ==========
MODEL_TYPE = "cinematic"  # Options: "cinematic", "realistic", "minimal", "dark"
# ==================================================

lat_min, lat_max = 8.0, 35.0
lon_min, lon_max = 68.0, 97.0
resolution = 400 if MODEL_TYPE == "cinematic" else 300
lat = np.linspace(lat_min, lat_max, resolution)
lon = np.linspace(lon_min, lon_max, resolution)
LON, LAT = np.meshgrid(lon, lat)

# Terrain generation
elevation = 3000 * np.exp(-((LAT - 30)**2 / 100 + (LON - 80)**2 / 200))
elevation += 800 * np.sin((LAT - 15) / 3) * np.cos((LON - 80) / 4)
elevation += 400 * np.sin((LAT - 20) / 2) * np.sin((LON - 85) / 3)
elevation = gaussian_filter(elevation, sigma=3)
elevation = np.maximum(elevation, 0)

# Minerals
minerals = {
    'Coal': [(23.5, 86.0), (23.0, 82.0), (18.0, 79.0)],
    'Iron Ore': [(15.5, 75.5), (22.0, 84.0), (15.0, 76.0)],
    'Bauxite': [(23.0, 82.0), (17.0, 82.0)],
    'Copper': [(24.5, 72.5), (22.5, 78.5)],
    'Gold': [(12.5, 78.0), (25.0, 85.0)],
    'Manganese': [(21.0, 79.0), (15.5, 74.5)],
}

# Model configurations
if MODEL_TYPE == "cinematic":
    bg_color = '#0a1628'
    colors_list = ['#001a33', '#00ffff', '#ff00ff', '#ffff00', '#00ff88']
    cmap = LinearSegmentedColormap.from_list('neon', colors_list, N=256)
    mineral_colors = {'Coal': '#ffffff', 'Iron Ore': '#ff0066', 'Bauxite': '#ff9900', 
                      'Copper': '#ffcc00', 'Gold': '#ffff00', 'Manganese': '#cc00ff'}
    grid_color = '#00ffff'
    text_color = '#00ffff'
    alpha_terrain = 0.95
    show_base = True
    
elif MODEL_TYPE == "realistic":
    bg_color = 'white'
    cmap = cm.terrain
    mineral_colors = {'Coal': 'black', 'Iron Ore': 'red', 'Bauxite': 'orange', 
                      'Copper': 'brown', 'Gold': 'gold', 'Manganese': 'purple'}
    grid_color = 'gray'
    text_color = 'black'
    alpha_terrain = 0.8
    show_base = False
    
elif MODEL_TYPE == "minimal":
    bg_color = '#f5f5f5'
    cmap = cm.viridis
    mineral_colors = {'Coal': '#e74c3c', 'Iron Ore': '#3498db', 'Bauxite': '#f39c12', 
                      'Copper': '#9b59b6', 'Gold': '#f1c40f', 'Manganese': '#1abc9c'}
    grid_color = '#95a5a6'
    text_color = '#2c3e50'
    alpha_terrain = 0.9
    show_base = False
    
elif MODEL_TYPE == "dark":
    bg_color = '#1a1a1a'
    colors_list = ['#1a1a1a', '#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    cmap = LinearSegmentedColormap.from_list('dark', colors_list, N=256)
    mineral_colors = {'Coal': '#ecf0f1', 'Iron Ore': '#e74c3c', 'Bauxite': '#f39c12', 
                      'Copper': '#d35400', 'Gold': '#f1c40f', 'Manganese': '#9b59b6'}
    grid_color = '#34495e'
    text_color = '#ecf0f1'
    alpha_terrain = 0.9
    show_base = True

# Create figure
fig = plt.figure(figsize=(20, 16), facecolor=bg_color)
ax = fig.add_subplot(111, projection='3d', facecolor=bg_color)

# Plot terrain
surf = ax.plot_surface(LON, LAT, elevation, cmap=cmap, alpha=alpha_terrain,
                       linewidth=0, antialiased=True, shade=True)

# Base platform
if show_base:
    base_elevation = -200
    ax.plot_surface(LON, LAT, np.full_like(elevation, base_elevation), 
                    color=grid_color, alpha=0.1, linewidth=0)

# Plot minerals
for mineral, locations in minerals.items():
    for lat_m, lon_m in locations:
        lat_idx = np.argmin(np.abs(lat - lat_m))
        lon_idx = np.argmin(np.abs(lon - lon_m))
        elev = elevation[lat_idx, lon_idx]
        
        ax.scatter(lon_m, lat_m, elev + 300, c=mineral_colors[mineral], s=400,
                  marker='o', edgecolors='white', linewidths=3, alpha=1.0, label=mineral)
        
        if MODEL_TYPE in ["cinematic", "dark"]:
            ax.plot([lon_m, lon_m], [lat_m, lat_m], [-200 if show_base else 0, elev + 300],
                   color=mineral_colors[mineral], linewidth=2, alpha=0.6)

# Styling
ax.set_xlabel('Longitude', fontsize=14, color=text_color, labelpad=15)
ax.set_ylabel('Latitude', fontsize=14, color=text_color, labelpad=15)
ax.set_zlabel('Elevation (m)', fontsize=14, color=text_color, labelpad=15)
ax.set_title(f'India 3D Terrain - {MODEL_TYPE.upper()} Model\nMineral Distribution', 
             fontsize=22, color=text_color, fontweight='bold', pad=30)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.grid(True, color=grid_color, alpha=0.2)
ax.tick_params(colors=text_color, labelsize=10)
ax.view_init(elev=35, azim=45)

# Legend
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='upper left', 
          fontsize=12, framealpha=0.3, facecolor=bg_color, 
          edgecolor=grid_color, labelcolor=text_color)

plt.tight_layout()
plt.savefig(f'india_terrain_{MODEL_TYPE}.png', dpi=300, bbox_inches='tight', 
            facecolor=bg_color)
print(f"✨ {MODEL_TYPE.upper()} model generated!")
print(f"📊 Saved as 'india_terrain_{MODEL_TYPE}.png'")
plt.show()
