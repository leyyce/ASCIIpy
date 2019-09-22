# ASCIIpy
![Console-Demo](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/demo.gif)

![ASCII-Art](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/thefuck_cap.jpg)

ASCIIpy is a simple to use command line tool that helps you to convert an input image into ascii art. For the moment the scrip will print the ascii art to the console (dependent on your src image size you might need to change the text size to something very small if you want to view it in the console) and generate a html and jpg file containing the ascii art all at once for every file you call it with. But I will look into a way how you can call the scrip with some more specific task and more options at hand

## Installation and dependencies
1. Download the ASCIIpy-master.zip from [here](https://github.com/ElCap1tan/ASCIIpy/archive/master.zip) and unzip it into a location of your liking. I will refer to this location as ```home folder``` from now on.
2. Place the images you want to convert into the ```in``` folder inside the ```home folder```
3. Open the terminal and move into the the ```home folder```.
4. Install the dependencies.
```
> pip install -r requirements.txt
```
## Usage
Run the ```ascii.py``` script 
```
> python ascii.py [-h] [-m CONVERSION_MODE] [--rainbow] [--no-console] image
```
where
* **image** is the full name of a file in the ```in``` folder for example ```car.jpg```
* **CONVERSION_MODE** is the way the RGB color values are converted to a single brightness value for each pixel. At the moment this script supports ```lum```inosity, ```avg``` or ```light```ness. The method that gives the best overall results imo is ```lum``` but it might be worth trying the others if you're not okay with the end result.
* The **--rainbow** argument doesn't do anything at the moment. Image will be in grayscale HTML in color by default.

*The output html and jpg files will be written to the ```out``` folder and are named the same as the input file*

## Examples
### Car
#### Original
![Original Car](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/in/car.jpg)
#### ASCII [[HTML Preview]](http://htmlpreview.github.io/?https://github.com/ElCap1tan/ASCIIpy/blob/master/out/examples/car.html)
![ASCII-Art Car](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/car.jpg)
### Eye
#### Original
![Original Eye](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/in/eye.jpg)
#### ASCII [[HTML Preview]](http://htmlpreview.github.io/?https://github.com/ElCap1tan/ASCIIpy/blob/master/out/examples/eye.html)
![ASCII-Art Eye](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/eye.jpg)
### Girl
#### Original
![Original Girl](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/in/girl.jpg)
#### ASCII [[HTML Preview]](http://htmlpreview.github.io/?https://github.com/ElCap1tan/ASCIIpy/blob/master/out/examples/girl.html)
![ASCII-Art Girl](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/girl.jpg)
### Pineapple
#### Original
![Original Pineapple](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/in/pineapple.jpg)
#### ASCII [[HTML Preview]](http://htmlpreview.github.io/?https://github.com/ElCap1tan/ASCIIpy/blob/master/out/examples/pineapple.html)
![ASCII-Art Pineapple](https://raw.githubusercontent.com/ElCap1tan/ASCIIpy/master/out/examples/pineapple.jpg)
