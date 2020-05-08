class PackWater:
    def __init__(self, packmol_input="/data_files/input.inp",
                       packmol_data ="/data_files/water_packmol.data"):
        self.geometries = []
        
        # Store all "hidden" files in data_files
        import os
        this_dir, this_filename = os.path.split(__file__)
        self.packmol_input  = this_dir + packmol_input
        self.packmol_data   = this_dir + packmol_data
        
    def append(self, geometry):
        """ Append new water geometry
        """
        self.geometries.append(geometry)
        
    def generate_input(self, tolerance):
        """ Generate Packmol input script.
        """
        with open(self.packmol_input, 'w') as f:
            f.write("tolerance {}\n".format(tolerance))
            f.write("filetype xyz\n")
            f.write("output {}\n".format(self.packmol_data))
            f.write("nloop0 1000\n")
            for geometry in self.geometries:
                f.write("\n")
                f.write(geometry() + "\n")
                
    def run_packmol(self):
        """ Run packmol.
        """
        from os import system
        call_string = "packmol < {}".format(self.packmol_input)
        system(call_string)
        
    def to_lammps(self, outfile, pbc):
        """ Convert from xyz format to Lammps readable file.
        
        Arguments:
        ----------
        out : str
            output file after converting.
        """
        import numpy as np
        
        # Find corners of system and total number of molecules
        ll_corner = np.full(3, + np.inf)
        ur_corner = np.full(3, - np.inf)
        number = 0
        for geometry in self.geometries:
            ll_corner = np.where(geometry.ll_corner < ll_corner, geometry.ll_corner, ll_corner)
            ur_corner = np.where(geometry.ur_corner > ur_corner, geometry.ur_corner, ur_corner)
            number += geometry.number
            
        if pbc is not None:
            ur_corner += pbc
        
        with open(outfile, 'w') as out:
            # Write header
            out.write(outfile + " (Built with Packmol)\n\n")
            out.write("{} atoms\n".format(3 * number))
            out.write("2 atom types\n")
            out.write("{}          {} xlo xhi\n".format(ll_corner[0], ur_corner[0]))
            out.write("{}          {} ylo yhi\n".format(ll_corner[1], ur_corner[1]))
            out.write("{}          {} zlo zhi\n\n".format(ll_corner[2], ur_corner[2]))
            out.write("Atoms\n\n")
            # Write positions
            with open(self.packmol_data, 'r') as infile:
                for i, line in enumerate(infile):
                    if i > 1:
                        line = str(i-1) + line
                        line = line.replace("H", "1")
                        line = line.replace("O", "2")
                        out.write(line)
        
    def __call__(self, outfile="water_config.data", pbc=None, tolerance=2.0):
        # Generate Packmol input script
        self.generate_input(tolerance)
        
        # Run Packmol input script
        self.run_packmol()
        
        # Convert to LAMMPS format
        self.to_lammps(outfile, pbc)
                    
if __name__ == "__main__":
    from geometry import SphereGeometry, BoxGeometry
    
    packer = PackWater()
    packer.append(BoxGeometry(0, 0, 0, 40, 40, 40, density=0.998,  side='in'))
    packer.append(SphereGeometry(70, 20, 20, 20, number=2000,  side='in'))
    packer(pbc=3.0, outfile="data.out")
