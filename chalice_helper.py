# Chalice Helper v2.4

from gui import GUI
from directory import Directory

# Creates a Directory object from the current directory
direc = Directory()
# Sets up and runs the GUI
interface = GUI(direc)