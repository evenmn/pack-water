import numpy as np

class Geometry:
    def __init__(self, number=None, density=None, side='in'): 
        
        # Convert from density to number of molecules
        if number is None and density is None:
            raise Warning("Warning! Neither number of molecules nor density is given, continue with density 1 g/cm^3")
            density = 1.0
            number = self.den2lnum(density)
        elif number is not None and density is not None:
            raise Warning("Warning! Both number of molecules and density are given, ignoring the number of molecules.")
            number = self.den2lnum(density)
        elif density is not None:
            number = self.den2num(density)
        self.number = number   # Number of molecules
        
        # Side in / out
        if side == 'in':
            self.side = 'inside'
        elif side == 'out':
            self.side = 'outside'
        
        # Store all "hidden" files in data_files
        import os
        this_dir, this_filename = os.path.split(__file__)
        self.structure_data = this_dir + "/data_files/water.xyz"
            
            
    def __call__(self):
        """ Make structure.
        """
        structure = "structure {}\n".format(self.structure_data)
        structure += "  number {}\n".format(self.number)
        structure += "  {} {} ".format(self.side, self.label)
        for param in self.params:
            structure += "{} ".format(param)
        structure += "\nend structure\n"
        return structure
        
    def den2num(self, density):
        """ Returns the number of molecules, given a mass density.
        """
        volume = self.compute_volume() * 1e-24      # Volume, Å³
        mass_H2O = 18.0152          # Mass of H2O molecule, g/mol
        NA = 6.02214075e23          # Avogadro's number, mol^-1
        return int(NA * volume * density / mass_H2O)
        
    
class CubeGeometry(Geometry):
    """ Make a cube.
    
    Parameters
    ----------
    xlo : float
        x-coordinate of lower left corner
    ylo : float
        y-coordinate of lower left corner
    zlo : float
        z-coordinate of lower left corner
    l : float
        length of cube sides
    """
    def __init__(self, xlo, ylo, zlo, l, **kwargs):
        super().__init__(**kwargs)
        self.length = l
        self.params = [xlo, ylo, zlo, l]
        self.label = 'cube'
        self.ll_corner = np.array([xlo, ylo, zlo])
        self.ur_corner = np.array([xlo + l, ylo + l, zlo + l])
        
    def compute_volume(self):
        """ Returning volume of geometry
        """
        return length ** 3

        
class BoxGeometry(Geometry):
    """ Make a box.
    
    Parameters
    ----------
    xlo : float
        x-coordinate of lower left corner
    ylo : float
        y-coordinate of lower left corner
    zlo : float
        z-coordinate of lower left corner
    xhi : float
        x-coordinate of upper right corner
    yhi : float
        y-coordinate of upper right corner
    zhi : float
        z-coordinate of upper right corner
    """
    def __init__(self, xlo, ylo, zlo, xhi, yhi, zhi, **kwargs):
        self.params = [xlo, ylo, zlo, xhi, yhi, zhi]
        super().__init__(**kwargs)
        self.label = 'box'
        self.ll_corner = np.array([xlo, ylo, zlo])
        self.ur_corner = np.array([xhi, yhi, zhi])
        
    def compute_volume(self):
        """ Returning volume of geometry
        """
        volume = 1
        for d in range(3):
            volume *= self.params[d+3] - self.params[d]
        return volume
        
class SphereGeometry(Geometry):
    """ Make a sphere defined by the equation
    
    (x-x0)^2  +  (y-y0)^2  +  (z-z0)^2  =  r^2
    
    Parameters
    ----------
    x : float
        x-coordinate of center
    y : float
        y-coordinate of center
    z : float
        z-coordinate of center
    r : float
        radius of sphere
    """
    def __init__(self, x, y, z, r, **kwargs):
        super().__init__(**kwargs)
        self.radius = r
        self.params = [x, y, z, r]
        self.label = 'sphere'
        self.ll_corner = np.array([x - r, y - r, z - r])
        self.ur_corner = np.array([x + r, y + r, z + r])
        
    def compute_volume(self):
        """ Returning volume of geometry
        """
        from math import pi
        return 4 * pi * self.radius ** 3 / 3
    
class EllipsoidGeometry(Geometry):
    """ Make an ellipsoid defined by the equation
    
    (x-x0)^2     (y-y0)^2     (z-z0)^2
    --------  +  --------  +  --------  =  r^2
       a^2          b^2          c^2
    
    Parameters
    ----------
    x : float
        x-coordinate of center
    y : float
        y-coordinate of center
    z : float
        z-coordinate of center
    a : float
        x semi axis
    b : float
        y semi axis
    c : float
        z semi axis
    r : float
        radius
    """
    def __init__(self, x, y, z, a, b, c, r, **kwargs):
        super().__init__(**kwargs)
        self.a, self.b, self.c = a, b, c
        self.params = [x, y, z, a, b, c, r]
        self.label = 'ellipsoid'
        self.ll_corner = np.array([x - a, y - b, z - b])
        self.ur_corner = np.array([x + a, y + b, z + b])
        
    def compute_volume(self):
        """ Returning volume of geometry
        """
        from math import pi
        return 4 * pi * self.a * self.b * self.c / 3
        
class CylinderGeometry(Geometry):
    """ Make an ellipsoid defined by the equation
    
    p = (x, y, z) + t(a, b, c)
    
    Parameters
    ----------
    x : float
        x-coordinate of center
    y : float
        y-coordinate of center
    z : float
        z-coordinate of center
    a : float
        slope of cylinder in x-direction
    b : float
        slope of cylinder in y-direction
    c : float
        slope of cylinder in z-direction
    r : float
        radius
    l : float
        length
    """
    def __init__(self, x, y, z, a, b, c, r, l, **kwargs):
        super().__init__(**kwargs)
        self.radius , self.length = r, l
        self.params = [x, y, z, a, b, c, r, l]
        self.label = 'cylinder'
        
        # TODO: Find ll_corner and ur_corner of cylinder
        #self.ll_corner = np.array([x - r, y - r, z - r])
        #self.ur_corner = np.array([x + r, y + r, z + r])
        
    def compute_volume(self):
        """ Returning volume of geometry
        """
        from math import pi
        return 2 * pi * self.radius * self.length
    
class PlaneGeometry(Geometry):
    """ Make an plane defined by the equation
    
    ax  +  by  +  cz  =  d
    
    Parameters
    ----------
    a : float
        x-slope
    b : float
        y-slope
    c : float
        z-slope
    d : float
        constant term
        
    NB: argument 'side' has to be given, side E [over, below]
    """
    def __init__(self, a, b, c, d, **kwargs):
        super().__init__(**kwargs)
        self.params = [a, b, c, d]
        self.label = 'plane'
