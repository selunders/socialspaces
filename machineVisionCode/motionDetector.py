import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from multiprocessing import Process, Queue
import os
import time
# print(os.listdir('.'))
import imageCaptureTimer as capTimer
import classifier

# Referenced this article on how to use opencv closing
# https://www.tutorialspoint.com/performing-a-closing-operation-on-an-image-using-opencv


def nothing(x):
    pass

def keepOdd(x):
    if x%2 == 0:
        return x+1
    else:
        return x

def detectMotion(webcam, commandQueue):
    saveObjects = False        
    key = ord('r')

    # Controls Window
    cv.namedWindow('controls')
    cv.createTrackbar("blurAmount", "controls", 0, 255, nothing)
    cv.setTrackbarPos("blurAmount", "controls", 15)
    # cv.createTrackbar("closeKernelSize1", "controls", 0, 255, nothing)
    # cv.setTrackbarPos("closeKernelSize1", "controls", 0)
    # cv.setTrackbarPos("closeKernelSize1", "controls", 8)
    cv.createTrackbar("closeKernelSize2", "controls", 0, 255, nothing)
    cv.setTrackbarPos("closeKernelSize2", "controls", 90)
    # cv.setTrackbarPos("closeKernelSize2", "controls", 45)
    # Background Subtractor
    bg = cv.createBackgroundSubtractorKNN()

    while(key != ord('s')):
        if not commandQueue.empty():
            saveObjects = commandQueue.get()
        blurAmount = keepOdd(cv.getTrackbarPos("blurAmount", "controls"))
        still = webcam.read()
        img = cv.cvtColor(still[1], cv.COLOR_BGR2GRAY)
        img = cv.GaussianBlur(img, (blurAmount, blurAmount), 0)
        cv.imshow("Preprocessed", img)

        # Close img
        # closedKernelSize1 = keepOdd(cv.getTrackbarPos("closeKernelSize1", "controls"))
        # kernel = np.ones((closedKernelSize1,closedKernelSize1), np.uint8)
        # img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
        # cv.imshow("Closed Img 1", img)

        # Remove background
        img = bg.apply(img)
        cv.imshow("BG Removed", img)
        
        # Close img
        closedKernelSize2 = keepOdd(cv.getTrackbarPos("closeKernelSize2", "controls"))
        kernel = np.ones((closedKernelSize2,closedKernelSize2), np.uint8)
        img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
        cv.imshow("Closed Img 2", img)

                
        (numLabels, labels, stats, centroids) = cv.connectedComponentsWithStats(img, 8, cv.CV_32S)
        # (numLabels, labels, stats, centroids) = cv.connectedComponentsWithStats(img, 8, cv.CV_32S)
        sortedStats = np.argsort(-stats[:,-1])
        sortedStats = sortedStats[1:11]
        numLabels = sortedStats.size
        # for i in range(0, numLabels):
        # print(numLabels)
        # if numLabels < 10:
        #     for i in range(numLabels+1, 10):
        #         cv.destroyWindow(f'Subimage {i}')
        for i in sortedStats:
            x = stats[i, cv.CC_STAT_LEFT]
            y = stats[i, cv.CC_STAT_TOP]
            w = stats[i, cv.CC_STAT_WIDTH]
            h = stats[i, cv.CC_STAT_HEIGHT]
            if w*h > (50 * 50): # arbitrarily picked this. Gets rid of some of the noisy tiny movements. May need changed depending on camera resolution, distance, etc.
                if saveObjects or key == ord('c'):
                    xslice = slice(x, x+w)
                    yslice = slice(y, y+h)
                    subImage = still[1][yslice, xslice]

                    # if(x>=0 and y>=0 and w > 0 and h > 0):
                    print(os.listdir('./imageOut'))
                    try:
                        cv.imwrite(f'./imageOut/Subimage{i}.jpg', subImage)
                    except:
                        print("Could not write image")
                    print(os.listdir('./imageOut'))
                        # cv.destroyWindow(f'Subimage {i}')
                    classifier.classifyImagesInDirectory('imageOut', time.time())

                # else:
                    # cv.destroyWindow(f'Subimage {i}')
                cv.rectangle(still[1], (x, y), (x+w, y+h), (0,255,0), 3)

        cv.imshow("Motion Detection", still[1])
        # cv.imshow("Image", img)
        # cv.imshow("Still", still[1])
        key = ord('r')
        saveObjects = False;
        key = cv.waitKey(10)

if __name__ == "__main__":
    webcam = cv.VideoCapture(0)
    runTimer = True
    if webcam:
        commandQueue = Queue()
        timerProcess = Process(target=capTimer.captureTimer, args=(5, commandQueue))
        timerProcess.start()
        detectMotion(webcam, commandQueue)
        timerProcess.runTimer = False
        timerProcess.terminate()
    else:
        print("ERROR: Could not access webcam")
        cv.destroyAllWindows()
        webcam.release()
        exit(1)
    cv.destroyAllWindows()
    webcam.release()