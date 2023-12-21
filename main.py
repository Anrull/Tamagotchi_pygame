import pygame
import random
import time
import sys

pygame.init()

sys.stdin = open("information_about_player.txt", "r+", encoding="UTF-8")
sys.stdout = open("information_about_player.txt", "r+")

global_flag_of_death = False
count_kill = 0


class MainTamg:
    def __init__(self, health=1000, attack=100):
        self.combat_power = 300
        
        self.health = health
        self.attack = attack
        
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

    def get_info(self):
        dict_info = {
            "CP": self.combat_power,
            "hp": self.health,
            "atc": self.attack
        }
        
        return dict_info
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=500, y=250, speed=7,
                 filename="enemy/ghost_small.png",
                 health=100, attack=10):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        
        self.health = health
        self.attack = attack
    
    def update(self, pos_player, player):
        global global_flag_of_death, count_kill
        
        self.rect.x -= self.speed
        
        if pos_player.colliderect(self.rect):
            player.hp -= self.attack
            self.health -= player.atc
            if player.hp <= 0:
                global_flag_of_death = True
            if self.health <= 0:
                player.CP += 5
                player.update_combat_power()
                count_kill += 1
                self.kill()

        
        if self.rect.x < -10:
            self.kill()
    
    # def die(self):
    #     if self.rect.x < -10:
    #         self.kill()
    #     # pass
    
    # def get_info(self):
    #     dict_info = {"x": self.rect.x, "y": self.rect.y,
    #                  "hp": self.health, "atc": self.attack}
    #     return dict_info


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 40)
global_SM_enemies = 5 # Summoning_multiple_enemies


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        global global_SM_enemies
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            if self.active:
                self.color = COLOR_ACTIVE
            else:
                self.color = COLOR_INACTIVE
                self.text = ""
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    try:
                        global_SM_enemies = int(self.text)
                    except:
                        self.text = "Error"
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
    
    def clear_text(self):
        self.text = ""


class Player(pygame.sprite.Sprite):
    def __init__(self, hp=1000, atc=50, x=30, y=250,
                 speed=7, jump_f=False, jump_count=8,
                 walk_count=0, walk_left=None,
                 walk_right=None, CP=300):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.CP = CP
        self.atc, self.hp = atc, hp
        self.start_atc, self.start_hp = atc, hp
        
        self.walk_left = walk_left
        self.walk_right = walk_right
        self.speed = speed
        
        self.jump_f = jump_f
        self.jump_count = jump_count
        self.start_jump_count = jump_count
        
        self.walk_count = walk_count
        self.walk = walk_right
        
        self.rect = walk_right[0].get_rect(topleft=(x, y))
        self.start_rect = walk_right[0].get_rect(topleft=(x, y))
    
    def run_left(self):
        self.rect.x -= self.speed
        self.walk = self.walk_left
        
        try:
            # screen.blit(walk[walk_count], (player_x, player_y))
            return_list = [self.walk[self.walk_count], self.rect]
            self.walk_count += 1
            return return_list
        except:
            self.walk_count = 0
            return_list = [self.walk[self.walk_count], self.rect]
            return return_list
    
    def run_right(self):
        self.rect.x += self.speed
        self.walk = self.walk_right
        
        try:
            # screen.blit(walk[walk_count], (player_x, player_y))
            return_list = [self.walk[self.walk_count], self.rect]
            self.walk_count += 1
            return return_list
        except:
            self.walk_count = 0
            return_list = [self.walk[self.walk_count], self.rect]
            return return_list

    def no_movement(self):
        return [self.walk[0], self.rect]
    
    def jump(self):
        if self.jump_count >= (-self.start_jump_count):
            if self.jump_count > 0:
                self.rect.y -= (self.jump_count ** 2) / 2
            else:
                self.rect.y += (self.jump_count ** 2) / 2
            self.jump_count -= 1
        else:
            self.jump_f = False
            self.jump_count = self.start_jump_count
            self.rect.y = self.start_rect.y
    
    def update_combat_power(self):
        self.start_atc += 1
        self.start_hp += 3
        self.atc += 1
        self.hp += 3


