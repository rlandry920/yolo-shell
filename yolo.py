#!/usr/bin/env python
import os
from PIL import Image
import matplotlib.pyplot as plt

import sys

if( len(sys.argv)==1):
    picture=raw_input('What picture do you want?') 
else:
    picture=str(sys.argv[1])

picCount=0;
all_objects={}
slices=[]
pictureName="data/testingPictures/%s.jpg"%picture
realPicture=Image.open(pictureName)
picWidth=realPicture.width/3
 
finalImage = Image.new('RGB', (realPicture.width, realPicture.height))

while (picCount<3):
    realPicture=Image.open(pictureName)
    
    croppedPicture = realPicture.crop((picWidth*picCount, 0,picWidth*(picCount+1) ,realPicture.height))
    croppedPicture.save("data/testing%s.jpg"%picCount)
    
 #   croppedPicture.show()
    
    os.system("./darknet detect cfg/yolo.cfg yolo.weights data/testing%s.jpg >output.txt"%picCount)
    img = Image.open('predictions.png')
    finalImage.paste(img,(picCount*picWidth,0))
    
    picCount=picCount+1
    
    myFile=open("output.txt","r")
    for line in myFile:
        detected_object=line[:line.index(":")]
        if detected_object in all_objects.keys():
            all_objects[detected_object]=all_objects[detected_object]+1
        else:
            all_objects[detected_object]=1
    
    



#finalImage.show()
finalImage.save("data/labeled/%s with labels.jpg"%picture)


for key in all_objects.keys():
    print key,":",all_objects[key]
    
plt.bar(range(len(all_objects)), all_objects.values(), align='center')
plt.xticks(range(len(all_objects)), all_objects.keys())

#plt.show()
plt.savefig("data/histograms/%s graph.jpg"%picture)