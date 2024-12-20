# Operating Systems Labs
In this repository I share my projects for my operating system lab course at the university. 


## Producer Consumer Problem
This is a classical problem of concurrency. It's also a simulation of a situation in operating systems when 1 or more processes consumes the shared resources and 1 or more ones produce shared resources. In this repository, I programmed a situation where there is a bounded buffer. Some scenarios are there for this problem which handled in the python files provided within the repository:

* [Empty buffer at the beginning:](ProducerConsumer/1_empty_buffer.py) This is a program in which the producer will produce items till the bounded buffer is full. Initialization of buffer is empty buffer. If time sleep of producer set to be more than consumer, the program would continue only when the producer produces something as all the consumers are waiting for it (and the number of consumers is more than the number of producers). There are 1 producer and 5 consumers.

* [Full buffer at the beginning: ](ProducerConsumer/1_full_buffer.py) This is a code for the situation in which the buffer is full and the producer has to wait for at least one consumer take action. There are 1 producer and 5 consumers.
* [Typical Situation:](ProducerConsumer/1_typical_buffer.py) This is a program in which the producer will produce items till the
bounded buffer is full. There are 1 producer and 5 consumers.

* [Many producers and many consumers:](ProducerConsumer/2_3producer_5consumer.py)This is a program in which the producer will produce items till the bounded buffer is full. Initialization is empty. There are 3 producers and 5 consumers)

* [Deadlock situation:](ProducerConsumer/deadlock.py) There is a deadlock situation when the consumer is waiting for the producer to produce something but it won't.


## P1 P2 Problem
* [P1 P2:](p1_p2.py) Using semaphores, this program ensures that for two processes, P1 and P2, the first process (P1) always executes before the second process (P2), under all circumstances.


