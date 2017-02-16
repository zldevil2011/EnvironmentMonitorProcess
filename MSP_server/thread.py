# A program to simulate selling tickets in multi-thread way
# Written by zhaolong

import threading
import time
import os

# This function could be any function to do other chores.
def doChore():
    time.sleep(0.5)


class TickBooth(threading.Thread):
    def __init__(self, tid):
        self.tid = tid
        threading.Thread.__init__(self)

    def run(self):
        while True:
            monitor['lock'].acquire()
            if monitor['tick'] != 0:
                monitor['tick'] -= 1
                print(self.tid, ':Now Left:', monitor['tick'])
                doChore()
            else:
                print("Thread id", self.tid, "No More tickets")
                os._exit(0)
            monitor['lock'].release()
            doChore()


# Function for each thread
def booth(tid):
    global i
    global lock
    while True:
        lock.acquire()                # Lock; or wait if other thread is holding the lock
        if i != 0:
            i = i - 1                 # Sell tickets
            print(tid,':now left:',i) # Tickets left
            doChore()                 # Other critical operations
        else:
            print("Thread_id",tid," No more tickets")
            os._exit(0)              # Exit the whole process immediately
        lock.release()               # Unblock
        doChore()                    # No n-critical operations

def receive(id):
    global ii
    while True:
        print(ii)
        ii -= 1
        time.sleep(0.01)
        if ii == 0:
            os._exit(0)

# Start of the main function
ii = 100000
i    = 100                           # Available ticket number
lock = threading.Lock()              # Lock (i.e., mutex)

# receive_thread = threading.Thread(target=receive,args=(1,))
# receive_thread.start()
#
# # Start 10 threads
# for k in range(10):
#     new_thread = threading.Thread(target=booth,args=(k,))   # Set up thread; target: the callable (function) to be run, args: the argument for the callable
#     new_thread.start()                                      # run the thread

monitor = {'tick': 12000000, 'lock': threading.Lock()}

for k in range(10):
    new_thread = TickBooth(k)
    new_thread.start()
