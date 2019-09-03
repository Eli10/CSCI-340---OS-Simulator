# Elijah Augustin
# CSC 340 Final Project

from collections import deque


def process_command(operating_system, command_list):
  if command_list[0] == "A":
    priority = int(command_list[1])
    mem_size = int(command_list[2])
    process = Process(priority, mem_size)
    operating_system.add_new_process(process)

  if command_list[0] == "S" and command_list[1] == "r":
    operating_system.print_cpu_usage()

  if command_list[0] == "d":
    hard_disk_id = int(command_list[1])
    file_to_use = command_list[2]
    operating_system.add_to_hard_disk(hard_disk_id, file_to_use)

  if command_list[0] == "D":
    hard_disk_id = int(command_list[1])
    operating_system.remove_process_from_hard_disk(hard_disk_id)

  if command_list[0] == "S" and command_list[1] == "i":
    operating_system.print_hard_disks()

  if command_list[0] == "t":
    operating_system.remove_cpu_process()

  if command_list[0] == "S" and command_list[1] == "m":
    operating_system.print_memory()




#Process Class
class Process(object):

  def __init__(self, priority, mem_size):
    self.priority = priority
    self.memory_size = mem_size
    self.PID = 0

  def __str__(self):
    return "PID: {} - Priority: {}".format(self.PID, self.priority)

  def set_pid(self, pid):
    self.PID = pid

  def get_pid(self):
    return self.PID

  def get_priority(self):
    return self.priority

  def get_memory_size(self):
    return self.memory_size

#Storing Process IDs from Process Table
class Ready_Queue(object):

  def __init__(self):
    self.ready_queue = list()

  def add(self, process_id):
    self.ready_queue.append(process_id)
    print self.ready_queue

  def get(self):
    process_id = self.ready_queue[0]
    self.ready_queue.remove(process_id)
    print self.ready_queue
    return process_id

  def remove(self, process_id):
    self.ready_queue.remove(process_id)
    print self.ready_queue

  def length(self):
    return len(self.ready_queue)

  def get_highest_priority_process_id(self, process_table):
    priority = 0
    process_id = 0
    for p in self.ready_queue:
      if process_table[p].get_priority() > priority:
        priority = process_table[p].get_priority()
        process_id = p
    return process_id

  def ___str___():
    str_queue = ""
    for r_id in self.ready_queue:
      str_queue += "\t {} ".format(r_id)
    return str_queue

  def update_queue(self, process_index_to_remove, process_table):

    print self.ready_queue 

    for index, process_id in enumerate(self.ready_queue):
        if process_id > process_index_to_remove:
          new_process_id = process_id - 1
          self.ready_queue[index] = new_process_id

    print self.ready_queue 

    if len(self.ready_queue) != 0:
      next_process_to_run = self.get_highest_priority_process_id(process_table)
      self.remove(next_process_to_run)
      return next_process_to_run


  def print_queue(self, process_table):
    str_queue = "Ready Queue: \n\n"
    for r_id in self.ready_queue:
      str_queue += "\t {}\n".format(process_table[r_id])
    print str_queue



#Create hard disk class -> Name, Disk_Id, process_id_in_use, i/o queue
# OS Class will have a list of Hard Disk Objects
class Hard_Disk(object):

  def __init__(self, id):
    self.disk_id = id
    self.process_id_in_use = None
    self.file_in_use = None
    self.io_queue = deque()


  def print_hard_disk(self, process_table):
    if self.process_id_in_use == None and self.file_in_use == None and len(self.io_queue) == 0:
      print "Disk {} : PID idle : File idle \n".format(self.disk_id)
    else:
      disk_str = "Disk {} : PID {} : File {} \n I/O Queue: \n".format(self.disk_id, process_table[self.process_id_in_use], self.file_in_use)
      for p in self.io_queue:
        disk_str += "\t PID {} : File {} \n".format(process_table[p["process_id"]], p["file_to_use"])
      print disk_str

  def get_id(self):
    return self.disk_id

  def get_pid(self):
    return self.process_id_in_use

  def get_file(self):
    return self.file_in_use

  def use_next_process_in_queue(self):
    if len(self.io_queue) == 0:
      return
    else:
      next_process = self.io_queue.popleft()
      self.process_id_in_use = next_process["process_id"]
      self.file_in_use = next_process["file_to_use"]


  def add_to_io_queue(self, process_id_and_file_hash):
    print len(self.io_queue)
    if len(self.io_queue) == 0 and self.file_in_use == None:
      print "Use 1"
      self.io_queue.append(process_id_and_file_hash)
      self.process_id_in_use = process_id_and_file_hash["process_id"]
      print self.process_id_in_use
      self.file_in_use = process_id_and_file_hash["file_to_use"]
      self.io_queue.popleft()
    else:
      print "Use 2"
      self.io_queue.append(process_id_and_file_hash)


  def remove_running_process(self):
    previously_running_process = self.process_id_in_use
    self.process_id_in_use = None
    self.file_in_use = None
    self.use_next_process_in_queue()
    return previously_running_process

  def update_queue(self, process_index_to_remove):

    if self.process_id_in_use == None:
      pass
    else:
      if self.process_id_in_use > process_index_to_remove:
        self.process_id_in_use = self.process_id_in_use - 1

    if len(self.io_queue) == 0:
      return

    for index, process_id in enumerate(self.io_queue):
        if process_id > process_index_to_remove:
          new_process_id = process_id - 1
          self.io_queue[index] = new_process_id



