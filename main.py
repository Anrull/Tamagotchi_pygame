import pygame
import random
import time

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
FONT = pygame.font.Font(None, 40)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, 5, 5)
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


def main():
    if True: # чисто для того, чтоб скрыть создание переменных. Можно удалить
        x, y = 1280, 720 # размер экрана
        idd = random.randint(0, 1) # случайный выбор фона 
        screen = pygame.display.set_mode((x, y))
        pygame.display.set_caption("Тамагочи")

        clock = pygame.time.Clock()

        tamg = MainTamg(x, y)

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
        info = label.render("Information", False, "green")
        info_rect = info.get_rect(topleft=(870, 340))
        
        add_enemy5_button = label.render("Добавить 5 врагов", False, "green")
        add_enemy5_button_rect = add_enemy5_button.get_rect(topleft=(446, 360))

        timer_button_enemy_5 = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_button_enemy_5, 10000)

        full = False

        enemies = pygame.sprite.Group()
        count_enemies = 5
        
        enemies_full = pygame.sprite.Group()
        
        input_box_enemies = InputBox(x=446, y=390, w=10, h=40)
        input_boxes = [input_box_enemies]

    while running:
        keys = pygame.key.get_pressed()
        
        if not full: # Если экран начальный
            if True: # Отрисовка интерфейса
                screen.fill((255, 255, 255))
                screen.blit(background, (0, 0))
                screen.blit(image, (x // 2, 0))
                
                pygame.draw.line(screen, "black", (571, 317), (x, 317), 3)
                pygame.draw.line(screen, "black", (426, 320), (426, y), 2)
                pygame.draw.line(screen, "black", (853, 320), (853, y), 2)
                
            if True: # Infromation # Нужно для того, чтоб скрыть и упростить навигацию
                """Information{"""
                info_x = label.render(f"Позиция x: {player_x}", False, "green")
                info_y = label.render(f"Позиция y: {player_y}", False, "green")
                info_speed = label.render(f"Скорость перемещения: {player_speed}", False, "green")
                info_x_rect = info_x.get_rect(topleft=(870, 380))
                info_y_rect = info_y.get_rect(topleft=(870, 420))
                info_speed_rect = info_speed.get_rect(topleft=(870, 460))

                screen.blit(info, info_rect)
                screen.blit(info_x, info_x_rect)
                screen.blit(info_y, info_y_rect)
                screen.blit(info_speed, info_speed_rect)
                """}Information"""
            
            if True: # Enemy, Fullscreen, etc
                """Enemy, Fullscreen, etc{"""
                screen.blit(add_enemy5_button, add_enemy5_button_rect)

                for box in input_boxes:
                    box.update()
                
                for box in input_boxes:
                    box.draw(screen)
                
                if enemies:
                    enemies.draw(screen)
                    enemies.update()
                
                pygame.draw.rect(screen, "white", (539, 288, 32, 32))
                screen.blit(fullscreen, fullscreen_rect)
                """}Enemy, Fullscreen, etc"""
            
            if True: # Перемещение персонажа
                """Перемещение персонажа{"""
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
                """}Перемещение пероснажа"""
            
            if True: # Прыжок
                """Прыжок{"""
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
                """}Прыжок"""
        else: # для full screen
            screen.blit(background_full, (0, 0)) # НЕ ТРОГАТЬ
            
            if True: # Передвижение персонажа
                """Передвижение персонажа{"""
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
                """}Передвижение персонажа"""
            
            if True: # прыжок
                """Прыжок персонажа{"""
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
                """}Прыжок персонажа"""
            
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
        
            if enemies_full: # Enemies
                enemies_full.draw(screen)
                enemies_full.update()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if not full:
                    if event.key == pygame.K_f:
                        full = True

                        player_x, player_y = 150, y - 150
                        jump_count = 10
                        player_speed *= 2

                        walk_right = tamg.run_right(True)
                        walk_left = tamg.run_left(True)
                        walk = walk_right[:]
                else:
                    if event.key == pygame.K_f or event.key == pygame.K_ESCAPE:
                        full = False
                        
                        player_x, player_y = tamg.start_coords()
                        player_speed //= 2
                        
                        walk_right = tamg.run_right()
                        walk_left = tamg.run_left()
                        walk = walk_right[:]
                        
                        jump_count = 8
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if fullscreen_rect.collidepoint(pos_mouse):
                    """Вывод изображения на фулл экран"""                    
                    full = True

                    player_x, player_y = 150, y - 150
                    jump_count = 10
                    player_speed *= 2

                    walk_right = tamg.run_right(True)
                    walk_left = tamg.run_left(True)
                    walk = walk_right[:]
                if add_enemy5_button_rect.collidepoint(pos_mouse):
                    pos_x = 500
                    for i in range(count_enemies):
                        enemies.add(Enemy(pos_x, y=250))
                        pos_x -= 50
            if event.type == timer_button_enemy_5:
                if full:
                    for i in range(5):
                        pos_x = x + 500
                        for i in range(count_enemies):
                            enemies_full.add(Enemy(x = pos_x, y = y - 200, filename="enemy/ghost_full.png"))
                            pos_x -= 200
            for box in input_boxes:
                box.handle_event(event)
        pygame.display.update()

        clock.tick(15)


if __name__ == "__main__":
    main()
    
# def main():
#     clock = pg.time.Clock()
#     input_box1 = InputBox(100, 100, 140, 32)
#     input_box2 = InputBox(100, 300, 140, 32)
#     input_boxes = [input_box1, input_box2]
#     done = False

#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             for box in input_boxes:
#                 box.handle_event(event)

#         for box in input_boxes:
#             box.update()

#         screen.fill((30, 30, 30))
#         for box in input_boxes:
#             box.draw(screen)

#         pg.display.flip()
#         clock.tick(30)