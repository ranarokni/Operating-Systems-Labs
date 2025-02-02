# This code sloves the philosopher problem by dividing the philosophers
# to even numbers and odd numbers. The philosophers by even id has to pick
# the right hand fork first and philosophers with odd id has to pick the left hand fork first.


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
        
        if self.id % 2 == 0:   # if your id is even, you have to pick the right hand side first
            right_fork.acquire()
            left_fork.acquire()
            
        else:   # if your id is odd, you have to pick the left hand side first
            left_fork.acquire()
            right_fork.acquire()
            
        print(f"{self.name} is eating.")
        time.sleep(2) 
        
        if self.id % 2 == 0:
            right_fork.release()
            left_fork.release()
        else:
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