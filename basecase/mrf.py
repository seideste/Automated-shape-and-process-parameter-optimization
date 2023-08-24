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

d = float(sys.argv[1])
d_m = 1.1*d/1000
name='./mrf.stl'
cube = ConfiguredOnshapeElement(url, client=client)
cube.configuration = 'h='+str(float(d_m))+'+meter;d='+str(float(d_m))+'+meter'

stl = client.part_studios_api.export_stl1(cube.did, cube.wvm, cube.wvmid, cube.eid, configuration = cube.configuration, scale = 1.0, units = 'meter', _preload_content=False)
with open(name, 'wb') as out:
    out.write(stl.data)