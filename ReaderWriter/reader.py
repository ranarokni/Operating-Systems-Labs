import multiprocessing
import time
import random


class ReadersWritersWithReaderPriority:
    def __init__(self):
        self.resource_lock = multiprocessing.Lock()
        self.reader_count_lock = multiprocessing.Lock()
        self.reader_count = multiprocessing.Value('i', 0)
        self.writer_waiting = multiprocessing.Value('i', 0)
        self.shared_resource = multiprocessing.Array('i', [0] * 5)

    def read(self, reader_id):
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
        with self.writer_waiting.get_lock():
            self.writer_waiting.value += 1

        self.resource_lock.acquire()
        with self.writer_waiting.get_lock():
            self.writer_waiting.value -= 1

        index = random.randint(0, len(self.shared_resource) - 1)
        new_value = random.randint(1, 100)
        print(f"Writer {writer_id} is writing: {new_value} at index {index}")
        self.shared_resource[index] = new_value
        time.sleep(2)
        print(f"Writer {writer_id} finished writing. Resource: {list(self.shared_resource)}")

        self.resource_lock.release()


def reader_task(rw_system, reader_id):
    while True:
        time.sleep(1)
        rw_system.read(reader_id)


def writer_task(rw_system, writer_id):
    while True:
        time.sleep(1)
        rw_system.write(writer_id)


if __name__ == "__main__":
    rw_system = ReadersWritersWithReaderPriority()

    readers = [multiprocessing.Process(target=reader_task, args=(rw_system, i), name=f"Reader-{i}") for i in range(5)]
    writers = [multiprocessing.Process(target=writer_task, args=(rw_system, i),  name=f"Writer-{i}") for i in range(2)]

    all_processes = readers + writers
    random.shuffle(all_processes)

    for p in all_processes:
        print(f"p id: {p.pid}, name: {p.name}")

    for p in all_processes:
        p.start()

    for p in all_processes:
        p.join()
