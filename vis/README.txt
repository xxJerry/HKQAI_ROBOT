Specific ackages may needed, install by:

pip install -r requirements.txt
#pip install ipynb


1. To call detection functions, first import:

import detect_holes
import detect_panel
import detect_monitor
import detect_meter
#from ipynb.fs.full.meters_reading import detect as detect_meter


2. Then call functions with:

detect_holes.detect(depth)
detect_panel.detect()
detect_monitor.detect()
detect_meter.detect()

(Note: "detect_holes" and "detect_panel" are for the centrifuge. The rest are for the other machine)


Outputs:

detect_holes.detect(depth):

[x, y, z]

detect_panel.detect():

[ListOfButton], [ListOfDigits]
example: (['power_on', 'open_on'], [0, 230, 1])
(Note: "open_on" and "open_off" indicate that whether the light of the "open" button is on or off, e.g., "open_on" means the light of "open" button is on and the machine is covered. 
"Power_on" and "power_off" indicate that whether power is on or off. 
The status of button "power will go first.)

detect_monitor.detect():

[CurrentTemperature, TargetTemperature]
example: [97.5, 170.0]

(Note: second element of the output list will be 0.0 if target temperature is not detected)

detect_meter.detect():
angle
example: 321.5