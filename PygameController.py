####################################################################################################################
# IMPORTS
import pygame
from pygame.event import Event
from KeyboardController import KeyboardController
from TelloPlus import TelloPlus

####################################################################################################################
# GLOBALS

# ---> Constants
TITLE = "CULA-Tello"
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400


# ---> Attributes

####################################################################################################################
# CORE

# ---> Functions
def pygame_init():

    # activate the pygame library
    # initiate pygame and give permission
    # to use pygame's functionality.
    pygame.init()

    # create the display surface object
    # of specific dimension..e(X, Y).
    display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # set the pygame window name
    pygame.display.set_caption(TITLE)

    # define the RGB value for white,
    # green, blue colour .
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 32)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('GeeksForGeeks', True, green, blue)

    # create a rectangular object for the
    # text surface object
    text_rect = text.get_rect()

    # set the center of the rectangular object.
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


def run(kb_controller: KeyboardController):
    # Starting main thread
    # infinite loop

    running = True
    while running:

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.

        quit_prog = False
        pygame_events = pygame.event.get()
        for event in pygame_events:
            if event.type == pygame.QUIT:
                quit_prog = True

        if not quit_prog:

            # if event.type != pygame.QUIT:
            if not quit_prog:
                kb_controller.update_pressed(pygame.key.get_pressed())
                running = kb_controller.exe_command()

            # If event object type is QUIT
            # then quitting the pygame
            # and program both.
            else:

                running = False

                # deactivates the pygame library
                pygame.quit()

                # quit the program.
                quit()

            # Draws the surface object to the screen.
            pygame.display.update()
