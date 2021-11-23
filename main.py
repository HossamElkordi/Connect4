from game import Game


def main():
    game = Game()
    work = game.current_menu.display_menu()
    if work != -1:
        game.game_loop(work)


if __name__ == '__main__':
    main()
