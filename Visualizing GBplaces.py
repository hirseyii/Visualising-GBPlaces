#A program to visualise GBplaces

#reads GBplaces.csv
#plots a scatter of each place colorcoded by type
#on top of a map of the UK coastline
#user has the option to plot either cities, towns or both
#user can also plot individual places which are labelled with name and population (Custom input)
#user has the option to save the figure generated as a png with custom name
#Currently broken =/

#####PREAMBLE#####
import matplotlib.pyplot as plt;
import sys;
import string;
import os;

#Function to check if an item is in a list
def InList(Input,List):
    count = 0;
    
    for entry in List:
        if Input.lower() == entry.lower():
            count = count + 1;
            
    if count == 0:
        return False;
    
    else:
        return True;
#End Function
#####END PREAMBLE#####

#open file
#check if GBplaces opened

#loop for user wanting  to do another calculation
restart = 1;
while restart == 1:
    opened =  0;

    try:
        readGBplaces = open("GBplaces.csv","r");
        opened = 1;

    except:
        opened = 0;
        print("An error occured, the file 'GBplaces.csv' failed to open.");
        sys.exit("This program will now quit.");
    

    if opened:
        #create lists of city latlong and town latlong
        readGBplaces.readline();
        Color = [];
        citylat = [];
        citylong = [];
        townlat = [];
        townlong = [];
    
        for line in readGBplaces:
            splitUp = line.split(",");
            if splitUp[1] == "City":
                citylat.append(splitUp[3]);
                citylong.append(splitUp[4]);
            
            elif splitUp[1] == "Town":
                townlat.append(splitUp[3]);
                townlong.append(splitUp[4]);
                
        readGBplaces.close();


    #Get coastline points data
    #Check if Coastline points opened
    opened =  0;

    try:
        readCoastline = open("Coastline points.txt","r");
        opened = 1;

    except:
        opened = 0;
        print("An error occured, the file `Coastline points.txt' failed to open.");
        sys.exit("This program will now quit.");   

    x = [];
    y = [];

    if opened:
        #read data line by line
        readCoastline.readline();
        for line in readCoastline:
        
            #create lists of coastline lat & long        
            splitUp = line.split(",");
            x.append(float(splitUp[0]));
            y.append(float(splitUp[1]));
                       
    readCoastline.close();
    #Plot coastline
    plt.scatter(x,y,s=1,color = "#D3D3D3",marker = "."); 

    #Ask user if they want to see towns, cities or both or custom input
    validinput = 0

    while validinput == 0:    
        CitiesOrTowns = input("Do you wish to display cities, towns or both?\nIf you wish to specify particular towns or cities, please enter 'custom'.\n");
    
        if CitiesOrTowns.lower() == "cities":
            validinput = 1;
            #plot only cities
            CityPlot = plt.scatter(citylong,citylat,color = "r",marker = "x" );
            plt.legend([CityPlot],["Cities"]);

        elif CitiesOrTowns.lower() == "towns":
            validinput = 1;
            #plot only towns
            TownPlot = plt.scatter(townlong,townlat,color = "b",marker = "x" );
            plt.legend([TownPlot],["Towns"]);

        elif CitiesOrTowns.lower() == "both":
            validinput = 1;
            #plot both
            CityPlot = plt.scatter(citylong,citylat,color = "r",marker = "x" );
            TownPlot = plt.scatter(townlong,townlat,color = "b",marker = "x" );
            plt.legend([CityPlot,TownPlot],["Cities","Towns"]);

        elif CitiesOrTowns.lower() == "custom":   
            validinput = 1;
            CustomPlaceslong = [];
            CustomPlaceslat = [];
            CustomPlacesname = [];
            CustomPlacespop = [];
            CustomPlacescolor = [];
        
            #plot a custom group of cities/towns
            EndRequest = 0;
       
            while EndRequest == 0:            
                UserPlace = input("Please input a place that you want to display on the map and press the return key. If you have finished entering places, please type 'end'.\n");
                readGBplaces = open("GBplaces.csv","r");


                #create list of names
                PlaceNames = [];
                for line in readGBplaces:
                    splitUpNames = line.split(",");
                    PlaceNames.append(splitUpNames[0]);
                                      
                readGBplaces.seek(0);                      
                #Exit condition
                if UserPlace.lower() == "end":
                    EndRequest = 1;                      
                 
                #Check that entry exists in the list of names     
                elif InList(UserPlace,PlaceNames) == False:
                    EndRequest = 0;
                    print("\nThe place you entered is not valid.");

                #Check for duplicate inputs
                elif InList(UserPlace,CustomPlacesname) == True:
                    EndRequest = 0;
                    print("\nYou have already entered this place.");                
                    
                else:
                    for line in readGBplaces:
                        splitUp = line.split(",");

                        #Create custom lists for long/lat, name and population
                        if splitUp[0].lower() == UserPlace.lower():
                            CustomPlaceslong.append(splitUp[4]);
                            CustomPlaceslat.append(splitUp[3]);
                            CustomPlacesname.append(splitUp[0]);
                            CustomPlacespop.append(splitUp[2]);

                            #Assign colors to towns/cities
                            if splitUp[1] == "City":
                                CustomPlacescolor.append("r");
                
                            elif splitUp[1] == "Town":
                                CustomPlacescolor.append("b");
        
            readGBplaces.close();

            print("The places you entered are:");
            print(CustomPlacesname);
            #Plot the custom points
            plt.scatter(CustomPlaceslong,CustomPlaceslat,color = CustomPlacescolor,marker = "x",s = 80);
        
            #Plot points for a legend
            plt.scatter(2,58,color = "b",marker = "x",s = 80);
            plt.annotate("Towns",xy = (2,58),xytext = (2.2,58));
            plt.scatter(2,57,color = "r",marker = "x",s = 80);
            plt.annotate("Cities",xy = (2,57),xytext = (2.2,57));
        
            #Annotate with name and population
            for n in range(0,len(CustomPlacesname)):           
                plt.annotate("\n" + CustomPlacesname[n] + "\n" + CustomPlacespop[n],xy = (CustomPlaceslong[n],CustomPlaceslat[n]));                    
                                 
        #If 'cities','towns','both' or 'custom' is not entered, ask again.                     
        else:
            validinput = 0;
        
    #Adjust axis sizes
    plt.xlim(-10,5);
    plt.ylim(49.5,59);
    plt.xlabel("Longitude");
    plt.ylabel("Latitude");
    plt.title("UK Cities and Towns");
    #Allows Figure to be accessed after calling show()
    fig = plt.gcf();
    plt.show();

    #ask user if they want to save the image    
    SaveImage = input("If you wish to save the figure, please enter 'yes'. If not, press any key.\n");
    if SaveImage.lower() == "yes":
        #Ensure the file name does not contain special characters
        ValidFileName = 0;
        while ValidFileName == 0:
            ImageName = input("What would you like to call the file? Do not use any special characters.\n");

            if any(char in string.punctuation for char in ImageName):
                ValidFileName = 0;
                
            else:
                ValidFileName = 1;
                
                #Prevent overwriting files with the same name
                Overwrite = 0
                while os.path.exists(ImageName + ".png"):
                    Overwrite = Overwrite + 1;
                    ImageName = ImageName + str(Overwrite);
                fig.savefig(ImageName + ".png",dpi = 400);

    #Restart condition
    UserRestart = input("If you would like to create another plot please enter 'yes'. If you wish to quit, press any key.\n");
    if UserRestart.lower() == "yes":
        restart = 1;
    
    else:
        restart = 0;
    