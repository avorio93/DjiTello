import PygameController
from KeyboardController import KeyboardController
from TelloPlus import TelloPlus

####################################################################################################################
# GLOBALS

# ---> Constants

# ---> Attributes

####################################################################################################################
# CORE

# ---> Functions

# Initialize Tello Instance
tello = TelloPlus()

# Initialize the Keyboard Controller with the tello instance
kbController = KeyboardController(tello)

# Run the main thread
PygameController.pygame_init()
PygameController.run(kbController)

# ---> Constructor

"""

"""