class Memory(object):

  def __init__(self, mem_size):
    self.min_memory = 0
    self.max_memory = 4000000000
    self.current_memory_usage = mem_size if mem_size <= self.max_memory else mem_size
    self.groups_wanted = 10
    self.divide_by = self.current_memory_usage / self.groups_wanted
    
    self.bins = self.current_memory_usage / self.divide_by

    self.bin_list = self.create_bin_list()

    print(self.bin_list)


  def get_memory_table(self, process_table):
    line_plot = "Memory Table Intervals\n"
    for b in self.bin_list:
      if len(b) == 2:
        line_plot += """|{}---------{}|  Processes Allocated: {} \n""".format(b[0], b[1], "None")
      else:
        process_list = [ process_table[p].get_pid() for p in b[2] ]
        line_plot += """|{}---------{}|  Processes Allocated: {} \n""".format(b[0], b[1], " ".join(str(p) for p in process_list) )
    return line_plot

  def create_bin_list(self):
    return [ [ i*self.divide_by, ((i+1)*self.divide_by)-1 ] for i in range(0, self.bins)]

  def check_memory_overflow(self, process_memory):
    return self.current_memory_usage - process_memory < self.min_memory

  def get_bin_size(self, bin_interval):
    return (bin_interval[1] - bin_interval[0]) + 1

  def get_a_bin_size(self):
    return self.get_bin_size(self.bin_list[0])

  def check_if_memory_fits_in_bin_interval(self, process_memory, bin_size):
    return bin_size - process_memory >= 0


  def check_if_multiple_process_memory_fits_in_bin_interval(self, bin_interval, new_process_memory, process_table):
    bin_interval_size = self.get_bin_size(bin_interval)
    process_list = bin_interval[2]
    total_process_memory = 0
    for p in process_list:
      mem = process_table[p].get_memory_size()
      total_process_memory += mem
    return (total_process_memory + new_process_memory) <= bin_interval_size 


  def add_process_to_memory(self, process_index, process_table):
    current_process_memory = process_table[process_index].get_memory_size()
    if self.check_memory_overflow(current_process_memory) == False:
      for bin_interval in self.bin_list:
        bin_size = self.get_bin_size(bin_interval)
        if len(bin_interval) == 2 and self.check_if_memory_fits_in_bin_interval(current_process_memory, bin_size) == True:
          bin_interval.append([process_index])
          return 
        elif len(bin_interval) == 3 and self.check_if_multiple_process_memory_fits_in_bin_interval(bin_interval, current_process_memory, process_table) == True:
          bin_interval[2].append(process_index)
          return
        else:
          continue

      print "Needs to be allocated to multiple intervals"


  def remove_process_from_memory(self, process_index_to_remove, process_table):
    for bin_interval in self.bin_list:
      if len(bin_interval) == 2:
        pass
      elif len(bin_interval) == 3:
        if process_index_to_remove in bin_interval[2]:
          bin_interval[2].remove(process_index_to_remove)
        for index, process_id in enumerate(bin_interval[2]):
          if process_id > process_index_to_remove:
            new_process_id = process_id - 1
            bin_interval[2][index] = new_process_id






