# ASCIIpy
![ASCII-Art](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/thefuck_cap.jpg)

ASCIIpy is a simple to use command line tool that helps you to convert an input image into ascii art. For the moment the scrip will print the ascii art to the console (dependent on your src image size you might need to change the text size to something very small if you want to view it in the console) and generate a html and jpg file containing the ascii art all at once for every file you call it with. But I will look into a way how you can call the scrip with some more specific task and more options at hand

## Usage
1. Download the ASCIIpy-master.zip from [here](https://github.com/ElCap1tan/ASCIIpy/archive/master.zip) and unzip it into a location of your liking. I will refer to this location as ```home folder``` from now on.
2. Place the images you want to convert into the ```in``` folder inside the ```home folder```
3. Open the terminal and move to the location of the ```ascii.py``` file. If you haven't already you need to install pillow
```
> pip install Pillow
```
4. Run the ```ascii.py``` script where
* IMAGE_FILE_NAME is the full name of a file in the ```in``` folder for example ```car.jpg```
* MODE is the way the RGB color values are converted to a single brighness value for each pixel. At the moment this script supports ```lum```inosity, ```avg``` or ```light```ness. The method that gives the best overall results imo is ```lum``` but it might be worth trying the others if you're not okay with the end result.
```
> python ascii.py IMAGE_FILE_NAME MODE
```
5. The output html and jpg files will be written to the ```out``` folder and are named the same as the input file

## Examples (For the html preview download the files for now thinking about a way how to link them here as online version but for now thats not possible.)
### Car
#### Original
![Original Car](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/in/car.jpg)
#### ASCII
![ASCII-Art Car](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/car.jpg)]
### Girl
#### Original
![Original Girl](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/in/girl.jpg)
#### ASCII
![ASCII-Art Girl](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/girl.jpg)]
### Girl
#### Original
![Original Pineapple](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/in/pineapple.jpg)
#### ASCII
![ASCII-Art Pineapple](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/pineapple.jpg)]
