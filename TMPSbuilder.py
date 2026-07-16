import numpy as np
import trimesh
from scipy import ndimage
import time

# -------- USER PARAMETERS --------
structure_type = "gyroid"  # Options: "gyroid" or "simple_cubic"
diameter_mm = 18.0
height_mm = 1.0
pitch = 0.025            # Resolution (25 µm)
feature_mm = 2.5        # Unit cell size
t_param = 0.150          # Adjust this to control wall thickness/porosity
# ---------------------------------

start = time.time()

# Compute grid dimensions
nx = int(np.ceil(diameter_mm / pitch))
ny = nx
nz = int(np.ceil(height_mm / pitch))

x = (np.arange(nx) - (nx-1)/2.0) * pitch
y = (np.arange(ny) - (ny-1)/2.0) * pitch
z = (np.arange(nz) - (nz-1)/2.0) * pitch
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Wave number (k)
k = 2.0 * np.pi / feature_mm

# Choose Equation
if structure_type == "gyroid":
    F = np.sin(k*X)*np.cos(k*Y) + np.sin(k*Y)*np.cos(k*Z) + np.sin(k*Z)*np.cos(k*X)
else:
    # Simple Cubic (Schwarz P)
    F = np.cos(k*X) + np.cos(k*Y) + np.cos(k*Z)

# Apply Cylinder Mask
radius = diameter_mm / 2.0
cylinder_mask = (X**2 + Y**2) <= radius**2

# Create Solid: |F| < t creates a "sheet" (wall) of thickness
solid = (np.abs(F) < t_param) & cylinder_mask

# --- Analysis ---
porosity = 1.0 - solid.sum() / solid.size
dist_solid = ndimage.distance_transform_edt(solid)
# We multiply by 2 because the distance transform gives the distance to the nearest '0' (half-thickness)
est_wall_um = 2.0 * np.median(dist_solid[solid]) * pitch * 1000.0

print(f"--- {structure_type.upper()} ANALYSIS ---")
print(f"Porosity: {porosity:.1%}")
print(f"Estimated Wall Thickness: {est_wall_um:.1f} µm")

# Create and Export Mesh
vox = trimesh.voxel.VoxelGrid(solid)
mesh = vox.marching_cubes
mesh.apply_scale(pitch)

outfile = f"{structure_type}_D{int(diameter_mm)}_t{t_param:.3f}.stl"
mesh.export(outfile)

print(f"✅ Exported '{outfile}' in {time.time() - start:.1f} s")