def main():
    if True: # чисто для того, чтоб скрыть создание переменных. Можно удалить
        x, y = 1280, 720 # размер экрана
        idd = random.randint(0, 1) # случайный выбор фона 
        screen = pygame.display.set_mode((x, y))
        pygame.display.set_caption("Тамагочи")
        
        tamg = MainTamg()
        
        walk_right = tamg.run_right()
        walk_left = tamg.run_left()
        
        player = Player(walk_right=walk_right, walk_left=walk_left, hp=int(input()), atc=int(input()), CP=int(input()))
        player.update_combat_power()

        clock = pygame.time.Clock()

        running = True # пока истина - работает

        background = tamg.small_image_to_alpha(idd) # малый задний фон
        background_full = tamg.full_image_to_alpha(idd) # большой задний фон
        gameover_small = pygame.image.load("gameover\gameover_small_1.png").convert()
        gameover_full = pygame.image.load("gameover\gameover_full_1.jpg").convert
        image = tamg.image_to_alpha("fox/fox_main_lvl1.png") # выбери сам если не нравится
        image = pygame.transform.scale(image, (500, 300)) # отформатирование животного, чтоб влезало

        fullscreen = tamg.image_to_alpha("icons/fullscreen.png")
        fullscreen_rect = fullscreen.get_rect(topleft=(547, 296))

        minimise = tamg.image_to_alpha("icons\minimise.png")
        minimise_rect = minimise.get_rect(topleft=(x - 32, 0))

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
        
        add_some_enemies = label.render("Добавить", False, "green")
        add_some_enemies_rect = add_some_enemies.get_rect(topleft=(446, y - 55))
        
        # input_box_enemies = InputBox(x=446 + 140, y=y - 60, w=10, h=40)
        # input_boxes = [input_box_enemies]
        
        player_rect = walk[0].get_rect(topleft=(player_x, player_y))

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
                info_x = label.render(f"Позиция x: {player.rect.x}", False, "green")
                info_y = label.render(f"Позиция y: {player.rect.y}", False, "green")
                info_speed = label.render(f"Скорость перемещения: {player.speed}", False, "green")
                info_x_rect = info_x.get_rect(topleft=(870, 380))
                info_y_rect = info_y.get_rect(topleft=(870, 420))
                info_speed_rect = info_speed.get_rect(topleft=(870, 460))

                screen.blit(info, info_rect)
                screen.blit(info_x, info_x_rect)
                screen.blit(info_y, info_y_rect)
                screen.blit(info_speed, info_speed_rect)
                """}Information"""
            if not global_flag_of_death:
                if True: # Enemy, Fullscreen, etc
                    """Enemy, Fullscreen, etc{"""
                    info_enemies_count = label.render(f"Врагов: {len(enemies)}", False, "green")
                    info_enemies_count_rect = info_enemies_count.get_rect(topleft=(446, 400))
                    
                    info_enemies_count_kill = label.render(f"Убито: {count_kill}", False, "green")
                    info_enemies_count_kill_rect = info_enemies_count.get_rect(topleft=(446, 440))
                    
                    screen.blit(add_enemy5_button, add_enemy5_button_rect)
                    screen.blit(info_enemies_count, info_enemies_count_rect)
                    screen.blit(info_enemies_count_kill, info_enemies_count_kill_rect)

                    # for box in input_boxes:
                    #     box.update()
                    
                    # for box in input_boxes:
                    #     box.draw(screen)
                    
                    # screen.blit(add_some_enemies, add_some_enemies_rect)
                    if enemies:
                        enemies.draw(screen)
                        # rect_player = pygame.rect(topleft=(player_x, player_y))
                        enemies.update(player_rect, player)
                    
                    pygame.draw.rect(screen, "white", (539, 288, 32, 32))
                    screen.blit(fullscreen, fullscreen_rect)
                    """}Enemy, Fullscreen, etc"""
                
                if True: # Перемещение персонажа
                    """Перемещение персонажа{"""
                    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.rect.x > 30:
                        run_lf = player.run_left()
                        screen.blit(run_lf[0], run_lf[1])
                    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.rect.x < 400:
                        run_rght = player.run_right()
                        screen.blit(run_rght[0], run_rght[1])
                    else:
                        # screen.blit(walk[0], (player_x, player_y))
                        no_move = player.no_movement()
                        screen.blit(no_move[0], no_move[1])
                    
                    player_rect = player.rect
                    """}Перемещение пероснажа"""
                
                if True: # Прыжок
                    """Прыжок{"""
                    if not player.jump_f:
                        if keys[pygame.K_SPACE]:
                            player.jump_f = True
                    else:
                        player.jump()
                    """}Прыжок"""
            else:
                screen.blit(gameover_small, (0, 0))
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
                print(player.start_hp)
                print(player.start_atc)
                print(player.CP)
                running = False
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
                if add_some_enemies_rect.collidepoint(pos_mouse):
                    pos_x = 500
                    for i in range(global_SM_enemies):
                        enemies.add(Enemy(pos_x, y=250))
                        pos_x -= 50
            if event.type == timer_button_enemy_5:
                if full:
                    for i in range(5):
                        pos_x = x + 500
                        for i in range(count_enemies):
                            enemies_full.add(Enemy(x = pos_x, y = y - 200, filename="enemy/ghost_full.png"))
                            pos_x -= 200
            # for box in input_boxes:
            #     box.handle_event(event)
        pygame.display.update()

        clock.tick(15)
    
    pygame.quit()


if __name__ == "__main__":
    main()