# Accident-Avoidance-And-Detection

## Report
[Here](https://www.ijltemas.in/DigitalLibrary/Vol.5Issue5/71-74.pdf)

## Vehicle Unit
- Get an Arduino Mega 2560 board and USB cable (the kind you would connect to a USB printer)
- Download and install the Arduino Software (IDE) from https://www.arduino.cc/en/Main/Software,
    you can choose between the Installer (.exe) and the Zip packages.
- When the download finishes, proceed with the installation and please allow the driver installation process.
- Connect the board to your computer using the USB cable. The green power LED (labelled PWR) should go on.
- Drivers will automatically be installed as soon as you connect your board.
- Launch the Arduino Software (IDE).
- Open the vehicle_unit.ino file located in this disc.
- You'll need to select the entry in the Tools > Board menu that corresponds to your Arduino.
- Select the serial device of the board from the Tools > Serial Port menu.
   This is likely to be COM3 or higher (COM1 and COM2 are usually reserved for hardware serial ports).
   To find out, you can disconnect your board and re-open the menu;
   the entry that disappears should be the Arduino board. 
   Reconnect the board and select that serial port.
- Now, simply click the "Upload" button in the environment.
- Place a SIM card in SIM808 and Power SIM808 by connecting it to your computer using a USB cable.
- Turn on SIM808 and connect it to the Arduino Board.
- Connect all the sensors to the Arduino Board.
- Then, simply click the "Upload" button in the environment.
- To view the output of the sensors, click on the serial monitor in the environment.

## Server Unit
- Download and Install python 2.7.11 from https://www.python.org/downloads/.
- Open Command Prompt.
- Run the command C:\>pip install Django==1.9.6 to install Django.
- Create a folder named django in C directory.
- Copy the mysite folder located in this disc to django folder, which was created.
- Place a SIM card to SIM900A board. 
- Connect SIM900A board to the PC using a USB Cable.
- Go to C:\django\mysite in the command prompt.
- Then run the command C:\django\mysite>python manage.py runserver
- Open a web browser, and type the link - http://127.0.0.1:8000/polls
