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
#                    DRAW
import pygame as pg
from pygame import gfxdraw
import sorry_board as board
from sorry_literals import *


def draw_board(surface, scale):
    """
    Creates and draws rectangles for the board game Sorry. A 14x14 perimeter + four 5x1 safety zones
    :param surface: (pygame.display) the pygame surface to be drawn on.
    :param scale: (sorry_board.BoardSize) a BoardSize object for the current window.
    """
    length, xshift, yshift = scale.length, scale.xshift, scale.yshift
    board_rects = {  # construct board_rects dict
        "normal": [],
        "safety": [],
        "start": [],
        "home": [],
        "start_square": []
    }

    # Create normal board spaces
    for space in board.normal_coords:
        board_rects["normal"].append(pg.Rect(space[0] * length + xshift, space[1] * length + yshift, length, length))

    # Create safety zone spaces
    for space in board.safety_coords:
        board_rects["safety"].append(pg.Rect(space[0] * length + xshift, space[1] * length + yshift, length, length))

    # Create start zone spaces
    for sc in board.start_coords:
        board_rects["start"].append(pg.Rect(sc[0] * length + xshift, sc[1] * length + yshift, length, length))

    # Create home zone spaces
    for hc in board.home_coords:
        board_rects["home"].append(pg.Rect(hc[0] * length + xshift, hc[1] * length + yshift, length, length))

    # Create start squares
    for ssc in start_square_coords:
        board_rects["start_square"].append(pg.Rect(ssc[0] * length + xshift, ssc[1] * length + yshift, length, length))

    # Draw all spaces
    for space in board_rects["normal"]:
        pg.draw.rect(surface, "white", space)
    for space in board_rects["safety"]:
        pg.draw.rect(surface, "grey75", space)
        pg.draw.rect(surface, "black", space, width=1)  # outline
    for space in board_rects["start"]:
        pg.draw.rect(surface, "grey50", space)
    for space in board_rects["home"]:
        pg.draw.rect(surface, "grey30", space)
    for space in board_rects["start_square"]:
        pg.draw.rect(surface, "grey80", space)
    draw_slides(surface, scale)
    for space in board_rects["normal"]:
        pg.draw.rect(surface, "black", space, width=1)  # outline


def draw_pieces(surface, scale):
    """
    Draws circles to represent the game pieces.
    :param surface: (pygame.display) the pygame surface to be drawn on.
    :param scale: (sorry_board.BoardSize) a BoardSize object for the current window.
    """
    length, xshift, yshift = scale.length, scale.xshift, scale.yshift

    for piece in board.pieces.values():
        x = int(piece.location[0] * length + length / 2 + xshift)
        y = int(piece.location[1] * length + length / 2 + yshift)
        color = pg.Color(piece.player.value)

        pg.gfxdraw.filled_circle(surface, x, y, int(length / 2) - 1, color)
        if piece.is_selected:
            pg.gfxdraw.aacircle(surface, x, y, int(length / 2) - 3, pg.Color("black"))
            pg.gfxdraw.aacircle(surface, x, y, int(length / 2) - 2, pg.Color("black"))
            pg.gfxdraw.aacircle(surface, x, y, int(length / 2) - 1, pg.Color("black"))
            pg.gfxdraw.aacircle(surface, x, y, int(length / 2), pg.Color("black"))
        else:
            pg.gfxdraw.aacircle(surface, x, y, int(length / 2) - 1, color)


def draw_cards(surface, scale, deck, card_to_display):
    """
    Draws rects to represent the game cards.
    :param surface: (pygame.display) the pygame surface to be drawn on.
    :param scale: (sorry_board.BoardSize) a BoardSize object for the current window.
    :param card_to_display: (int) the index of the card to display from the deck.
    :param deck" (list of int and str) the list containing the values for the whole deck.
    """
    length, xshift, yshift = scale.length, scale.xshift, scale.yshift
    font, font_small = scale.font, scale.font_small

    # Draw 3x2 rectangle backgrounds
    draw_pile = pg.Rect(6 * length + xshift, 6 * length + yshift, length * 2, length * 3)
    discard_pile = pg.Rect(10 * length + xshift, 9 * length + yshift, length * 2, length * 3)
    pg.draw.rect(surface, "white", draw_pile)
    pg.draw.rect(surface, "white", discard_pile)

    # Draw pile text
    draw_pile_text = font.render("SORRY!", True, "black")
    draw_pile_text_rect = draw_pile_text.get_rect(center=(7 * length + xshift, 7.5 * length + yshift))
    surface.blit(draw_pile_text, draw_pile_text_rect)

    active_card = deck[card_to_display]
    active_card_description = card_descriptions[active_card]

    top_of_card = font.render(str(active_card), True, "black")
    top_of_card_rect = top_of_card.get_rect(center=(11 * length + xshift, 9.5 * length + yshift))
    surface.blit(top_of_card, top_of_card_rect)

    for j, line in enumerate(active_card_description):
        text = font_small.render(line, True, "black")
        text_rect = text.get_rect(center=(11 * length + xshift, (10 + 0.5 * j) * length + yshift))
        surface.blit(text, text_rect)


