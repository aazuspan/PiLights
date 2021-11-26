import opensimplex

from backend import utils


class Noise:
    def __init__(self, shift, width=1, val_range=(-1, 1)):
        """Initialize a noise object.

        Parameters
        ----------
        shift : float
            The shift to apply to the noise offset every update. Larger values will
            create faster changes.
        width : int, default 1
            The width modifier used to scale noise. Larger values will create less
            spatial variability.
        val_range : Tuple[int, int]
            The minimum and maximum output values. Noise will be rescaled to this
            range.
        """
        self.shift = shift
        self.perlin = opensimplex.OpenSimplex()
        self.width = width
        self.offset = 0
        self.val_range = val_range
    
    def update(self):
        """Apply the shift to update the noise value"""
        self.offset += self.shift
    
    def value(self, x):
        """Retrieve the noise value at location x"""
        noise = self.perlin.noise2d(x/self.width, self.offset)
        return utils.remap(noise, -1, 1, self.val_range[0], self.val_range[1])
    