""" Pack 2000 water molecules in a box of size 50 x 50 x 50 [Å³] in
xyz-file. 
"""

from pack_water import PackWater

packer = PackWater(nummol=2000, lencube=50)
packer(filetype="xyz")
