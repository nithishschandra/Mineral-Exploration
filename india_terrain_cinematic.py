import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap, LightSource
from scipy.ndimage import gaussian_filter

# Ultra high resolution grid
lat_min, lat_max = 8.0, 35.0
lon_min, lon_max = 68.0, 97.0
lat = np.linspace(lat_min, lat_max, 600)
lon = np.linspace(lon_min, lon_max, 600)
LON, LAT = np.meshgrid(lon, lat)

# Ultra smooth realistic terrain resembling Indian subcontinent
# Himalayas in the north (high elevation)
himalayas = 8000 * np.exp(-((LAT - 32)**2 / 20 + (LON - 82)**2 / 150))
himalayas += 6000 * np.exp(-((LAT - 30)**2 / 25 + (LON - 88)**2 / 120))

# Western Ghats (western coast mountain range)
western_ghats = 2000 * np.exp(-((LAT - 15)**2 / 80 + (LON - 74)**2 / 8))

# Eastern Ghats (eastern coast hills)
eastern_ghats = 1200 * np.exp(-((LAT - 16)**2 / 100 + (LON - 82)**2 / 12))

# Deccan Plateau (central elevated region)
deccan_plateau = 800 + 400 * np.exp(-((LAT - 18)**2 / 150 + (LON - 78)**2 / 100))

# Indo-Gangetic Plains (low elevation in north-central)
plains = -300 * np.exp(-((LAT - 26)**2 / 40 + (LON - 82)**2 / 80))

# Combine all terrain features
elevation = himalayas + western_ghats + eastern_ghats + deccan_plateau + plains

# Add natural terrain variation
elevation += 200 * np.sin((LAT - 15) / 3) * np.cos((LON - 80) / 4)
elevation += 150 * np.sin((LAT - 20) / 2) * np.sin((LON - 85) / 3)

# Smooth the terrain
elevation = gaussian_filter(elevation, sigma=5)
elevation = np.maximum(elevation, 0)

# Vibrant neon gradient colormap with smooth transitions
colors_list = ['#0a0a2e', '#00d4ff', '#00ffaa', '#ffff00', '#ff00ff', '#ff0080']
n_bins = 512
cmap = LinearSegmentedColormap.from_list('neon', colors_list, N=n_bins)

# Advanced lighting setup
ls = LightSource(azdeg=315, altdeg=45)

# Mineral deposits with realistic locations across India
minerals = {
    'Coal': [(23.5, 86.0), (23.0, 82.0), (18.0, 79.0), (25.5, 85.5), (21.0, 81.5)],
    'Iron Ore': [(15.5, 75.5), (22.0, 84.0), (15.0, 76.0), (19.5, 85.5), (21.5, 81.0)],
    'Bauxite': [(23.0, 82.0), (17.0, 82.0), (20.5, 84.5), (11.0, 76.0)],
    'Copper': [(24.5, 72.5), (22.5, 78.5), (28.0, 76.0), (13.0, 78.5)],
    'Gold': [(12.5, 78.0), (25.0, 85.0), (13.5, 76.5), (15.0, 74.5)],
    'Manganese': [(21.0, 79.0), (15.5, 74.5), (19.0, 77.0), (22.5, 86.0)],
}

mineral_colors = {
    'Coal': '#ffffff',      # White
    'Iron Ore': '#ff0066',  # Hot Pink
    'Bauxite': '#ff9900',   # Orange
    'Copper': '#ffcc00',    # Gold-Orange
    'Gold': '#ffff00',      # Yellow
    'Manganese': '#cc00ff'  # Purple
}

# Create figure with dark gradient background
fig = plt.figure(figsize=(24, 20), facecolor='#050520')
ax = fig.add_subplot(111, projection='3d', facecolor='#050520')
ax.set_facecolor('#050520')

