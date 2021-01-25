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


import pygame as pg
import sorry_draw as draw
import sorry_board as board
import sorry_network as network
from sorry_literals import *
from random import shuffle, seed


def determine_space_clicked(scale):
    """
    Determines which square of the 14x14 grid was clicked.
    :param scale: (sorry_board.BoardSize) a BoardSize object for the current window.
    :return: (tuple) (x, y) coordinates of click, None if click is outside the 14x14 grid.
    """
    length, xshift, yshift = scale.length, scale.xshift, scale.yshift  # unpack scale
    x, y = pg.mouse.get_pos()  # get click location

    if x < xshift + length or x > xshift + length * 17:  # click is to the left or right of the grid
        return None
    elif y < yshift + length or y > yshift + length * 17:  # click is to the top or bottom of the grid
        return None
    else:  # click is within grid
        coords = ((x - xshift) // length, (y - yshift) // length)  # translate absolute coords to grid coords
        if coords in board.board or coords in draw_pile_coords or coords in discard_pile_coords:  # space exists
            return coords
        else:
            return None


def select_and_move(selected_coords, new_coords, active_card):
    """
    Selects piece if no piece is selected, moves piece if piece is already selected.
    :param selected_coords: (tuple) the (x, y) coordinates of the previously selected piece (None if no piece selected).
    :param new_coords: (tuple) the (x, y) coordinates to select or move to.
    :param active_card: (int or str) the value of the currently active card.
    :return: (tuple) the (x, y) coordinates selected. None if no piece is currently selected.
    """
    if selected_coords:  # there is a previously-selected piece
        new_space = board.board[new_coords]
        piece = board.pieces[selected_coords]

        # The new space is either type NORMAL or is "owned" by the player
        if new_space.space_type == SpaceType.NORMAL or new_space.player == piece.player:
            if new_space.is_occupied:  # The new space is occupied
                if board.pieces[new_coords].player != piece.player:  # The space is occupied by another player
                    if active_card == 11:  # the current card is an 11 so the pieces switch
                        swap_location = piece.location
                        board.pieces[new_coords].move((100, 100))
                        piece.move(new_coords)
                        board.pieces[(100, 100)].move(swap_location)
                        piece.slide()
                    else:  # the card is not an 11 so it's a sorry
                        piece.sorry(new_coords)
                        piece.slide()
                else:  # The space is occupied by the same player
                    piece.deselect()
                    board.pieces[new_coords].select()
                    return new_coords  # select new piece
            else:  # The new space is not occupied
                piece.move(new_coords)
                piece.slide()
        else:  # The player selected a piece in another player's START, SAFETY, or HOME
            piece.deselect()
    else:  # there is not a previously selected piece
        if board.board[new_coords].is_occupied:  # The selected space has a piece
            board.pieces[new_coords].select()  # select new piece
            return new_coords
    return None


def main():
    # PyGame setup
    pg.init()
    pg.display.set_caption("Sorry!")
    logo = pg.image.load("logo.png")
    pg.display.set_icon(logo)
    width, height = pg.display.Info().current_w, pg.display.Info().current_h
    size = min(width, height)
    surf = pg.display.set_mode((int(size / 1.5), int(size / 1.5)), pg.RESIZABLE, pg.SCALED)
    clock = pg.time.Clock()
    width, height = pg.display.Info().current_w, pg.display.Info().current_h
    scale = board.BoardSize(width, height)

    # Sorry game setup
    bg = "grey90"
    selected_location, new_location, n = None, None, None
    host_text, port_text, host_active = "", "", True
    running, online_multiplayer, game_state = True, False, "menu"
    deck, deck_index, card_blink_timer = new_deck, 0, 0

    while running:
        # Menu loop
        if game_state == "menu":
            # Draw menu+buttons and get button Rects
            surf.fill(bg)
            local_button, online_button, host_button, port_button = draw.draw_menu(surf, scale, host_text, port_text)

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    running = False
                elif ev.type == pg.VIDEORESIZE:  # window has been resized
                    width, height = pg.display.Info().current_w, pg.display.Info().current_h  # get new size
                    scale = board.BoardSize(width, height)  # update scale
                elif ev.type == pg.MOUSEBUTTONUP:  # Click
                    click = pg.mouse.get_pos()

                    if local_button.collidepoint(click):  # clicked Play Local
                        online_multiplayer = False
                        shuffle(deck)
                        deck.insert(0, "")
                        game_state = "game"
                    elif online_button.collidepoint(click):  # clicked Play Online
                        # noinspection PyBroadException
                        try:  # attempt to connect to server
                            ip = host_text  # "127.0.0.1"
                            port = int(port_text)  # 65432
                            n = network.Network(ip, port)
                            print(n.connect())
                            s = int(n.send("SEED"))
                            seed(s)
                            shuffle(deck)
                            deck.insert(0, "")
                            online_multiplayer = True
                            game_state = "game"
                        except Exception:  # otherwise, do nothing
                            pass
                    elif host_button.collidepoint(click):
                        host_active = True
                    elif port_button.collidepoint(click):
                        host_active = False

                elif ev.type == pg.KEYDOWN:  # key pressed
                    if ev.key == pg.K_BACKSPACE:  # delete
                        if host_active:
                            host_text = host_text[:-1]
                        else:
                            port_text = port_text[:-1]
                    elif ev.key == pg.K_TAB:  # move to next field
                        host_active = not host_active
                    else:  # add text
                        if host_active:
                            host_text += ev.unicode
                        else:
                            port_text += ev.unicode

        # Main loop
        if game_state == "game":
            surf.fill(bg)  # reset background color

            # Event loop
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    running = False
                elif ev.type == pg.VIDEORESIZE:  # window has been resized
                    width, height = pg.display.Info().current_w, pg.display.Info().current_h  # get new size
                    scale = board.BoardSize(width, height)  # update scale

                elif ev.type == pg.MOUSEBUTTONUP:
                    new_location = determine_space_clicked(scale)
                    if online_multiplayer and new_location and n:
                        n.send("CLICK")
                        n.send(str(new_location[0]) + "," + str(new_location[1]))
                    else:  # local only
                        pg.event.post(pg.event.Event(999, {}))

                elif ev.type == 999:  # Click Event
                    # First, check if the click was on the draw pile
                    if new_location in draw_pile_coords:  # draw pile clicked
                        deck_index += 1  # advance to next card
                        card_blink_timer = 0
                    
                    # Next, check if the click was on the discard pile
                    # or if the deck needs to be reshuffled
                    if deck_index == len(deck) or new_location in discard_pile_coords:
                        del deck[0]  # remove blank
                        shuffle(deck)  # shuffle
                        deck.insert(0, "")  # add black
                        deck_index = 0  # reset index

                    # Finally, check if the click was on the board
                    if new_location in board.board:  # board clicked
                        selected_location = select_and_move(selected_location, new_location, deck[deck_index])

            if online_multiplayer:
                update = n.check_for_update()
                if update:
                    new_location = update
                    pg.event.post(pg.event.Event(999, {}))

            draw.draw_board(surf, scale)
            draw.draw_pieces(surf, scale)
            draw.draw_cards(surf, scale, deck, deck_index)
            if card_blink_timer < 100:
                pg.draw.rect(surf, "white", pg.Rect(10 * scale.length + scale.xshift, 9 * scale.length + scale.yshift,
                                                    scale.length * 2, scale.length * 3))
                card_blink_timer += clock.get_time()

        pg.display.update()  # update display
        clock.tick(30)  # set frame rate
    pg.quit()


if __name__ == "__main__":
    main()
