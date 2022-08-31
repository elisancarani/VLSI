# VLSI
VLSI Very Large Scale Integration   
CP 

-TO RUN ALL THE INSTANCES WITHOUT ROTATION
Download the folder and open it using any python IDE. We used Pycharm.
Add a Venv (we used python 3.9).
Open the file run.py and set the parameter "rotation" at line 147 to False.
Run the file (minizinc has to be installed).
The results are placed in the folder out/noRotation.  

-TO RUN ALL THE INSTANCES WITH ROTATION
Download the folder and open it using any python IDE. We used Pycharm.
Add a Venv (we used python 3.9). Import all the necessary libraries.
Open the file run.py and set the parameter "rotation" at line 147 to True.
Run the file (minizinc has to be installed).
The results are placed in the folder out/Rotation.  

-TO RUN A SINGLE FILE
Download the folder.
Open the desired model (csp.mzn for no rotation, csp.mzn for rotation) using minizinc.
If the folder instancesdzn is already present skip the next step: run the file "txttodzn.sh" from the command prompt.
Open the desired instance from the folder instancesdzn using minizinc.
Run the model, selecting the desired instance from the pop up window.

