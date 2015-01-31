/**
*Programmers Name: Pavel Lovtsov
*Date Last Updated: January 20th, 2014
*Course: ICS - 4UO 
*Decription: Displays a map and pCO2 data for most locations in the ocean. 
*Limitation: Needs Google Mapper + Internet COnnection
*/

//Importing Google Mapper
import googlemapper.*;

//Text for textfile
String s = "";

//Map Varaiables
PImage map;
GoogleMapper gMapper;

//Position of rectangle and textbox
float posix;
float posiy;

//Mouses latitude and longitude
float mouselatpoint; 
float mouselonpoint;

public void setup() {
  /**
  *Sets up the window and the map
  */
  size(1026,768,JAVA2D);

  double maCenterLat = 0;
  double mapCenterLon = 10;
  int zoomLevel = 2;
  String mapType = GoogleMapper.MAPTYPE_HYBRID;
  int mapWidth=1026;
  int mapHeight=768;
  
  gMapper = new GoogleMapper(maCenterLat, mapCenterLon, zoomLevel, mapType, mapWidth,mapHeight);
  
  map = gMapper.getMap();
  posix = -10000;
  posiy = -10000;
}

public void draw() {
  /**
  *Draws the window, map, rectangle and textbox
  */
  image(map,0,0);

  fill(0);
  rect(posix,posiy,600,190);
  fill(#FFFFFF);
  text(s, posix,posiy, 600, 190);
  mouselatpoint = (float)(gMapper.y2lat(mouseY));
  mouselonpoint = (float)(gMapper.x2lon(mouseX));
  fill(0);
  text(((str(mouselatpoint)) + "," + (str(mouselonpoint))),mouseX - 75, mouseY-25, 200,100);
}


public void mousePressed(){
    /**
  *Gets the position of mouse pointer and draws rectangle
  *and textbox. Reads corresponding file and displays the info
  *If the file can't be found, displays "File not found.".
  */
     s = "";
     float latpoint = (float)(gMapper.y2lat(mouseY));
     float lonpoint = (float)(gMapper.x2lon(mouseX));
     try{
     String[] pieces = loadStrings("LAT[" + str(round(latpoint)) + "]LON[" + str(round(lonpoint)) + "].txt");

       for (int i = 0; i < pieces.length; i++){

      s = s + pieces[i] + "\n";
  }  if (latpoint <= 0 && lonpoint >= 0){
      posix = (50);
      posiy = (50);
  }else if (latpoint <= 0 && lonpoint < 0){
    posix = (1026 - 600);
    posiy = 50;
    
  }else if (latpoint > 0 && lonpoint >= 0){
    posix = 50;
    posiy = 768 - 300;
  }else{
    posix = (1026 - 600);
    posiy = 768 - 300;
  }
     }catch (Exception e){
       if (latpoint <= 0 && lonpoint >= 0){
      posix = (50);
      posiy = (50);
  }else if (latpoint <= 0 && lonpoint < 0){
    posix = (1026 - 600);
    posiy = 50;
    
  }else if (latpoint > 0 && lonpoint >= 0){
    posix =50;
    posiy = 768 - 300;
  }else{
    posix = (1026 - 600);
    posiy = 768 - 300;
  }
       s = "File not found.";
     }
        // Text wraps within text box
     
   
 
  
}

void keyPressed() { 
  /**
  *Changes X and Y of rectangle and textbox and clears textbox.
  */  
if (keyCode == DELETE) {
  s = ""; 
  posix = -10000;
  posiy = -10000;
}

}

