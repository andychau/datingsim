import datingsim, pygame
from button import BlockButton
from textbox import TextBox
from gurl import Gurl

class MeetScene:

    def __init__(self, gurl, bg_img=None, gurl_img_pos=(300, 300), textPos=(0,400),
                 textSize=(130,180), use_default_buttons=True):
        self.gurl = gurl
        self.bg_img = bg_img
        self.gurl_img_pos = gurl_img_pos
        self.mood = "default"
        self.meet_advisor = MeetAdvisor(gurl)


        self.gurl_textbox = TextBox("filler", textPos, textSize)
        self.all_sprites = pygame.sprite.Group(self.meet_advisor,
                            self.gurl_textbox)

        self.buttons = pygame.sprite.Group()
        prevx, prevy = None, 300
        def make_button(name, on_click, size=(110, 50), color=(140,60,60),
                        dx=20):
            nonlocal prevx
            if prevx == None:
                x = dx
            else:
                x = prevx + dx + size[0]
            y = prevy
            b = BlockButton(on_click, color, pos=(x,y), size=size, text=name)
            prevx = x
            self.buttons.add(b)
            self.all_sprites.add(b)
        self.add_button = make_button
        if use_default_buttons:
            self.add_default_buttons()

        self.done = False;
        self.main_surface = pygame.display.get_surface()

    def add_default_buttons(self):
        b_data = [("talk", self.select_talk), ("ask", self.select_ask), ("date", self.select_date),
                  ("give", self.select_give)]
        for name, on_click in b_data:
            self.add_button(name, on_click)

    def select_talk(self):
        self.update_conversation("select talk filler")
    def select_ask(self):
        self.update_conversation("select ask filler")
    def select_date(self):
        self.update_conversation("select date filler")
    def select_give(self):
        self.change_mood("askance")
        self.update_conversation("select give filler")

    def ath(self):
        for s in self.all_sprites:
            s.kill()

    def get_gurl_img(self):
        #TODO: get img based on mood
        if self.mood in self.gurl.img_dict:
            return self.gurl.img_dict[self.mood]
        elif 'default' in self.gurl.img_dict:
            return self.gurl.img_dict['default']
        else:
            # just return any image
            for img in self.gurl.img_dict.values():
                return img

    def change_mood(self, new_mood):
        if new_mood in self.gurl.img_dict:
            self.mood = new_mood

    def update_conversation(self, text):
        self.gurl_textbox.text = text;
        self.gurl_textbox.render()


    def main_loop(self):

        while not self.done:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.done = True
                    # datingsim.quit()
                    # pygame.quit()
                # implement button fade on mouse hover
                # make this part of button class default??
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.on_click()

            if self.bg_img:
                self.main_surface.blit(self.bg_img, (0, 0))
            else:
                self.main_surface.fill((0, 0, 0))
            self.main_surface.blit(self.get_gurl_img(), self.gurl_img_pos)

            self.all_sprites.update()
            self.all_sprites.draw(self.main_surface)
            pygame.display.flip()
            pygame.time.wait(1000//20)



    @staticmethod
    def test_instantiate():
        pygame.init()
        datingsim.init()
        gurl = Gurl("Rudy", None, None)
        gurl.exp = 2000
        d = MeetScene(gurl)

    @staticmethod
    def test_run_test_buttons():
        pygame.init()
        datingsim.init()
        gurl_imgs = {}
        gurl_imgs['askance'] = datingsim.assets.get_img_safe('GURL_kanaya_askance')
        gurl_imgs['happy'] = datingsim.assets.get_img_safe('GURL_kanaya_smile')
        gurl = Gurl("Kanaya", gurl_imgs, None)
        gurl.exp = 3998
        d = MeetScene(gurl, use_default_buttons=False)
        d.add_button("test button", lambda: print("test 1"))
        def finish():
            d.done = True
        d.add_button("end", finish)
        d.add_button("update conv", lambda: d.update_conversation("changed"))
        def increase_exp():
            d.gurl.exp += 1
        d.add_button("increase exp", increase_exp)
        d.add_button("happy", lambda: d.change_mood("happy"))
        d.add_button("askance", lambda: d.change_mood("askance"))

        d.main_loop()
        d.ath()
        datingsim.quit()
        pygame.quit()

    @staticmethod
    def test_run():
        pygame.init()
        datingsim.init()
        gurl_imgs = {}
        gurl_imgs['askance'] = datingsim.assets.get_img_safe('GURL_kanaya_askance')
        gurl_imgs['happy'] = gurl_imgs['default'] = datingsim.assets.get_img_safe('GURL_kanaya_smile')
        gurl = Gurl("Kanaya", gurl_imgs, None)
        gurl.exp = 3998
        d = MeetScene(gurl)

        d.main_loop()
        d.ath()
        datingsim.quit()
        pygame.quit()


class MeetAdvisor(pygame.sprite.Sprite):
    def __init__(self, gurl, pos=(600, 20), font_color=(200,50,60),
                 font_size=20, font_file=None
                 ):
        pygame.sprite.Sprite.__init__(self)
        self.gurl = gurl
        self.pos = pos
        self.font_color = font_color
        self.font = pygame.font.Font(font_file, font_size)
        self.update()

    def update(self):
        exp = self.gurl.exp
        rel_name = self.gurl.rel_name
        self.text = ("Gurl: {} exp:{} lvl:{}"
                ).format(self.gurl.name, exp, rel_name)
        self.image = self.font.render(self.text, False, self.font_color)
        self.rect = self.image.get_rect().move(self.pos)

    # TODO: center rectangle at bottom of screen?

    @staticmethod
    def test_text():
        pygame.init()
        datingsim.init()
        gurl = Gurl("Rudy", None, None)
        gurl.exp = 2000
        m = MeetAdvisor(gurl)
        print(m.text)

if __name__ == "__main__":
    #MeetAdvisor.test_text()
    #MeetScene.test_instantiate()
    MeetScene.test_run_test_buttons()
    MeetScene.test_run()




