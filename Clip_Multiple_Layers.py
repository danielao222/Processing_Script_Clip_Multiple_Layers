##selection_layer=vector
##output_folder=folder


import processing, os, subprocess
from qgis.utils import *
from qgis.core import *

# create a class to return custom error
class Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
            



legend = iface.legendInterface()
layers = iface.legendInterface().layers()




#search existence of output folder, if not create it
directory = output_folder + "/output/vectors"
if not os.path.exists(directory):
    os.makedirs(directory)

directory = output_folder + "/output/rasters"
if not os.path.exists(directory):
    os.makedirs(directory)

trouvee = 0
for layer in layers :
    if layer.type() == QgsMapLayer.VectorLayer and layer.source() == selection_layer :
        selection = layer
        trouvee = 1

if trouvee == 0 :
    raise Error ("Layer selection not found ! or the layer isn't a vector layer")


#clip part
for layer in layers  :
    #clip vector layer (if displayed)
    if layer.type() == QgsMapLayer.VectorLayer and layer != selection and legend.isLayerVisible(layer) == True :
        output = output_folder + "/output/vectors/clip_" + layer.name() + ".shp"
        processing.runalg("qgis:clip",layer,selection,output)
                
    #clip raster layer (if displayed)
    if layer.type() == QgsMapLayer.RasterLayer and legend.isLayerVisible(layer) == True :
        output = output_folder + "/output/rasters/clip-" + layer.name() + ".tif"
        command_cut = "gdalwarp -q -cutline %s -crop_to_cutline -of GTiff %s %s " % ( selection.source(), layer.source(), output )
        subprocess.call(command_cut)
