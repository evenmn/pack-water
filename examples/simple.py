""" Pack water molecules with density 0.998 in a box of size 357 x 143 x 143 [Å³]. 
"""

from pack_water import PackWater
from pack_water.geometry import BoxGeometry

packer = PackWater()
packer.append(BoxGeometry(0, 0, 0, 30, 40, 50, density=0.998))
packer(outfile="water.data")
