import csv
import glob
import os
from tensorflow import keras
import numpy as np
from PIL import Image
import time

model = keras.models.load_model('natural_identifier_80')
model.summary()
saveFile = '../static/sampleData.csv'
imagesToClassify = []

# not positive my labels are correct

y_labels = {0:'car',1:'human',2:'cat',3:'motorcycle',4:'human'}
csv_columns = ['timestamp', 'people', 'dogs', 'other']

def setCSV(csvLocation):
    if not saveFile:
        saveFile = csvLocation
    else:
        print("ERROR: Already set a save location.")

def classifyImagesInDirectory(dir, currentTime):
    # if not saveFile:
        # print("Please set a csv save file with 'setCSV(filename)'")
    # elif not os.path.exists(dir):
        # print(f"Invalid save directory '{dir}'")
    
    # Convert to milliseconds for exporting to Javascript
    currentTime = currentTime * 1000

    images = glob.glob('imageOut/*.jpg')
    predictions = {'timestamp':currentTime, 'people':0, 'dogs':0, 'other':0}
    for image in images:
        name = image
        image = Image.open(image)
        image = image.resize((256,256))
        image = np.asarray(image)
        image = image.reshape(1, 256,256,3)

        prediction = y_labels[np.argmax(model.predict(image, verbose = 0))]
        # print(f'Found {prediction}')
        if prediction == 'human':
            predictions['people'] = predictions.get('people') + 1
        elif prediction == 'dog':
            predictions['dogs'] = predictions.get('dogs') + 1
        else:
            predictions['other'] = predictions.get('other') + 1
        os.remove(name)
    # try:
    if(os.path.exists(saveFile)):
        with open(saveFile, 'a+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writerow(predictions)
    else:
        with open(saveFile, 'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(predictions) 

classifyImagesInDirectory('imageOut', time.time())


# images = glob.glob('imageOut/*.jpg')
# for image in images:
#     name = image
#     image = Image.open(image)
#     image = image.resize((256,256))
#     image = np.asarray(image)
#     image = image.reshape(1, 256,256,3)

#     print(name, y_labels[np.argmax(model.predict(image, verbose = 0))])

# images = glob.glob('imageOut/*.jpg')


# print(predictions)