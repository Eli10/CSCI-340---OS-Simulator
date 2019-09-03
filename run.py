# Elijah Augustin
# CSC 340 Final Project

from needed_classes import Process, OS, process_command


if __name__ == "__main__":
  mem_size = raw_input("How much RAM memory is on the computer? ")
  hard_disks = raw_input("How many hard disks does the computer have? ")
  os = OS(mem_size, hard_disks)
  while(True):
    command = raw_input(">> ")
    command_list = command.split(" ")
    process_command(os, command_list)