import xmltodict
import pprint
import json
my_xml="""

<annotation>

<folder>Pictures</folder>

<filename>packmegood3.jpg</filename>

<path>C:/Users/91908/Pictures/packmegood3.jpg</path>


<source>

<database>Unknown</database>

</source>


<size>

<width>453</width>

<height>1280</height>

<depth>3</depth>

</size>

<segmented>0</segmented>


<object>

<name>11</name>

<pose>Unspecified</pose>

<truncated>0</truncated>

<difficult>0</difficult>

<crew>1</crew>

<fake>0</fake>

<occluded>0</occluded>

<reflection>0</reflection>

<behindglass>0</behindglass>


<bndbox>

<xmin>66</xmin>

<ymin>325</ymin>

<xmax>258</xmax>

<ymax>506</ymax>

</bndbox>

</object>

</annotation>"""
pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(json.dumps(xmltodict.parse(my_xml)))
with open('jsondata.json', 'w') as out_file:
    json.dump(xmltodict.parse(my_xml), out_file)