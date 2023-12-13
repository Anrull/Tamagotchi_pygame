import pygame
import random
import time
import pygame_gui # убейте методистов, максимально неудобная подача материала по pygame

pygame.init()


class MainTamg:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.combat_power = 300
        
    def image_to_alpha(self, path):
        """For format png"""
        image = pygame.image.load(path).convert_alpha()
        return image
    
    def run_right(self, size=False):
        """Получение списка движения вправо"""
        walk = [
            pygame.image.load("fox/fox_right/fox_right_1.png").convert_alpha(),
            pygame.image.load("fox/fox_right/fox_right_2.png").convert_alpha(),
            pygame.image.load("fox/fox_right/fox_right_3.png").convert_alpha()
        ]
        
        walk_full = [
            pygame.image.load("fox/fox_right/fox_right_1_full.png"),
            pygame.image.load("fox/fox_right/fox_right_2_full.png"),
            pygame.image.load("fox/fox_right/fox_right_3_full.png")
        ]
        return walk if not size else walk_full
    
    def run_left(self, size=False):
        """Получение списка движения влево"""
        walk = [
            pygame.image.load("fox/fox_left/fox_left_1.png").convert_alpha(),
            pygame.image.load("fox/fox_left/fox_left_2.png").convert_alpha(),
            pygame.image.load("fox/fox_left/fox_left_3.png").convert_alpha()
        ]
        
        walk_full = [
            pygame.image.load("fox/fox_left/fox_left_1_full.png"),
            pygame.image.load("fox/fox_left/fox_left_2_full.png"),
            pygame.image.load("fox/fox_left/fox_left_3_full.png")
        ]
        return walk if not size else walk_full

    def start_coords(self):
        """Стартовые координаты питомца"""
        return (30, 250)

    def add_CP(self):
        """Добавление Боевой Мощи"""
        self.combat_power += 10
    
    def min_CP(self):
        """Вычитание БМ"""
        self.combat_power -= 10
    
    def show_CP(self):
        """Получение БМ"""
        return self.combat_power
    
    def small_image_to_alpha(self, idd):
        """For format png"""
        images = [
            pygame.image.load("background/background_2_small.png").convert_alpha(),
            pygame.image.load("background/background_3_small.png").convert_alpha()
            ]
        return images[idd]
    
    def full_image_to_alpha(self, idd):
        """For format png"""
        images = [
            pygame.image.load("background/background_2_full.png").convert_alpha(),
            pygame.image.load("background/background_3_full.png").convert_alpha()
            ]
        return images[idd]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=500, y=250, speed=7, filename="enemy/ghost_small.png"):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
    
    def update(self):
        self.rect.x -= self.speed
    
    def check(self):
        return self.rect.x < -10


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


# def draw_enemy(screen, enemy, size=False, speed=7):
#     if not size:
#         screen.blit(enemy.image, enemy.rect)
        
#         enemy.rect.x -= speed