# Plot terrain with advanced lighting and neon colors
rgb = ls.shade(elevation, cmap=cmap, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(LON, LAT, elevation, facecolors=rgb, 
                       linewidth=0, antialiased=True, shade=False,
                       rcount=500, ccount=500, alpha=0.98)

# Glass-like base platform with glow
base_elevation = -300
ax.plot_surface(LON, LAT, np.full_like(elevation, base_elevation), 
                color='#00d4ff', alpha=0.15, linewidth=0, shade=True)

# Transparent grid overlay with glow effect
grid_alpha = 0.12
ax.plot_wireframe(LON, LAT, elevation, color='#00ffff', alpha=grid_alpha, 
                  linewidth=0.4, rcount=25, ccount=25)

# Volumetric grid walls
for i in [0, -1]:
    ax.plot_wireframe(LON[:, [i]*LON.shape[0]].T, LAT[:, [i]*LAT.shape[0]].T, 
                     elevation[:, [i]*elevation.shape[0]].T,
                     color='#00d4ff', alpha=0.08, linewidth=0.5, rcount=25)
for i in [0, -1]:
    ax.plot_wireframe(LON[[i]*LON.shape[1], :], LAT[[i]*LAT.shape[1], :], 
                     elevation[[i]*elevation.shape[1], :],
                     color='#00d4ff', alpha=0.08, linewidth=0.5, ccount=25)

# Plot floating holographic mineral markers with multi-layer glow
for mineral, locations in minerals.items():
    for lat_m, lon_m in locations:
        lat_idx = np.argmin(np.abs(lat - lat_m))
        lon_idx = np.argmin(np.abs(lon - lon_m))
        elev = elevation[lat_idx, lon_idx]
        
        # Floating height above terrain
        float_height = elev + 500
        
        # Core holographic marker (bright center)
        ax.scatter(lon_m, lat_m, float_height, c=mineral_colors[mineral], s=1000,
                  marker='o', edgecolors='white', linewidths=5, alpha=1.0, 
                  label=mineral, depthshade=False)
        
        # Inner glow layer
        ax.scatter(lon_m, lat_m, float_height, c=mineral_colors[mineral], s=2000,
                  marker='o', alpha=0.4, edgecolors='none', depthshade=False)
        
        # Middle glow layer
        ax.scatter(lon_m, lat_m, float_height, c=mineral_colors[mineral], s=3200,
                  marker='o', alpha=0.25, edgecolors='none', depthshade=False)
        
        # Outer glow halo
        ax.scatter(lon_m, lat_m, float_height, c=mineral_colors[mineral], s=4800,
                  marker='o', alpha=0.12, edgecolors='none', depthshade=False)
        
        # Holographic connection beam from terrain to marker
        ax.plot([lon_m, lon_m], [lat_m, lat_m], [elev, float_height],
               color=mineral_colors[mineral], linewidth=4, alpha=0.8, 
               linestyle='-', solid_capstyle='round')
        
        # Secondary glow beam
        ax.plot([lon_m, lon_m], [lat_m, lat_m], [elev, float_height],
               color=mineral_colors[mineral], linewidth=8, alpha=0.3, 
               linestyle='-', solid_capstyle='round')
        
        # Base glow on terrain surface
        ax.scatter(lon_m, lat_m, elev, c=mineral_colors[mineral], s=600,
                  marker='o', alpha=0.5, edgecolors='none', depthshade=False)
        
        # Vertical beam to base platform
        ax.plot([lon_m, lon_m], [lat_m, lat_m], [base_elevation, elev],
               color=mineral_colors[mineral], linewidth=2, alpha=0.4, 
               linestyle='--', dashes=(5, 5))

# Premium styling
ax.set_xlabel('Longitude', fontsize=16, color='#00d4ff', labelpad=20, fontweight='bold')
ax.set_ylabel('Latitude', fontsize=16, color='#00d4ff', labelpad=20, fontweight='bold')
ax.set_zlabel('Elevation (m)', fontsize=16, color='#00d4ff', labelpad=20, fontweight='bold')
ax.set_title('ADVANCED 3D TERRAIN MODEL\nMineral Distribution Visualization', 
             fontsize=28, color='#00ffff', fontweight='bold', pad=40, 
             family='sans-serif', style='normal')

# Transparent panes with subtle glow
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('#00d4ff')
ax.yaxis.pane.set_edgecolor('#00d4ff')
ax.zaxis.pane.set_edgecolor('#00d4ff')
ax.xaxis.pane.set_alpha(0.05)
ax.yaxis.pane.set_alpha(0.05)
ax.zaxis.pane.set_alpha(0.05)

# Grid styling with glow
ax.grid(True, color='#00d4ff', alpha=0.15, linewidth=0.6, linestyle='-')
ax.tick_params(colors='#00d4ff', labelsize=11)

# Cinematic isometric view
ax.view_init(elev=30, azim=50)
ax.dist = 9

# Premium legend
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
legend = ax.legend(by_label.values(), by_label.keys(), loc='upper left', 
                  fontsize=13, framealpha=0.25, facecolor='#050520', 
                  edgecolor='#00d4ff', labelcolor='#00ffff', 
                  shadow=False, borderpad=1.2)

# Premium colorbar
cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap, 
                    norm=plt.Normalize(vmin=0, vmax=elevation.max())),
                    ax=ax, shrink=0.5, aspect=12, pad=0.08)
cbar.set_label('Elevation (m)', color='#00d4ff', fontsize=14, fontweight='bold')
cbar.ax.tick_params(colors='#00d4ff', labelsize=11)
cbar.outline.set_edgecolor('#00d4ff')
cbar.outline.set_linewidth(1.5)

plt.tight_layout(pad=2)
plt.savefig('india_terrain_cinematic_4k.png', dpi=400, bbox_inches='tight', 
            facecolor='#050520', edgecolor='none', format='png')
print("Ultra-premium cinematic 3D terrain model generated!")
print("Ultra HD visualization saved as 'india_terrain_cinematic_4k.png'")
print(f"Plotted {sum(len(v) for v in minerals.values())} mineral deposits with glow effects")
print(f"Resolution: {len(lat)}x{len(lon)} | DPI: 400 | Quality: Premium")
plt.show()