class OS(object):

  def __init__(self, ram_size, num_of_hard_disks):
    self.total_memory = Memory(int(ram_size))
    self.num_of_hard_disks = self.create_hard_disk(num_of_hard_disks)
    self.current_pid = 1
    self.process_table = list()
    self.ready_queue = Ready_Queue()
    self.process_using_cpu_index = None
    # print(self.total_memory)

  def create_hard_disk(self, num_of_hard_disks):
    return [ Hard_Disk(i) for i in range(0, int(num_of_hard_disks)) ]


  def print_hard_disks(self):
    for i in self.num_of_hard_disks:
      i.print_hard_disk(self.process_table)
      


  def add_to_hard_disk(self, hard_disk_id, file_to_use):

    for i in self.num_of_hard_disks:
      if i.get_id() == hard_disk_id:
        process_id_file_hash = {"process_id": self.process_using_cpu_index, "file_to_use": file_to_use  }
        # i.add_to_io_queue(self.process_using_cpu_index, file_to_use)
        i.add_to_io_queue(process_id_file_hash)
        self.process_using_cpu_index = None
        self.cpu_null_check()

  def remove_process_from_hard_disk(self, hard_disk_id):

    for i in self.num_of_hard_disks:
      if i.get_id() == hard_disk_id:
        process_index_from_io_queue = i.remove_running_process()
        self.add_back_old_process(process_index_from_io_queue)


  #Making sure that when Cpu is checking for next available process to run
  def cpu_null_check(self):
    if self.process_using_cpu_index == None:
      id_of_process_with_highest_id = self.ready_queue.get_highest_priority_process_id(self.process_table)
      self.ready_queue.remove(id_of_process_with_highest_id)
      self.process_using_cpu_index = id_of_process_with_highest_id


  def add_check_to_ready_queue(self, process_index):
    if self.ready_queue.length() == 0:
      self.ready_queue.add(process_index)
      if self.process_using_cpu_index == None:
        self.process_using_cpu_index = self.ready_queue.get()
      else:
        currently_running_process = self.process_table[self.process_using_cpu_index]
        id_of_process_with_highest_id = self.ready_queue.get_highest_priority_process_id(self.process_table)
        process_with_higest_id = self.process_table[id_of_process_with_highest_id]
        if (id_of_process_with_highest_id == process_index) and process_with_higest_id.get_priority() > currently_running_process.get_priority():
          self.ready_queue.remove(id_of_process_with_highest_id)
          self.ready_queue.add(self.process_using_cpu_index)
          self.process_using_cpu_index = id_of_process_with_highest_id
    else:
      self.ready_queue.add(process_index)
      currently_running_process = self.process_table[self.process_using_cpu_index]
      id_of_process_with_highest_id = self.ready_queue.get_highest_priority_process_id(self.process_table)
      process_with_higest_id = self.process_table[id_of_process_with_highest_id]
      if (id_of_process_with_highest_id == process_index) and process_with_higest_id.get_priority() > currently_running_process.get_priority():
        self.ready_queue.remove(id_of_process_with_highest_id)
        self.ready_queue.add(self.process_using_cpu_index)
        self.process_using_cpu_index = id_of_process_with_highest_id


  # Add Process to process_table and assign PID -> add to ready queue -> check if process in CPU use needs to be changed
  def add_new_process(self, process):
    process.set_pid(self.current_pid)

    if process.get_memory_size() > self.total_memory.get_a_bin_size():
      print "Process is allocating more memory than an interval can hold. Not creating"
      return

    self.process_table.append(process)
    self.current_pid += 1

    self.add_check_to_ready_queue(self.process_table.index(process))

    self.total_memory.add_process_to_memory(self.process_table.index(process), self.process_table)


  #Adding process from i/o queues back to the ready queue
  def add_back_old_process(self, process_index):
    self.add_check_to_ready_queue(process_index)


  #When you a remove a process, if other processes in that list had a lesser index, do not change
  # if the process has a higher index then the one you remove, decrement the index of that process
  # - Remove from CPU Usage
  # - Update Ready Queue
  # - Update IO Queue


  def remove_cpu_process(self):
    process_index_to_remove = self.process_using_cpu_index
    self.process_table.remove(self.process_table[process_index_to_remove])

    self.process_using_cpu_index == None
    next_process_to_run = self.ready_queue.update_queue(process_index_to_remove, self.process_table)
    self.process_using_cpu_index = next_process_to_run


    for disk in self.num_of_hard_disks:
      disk.update_queue(process_index_to_remove)

    self.total_memory.remove_process_from_memory(process_index_to_remove, self.process_table)

    
  def print_cpu_usage(self):
    if len(self.process_table) == 0:
      print "No Process In Usage Or in Ready Queue"
    else:
      print "CPU -> {}".format(self.process_table[self.process_using_cpu_index]) 
      self.ready_queue.print_queue(self.process_table)


  def print_memory(self):
    print self.total_memory.get_memory_table( self.process_table)

        












