import warnings
warnings.simplefilter("ignore", UserWarning)
from onshape_client.client import Client
from onshape_client.onshape_url import OnshapeElement, ConfiguredOnshapeElement
import sys
import numpy as np

base = 'https://cad.onshape.com'
access = ''
secret = ''
client = Client(configuration={"base_url": base,
                               "access_key": access,
                               "secret_key": secret})
                               
# Turn the URL into an "OnshapeElement" -> Dokument url
url = ""

d = float(sys.argv[1]) # stirrer diameter
a1 = float(sys.argv[2]) # pitch angle
a2 = float(sys.argv[3]) # blade size angle

a1_rad = a1*np.pi/180
a2_rad = a2*np.pi/180
d_m = d/1000

name='./stirrer.stl'
cube = ConfiguredOnshapeElement(url, client=client)
cube.configuration = 'd='+str(d_m)+'+meter;a='+str(float(a1_rad))+'+radian;a2='+str(float(a2_rad))+'+radian' 

stl = client.part_studios_api.export_stl1(cube.did, cube.wvm, cube.wvmid, cube.eid, configuration = cube.configuration, scale = 1.0, units = 'meter', _preload_content=False)
with open(name, 'wb') as out:
    out.write(stl.data)