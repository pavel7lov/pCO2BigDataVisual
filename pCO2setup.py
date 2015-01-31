'''
Programmers Name: Pavel Lovtsov
Date Last Updated: January 20th, 2014
Course: ICS - 4UO 
Decription: Organizes data needed for visualization 
Limitation: Takes some time to finish

'''

#Initializing key variables and importing necessary libraries.
import linecache
filename1 = []

import random

import sys
sys.setrecursionlimit(60000000)

i = 3

'''
Works cited:
Quicksort: c2.com/cgi/wiki?QuickSortInPython
Used the quicksort code. Modified it to work with my objects.

Linecache: http://python.about.com/od/simplerscripts/qt/Getlinebynumber.htm
Used to read file line by line.
'''

class Information():
    def __init__(self,name,info,divisor,sortlat):
        self.name = name
        self.info = info
        self.divisor = divisor
        self.sortlat = sortlat    

class Location(Information):
    def __init__(self,lat,lon,name,info,divisor,sortlat):
        self.lat = lat
        self.lon = lon
        Information.__init__(self,name,info,divisor,sortlat)
    
def latsort(list1):
    ''' 
    (list) -> (list)
    
    This method takes a list of Location objects and sorts it by latitude. 
    
    '''
    if len(list1) < 2: 
        return list1
    else:
        pivot = random.choice(list1)
        small = [i for i in list1 if float(i.lat)< float(pivot.lat)]
        medium = [i for i in list1 if float(i.lat)==float(pivot.lat)]
        large = [i for i in list1 if float(i.lat)> float(pivot.lat)]
        return latsort(small) + medium + latsort(large)
    
    



def lonsorthelp(list1):
    ''' 
    (list) -> (list)
    
    This method takes a list of Location objects and sorts it by longitude.  
    
    '''    
    if len(list1) < 2: 
        return list1
    else:
        pivot = random.choice(list1)
        small = [i for i in list1 if float(i.lon)< float(pivot.lon)]
        medium = [i for i in list1 if float(i.lon)==float(pivot.lon)]
        large = [i for i in list1 if float(i.lon)> float(pivot.lon)]
        return lonsorthelp(small) + medium + lonsorthelp(large)



        
def lonsort(list1,lastplace,current,final):
    ''' 
    (list, integer, integer, list) -> (list)
    
    This method takes a list of Location objects, two integers(should be 0), 
    and an empty list and returns the list of Location objects sorted by 
    longitude while maintaining the order of latitude. 
    
    '''    
    list1.append(Location(1000,1000,0,0,0,0))
    for i in range(0,((len(list1))-1)):
        if list1[i].sortlat == list1[i+1].sortlat:
            current +=1
        else:
            partial = []
            for x in range(lastplace,((current)+1)):
                partial.append(list1[x])
            final.append(partial)
            lastplace = current + 1
            current += 1  
    for i in range(0,(len(final))):
        final[i] = lonsorthelp(final[i])
    lastone = []
    for i in range(0,(len(final))):
        for x in range (0, (len(final[i]))):
            lastone.append(final[i][x])
    final = []
    return lastone    


