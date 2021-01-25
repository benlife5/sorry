# Ben Life
# Copyright 2021
# Licensed under GNU GPLv3 (see COPYING.txt)
#
#  ▄█▀▀▀▄█
#  ██▄▄  ▀    ▄▄▄   ▄▄▄ ▄▄  ▄▄▄ ▄▄   ▄▄▄▄ ▄▄▄
#   ▀▀███▄  ▄█  ▀█▄  ██▀ ▀▀  ██▀ ▀▀   ▀█▄  █
# ▄     ▀██ ██   ██  ██      ██        ▀█▄█
# █▀▄▄▄▄█▀   ▀█▄▄█▀ ▄██▄    ▄██▄        ▀█
#                                    ▄▄ █
#                                     ▀▀
#              VERSION 2.0 BETA
#                    BOARD

from sorry_literals import *
from pygame import font


class BoardSize:
    """
    A class to contain all size and scale related variables.
    Attributes:
        length: (int) the length (and width) of a single square in the 16x16 grid.
        xshift: (int) the horizontal offset of the entire grid.
        yshift: (int) the vertical offset of the entire grid.
        font: (pygame.font) the main font size.
        font_small: (pygame.font) a smaller font size.
    """
    def __init__(self, window_width, window_height):
        """
        Creates a BoardSize object (16x16 grid centered on the window)
        :param window_width: (int) the width of the window.
        :param window_height: (int) the height of the window.
        """
        self.length = min(window_width, window_height) // 18  # divide the smaller dimension into 18 parts
        if window_width > window_height:  # if width is greater, create xshift
            self.xshift = (window_width - window_height) // 2
            self.yshift = 0
        else:  # if height is greater, create yshift
            self.xshift = 0
            self.yshift = (window_height - window_width) // 2
        self.font = font.SysFont("Arial", int(self.length / 2))
        self.font_small = font.SysFont("Arial", int(self.length / 3))
        self.font_title = font.SysFont("Tahoma", int(self.length) * 3, bold=True)
        self.font_menu = font.SysFont("Tahoma", int(self.length) * 2)
        self.font_menu_small = font.SysFont("Tahoma", int(self.length / 3) * 2)


class BoardSpace:
    """
    A class to represent each space on a Sorry board.
    Attributes:
        space_type: (enum SpaceType.NORMAL/SAFETY/START/HOME) The type of space (affects gameplay options)
        is_occupied: (bool) True if there is a piece in the spot, False otherwise
        player: (None or enum Player.P1/P2/P3/P4) Some spaces (normal, safety, start, and home)
                are reserved for specific players. None if it is a Normal space.
        is_slide: (bool or int) False if it is not a slide, the length of the slide (3 or 4) if it is a slide
    No methods.
    """
    def __init__(self, space_type=SpaceType.NORMAL, is_occupied=False, player=None, is_slide=False):
        """
        Creates a BoardSpace object.
        :param space_type: (enum SpaceType.NORMAL/SAFETY/START/HOME) The type of space.
        :param is_occupied: (bool) True if there is a piece in the spot, False otherwise
        :param player: (None or enum Player.P1/P2/P3/P4) Player that the space is reserved for,
                                                         None if it is a Normal space.
        :param is_slide: (bool or int) False if it is not a slide, the length of the slide (3 or 4) if it is a slide
        """
        self.space_type = space_type
        self.is_occupied = is_occupied
        self.player = player
        self.is_slide = is_slide

    def __repr__(self):
        return "BoardSpace(space_type=" + str(self.space_type) + ", is_occupied=" + str(self.is_occupied) + \
               ", player=" + str(self.player) + ", is_slide=" + str(self.is_slide) + ")"

    def __str__(self):
        return str(self.space_type.name) + " Board Space (is_occupied=" + str(self.is_occupied) + \
               ", player=" + str(self.player) + ", is_slide=" + str(self.is_slide) + ")"


