# Pack water
This is a package for water packing, which relies on [the Packmol package](http://m3g.iqm.unicamp.br/packmol/home.shtml). This is ment to be used as input to LAMMPS for molecular dynamics simulations. The inputs are number of molecules, length of box of density of water and whether or not the packed water should support periodic boundary conditions. However, the package supports cubic shapes only. 

## Installation


## Prerequisites
- [Packmol](http://m3g.iqm.unicamp.br/packmol/home.shtml)

## Usage
The package is very straightforward to use:

``` python
from pack_water import PackWater

packer = PackWater(nummol=10000, density=0.998)
packer(outfile="water_10000mol_PBC.data", pbc=2.0)
```

### Number of molecules
The number of molecules is specified by ```PackWater``` the argument ```nummol```:
``` python
packer = PackWater(nummol=10000)
```
This argument is required

### Box length
Length of the box is specified by the ```PackWater``` argument ```lencube```:
``` python
packer = PackWater(nummol=10000, lencube=0.39)
```
This argument is optional

### Water density
The water density is specified by the PackWater argument ```density```:
``` python
packer = PackWater(nummol=10000, density=0.998)
```
this argument is optional. If both ```lencube``` and ```density``` are given, ```lencube``` is overwritten.

### Writing file
The outfile name and path can be specified by the ```__call__``` argument ```outfile```:
``` python
packer(outfile="out.data")
```
The default name is "water_config.data".

### Periodic boundary conditions
If the LAMMPS script is using periodic boundary conditions, we should ensure that the particles are separated by a certain distance across the boundaries. This can be done by the ```__call__``` argument ```pbc```, which takes in the separation length:
``` python
packer(pbc=2.0)
```
This argument is optional

### Separation tolerance
Initially, the molecules should be separated by a minimum distance, or a tolerance, to ensure that the potential energy is not too high. This minimum separation distance is specified by the ```__call__``` argument ```tolerance```:
``` python
packer(tolerance=2.0)
```
The default value is 2.0.
