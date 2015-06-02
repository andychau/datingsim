import pygame
import pygame.gfxdraw
import random
import datingsim

class Dream():
    def update(self):
        pass
    def draw(self, surf):
        pass

class DreamMap():
    def __init__(self):
        self.next_id = 1
        self.button_map = {}
        self.ghost_surf = None

    def get_at(self, pos):
        D = self
        id = D.ghost_surf.get_at(pos)[0]
        if id in D.button_map:
            return D.button_map[id]
        else:
            return None

    def reset(self):
        D = self
        D.ghost_surf = None
        D.next_id = 1
        D.buttons_map = {}

    def add_dreambutton(self, button):
        if not self.ghost_surf:
            W, H = datingsim.RESOLUTION
            self.ghost_surf = pygame.Surface([W, H])
        id = self.next_id
        self.button_map[id] = button
        self.next_id += 1
        id_color = (id, 0, 0)
        button.draw(self.ghost_surf, color=id_color)

class DreamButton(Dream):
    next_id = 1
    ghost_surf = None

    def __init__(self, draw_fn, on_click=lambda:None, on_hover=lambda:None):
        """draw_fn takes arguments (surf, color=None)"""
        if not DreamButton.ghost_surf:
            W, H = datingsim.RESOLUTION
            DreamButton.ghost_surf = pygame.Surface([W, H])
        self.draw = draw_fn
        self.on_click = on_click
        self.on_hover = on_hover


class EllipseButton(DreamButton):
    def __init__(self, pos, size, on_click=None, color=(123, 23, 127)):
        def draw_this(surf, color=color):
            x, y = [int(i) for i in pos]
            w, h = [int(i) for i in size]
            pygame.gfxdraw.filled_ellipse(surf, x, y, w, h, color)
        DreamButton.__init__(self, draw_this, on_click)

    @staticmethod
    def test():
        global GAME_WIDTH, GAME_HEIGHT, GAME_SIZE
        GAME_WIDTH, GAME_HEIGHT = GAME_SIZE = [800, 600]
        pygame.init()
        pygame.display.set_caption("DreamButton")
        global screen
        screen = pygame.display.set_mode(GAME_SIZE)

        # populate screen with ellipses
        dreams = []
        dream_map = DreamMap()
        for _ in range(1):
            pos = random.uniform(0, GAME_WIDTH), random.uniform(0, GAME_HEIGHT)
            size = 20, 40
            color = (255, 20, 20)
            on_click = lambda: print("id")
            ellipse = EllipseButton(pos, size, on_click, color)
            dreams.append(ellipse)
            dream_map.add_dreambutton(ellipse)

            ellipse.on_hover = lambda: print("heheheh found YOU")


        done = False
        while not done:
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    done = True
                elif e.type is pygame.MOUSEBUTTONDOWN:
                    dreambutton = dream_map.get_at(e.pos)
                    if dreambutton:
                        dreambutton.on_click()
                elif e.type is pygame.MOUSEMOTION:
                    dreambutton = dream_map.get_at(e.pos)
                    if dreambutton:
                        dreambutton.on_hover()
            for dream in dreams:
                dream.update()
                dream.draw(screen)
            pygame.display.flip()
            pygame.time.wait(1000//20)
        pygame.quit()

if __name__ == '__main__':
    EllipseButton.test()