def avg(filename1, locationarray):
    ''' 
    
    (list, list)
    
    This method takes the list of raw data and an empty list. It creates Location objects, 
    sorts them, combines data that have similar latitude and longitude, averages it, and 
    outputs the objects' data to a text file. 
    
    '''    
    
    #The 'avgconv' list is a list of average values for the data. It was calculated using a seperate program.
    avgconv = [0,0,372.10447779649525,14.660290051500347,14.40008071967913,34.085836704855666,358.8570867413065,36.361194911183425,362.61888945523253,1005.8678425248053,1005.6044413049046]
    #Splits up the data by the ',' character and creates a list.
    for d in range(0,(len(filename1))):
        filename1[d] = filename1[d].split(",")
        filename1[d][-1] = filename1[d][-1].replace('\n',"")
    #Creates Location objects. The objects need a latitude,longitude, a name, their information, a divisor and
    #a number called a 'sortlat', which is needed by the sorting functions.
    print ("Creating Objects")    
    for q in range(0,(len(filename1))):
        filewriting = "LAT[" + (str(round(float(filename1[q][2])))) + "]LON[" + (str(round(float(filename1[q][3])))) + "]"
        locationarray.append(Location((filename1[q][2]),(filename1[q][3]),filewriting,filename1[q][4:],1,(str(round(float(filename1[q][2]))))))
    #I recently found out the values that weren't measured were denoted using 
    #'-999.9'. Since we don't know what the value is, a safe guess is that it was an average value. So the part replaces
    #all the '-999.9' with average values calculated earlier.
    print ("Replacing null values with average values.")
    for i in range(0,(len(locationarray))):
        for x in range(2,(len(locationarray[i].info))):
            if float(locationarray[i].info[x]) == -999.9:
                locationarray[i].info[x] = avgconv[x]
                print ("Replaced.")
    #Sorts the objects by both latitude and longitude
    print ("Sorting.")
    locationarray = (latsort(locationarray))    
    locationarray = (lonsort(locationarray,0,0,[]))
    #Objects that have the same name are combined into one object which holds the all the totals.
    print ("Sorted. Collecting 'like' terms.")
    h = 1
    while h != ((len(locationarray))):
        if locationarray[h-1].name == locationarray[h].name:
            for y in range(2,(len(locationarray[h].info))):
                locationarray[h-1].info[y] = (float(locationarray[h-1].info[y]))+(float(locationarray[h].info[y]))
            if float(locationarray[h-1].info[1]) < float(locationarray[h].info[1]):
                locationarray[h-1].info[0] = locationarray[h].info[0]
                locationarray[h-1].info[1] = locationarray[h].info[1]
            
            locationarray[h-1].divisor += 1
            locationarray.remove(locationarray[h])                
            h = 1
            
        else:
            h+=1
            
    #Averages out all the data.    
    print ("Done. Now averaging.")
    for i in range(0,(len(locationarray))):
        for x in range(2,(len(locationarray[i].info))):
            locationarray[i].info[x] = ("%.2f" %(float(float(locationarray[i].info[x]))/(locationarray[i].divisor)))
    for i in range(0,(len(locationarray))):
        '''
        Firstly, it trys to read a pre-existing file that has the same latitude and longitude as the object. If it finds one, the data is combined and re-averaged. If not, a new file is created holding all the averages.
        '''
        try:
            with open(locationarray[i].name + '.txt', 'r') as in_file:
                holder = in_file.readlines()
            for x in range(2,((len(holder))-1)):
                holder[x] = (float((holder[x].split(": ")[1]).replace('\n',"")))
            holder[-1] = int(holder[-1])
            for x in range(2,(len(locationarray[i].info))):
                holder[x] = ("%.2f" %((((holder[x]) * (holder[-1])) + ((float(locationarray[i].info[x])) * (locationarray[i].divisor))) / (int(holder[-1]) + locationarray[i].divisor)))
            holder[-1] = (int(holder[-1]) + locationarray[i].divisor)
            print ("Overwriting file " + locationarray[i].name)
            with open(locationarray[i].name + '.txt', 'w') as out_file:
                out_file.write("Date last updated: " + str(locationarray[i].info[0]) + "\n")
                out_file.write("Date last updated (Julian Date in decimal notation): " + str(locationarray[i].info[1]) + "\n")
                out_file.write("Mole fraction concentration of CO2(ppm) in dried air: " + (str(holder[2])) + "\n")
                out_file.write("Temperature at which pCO2 was measured in C: " + (str(holder[3]))+ "\n")
                out_file.write("Sea Surface Temperature in C: " + (str(holder[4]))+ "\n")
                out_file.write("Sea Surface Salinity: " + (str(holder[5]))+ "\n")
                out_file.write("Partial Pressure of CO2 in seawater (in units of microatmospheres) at the temperature in the SST line: " + (str(holder[6]))+ "\n")
                out_file.write("Partial Pressure of CO2 in seawater (in units of Pascals) at the temperature in the TEMP line: " + (str(holder[7]))+ "\n")
                out_file.write("Partial Pressure of CO2 in seawater (in units of microatmospheres) at the temperature in the TEMP_PCO2 line: " + (str(holder[8]))+ "\n")
                out_file.write("Pressure in the equilibration vessel in units of millibars: " + str((holder[9]))+ "\n")
                out_file.write("Barometric pressure in the outside air from the ship's observation system in units of millibars: " + (str(holder[10]))+ "\n")
                out_file.write(str(holder[11]))            
        except IOError:    
            print ("Creating new file " + locationarray[i].name)
            with open(locationarray[i].name + '.txt', 'w') as out_file:
                out_file.write("Date last updated: " + str(locationarray[i].info[0]) + "\n")
                out_file.write("Date last updated (Julian Date in decimal notation): " + str(locationarray[i].info[1]) + "\n")               
                out_file.write("Mole fraction concentration of CO2(ppm) in dried air: " + (locationarray[i].info[2]) + "\n")
                out_file.write("Temperature at which pCO2 was measured in C: " + (locationarray[i].info[3])+ "\n")
                out_file.write("Sea Surface Temperature in C: " + (locationarray[i].info[4])+ "\n")
                out_file.write("Sea Surface Salinity: " + (locationarray[i].info[5])+ "\n")
                out_file.write("Partial Pressure of CO2 in seawater (in units of microatmospheres) at the temperature in the SST line: " + (locationarray[i].info[6])+ "\n")
                out_file.write("Partial Pressure of CO2 in seawater (in units of Pascals) at the temperature in the TEMP line: " + (locationarray[i].info[7])+ "\n")
                out_file.write("Partial Pressure of CO2 in seawater (in units of microatmospheres) at the temperature in the TEMP_PCO2 line: " + (locationarray[i].info[8])+ "\n")
                out_file.write("Pressure in the equilibration vessel in units of millibars: " + (locationarray[i].info[9])+ "\n")
                out_file.write("Barometric pressure in the outside air from the ship's observation system in units of millibars: " + (locationarray[i].info[10])+ "\n")
                out_file.write(str(locationarray[i].divisor))

            
    print ("Done. Next chunk...")
    
    
#Gets the number of lines in the file.    
print ("Getting number of lines.")
with open('LDEO_Database_V2012.csv','r') as x:
    file = x.readlines()
lenfile = len(file)
file = None

print (str(lenfile) + " lines.")
print ("Processing Data.")
#Chunks the data together according to the first 4 characters (denoted as 'FILENAME' in the main file)
#and feeds the chinks of data into the 'avg' function.
while i < lenfile:
    i+= 1
    while (linecache.getline('LDEO_Database_V2012.csv',i))[:4] == (linecache.getline('LDEO_Database_V2012.csv',i+1))[:4]:
        filename1.append(linecache.getline('LDEO_Database_V2012.csv',i))
        i+=1
    filename1.append(linecache.getline('LDEO_Database_V2012.csv',i))
    print ("Up to line " + (str(i)) + ".")
    avg(filename1,[])

    filename1 = []
    


        