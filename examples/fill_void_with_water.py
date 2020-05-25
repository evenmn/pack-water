import numpy as np
from molecular_builder import fetch_prepared_system, carve_geometry
from molecular_builder.geometry import SphereGeometry
from pack_water import PackWater
from pack_water.geometry import BoxGeometry, Fixed
import ase

# Fetch amorphous silica
silica = fetch_prepared_system("amorphous_silica_1")

num_spheres = 20

for sphere in range(num_spheres):
    i, j, k, l = np.random.uniform(size=4)
    x, y, z, r = i*357, j*143, k*143, l*30
    geometry = SphereGeometry([x, y, z], r, periodic_boundary_condition=(True, True, True))
    tmp_carved = carve_geometry(silica, geometry, side="in")
    print(f"tmp carved: {tmp_carved}")

# Write amorphous silica with voids to pdb-filetype
silica.write("amorphous_void.pdb", format="proteindatabank")

# Fill voids with water
packer = PackWater(filetype="pdb")
packer.append(Fixed("amorphous_void.pdb", 0, 0, 0, number=1))
packer.append(BoxGeometry(0, 0, 0, 358, 143.2, 143.2, density=0.998))
packer(outfile="water.data")


