import multiprocessing
import time
import random


class ReadersWriters:
    def __init__(self):
        self.resource_lock = multiprocessing.Lock()  # Controls access to the shared resource
        self.reader_count_lock = multiprocessing.Lock()  # Protects access to reader_count
        self.reader_count = multiprocessing.Value('i', 0)  # Shared counter for active readers

    def read(self, reader_id):
        """Simulates a reader accessing the shared resource."""
        with self.reader_count_lock:  # Lock to safely modify reader_count
            self.reader_count.value += 1
            if self.reader_count.value == 1:  # First reader locks the resource
                self.resource_lock.acquire()

        print(f"Reader {reader_id} is reading. Active readers: {self.reader_count.value}")
        time.sleep(random.uniform(0.5, 2))  # Simulate reading time

        with self.reader_count_lock:
            self.reader_count.value -= 1
            if self.reader_count.value == 0:  # Last reader unlocks the resource
                self.resource_lock.release()

        print(f"Reader {reader_id} finished reading. Active readers: {self.reader_count.value}")

    def write(self, writer_id):
        """Simulates a writer accessing the shared resource."""
        self.resource_lock.acquire()  # Exclusive access for writers
        print(f"Writer {writer_id} is writing.")
        time.sleep(random.uniform(1, 3))  # Simulate writing time
        print(f"Writer {writer_id} finished writing.")
        self.resource_lock.release()


def reader_task(rw_system, reader_id):
    while True:
        time.sleep(random.uniform(1, 3))  # Random delay before reading
        rw_system.read(reader_id)


def writer_task(rw_system, writer_id):
    while True:
        time.sleep(random.uniform(2, 4))  # Random delay before writing
        rw_system.write(writer_id)


if __name__ == "__main__":
    rw_system = ReadersWriters()

    # Create reader and writer processes
    readers = [multiprocessing.Process(target=reader_task, args=(rw_system, i)) for i in range(5)]
    writers = [multiprocessing.Process(target=writer_task, args=(rw_system, i)) for i in range(2)]

    # Start all reader and writer processes
    for reader in readers:
        reader.start()
    for writer in writers:
        writer.start()

    # Wait for all processes to finish
    for reader in readers:
        reader.join()
    for writer in writers:
        writer.join()
