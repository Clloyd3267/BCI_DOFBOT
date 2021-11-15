from threading import Thread

inference = ""
threadRunning = False

def subscribe():
    print("Subscribed to Stream")
    global threadRunning
    threadRunning = True

    # Spawn thread
    thread = Thread(target=getInference)
    thread.start()

def receiveInference():
    return inference

def unsubscribe():
    print("Unsubscribed from Stream")
    global threadRunning
    threadRunning = False

def getInference():
    print("Thread function start!")
    i = 0
    global inference
    while threadRunning:
        inference = "Hello World {}".format(i)
        i += 1

    print("Thread function all done!")


if __name__ == "__main__":
    subscribe()

    try:
        while True:
            print(receiveInference())
    except KeyboardInterrupt:
        unsubscribe()

    print("All done")