def main():
    x, y = 1280, 720 # размер экрана
    idd = random.randint(0, 1) # случайный выбор фона 
    screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Тамагочи")

    clock = pygame.time.Clock()

    tamg = MainTamg(x, y)
    
    manager_gui = pygame_gui.UIManager((x, y))

    running = True # пока истина - работает

    background = tamg.small_image_to_alpha(idd) # малый задний фон
    background_full = tamg.full_image_to_alpha(idd) # большой задний фон
    image = tamg.image_to_alpha("fox/fox_main_lvl1.png") # выбери сам если не нравится
    image = pygame.transform.scale(image, (500, 300)) # отформатирование животного, чтоб влезало

    fullscreen = tamg.image_to_alpha("icons/fullscreen.png")
    fullscreen_rect = fullscreen.get_rect(topleft=(547, 296))

    minimise = tamg.image_to_alpha("icons\minimise.png")
    minimise_rect = minimise.get_rect(topleft=(x - 32, 0))

    walk_right = tamg.run_right()
    walk_left = tamg.run_left()

    walk_count = 0

    player_x, player_y = tamg.start_coords()
    player_speed = 7

    jump_f = False
    jump_count = 8

    walk = walk_right[:]

    label = pygame.font.Font(size=40)
    # info = label.render("Information", False, "green")
    # info_rect = info.get_rect(topleft=(870, 340))
    
    info_gui = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((870, 340), (100, 50)),
        text='Information',
        manager=manager_gui
        )
    
    count_enemies_gui = pygame_gui.elements.UIDropDownMenu(
        options_list=["1", "5", "10", "15"], starting_option="5",
        relative_rect=pygame.Rect((556, 360), (50, 20)),
        manager=manager_gui
    )

    # add_enemy5_button = label.render("Добавить 5 врагов", False, "green")
    # add_enemy5_button_rect = add_enemy5_button.get_rect(topleft=(446, 360))
    
    add_enemy5_gui = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((446, 360), (100, 20)),
        text="Add 5 enemies",
        manager=manager_gui 
    )

    timer_button_enemy_5 = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_button_enemy_5, 0)

    full = False

    enemies = pygame.sprite.Group()
    count_enemies = 0
    # enemies = []

    while running:
        if not full:
            time_delta = clock.tick(60) / 1000.0
            # manager_gui.process_events(event)
            # manager_gui.update(time_delta)
            # manager_gui.draw_ui(screen)
            
            keys = pygame.key.get_pressed()
            
            screen.fill((255, 255, 255))
            screen.blit(background, (0, 0))
            screen.blit(image, (x // 2, 0))
            
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_x > 30:
                player_x -= player_speed
                walk = walk_left
                try:
                    screen.blit(walk[walk_count], (player_x, player_y))
                    walk_count += 1
                except:
                    walk_count = 0
                    screen.blit(walk[walk_count], (player_x, player_y))
            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_x < 400:
                player_x += player_speed
                walk = walk_right
                try:
                    screen.blit(walk[walk_count], (player_x, player_y))
                    walk_count += 1
                except:
                    walk_count = 0
                    screen.blit(walk[walk_count], (player_x, player_y))
            else:
                screen.blit(walk[0], (player_x, player_y))
            
            if not jump_f:
                if keys[pygame.K_SPACE]:
                    jump_f = True
            else:
                if jump_count >= -8:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 1
                else:
                    jump_f = False
                    jump_count = 8
            
            pygame.draw.rect(screen, "white", (539, 288, 32, 32))
            screen.blit(fullscreen, fullscreen_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            # if event.type == pygame.KEYDOWN:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if not full:
                    if event.ui_element == add_enemy5_gui:
                        pos_x = 500
                        for i in range(5):
                            enemies.add(Enemy(pos_x, y=250))
                            pos_x -= 50
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == count_enemies_gui:
                    # count_enemies = event.text
                    print(1)
                    
        
        if not full:
            # time_delta = clock.tick(60) / 1000.0
            manager_gui.process_events(event)
            manager_gui.update(time_delta)
            manager_gui.draw_ui(screen)
            
            # screen.fill((255, 255, 255)) # (65, 138, 65) / (92, 163, 92) / (54, 92, 54) / выбери сам / (52, 64, 52)
            # screen.blit(background, (0, 0)) # НЕ ТРОГАТЬ
            # screen.blit(image, (x // 2, 0))
            # draw_enemy(screen, enemy)

            keys = pygame.key.get_pressed()

            if enemies:
                # for el in enemies:
                #     el.update()
                #     # flag = el.check()
                #     # if not flag:
                #     #     enemies[0]
                enemies.draw(screen)
                enemies.update()


            # НЕ ТРОГАТЬ
            # движение по оси x влево и вправо
            # if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_x > 30:
            #     player_x -= player_speed
            #     walk = walk_left
            #     try:
            #         screen.blit(walk[walk_count], (player_x, player_y))
            #         walk_count += 1
            #     except:
            #         walk_count = 0
            #         screen.blit(walk[walk_count], (player_x, player_y))
            # elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_x < 400:
            #     player_x += player_speed
            #     walk = walk_right
            #     try:
            #         screen.blit(walk[walk_count], (player_x, player_y))
            #         walk_count += 1
            #     except:
            #         walk_count = 0
            #         screen.blit(walk[walk_count], (player_x, player_y))
            # else:
            #     screen.blit(walk[0], (player_x, player_y))

            # НЕ ТРОГАТЬ 
            # прыжок
            # if not jump_f:
            #     if keys[pygame.K_SPACE]:
            #         jump_f = True
            # else:
            #     if jump_count >= -8:
            #         if jump_count > 0:
            #             player_y -= (jump_count ** 2) / 2
            #         else:
            #             player_y += (jump_count ** 2) / 2
            #         jump_count -= 1
            #     else:
            #         jump_f = False
            #         jump_count = 8

            """Information"""
            # pygame.draw.line(screen, "black", (571, 317), (x, 317), 3)
            # pygame.draw.line(screen, "black", (426, 320), (426, y), 2)
            # pygame.draw.line(screen, "black", (853, 320), (853, y), 2)

            # info_x = label.render(f"Позиция x: {player_x}", False, "green")
            # info_y = label.render(f"Позиция y: {player_y}", False, "green")
            # info_speed = label.render(f"Скорость перемещения: {player_speed}", False, "green")
            # info_x_rect = info_x.get_rect(topleft=(870, 380))
            # info_y_rect = info_y.get_rect(topleft=(870, 420))
            # info_speed_rect = info_speed.get_rect(topleft=(870, 460))

            # # screen.blit(info_gui, info_rect)
            # screen.blit(info_x, info_x_rect)
            # screen.blit(info_y, info_y_rect)
            # screen.blit(info_speed, info_speed_rect)
            """Information finish"""


            """Fullscreen, Enemy, etc"""
            pygame.draw.rect(screen, "white", (539, 288, 32, 32))
            screen.blit(fullscreen, fullscreen_rect)
            # screen.blit(add_enemy5_button, add_enemy5_button_rect)

            mouse = pygame.mouse.get_pos()

            if (fullscreen_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]) or keys[pygame.K_f]:
                """Вывод изображения на фулл экран"""
                time.sleep(0.05)
                
                full = True

                player_x, player_y = 150, y - 150
                jump_count = 10
                player_speed *= 2

                walk_right = tamg.run_right(True)
                walk_left = tamg.run_left(True)
                walk = walk_right[:]
            
            # if (add_enemy5_button_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]):
            #     time.sleep(0.2) # необходимо для того, чтоб не вызывалось сразу несколько врагов.
            #                     # знаешь как исправить - сделай по другому
            #     pos_x = 500
            #     for i in range(5):
            #         enemies.add(Enemy(pos_x, y=250))
            #         pos_x -= 50
            """Fullscreen, Enemy, etc finish"""
        else:
            screen.blit(background_full, (0, 0)) # НЕ ТРОГАТЬ
            
            keys = pygame.key.get_pressed()
            
            # НЕ ТРОГАТЬ
            # движение по оси x влево и вправо
            if keys[pygame.K_a] or keys[pygame.K_LEFT] and player_x > 30:
                player_x -= player_speed
                walk = walk_left
                try:
                    screen.blit(walk[walk_count], (player_x, player_y))
                    walk_count += 1
                except:
                    walk_count = 0
                    screen.blit(walk[walk_count], (player_x, player_y))
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT] and player_x < (x - 50):
                player_x += player_speed
                walk = walk_right
                try:
                    screen.blit(walk[walk_count], (player_x, player_y))
                    walk_count += 1
                except:
                    walk_count = 0
                    screen.blit(walk[walk_count], (player_x, player_y))
            else:
                screen.blit(walk[0], (player_x, player_y))
            
            # НЕ ТРОГАТЬ 
            # прыжок
            if not jump_f:
                if keys[pygame.K_SPACE]:
                    jump_f = True
            else:
                if jump_count >= -10:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 1
                else:
                    jump_f = False
                    jump_count = 10
            
            pygame.draw.rect(screen, "white", (x - 32, 0, 32, 32))
            screen.blit(minimise, minimise_rect)
            
            mouse = pygame.mouse.get_pos()
            
            if keys[pygame.K_ESCAPE] or keys[pygame.K_f] or (minimise_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]):
                time.sleep(0.05)
                full = False
                
                player_x, player_y = tamg.start_coords()
                player_speed //= 2
                
                walk_right = tamg.run_right()
                walk_left = tamg.run_left()
                walk = walk_right[:]
                
                jump_count = 8


        pygame.display.update()


        clock.tick(15)


if __name__ == "__main__":
    main()