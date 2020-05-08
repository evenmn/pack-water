""" Pack 10000 water molecules and periodic boundary condition
"""

from pack_water import PackWater
from pack_water.geometry import CubeGeometry
    
packer = PackWater()
packer.append(CubeGeometry(0, 0, 0, 40, number=10000))
packer(pbc=2.0, outfile="water_10000mol_PBC.out")
