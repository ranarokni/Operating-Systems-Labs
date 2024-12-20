# program in which p2 thread always wait for p1 to be run at first.
#  there are 3 scenarios to garantee this fact, in the first scenario 
# different number of p1 and p2 threads are defined and then all the p1s would 
# be run then all the p2s. In the second scenario, they run in turn, and in the 
# third scenario the threads would shuffle in random order, but still a p2 thread would
# run only if a p1 one have been run earlier.

import threading
import time
import random

sequence_semaphore = threading.Semaphore(0)

def p1(p1_id):
    print(f"P1 {p1_id} is running")
    time.sleep(1)
    sequence_semaphore.release()  # allow p2 to run

def p2(p2_id):
    sequence_semaphore.acquire()  # wait for p1 to finish
    print(f"P2 {p2_id} is running")


#  scenario 1

# if the number of p1 threads is less than the number of p2 threads, the program would 
# trap in a deadlock
# p1_threads = [threading.Thread(target=p1, args=(i,)) for i in range(5)]     
# p2_threads = [threading.Thread(target=p2, args=(i,)) for i in range(3)]


# for thread in p1_threads:
#     thread.start()
    
# for thread in p2_threads:
#     thread.start()

# for thread in p1_threads:
#     thread.join()
# for thread in p2_threads:
#     thread.join()

# print('Program terminated')


# scnario 2

# for i in range(5):
#         p2 = threading.Thread(target=p2)
#         p1 = threading.Thread(target=p1)

#         p2.start()
#         p1.start()

#         p1.join()
#         p2.join()
# print ("program terminated")


# scenario 3

all_threads = []

for i in range(5):
    all_threads.append(threading.Thread(target=p1, args=(i,)))
    all_threads.append(threading.Thread(target=p2, args=(i,)))
    
random.shuffle(all_threads)

for thread in all_threads:
    thread.start()
    time.sleep(1)

for thread in all_threads:
    thread.join()

print ("program terminated")