def draw_slides(surface, scale):
    """
    Draws the slides on each side of the board.
    :param surface: (pygame.display) the pygame surface to be drawn on.
    :param scale: (sorry_board.BoardSize) a BoardSize object for the current window.
    """
    length, xshift, yshift = scale.length, scale.xshift, scale.yshift  # unpack scale
    for coord in slide_coords:
        if coord[0] == 1:  # left column
            rect = pg.Rect((coord[0] + 0.39) * length + xshift,
                           coord[1] * length + yshift - (board.board[coord].is_slide - 1) * length,
                           length * .25, length * board.board[coord].is_slide)
            triangle = (
                (coord[0] * length + xshift, (coord[1] + 1) * length + yshift),
                ((coord[0] + 1) * length + xshift, (coord[1] + 1) * length + yshift),
                ((coord[0] + 0.5) * length + xshift, (coord[1]) * length + yshift)
            )
            pg.draw.rect(surface, Player.P3.value, rect)
            pg.draw.polygon(surface, Player.P3.value, triangle)
        elif coord[0] == 16:  # right column
            rect = pg.Rect((coord[0] + 0.39) * length + xshift,
                           coord[1] * length + yshift,
                           length * .25, length * board.board[coord].is_slide)
            triangle = (
                (coord[0] * length + xshift, coord[1] * length + yshift),
                ((coord[0] + 1) * length + xshift, coord[1] * length + yshift),
                ((coord[0] + 0.5) * length + xshift, (coord[1] + 1) * length + yshift)
            )
            pg.draw.rect(surface, Player.P2.value, rect)
            pg.draw.polygon(surface, Player.P2.value, triangle)
        elif coord[1] == 1:  # top row
            rect = pg.Rect(coord[0] * length + xshift,
                           (coord[1] + .39) * length + yshift,
                           length * board.board[coord].is_slide, length * .25)
            triangle = (
                (coord[0] * length + xshift, coord[1] * length + yshift),
                (coord[0] * length + xshift, (coord[1] + 1) * length + yshift),
                ((coord[0] + 1) * length + xshift, (coord[1] + 0.5) * length + yshift)
            )
            pg.draw.rect(surface, Player.P1.value, rect)
            pg.draw.polygon(surface, Player.P1.value, triangle)
        elif coord[1] == 16:  # bottom row
            rect = pg.Rect((coord[0] - board.board[coord].is_slide + 1) * length + xshift,
                           (coord[1] + 0.39) * length + yshift,
                           length * board.board[coord].is_slide, length * .25)
            triangle = (
                ((coord[0] + 1) * length + xshift, coord[1] * length + yshift),
                ((coord[0] + 1) * length + xshift, (coord[1] + 1) * length + yshift),
                ((coord[0]) * length + xshift, (coord[1] + 0.5) * length + yshift)
            )
            pg.draw.rect(surface, Player.P4.value, rect)
            pg.draw.polygon(surface, Player.P4.value, triangle)


def draw_menu(surface, scale, host_input, port_input):
    """
    Draws the menu screen and buttons.
    :param surface: (pygame.display) the pygame surface to be drawn on.
    :param scale: (sorry_board.BoardSize) a BoardSize object for the current window.
    :param host_input: (str) The current text for the Host field.
    :param port_input: (str) The current text for the Port field.
    :return: (four pygame.Rect's) Rects containing the Play buttons and the Host/Port fields.
    """
    # Unpack scale variables and fonts
    length, xshift, yshift = scale.length, scale.xshift, scale.yshift
    font_title, font_menu, font_menu_small = scale.font_title, scale.font_menu, scale.font_menu_small

    title_text = font_title.render("SORRY!", True, "black")  # TITLE
    title_text_rect = title_text.get_rect(center=(9 * length + xshift, 2.5 * length + yshift))
    surface.blit(title_text, title_text_rect)

    play_local_text = font_menu.render("Play Local", True, "black")  # PLAY LOCAL
    play_local_text_rect = play_local_text.get_rect(center=(9 * length + xshift, 6.5 * length + yshift))
    pg.draw.rect(surface, "grey75", play_local_text_rect.inflate(length * 0.5, length * 0.5), border_radius=10)
    surface.blit(play_local_text, play_local_text_rect)

    play_online_text = font_menu.render("Play Online", True, "black")  # PLAY ONLINE
    play_online_text_rect = play_online_text.get_rect(center=(9 * length + xshift, 10.5 * length + yshift))
    pg.draw.rect(surface, "grey75", play_online_text_rect.inflate(length * 0.5, length * 0.5), border_radius=10)
    surface.blit(play_online_text, play_online_text_rect)

    host_label = font_menu_small.render("Host:", True, "black")  # HOST FIELD
    host_label_rect = host_label.get_rect(left=(4 * length + xshift), centery=(12.5 * length + yshift))
    host_label_rect.width = play_online_text_rect.width
    surface.blit(host_label, host_label_rect)
    host_value = font_menu_small.render(host_input, True, "black")
    host_value_rect = host_value.get_rect(left=(6 * length + xshift), centery=(12.5 * length + yshift))
    surface.blit(host_value, host_value_rect)

    port_label = font_menu_small.render("Port:", True, "black")  # PORT FIELD
    port_label_rect = host_label.get_rect(left=(4 * length + xshift), centery=(13.5 * length + yshift))
    port_label_rect.width = play_online_text_rect.width
    surface.blit(port_label, port_label_rect)
    port_value = font_menu_small.render(port_input, True, "black")
    port_value_rect = port_value.get_rect(left=(6 * length + xshift), centery=(13.5 * length + yshift))
    surface.blit(port_value, port_value_rect)

    bottom_left = font_menu_small.render("v2.0", True, "black")  # VERSION
    bottom_left_rect = bottom_left.get_rect(center=(1 * length + xshift, 17.5 * length + yshift))
    surface.blit(bottom_left, bottom_left_rect)

    bottom_right = font_menu_small.render("Ben Life", True, "black")  # AUTHOR
    bottom_right_rect = bottom_right.get_rect(center=(16.5 * length + xshift, 17.5 * length + yshift))
    surface.blit(bottom_right, bottom_right_rect)

    return play_local_text_rect, play_online_text_rect, host_label_rect, port_label_rect
