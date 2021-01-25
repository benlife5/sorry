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
#                  LITERALS

from enum import Enum


class Player(Enum):
    P1 = "blue"  # top left
    P2 = "red"  # top right
    P3 = "green"  # bottom left
    P4 = "yellow"  # bottom right


class SpaceType(Enum):
    NORMAL = 0
    SAFETY = 100
    START = 200
    HOME = 300


class Events(Enum):
    CLICK = 999


# hard-coded locations of start spaces
p1_start_coords = ((4, 2), (4, 3), (5, 2), (5, 3))  # top left
p2_start_coords = ((14, 4), (14, 5), (15, 4), (15, 5))  # top right
p3_start_coords = ((2, 12), (2, 13), (3, 12), (3, 13))  # bottom left
p4_start_coords = ((12, 14), (12, 15), (13, 14), (13, 15))  # bottom right
start_coords = p1_start_coords + p2_start_coords + p3_start_coords + p4_start_coords
start_coord_dict = {Player.P1: p1_start_coords, Player.P2: p2_start_coords,
                    Player.P3: p3_start_coords, Player.P4: p4_start_coords}

p1_home_coords = ((3, 7), (3, 8), (4, 7), (4, 8))  # top left
p2_home_coords = ((9, 3), (9, 4), (10, 3), (10, 4))  # top right
p3_home_coords = ((7, 13), (7, 14), (8, 13), (8, 14))  # bottom left
p4_home_coords = ((13, 9), (13, 10), (14, 9), (14, 10))  # bottom right
home_coords = p1_home_coords + p2_home_coords + p3_home_coords + p4_home_coords

normal_list = []
for row in range(1, 17):  # 16x16 grid
    for column in range(1, 17):
        if row == 1 or row == 16 or column == 1 or column == 16:  # only create perimeter
            normal_list.append((row, column))
normal_coords = tuple(normal_list)

p1_safety_list, p2_safety_list, p3_safety_list, p4_safety_list = [], [], [], []
for i in range(2, 7):  # four 1x5 grids
    p1_safety_list.append((3, i))  # top left
    p2_safety_list.append(((17 - i), 3))  # top right
    p3_safety_list.append((i, 14))  # bottom left
    p4_safety_list.append((14, (17 - i)))  # bottom right
p1_safety_coords, p2_safety_coords, p3_safety_coords, p4_safety_coords = \
    tuple(p1_safety_list), tuple(p2_safety_list), tuple(p3_safety_list), tuple(p4_safety_list)
safety_coords = p1_safety_coords + p2_safety_coords + p3_safety_coords + p4_safety_coords

new_deck = [
    1, 1, 1, 1, 1,
    2, 2, 2, 2,
    3, 3, 3, 3,
    4, 4, 4, 4,
    5, 5, 5, 5,
    7, 7, 7, 7,
    8, 8, 8, 8,
    10, 10, 10, 10,
    11, 11, 11, 11,
    12, 12, 12, 12,
    "Sorry", "Sorry", "Sorry", "Sorry"
]

card_descriptions = {
    "": ["Deck", "Shuffled"],
    1: ["", "Move 1", "or move", "from Start"],
    2: ["Move 2", "or move", "from Start.", "Draw Again!"],
    3: ["", "", "Move 3"],
    4: ["", "Move", "backwards", "4"],
    5: ["", "", "Move 5"],
    7: ["Move 7", "or split", "between", "two pawns"],
    8: ["", "Move 8"],
    10: ["", "Move 10", "or", "backwards 1"],
    11: ["Move 11", "or switch", "with another", "player"],
    12: ["", "", "Move 12"],
    "Sorry": ["Move from", "Start, sending", "opponent", "to Start"]
}

test_deck = [11, 1, 11, 1, 11, 1]

draw_pile_coords = [(6, 6), (7, 6), (6, 7), (7, 7), (6, 8), (7, 8)]
discard_pile_coords = [(10, 9), (11, 9), (10, 10), (11, 10), (10, 11), (11, 11)]
slide_coords = [(2, 1), (10, 1), (16, 2), (16, 10), (15, 16), (7, 16), (1, 15), (1, 7)]
start_square_coords = [(5, 1), (1, 12), (16, 5), (12, 16)]
