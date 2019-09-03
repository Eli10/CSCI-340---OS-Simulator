# CSCI-340---OS-Simulator

Project simulates the CPU scheduling and memory management of a typical operating system. 
- Scheduling is implemented using preemptive priority CPU-scheduling.
- All I/O queues are FCFS
- Contiguous memory management with a best fit approach.

## Installation

Project is run using Python 2 NOT Python 3. Running Project in Python 3 will cause error
If Python 2 is not installed on the computer, Run
```
  brew install python2 <- mac
  sudo apt install python2.7 python-pip <- linux
```

## Usage

```
  make run <- start the project in Python 2
```

## Commands

At the start, your program asks the user two questions:

- How much RAM memory is there on the simulated computer? Your program receives the number in bytes (no kilobytes or words). I can enter any number up to 4000000000 (4 billions).

- How many hard disks does the simulated computer have? The enumeration of the hard disks starts with 0.


- (A priority memory_size) -> ‘A’ input means that a new process has been created. This process has a priority priority and requires memory_size bytes of memory. When choosing a PID for a new process start from 1 and go up.

- (t) The process that is currently using the CPU terminates. It leaves the system immediately.

- (d number file_name) The process that currently uses the CPU requests the hard disk number. It wants to read or write the file file_name.

- (D number) The hard disk number has finished the work for one process.

- (S r) Shows a process currently using the CPU and processes waiting in the ready-queue.

- (S i) Shows what processes are currently using the hard disks and what processes are waiting to use them.

- (S m) Shows the state of memory. Show the range of memory addresses used by each process in the system.






