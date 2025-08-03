# This code solves starvation problem by defining a condition on picking forks:
# A philosopher can only pickup a fork if both the forks are free. If the second one
# (the right hand in the code) is not free, then it should release the first fork as well 
# and wait for the right philosopher to stop eating and releasing the right hand fork.


import threading
import time
import random


class Philosopher(threading.Thread):
    def __init__(self, name, id, left, right):
        threading.Thread.__init__(self)
        self.name = name
        self.id = id
        self.left_frok = left
        self.right_fork = right
        
    def run(self):
        
        while(True):
            self.think()
            print(f"{self.name} is hungry.")
            self.eat()
        
    def think(self):
        think_time = random.randint(1, 5)
        print(f"{self.name} is thinking for {think_time} seconds")
        time.sleep(think_time)
        print(f"{self.name} stopped thinking")
        
    
    def eat(self):
        left_fork = self.left_frok
        right_fork = self.right_fork
        
        while(True):
            left_fork.acquire()
            is_right_available = right_fork.acquire(False)  # checks whether the right hand fork is free or not
            
            if(is_right_available):  # if it was available, it would start eating, if it wasn't it would check
                                    # and wait untill it's available.
                break
            
            left_fork.release()
            print(f"{self.name} is waiting for forks to get free")
            time.sleep(1)
            
        print(f"{self.name} is eating.")
        time.sleep(2) 
        
        left_fork.release()
        right_fork.release()
        
        print(f"{self.name} stopped eating.")
        


forks = [threading.Semaphore(1) for i in range(5)]

philosophers = [
    Philosopher(f"Philosopher {i + 1}", i + 1, forks[i % 5], forks[(i + 1) % 5])
    for i in range(5)
]


for philosopher in philosophers:
    philosopher.start()
    
for philosopher in philosophers:
    philosopher.join()