import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.menus = True
        self.states = []
        self.cur = 0
        self.menu_x = (self.game.w / 1.5) - 20
        self.menu_y = (self.game.h / 1.2) - 30
        self.cur_surface = pygame.Rect(0, 0, 20, 20)
        self.back_img = pygame.image.load('res/Images/logo.png')
        self.back_img = pygame.transform.scale(self.back_img, (self.game.w, self.game.h))

    def draw_cursor(self):
        self.game.draw_text('>>', 15, self.cur_surface.x, self.cur_surface.y)

    def move_cursor_up(self):
        if self.cur == 0:
            self.cur = len(self.states) - 1
        else:
            self.cur -= 1
        self.cur_surface.midtop = (self.menu_x - 10, self.menu_y + (20 * self.cur))

    def move_cursor_down(self):
        self.cur = (self.cur + 1) % len(self.states)
        self.cur_surface.midtop = (self.menu_x - 10, self.menu_y + (20 * self.cur))

    def check_choose(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.menus = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.move_cursor_up()
                    return -1
                elif e.key == pygame.K_DOWN:
                    self.move_cursor_down()
                    return -2
                elif e.key == pygame.K_RETURN:
                    return self.cur
                elif e.key == pygame.K_ESCAPE:
                    self.menus = False
                    return -3


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.states.extend(['Single Player', 'Multiplayer', 'Quit'])
        self.xSingle, self.ySingle = self.menu_x, self.menu_y
        self.xMul, self.yMul = self.menu_x, self.menu_y + 20
        self.xQuit, self.yQuit = self.menu_x, self.menu_y + 40
        self.cur_surface.midtop = (self.menu_x - 10, self.menu_y)
        self.choiceMenu = AlgorithmMenu(game)

    def check_choose(self):
        choice = super().check_choose()
        if choice == -1 or choice == -2 or choice == -3 or choice is None:
            return -1
        else:
            self.menus = False
            if choice == 0:
                algo = self.choiceMenu.display_menu()
                if algo == 3:
                    self.menus = True
                    return -1
                elif algo == 1 or algo == 2:
                    self.game.playing = True
                    return algo
            elif choice == 1:
                self.game.playing = True
                return 3
        return -1

    def display_menu(self):
        self.menus = True
        ret = -1
        while self.menus:
            ret = self.check_choose()
            self.game.screen.fill((255, 255, 255))
            self.game.screen.blit(self.back_img, (0, 0))
            self.game.draw_text('Main Menu', 20, self.menu_x, self.menu_y - 30)
            self.game.draw_text(self.states[0], 20, self.xSingle, self.ySingle)
            self.game.draw_text(self.states[1], 20, self.xMul, self.yMul)
            self.game.draw_text(self.states[2], 20, self.xQuit, self.yQuit)
            self.draw_cursor()
            pygame.display.update()
        return ret


class AlgorithmMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.states.extend(['Min-Max', 'Expect-Max', 'Back'])
        self.xMin, self.yMin = self.menu_x, self.menu_y
        self.xExp, self.yExp = self.menu_x, self.menu_y + 20
        self.xBack, self.yBack = self.menu_x, self.menu_y + 40
        self.cur_surface.midtop = (self.menu_x - 10, self.menu_y)

    def check_choose(self):
        choice = super().check_choose()
        if choice == -1 or choice == -2 or choice == -3 or choice is None:
            return -1
        else:
            self.menus = False
            if choice == 0:
                return 1
            elif choice == 1:
                return 2
            else:
                return 3

    def display_menu(self):
        self.menus = True
        ret = -1
        while self.menus:
            ret = self.check_choose()
            self.game.screen.fill((255, 255, 255))
            self.game.screen.blit(self.back_img, (0, 0))
            self.game.draw_text('Choose Algorithm', 20, self.menu_x, self.menu_y - 30)
            self.game.draw_text(self.states[0], 20, self.xMin, self.yMin)
            self.game.draw_text(self.states[1], 20, self.xExp, self.yExp)
            self.game.draw_text(self.states[2], 20, self.xBack, self.yBack)
            self.draw_cursor()
            pygame.display.update()
        return ret
