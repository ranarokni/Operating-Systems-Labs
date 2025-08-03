import multiprocessing
import time
import random


class ReadersWriter:
    def __init__(self):
        self.write_lock = multiprocessing.Lock() 
        self.resource_lock = multiprocessing.Lock()  
        self.reader_count_lock = multiprocessing.Lock()  
        self.reader_count = multiprocessing.Value('i', 0)  
        self.shared_resource = multiprocessing.Array('i', [0] * 5)  

    def read(self, reader_id):
        with self.write_lock:
            with self.reader_count_lock:
                self.reader_count.value += 1
                if self.reader_count.value == 1:
                    self.resource_lock.acquire()

        print(f"Reader {reader_id} is reading: {list(self.shared_resource)}")
        time.sleep(1)
        print(f"Reader {reader_id} is done reading.")

        with self.reader_count_lock:
            self.reader_count.value -= 1
            if self.reader_count.value == 0:
                self.resource_lock.release()

    def write(self, writer_id):
        self.write_lock.acquire()
        self.resource_lock.acquire()
        index = random.randint(0, len(self.shared_resource) - 1)
        new_value = random.randint(1, 100)
        print(f"Writer {writer_id} is writing: {new_value} at index {index}")
        self.shared_resource[index] = new_value
        time.sleep(1)
        print(f"Writer {writer_id} finished writing. Resource: {list(self.shared_resource)}")
        self.resource_lock.release()
        self.write_lock.release()


def reader_task(rw_system, reader_id):
    while True:
        time.sleep(1)
        rw_system.read(reader_id)


def writer_task(rw_system, writer_id):
    while True:
        time.sleep(2)
        rw_system.write(writer_id)


if __name__ == "__main__":
    rw_system = ReadersWriter()

    readers = [multiprocessing.Process(target=reader_task, args=(rw_system, i), name=f"Reader-{i}") for i in range(5)]
    writers = [multiprocessing.Process(target=writer_task, args=(rw_system, i), name=f"Writer-{i}") for i in range(2)]

    all_proccess = readers + writers 

    random.shuffle(all_proccess)
    
    for p in all_proccess:
        print(f"p id: {p.pid}, name: {p.name}")
    
    for p in all_proccess:
        p.start()
    
    for p in all_proccess:
        p.join()
