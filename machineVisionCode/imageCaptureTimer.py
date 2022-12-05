from multiprocessing import Queue
import sched, time

runTimer = True

def captureTimer(s, queue):
    while runTimer:
        time.sleep(s)
        queue.put(True)
        print("Saving objects")