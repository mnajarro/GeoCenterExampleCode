import zipfile
import re
import os
import arcpy
from arcpy import env

#This scripts unzips all Seamline_SHAPEE.zip found in downloaded image zip files
#and extracts all of the foot print shapefiles. It then grabs all shapefiles in
#the destination folder and adds an area field to each, calculates the area and
#sums the total area in square kilometers based off the Cylindrical_aqual area
#projection. The final shapefiles are set in the same folder the zips files are
#found in and generates a text file names AreaSum.
#dest = 'F:\ImageDownloads_from June2015\Zambia\Forestry\ShapefileAOIs'


if len(sys.argv) < 2:
  print "\nUsage: ",sys.argv[0]," file1.zip, [file2, file3...]"
  print 'Press <ENTER> to finish...'
  raw_input()
  sys.exit()
   
try:
  p = re.compile('\S*_SEAMLINES_SHAPE.zip')
  dest = os.path.dirname(sys.argv[1])
  for f in sys.argv[1:]:
    print f
    if zipfile.is_zipfile(f):
      zf = zipfile.ZipFile(f,'r')
      for x in zf.namelist():
        if p.match(x):
		print "Extracting ",zf.extract(x,dest)
		newname = dest+'\\'+x
		zf2 = zipfile.ZipFile(newname,'r')
		zf2.extractall(dest)
		zf2.close()
		os.remove(newname)
      zf.close()
except Exception as ex:
  print ex 
  print '\nPress <ENTER> to finish...'
  raw_input()
  sys.exit()
  
print '\nPress <ENTER> to finish...'
raw_input()


# Set the workspace for ListFeatureClasses
#workspace = arcpy.GetParameterAsText(0)
#workspace = arcpy.GetParameterAsText(0)
arcpy.env.workspace = dest

# Use the ListFeatureClasses function to return a list of
#  shapefiles.
AOIshapefiles = arcpy.ListFeatureClasses()
AreaSummery = []

for x in AOIshapefiles:
    arcpy.AddField_management(x,"Area","DOUBLE")
    with arcpy.da.UpdateCursor (x, ["SHAPE@AREA","Area"], spatial_reference=arcpy.SpatialReference(53034)) as cursor:
        for row in cursor:
            row[1] = row[0]/1000000
            AreaSummery.append(row[0]/1000000)
            cursor.updateRow(row)

Totalarea= str(sum(AreaSummery))
outFile = open(dest+"\AreaSum.text", "w")
outFile.write("The total area of all AOIs in this request is "+Totalarea+ " kilometers squared" "\n")
outFile.close()

print "The script ran successfully!"
