""" Pack 10000 water molecules with density 0.998 g/cm³ and 
periodic boundary condition
"""

from pack_water import PackWater

packer = PackWater(nummol=10000, density=0.998)
packer(outfile="water_10000mol_PBC.data")