class Piece:
    """
    A class to represent a Sorry game piece.
    Attributes:
        location: (tuple) the location of the piece on the 16x16 grid (x, y)
        player: (enum Player.P1/P2/P3/P4) the player whose piece it is
    Methods:
        sorry()
            Move piece back to START
        move()
            Move piece to new space
    """
    def __init__(self, location, player, is_selected=False):
        """
        Creates a Piece object.
        :param location: (tuple) the location of the piece on the 16x16 grid (x, y)
        :param player: (enum Player.P1/P2/P3/P4) the player whose piece it is
        :param is_selected: (bool) True if the piece is selected
        """
        self.location = location
        self.player = player
        self.is_selected = is_selected

    def __repr__(self):
        return "Piece(player=" + str(self.player) + ", location=" + str(self.location) \
               + ", is_selected=" + str(self.is_selected) + ")"

    def select(self):
        """Select a piece at the coordinate given."""
        self.is_selected = True

    def deselect(self):
        """Deselect a piece at the coordinate given."""
        self.is_selected = False

    def move(self, new_location):
        """
        Move a piece object
        :param new_location: (tuple) the (x, y) location to move the piece to
        """
        # Define new and old locations
        old_location = self.location
        self.location = new_location

        # Update board locations
        board[old_location].is_occupied = False
        board[new_location].is_occupied = True

        # Update pieces dictionary
        pieces[new_location] = self
        del pieces[old_location]

        # Deselect piece
        self.deselect()

    def slide(self):
        """
        Attempts to perform a slide maneuver.
        """
        if board[self.location].is_slide:
            slide_length = board[self.location].is_slide
            if self.location[1] == 1 and self.player != Player.P1:  # top
                for j in range(slide_length - 1):
                    self.sorry((self.location[0] + 1, self.location[1]))
            elif self.location[0] == 16 and self.player != Player.P2:  # right side
                for j in range(slide_length - 1):
                    self.sorry((self.location[0], self.location[1] + 1))
            elif self.location[0] == 1 and self.player != Player.P3:  # left side
                for j in range(slide_length - 1):
                    self.sorry((self.location[0], self.location[1] - 1))
            elif self.location[1] == 16 and self.player != Player.P4:  # bottom
                for j in range(slide_length - 1):
                    self.sorry((self.location[0] - 1, self.location[1]))

    def sorry(self, location):
        """
        Move the piece and "Sorry" the piece that is at it's new location
        :param location: (tuple) the (x, y) location to move the piece to
        """
        if location in pieces:  # there is a piece to "sorry"
            for coordinate in start_coord_dict[pieces[location].player]:
                if not board[coordinate].is_occupied:
                    pieces[location].move(coordinate)
                    break
        self.move(location)


# Created all BoardSpaces and pieces
board = {}
pieces = {}

# Normal spaces
for coord in normal_coords:
    board[coord] = BoardSpace()

# Safety spaces
for coord in p1_safety_coords:
    board[coord] = BoardSpace(space_type=SpaceType.SAFETY, player=Player.P1)
for coord in p2_safety_coords:
    board[coord] = BoardSpace(space_type=SpaceType.SAFETY, player=Player.P2)
for coord in p3_safety_coords:
    board[coord] = BoardSpace(space_type=SpaceType.SAFETY, player=Player.P3)
for coord in p4_safety_coords:
    board[coord] = BoardSpace(space_type=SpaceType.SAFETY, player=Player.P4)

# Start spaces (and pieces)
for coord in p1_start_coords:
    board[coord] = BoardSpace(space_type=SpaceType.START, player=Player.P1, is_occupied=True)
    pieces[coord] = Piece(coord, Player.P1)
for coord in p2_start_coords:
    board[coord] = BoardSpace(space_type=SpaceType.START, player=Player.P2, is_occupied=True)
    pieces[coord] = Piece(coord, Player.P2)
for coord in p3_start_coords:
    board[coord] = BoardSpace(space_type=SpaceType.START, player=Player.P3, is_occupied=True)
    pieces[coord] = Piece(coord, Player.P3)
for coord in p4_start_coords:
    board[coord] = BoardSpace(space_type=SpaceType.START, player=Player.P4, is_occupied=True)
    pieces[coord] = Piece(coord, Player.P4)

# Home spaces
for coord in p1_home_coords:
    board[coord] = BoardSpace(space_type=SpaceType.HOME, player=Player.P1)
for coord in p2_home_coords:
    board[coord] = BoardSpace(space_type=SpaceType.HOME, player=Player.P2)
for coord in p3_home_coords:
    board[coord] = BoardSpace(space_type=SpaceType.HOME, player=Player.P3)
for coord in p4_home_coords:
    board[coord] = BoardSpace(space_type=SpaceType.HOME, player=Player.P4)

# Set slides
for coord in slide_coords[1::2]:
    board[coord].is_slide = 5
for coord in slide_coords[::2]:
    board[coord].is_slide = 4

board[100, 100] = BoardSpace()
