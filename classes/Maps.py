import numpy as np
from math import pow, tanh
from datetime import datetime
from perlin_noise import PerlinNoise


class Map:
    """
    This shall be a very broad class with all tools necessary to create, tweak and modify maps.
    Any future implementation of 3D maps will be done in a different class that OR may not inherit this class.

    This class is heavily inspired by: https://www.redblobgames.com/maps/terrain-from-noise/
    """
    # TODO: add functions to man-made structures (bridges, mines, etc) and cities, towns and castles
    def __init__(self, width: int, height: int, amplitudes: list, zoomed: bool = False, elevation: float = 1):
        """
        To simplify things, the map will me created blank. The user needs to refer to static methods to add and
        tweak features.
        :param width:
        :param height:
        :param amplitudes: related to the octaves
        """
        self.width = int(width)
        self.height = int(height)
        amplitudes.sort(key=lambda x: abs(x))
        noise = []

        for amplitude in amplitudes:
            noise.append(PerlinNoise(octaves=amplitude, seed=int(datetime.timestamp(datetime.now()))))

        pic = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                noise_val = 0
                for octave, amplitude in zip(noise, amplitudes):
                    '''
                    Multiplying by 1/amplitude yields a zoomed in map, while amplitude/max(amplitudes) yields a very
                    sparse ocean-filled map. It may be interesting to let the user play with this.
                    '''
                    if zoomed:
                        weight = (1 / amplitude)
                    else:
                        weight = amplitude/max(amplitudes)

                    noise_val += weight * octave([i/self.width, j/self.height])

                row.append(noise_val)
            pic.append(row)
        self.map = np.array(pic)/sum(amplitudes)
        self.normalize_map()

        if elevation != 1:
            self.transform_elevation(elevation)

    def __repr__(self):
        """
        It is not recommended to look at your map this way, thus, only metadata is returned.
        :return: related metadata
        """
        return f'''
        width: {self.width}\n
        height: {self.height}
        '''

    def normalize_map(self, min_value: int = 0, max_value: int = 1):
        """
        https://stats.stackexchange.com/questions/178626/how-to-normalize-data-between-1-and-1
        :param min_value:
        :param max_value:
        :return:
        """
        abs_max, abs_min = 0, 0
        for i in range(self.height):
            local_max = self.map[i:].max()
            local_min = self.map[i:].min()

            if local_max > abs_max:
                abs_max = local_max

            if local_min < abs_min:
                abs_min = local_min

        # normalize to [0; 1] interval
        self.map = (self.map - abs_min)/(abs_max - abs_min)

        if min_value != 0 or max_value != 1:
            self.map = (max_value - min_value)*self.map + min_value

    def transform_elevation(self, elevation):
        for i in range(self.height):
            for j in range(self.width):
                self.map[i][j] = pow(self.map[i][j], elevation)
        self.normalize_map()

    def transform_dungeon(self):
        """
        transform the elevation between [-10, 10] and apply a hyperbolic tangent activation, to create borders
        """
        # TODO: trim the wall weights and raise any 'outlier' ground dents
        self.normalize_map(min_value=-10, max_value=10)
        for i in range(self.height):
            for j in range(self.width):
                self.map[i][j] = tanh(self.map[i][j])

        self.map[self.map < 0] = 0
        self.map[self.map > 0] = 1
        self.normalize_map()

    def export_map(self, filename: str, view3d: bool = False, colormap: str = 'terrain_map'):
        from matplotlib import pyplot as plt
        import matplotlib.colors as colors

        fig = plt.figure()

        '''
        TODO: take the color from a self.sea_level variable. The current function is good to have a look at what under-
        water looks like and at which level they are. Nevertheless, it is interesting to at convert anything below a
        given level to water, transforming from self.sea_level to a different map, so we wont loose info.
        
        Is it interesting that all point surrounded by land becomes water?
        Yes, there will be some lakes and puddles, but we should expect that some places remain dry.
        '''
        if colormap == 'terrain_map':
            # TODO: not necessarily the highest point will have snow, nor the lowest will have water
            colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 64))  # the step tells me how much of it is in the map
            colors_land = plt.cm.terrain(np.linspace(0.25, 1, 256))  # the min and max only tells the color gradient
            all_colors = np.vstack((colors_undersea, colors_land))
            custom_map = colors.LinearSegmentedColormap.from_list('terrain_map', all_colors)
        elif colormap == 'dungeon':
            custom_map = 'gray'
        else:
            custom_map = 'terrain'

        if view3d is False:
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlim(0, self.width)
            ax.set_ylim(0, self.height)

            major_ticks_x = np.arange(0, self.width, 20)
            minor_ticks_x = np.arange(0, self.width, 10)
            major_ticks_y = np.arange(0, self.height, 20)
            minor_ticks_y = np.arange(0, self.height, 10)

            ax.set_xticks(major_ticks_x)
            ax.set_xticks(minor_ticks_x, minor=True)
            ax.set_yticks(major_ticks_y)
            ax.set_yticks(minor_ticks_y, minor=True)
            ax.grid(which='both')

            surface = ax.imshow(self.map, cmap=custom_map)
            fig.colorbar(surface)
            # ax.invert_yaxis()
            plt.gca().invert_yaxis()  # y axis is plotted inverted

        else:
            from mpl_toolkits.mplot3d import axes3d
            ax = fig.add_subplot(111, projection='3d')
            X, Y = np.arange(0, self.height, 1), np.arange(0, self.width, 1)
            X, Y = np.meshgrid(X, Y)
            surface = ax.plot_surface(X, Y, self.map, cmap=custom_map)
            fig.colorbar(surface)

        plt.savefig(filename, dpi=600)
