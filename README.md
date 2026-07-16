# TPMS-Electrode-Generator
Python script for generating and analyzing Gyroid and Schwarz P TPMS architectures
Features
TPMS Topology Generation: Generates discrete 3D voxel matrices for both Gyroid and Schwarz P geometries using standard level-set nodal equations.
Cylindrical Masking: Applies a precise, user-defined cylindrical boundary mask (e.g., matching a physical $18\text{ mm}$ die or printing bed) to truncate the raw rectangular lattice blocks.
Iterative Porosity Optimization: Dynamically calculates volumetric porosity using voxel-counting algorithms and iteratively tunes the level-set parameter ($t$) to match target design porosities.
STL Export: Converts binary voxel arrays into high-resolution continuous triangular surface meshes via the Marching Cubes algorithm for downstream slicing and 3D printing.
Installation & Requirements
Ensure you have Python 3.x installed along with the following standard scientific computing libraries:
NumPy: For high-performance multidimensional array manipulations and coordinate grid mapping.

SciPy: For spatial and distance transformations.

scikit-image: Specifically skimage.measure.marching_cubes to convert voxel grids into mesh models.

Trimesh (Optional): For handling and inspecting exported STL meshes.
