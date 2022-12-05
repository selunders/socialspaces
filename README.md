# socialspaces
An OpenCV, Tensorflow/Keras, Flask, and ChartJS project to display activity in social spaces.

## To try yourself:
- Set up a Conda environment with the environment.yml file
  - conda env create -n socialSpaces -f environment.yml
  - conda activate socialSpaces
- Set how often you would like to collect data via the waitMinutes variable in machineVision/motionDetector.py
- Run the motionDetector.py file
  - python motionDetector.py
- In another terminal, navigate to the root directory and execute 'flask run'
- In a browser, navigate to the url given by flask. Usually '127.0.0.1:5000' or 'localhost:5000'
