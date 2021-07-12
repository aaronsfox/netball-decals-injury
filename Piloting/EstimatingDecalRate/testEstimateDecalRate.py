# -*- coding: utf-8 -*-
"""
Created on Wed May 19 15:22:29 2021

@author:
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
"""

# %% Import packages

from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
import random
from shapely.geometry import Point, Polygon

# %% Generate a visual of a court with certain decals

# Note the court has coordinates of 0-305 width and 0-152.5 height and these 
# indicate the court dimensions in centimetres.
#
#

#Create figure
fig,ax = plt.subplots(figsize = (15,7.5))

#Set axes limits to just outside court boundaries
ax.set_xlim([-0.5,305.5])
ax.set_ylim([-0.25,152.75])

#Turn off axes
plt.axis('off')

###TODO: Set court width and height variables instead of repeating

#Draw the outside of the court
ax.add_patch(Rectangle((0,0), 305, 152.5,
                       linestyle = '-', linewidth = 2,
                       edgecolor = 'k', facecolor = 'none'))

#Draw the third lines
ax.plot([305/3,305/3], [0,152.5],
        linestyle = '-', linewidth = 2,
        color = 'k')
ax.plot([305/3*2,305/3*2], [0,152.5],
        linestyle = '-', linewidth = 2,
        color = 'k')

#Draw centre circle
ax.add_patch(Circle((305/2,152.5/2), 9,
                    linestyle = '-', linewidth = 2,
                    edgecolor = 'k', facecolor = 'none'))

#Add shooting circles
ax.add_patch(Circle((0,152.5/2), 49,
                    linestyle = '-', linewidth = 2,
                    edgecolor = 'k', facecolor = 'none'))
ax.add_patch(Circle((305,152.5/2), 49,
                    linestyle = '-', linewidth = 2,
                    edgecolor = 'k', facecolor = 'none'))

#Add some decals in the top and bottom of the middle third
#Plot twice to decouple edge colour and hatch colour
#Top of court
ax.add_patch(Rectangle(((305/3)+10,152.5-30), (305/3)-20, 20,
                       linestyle = '-', linewidth = 2,
                       edgecolor = 'r', facecolor = 'none',
                       hatch = '/'))
ax.add_patch(Rectangle(((305/3)+10,152.5-30), (305/3)-20, 20,
                       linestyle = '-', linewidth = 2,
                       edgecolor = 'k', facecolor = 'none'))
#Bottom of court
ax.add_patch(Rectangle(((305/3)+10,0+10), (305/3)-20, 20,
                       linestyle = '-', linewidth = 2,
                       edgecolor = 'r', facecolor = 'none',
                       hatch = '/'))
ax.add_patch(Rectangle(((305/3)+10,0+10), (305/3)-20, 20,
                       linestyle = '-', linewidth = 2,
                       edgecolor = 'k', facecolor = 'none'))

# %% Randomly sample some injuries in the centre third

# Here we'll assume that a player spends equal time across the entire centre third
# In that case we simply sample points from a series of x,y coordinates that
# represent the centre third

### NOTE: normalising court to integer units might help here???

#The centre third starts at 305/3 and ends at 305/3*2 on the x-axis; and sits
#between zero and 152.5 on the y-axis - hence we need an equal number of EVERY
#combination of these x,y coordinates to sample from. We'll separate into rounded
#integers for now to make it easy, and go from 102 to 203 on the x-axis and 0
#to 152 on the y-axis
coordsSelect = []
for xx in np.linspace(102, 203, 203-102+1):
    for yy in np.linspace(0, 152, 152-0+1):
        coordsSelect.append([int(xx),int(yy)])
        
#Set seed for random selection
random.seed(12345)

#Set nuymber of trials
nTrials = 1000

#Set list to store selections
selectedCoords = []

#Randomly select 1000 samples from the coords list and plot
for nn in range(nTrials):
    #Select coordinate
    selectedCoord = random.choice(coordsSelect)
    #Plot it
    ax.plot(selectedCoord[0], selectedCoord[1],
            marker = 'o', markersize = 2, color = 'b')
    #Append coordinate to list
    selectedCoords.append(selectedCoord)
    
# %% Check the rate at which the random samples fall within the 'decals'      

#Create the two decal polygons using their x,y coordinates
#Set the corner points of the decals
decalTop = [((305/3)+10,152.5-30), #bottom left
          ((305/3)+10+(305/3)-20,152.5-30), #bottom right
          ((305/3)+10+(305/3)-20,152.5-10), #top right
          ((305/3)+10,152.5-10), #top left
          ((305/3)+10,152.5-30) #bottom left
          ]
decalBottom = [((305/3)+10,0+10), #bottom left
               ((305/3)+10+(305/3)-20,0+10), #bottom right
               ((305/3)+10+(305/3)-20,30), #top right
               ((305/3)+10,30), #top left
               ((305/3)+10,0+10) #bottom left
               ]
#Convert the decals to polygons
decalTopPoly = Polygon(decalTop)
decalBottomPoly = Polygon(decalBottom)

#Method to plot polygons
# x,y = decalTopPoly.exterior.xy
# plt.plot(x,y,linewidth=2,linestyle='--',color='r')

#Loop through selected coordinates and check if within one of the decal polygons
selectedInside = []
for pp in range(len(selectedCoords)):
    #Create the current points
    currPoint = Point(selectedCoords[pp][0],selectedCoords[pp][1])
    #Check if within any of the decal polygons
    if decalTopPoly.contains(currPoint) or decalBottomPoly.contains(currPoint):
        #Append as true for this point
        selectedInside.append(True)
    else:
        #Append as false for this point
        selectedInside.append(False)

#Sum the number of points inside and divide by total number of points to get %
perInside = np.sum(selectedInside) / len(selectedInside)

#Print output
print(f'Proportion of points inside decals: {np.round(perInside*100,2)}%')



