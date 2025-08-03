# Operating Systems Labs
In this repository I share my projects for my operating system lab course at the university. 


## Producer Consumer Problem
This is a classical problem of concurrency. It's also a simulation of a situation in operating systems when 1 or more processes consumes the shared resources and 1 or more ones produce shared resources. In this repository, I programmed a situation where there is a bounded buffer. Some scenarios are there for this problem which handled in the python files provided within the repository:

* [Empty buffer at the beginning:](ProducerConsumer/1_empty_buffer.py) This is a program in which the producer will produce items till the bounded buffer is full. Initialization of buffer is empty buffer. If time sleep of producer set to be more than consumer, the program would continue only when the producer produces something as all the consumers are waiting for it (and the number of consumers is more than the number of producers). There are 1 producer and 5 consumers.

* [Full buffer at the beginning: ](ProducerConsumer/1_full_buffer.py) This is a code for the situation in which the buffer is full and the producer has to wait for at least one consumer take action. There are 1 producer and 5 consumers.
* [Typical Situation:](ProducerConsumer/1_typical_buffer.py) This is a program in which the producer will produce items till the
bounded buffer is full. There are 1 producer and 5 consumers.

* [Many producers and many consumers:](ProducerConsumer/2_3producer_5consumer.py)This is a program in which the producer will produce items till the bounded buffer is full. Initialization is empty. There are 3 producers and 5 consumers)

* [Deadlock situation:](ProducerConsumer/3_deadlock.py) There is a deadlock situation when the consumer is waiting for the producer to produce something but it won't.


## P1 P2 Problem
* [P1 P2:](p1_p2.py) Using semaphores, this program ensures that for two processes, P1 and P2, the first process (P1) always executes before the second process (P2), under all circumstances.


## Dining Philosophers Problem
The [Dining Philosophers](https://github.com/ranarokni/Operating-Systems-Labs/tree/main/Dining-Philosophers) problem is a classic synchronization problem in com-
puter science. It involves five philosophers sitting at a table, alternating between
thinking and eating. Each philosopher requires two forks (left and right) to eat.
The challenge is to devise a solution that avoids deadlock and starvation while
ensuring fairness.
This document provides the implementation details of three solutions to the
Dining Philosophers problem:

- [Solution 1](https://github.com/ranarokni/Operating-Systems-Labs/blob/main/Dining-Philosophers/solution1.py): Conditional Fork Acquisition
- [Solution 2](https://github.com/ranarokni/Operating-Systems-Labs/blob/main/Dining-Philosophers/solution2.py): Fork Acquisition Based on ID Parity
- [Solution 3](https://github.com/ranarokni/Operating-Systems-Labs/blob/main/Dining-Philosophers/solution3.py): Priority Queue for Fairness

#### Solution 1: Conditional Fork Acquisition
This solution prevents deadlock by enforcing a rule: a philosopher can pick up
a fork only if both forks are available. If the second fork is not available, the
first fork is released, and the philosopher waits.

**Key Features:**
- Ensures no circular waiting by alternating the order of fork acquisition.
- Simple to implement and avoids deadlock.


#### Solution 2: Fork Acquisition Based on ID Parity
This solution divides philosophers into two groups based on their ID parity
(even or odd). Philosophers with even IDs pick up their right-hand fork first,
followed by the left-hand fork. Conversely, philosophers with odd IDs pick up
their left-hand fork first, followed by the right-hand fork.

**Key Features:** 
- Reduces the risk of deadlock by altering the fork acquisition order based
on ID parity.
- Simple to implement and ensures synchronization.


#### Solution 3: Priority Queue for Fairness
This solution uses a shared priority queue to ensure fairness. Philosophers are
served based on their waiting time, preventing starvation.

**Key Features:**
- Uses a priority queue to serve philosophers based on the order they became
hungry.
- Avoids both deadlock and starvation, ensuring fairness.

## Reader-Writer Problem
The [Reader-Writer](https://github.com/ranarokni/Operating-Systems-Labs/tree/main/ReaderWriter) problem is a classical synchronization problem that focuses
on synchronizing access to a shared resource. The problem involves multiple
readers and writers: readers can access the resource simultaneously, but writers
require exclusive access. Two common variations are implemented here:
- [Reader Priority](https://github.com/ranarokni/Operating-Systems-Labs/blob/main/ReaderWriter/reader.py)
- [Writer Priority](https://github.com/ranarokni/Operating-Systems-Labs/blob/main/ReaderWriter/writer.py)

#### Reader Priority
In this variation, priority is given to readers. If a reader is accessing the resource,
writers must wait until all readers have finished. The reader-priority solution
ensures that readers are given preferential access to the shared resource. This is
achieved through the use of two locks: a reader count lock and a resource lock.
The reader count lock is used to update the number of active readers safely,
while the resource lock ensures that writers have exclusive access when writing.
When a reader starts reading, it increments the reader count. If it is the first
reader, it acquires the resource lock, preventing writers from accessing the re-
source. Additional readers can read concurrently without blocking each other.
When a reader finishes, it decrements the reader count. If it is the last reader,
it releases the resource lock, allowing writers to proceed.
This approach guarantees that readers are not blocked as long as there are other
readers in the system, ensuring reader priority. Writers, on the other hand, must
wait for all readers to finish before they can access the resource, as the resource
lock remains held until the last reader releases it.


#### Writer Priority
In this variation, priority is given to writers. If a writer is waiting to access the
resource, readers must wait until the writer has finished. The writer-priority
solution ensures that writers are given preferential access to the shared resource.
This is achieved through the use of a write lock and a resource lock. The write
lock ensures that writers have exclusive access when writing, and it prevents
new readers from incrementing the reader count while a writer is waiting or
writing.
When a writer wants to write, it first acquires the write lock, indicating its
intent to write. It then acquires the resource lock, ensuring exclusive access to
the resource. Once the writer has completed its task, it releases both locks,
allowing readers or other writers to proceed.
Readers must check the write lock before incrementing the reader count. This
prevents new readers from starting if a writer is waiting or currently writing,
thus giving priority to writers.
This approach guarantees that writers are not starved as they are always given
priority over new readers. However, it may temporarily delay readers when a
writer is waiting or writing.