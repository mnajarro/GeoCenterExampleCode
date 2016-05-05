import zipfile
import re
import os
import tarfile
import shutil
import arcpy
from arcpy import env
  
#Recieve Zipfiles from User
if len(sys.argv) < 2:
  print "\nUsage: ",sys.argv[0]," file1.zip, [file2, file3...]"
  print 'Press <ENTER> to finish...'
  raw_input()
  sys.exit()

#unzip tarfile from zipfile
try:

  dest = os.path.dirname(sys.argv[1])
  for f in sys.argv[1:]:
    print f
    if zipfile.is_zipfile(f):
      zipfiles = zipfile.ZipFile(f,'r')
      for y in zipfiles.namelist():
        if y.endswith('.tar'):
          print y
          zipfiles.extract(y,dest)
      zipfiles.close()
  #Shapefile extraction from tarfile
  arcpy.env.overwriteOutput = True
  for item in os.listdir(dest):
    if item.endswith('.tar'):
      tar2 = tarfile.open(dest+'\\'+item, "r")
      p = re.compile('(?!\S*DVD_VOL)(\S*_TILE_SHAPE)')
      for x in tar2.getnames():
        if p.match(x):
                print "Extracting ", x
                tar2.extract(x,dest)
                path, filename = os.path.split(dest+'\\'+x)
                newplace = os.path.join(dest, filename)
                shutil.move(dest+'\\'+x,dest+'\\'+filename)
                shutil.rmtree(path)
                
      tar2.close()    

except Exception as ex:
  print ex 
  print '\nPress <ENTER> to finish...'
  raw_input()
  sys.exit()    




#Arcpy Area Calculation
arcpy.env.overwriteOutput = True
arcpy.env.workspace = dest
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

#Delete empty folders
j = re.compile('(?!\S*order-)')
for x in os.listdir(dest): 
  if os.path.isdir(dest+'\\'+x):
    if j.match(x):
      shutil.rmtree(dest+'\\'+x)



print '\nThe script ran successfully! Press <ENTER> to finish...'
raw_input()
