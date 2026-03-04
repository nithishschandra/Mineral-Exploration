import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Create terrain grid
x = np.linspace(76.40, 76.50, 50)
y = np.linspace(14.04, 14.08, 50)
X, Y = np.meshgrid(x, y)
Z = 500 + 50 * np.sin(5*X) * np.cos(5*Y)  # Terrain elevation

# Mineral spots
np.random.seed(42)
n_minerals = 80
mx = np.random.uniform(76.40, 76.50, n_minerals)
my = np.random.uniform(14.04, 14.08, n_minerals)
mz = 500 + 50 * np.sin(5*mx) * np.cos(5*my) + 20

# Create figure
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111, projection='3d')

# Plot terrain with light blue grid
ax.plot_surface(X, Y, Z, alpha=0.3, color='lightblue', edgecolor='cyan', linewidth=0.5)

# Plot mineral spots as red spheres
ax.scatter(mx, my, mz, c='red', s=200, marker='o', edgecolors='darkred', linewidth=2, alpha=0.9)

ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.set_zlabel('Elevation (m)', fontsize=12)
ax.set_title('3D Terrain Map - Mineral Deposits', fontsize=16, fontweight='bold')
ax.view_init(elev=30, azim=45)

plt.savefig('mineral_terrain_3d.png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"Saved realistic 3D terrain with {n_minerals} mineral spots")
plt.show()
