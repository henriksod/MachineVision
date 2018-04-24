import numpy as np

"""
This is a class used for segmenting a 3d model imported by PyWavefront library.
"""
class Segmenting:
    
    segments = []
    colorDict = {}
    
    def __init__(self, numSegments, array):
        """
        Contructor of class Segmenting.
        
        The segments are stored in the array segments.

        Keyword arguments:
        numSegments -- the desired number of segments to divide the 3d model in
        array -- the PyWavefront array, structure [TTNNNVVV...]
        """
        
        array = np.copy(array)
        array = array.reshape(len(array)/8, 8)
        
        array = array[array[:,7].argsort()]
        self.segments = np.split(array, numSegments)
        
    # texture[0,0] = [83 44 37] = [ R G B ], texture :: ndarray
    def pairWithTexture(self, texture):
        """
        Pairs colors from a texture with each vertex from the segments.
        
        Results are stored in the dictionary colorDict.

        Keyword arguments:
        texture -- is an image ndarray with shape (width, height, 3)
        """
        
        texShape = texture.shape
        width = texShape[0]
        height = texShape[1]
        for i in range(0, len(self.segments)):
            for j in range(0, len(self.segments[i])):
                point = self.segments[i][j]
                color = texture[int(width*point[0])-1, int(height*point[1])-1]
                self.colorDict[(i, j)] = color
    
    def isBlob(self, color): # color = [ R G B ], returns bool
        """
        Determines if a color matches a blob or not.

        Keyword arguments:
        color -- color to determine if it is a blob or not ([R G B])
        """
        
        # THIS IS THE HARD PART MAN
        if color[1] < 100: # I observed that the green component of the image is good for distinguishing blob from background
            return True
        return False