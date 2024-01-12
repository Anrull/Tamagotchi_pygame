import pygame
import random
import time
import sys
import math

pygame.init()

sys.stdin = open("information_about_player.txt", "r+", encoding="UTF-8")
sys.stdout = open("information_about_player.txt", "r+")

global_flag_of_death = False
screen_rect = (0, 0, 571, 321)
global_SM_enemies = 5  # Summoning_multiple_enemies
x, y = 1280, 720  # размер экрана

sprites_attack_fire_1 = pygame.sprite.Group()

images_hp_paths = ["health/hp_0.png",
                   "health/hp_1.png",
                   "health/hp_2.png",
                   "health/hp_3.png",
                   "health/hp_4.png",
                   "health/hp_5.png"]


def images_hp():
    return [pygame.image.load(i).convert_alpha() for i in images_hp_paths]


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
                 health=100, attack=100):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

        self.health = health
        self.attack = attack

    def update(self, pos_player=None, player=None, take_hp=None, other_rect=None, other=None, die=None):
        global global_flag_of_death

        if take_hp != None:
            if self.rect.colliderect(other_rect):
                self.health -= take_hp
                other.kill()

        if pos_player != None:
            if pos_player.colliderect(self.rect):
                player.hp -= self.attack
                self.health -= player.atc
                if player.hp <= 0:
                    global_flag_of_death = True
                    player.status = "death"
            self.rect.x -= self.speed
            if self.rect.x < -10:
                self.kill()

        if die != None:
            self.kill()

        if self.health <= 0:
            player.update_CP_EXP_etc()
            player.update_combat_power()
            self.kill()


class Show_HP_EXP(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = images_hp()

    def update(self, screen, player):
        procent_HP = int((player.hp / player.start_hp) * 100)
        image_hp = None

        if 100 <= procent_HP and procent_HP > 80:
            image_hp = self.images[5]
        elif 80 <= procent_HP and procent_HP > 60:
            image_hp = self.images[4]
        elif 60 <= procent_HP and procent_HP > 40:
            image_hp = self.images[3]
        elif 40 <= procent_HP and procent_HP > 20:
            image_hp = self.images[2]
        elif 20 <= procent_HP and procent_HP > 0:
            image_hp = self.images[1]
        elif procent_HP <= 0:
            image_hp = self.images[0]
        if image_hp:
            screen.blit(image_hp, (0, 0))

        len_exp = player.exp / player.exp_new_lvl

        # если на одном уровне с hp
        # pygame.draw.rect(screen, (105, 105, 105), (300, 2, 269, 50))
        # pygame.draw.rect(screen, "green", (300, 2, 269 * len_exp, 50))

        # под hp
        pygame.draw.rect(screen, (105, 105, 105), (2, 57, 288, 10))
        pygame.draw.rect(screen, "green", (2, 57, 288 * len_exp, 10))


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.image.load("attack/fire/fireattack_16_1.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(sprites_attack_fire_1)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.5

    def update(self, player, enemies):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if enemies:
            enemies.update(take_hp=player.atc, player=player, other_rect=self.rect, other=self)
        if not self.rect.colliderect(screen_rect):
            self.kill()


class Equipment(pygame.sprite.Sprite):
    def __init__(self, sword_name="Меч", armor_name="Доспех",
                 helmet_name="Шлем", boots_name="Сапоги",
                 path_sword="equipment/sword.png", path_armor="equipment/armor.png",
                 path_helmet="equipment/helmet.png", path_boots="equipment/boots.png",
                 sword_atc=50, helmet_hp=100, armor_hp=100, boots_speed=1, show_flag=False):
        pygame.sprite.Sprite.__init__(self)

        self.name_sword = sword_name
        self.sword_atc = sword_atc
        self.image_sword = pygame.image.load(path_sword).convert_alpha()

        self.name_armor = armor_name
        self.armor_hp = armor_hp
        self.image_armor = pygame.image.load(path_armor).convert_alpha()

        self.name_helmet = helmet_name
        self.helmet_hp = helmet_hp
        self.image_helmet = pygame.image.load(path_helmet).convert_alpha()

        self.name_boots = boots_name
        self.boots_speed = boots_speed
        self.image_boots = pygame.image.load(path_boots).convert_alpha()

        self.show_flag = show_flag

    def update_armor(self, screen):
        pass

    def update_helmet(self, screen):
        pass

    def update_boots(self, screen):
        pass

    def update_sword(self, screen):
        pass

    def show(self, screen):
        screen.blit(self.image_helmet, (0, 0))
        screen.blit(self.image_armor, (0, 64))
        screen.blit(self.image_boots, (0, 128))
        screen.blit(self.image_sword, (0, 192))


class Player(pygame.sprite.Sprite):
    def __init__(self, hp=1000, atc=50, x=30, y=250,
                 speed=7, jump_f=False, jump_count=8,
                 walk_count=0, walk_left=None,
                 walk_right=None, CP=300,
                 count_kill=0, status="Alive", lvl=1, exp=0,
                 location=0, CP_location=0, special_kill=0):

        pygame.sprite.Sprite.__init__(self)

        self.CP = CP
        self.atc, self.hp = atc, hp
        self.start_atc, self.start_hp = atc, hp
        self.count_kill = count_kill
        self.status = status

        self.location = location
        self.CP_location = CP_location

        # self.exp_new_lvl = 10000 * (1.1)**lvl
        self.exp_new_lvl = int(5000 * 2 * lvl)
        self.exp = exp
        self.lvl = lvl

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

        if self.exp >= self.exp_new_lvl and self.lvl != 99:
            self.exp_new_lvl = int(5000 * 2 * self.lvl)
            self.lvl += 1
            self.exp = 0

        if self.CP_location >= 10000 and not self.location:
            self.location = 1
            self.CP_location = 0
    
    def update_CP_EXP_etc(self):
        self.CP += 5
        self.CP_location += 5
        self.exp += 10
        self.count_kill += 1


class Information:
    def __init__(self, label):
        self.label = label
        self.info = label.render("Information", False, "green")
        self.info_rect = self.info.get_rect(topleft=(870, 340))

    def update_interface(self, screen, background, image, x, y):
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(image, (x // 2, 0))

        pygame.draw.line(screen, "black", (571, 317), (x, 317), 3)
        pygame.draw.line(screen, "black", (426, 320), (426, y), 2)
        pygame.draw.line(screen, "black", (853, 320), (853, y), 2)

    def update_information(self, screen, player, equipment_button, equipment_button_rect, enemies):
        info_x = self.label.render(f"Позиция x: {player.rect.x}", False, "green")
        info_y = self.label.render(f"Позиция y: {player.rect.y}", False, "green")
        info_speed = self.label.render(f"Скорость перемещения: {player.speed}", False, "green")
        info_x_rect = info_x.get_rect(topleft=(870, 380))
        info_y_rect = info_y.get_rect(topleft=(870, 420))
        info_speed_rect = info_speed.get_rect(topleft=(870, 460))

        info_player_CP = self.label.render(f"БМ: {player.CP}", False, "green")
        info_attack = self.label.render(f"ATC: {player.atc}", False, "green")
        info_HP = self.label.render(f"HP: {player.hp}", False, "green")
        info_status = self.label.render(f"Status: {player.status}", False, "green")
        info_exp = self.label.render(f"EXP: {player.exp} / {player.exp_new_lvl}", False, "green")
        info_lvl = self.label.render(f"Lvl: {player.lvl}", False, "green")

        info_attack_rect = info_attack.get_rect(topleft=(10, 380))
        info_player_CP_rect = info_player_CP.get_rect(topleft=(10, 340))
        info_HP_rect = info_HP.get_rect(topleft=(10, 420))
        info_status_rect = info_status.get_rect(topleft=(10, 460))
        info_exp_rect = info_exp.get_rect(topleft=(10, 500))
        info_lvl_rect = info_lvl.get_rect(topleft=(10, 540))

        screen.blit(self.info, self.info_rect)
        screen.blit(info_x, info_x_rect)
        screen.blit(info_y, info_y_rect)
        screen.blit(info_speed, info_speed_rect)

        screen.blit(info_player_CP, info_player_CP_rect)
        screen.blit(info_attack, info_attack_rect)
        screen.blit(info_HP, info_HP_rect)
        screen.blit(info_status, info_status_rect)
        screen.blit(info_exp, info_exp_rect)
        screen.blit(info_lvl, info_lvl_rect)

        info_enemies_count = self.label.render(f"Врагов: {len(enemies)}", False, "green")
        info_enemies_count_rect = info_enemies_count.get_rect(topleft=(446, 380))

        info_enemies_count_kill = self.label.render(f"Убито: {player.count_kill}", False, "green")
        info_enemies_count_kill_rect = info_enemies_count.get_rect(topleft=(446, 420))

        screen.blit(info_enemies_count, info_enemies_count_rect)
        screen.blit(info_enemies_count_kill, info_enemies_count_kill_rect)

        screen.blit(equipment_button, equipment_button_rect)

    def some(self):
        pass


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 6
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def main():
    global global_flag_of_death

    if True:  # чисто для того, чтоб скрыть создание переменных. Можно удалить
        idd = random.randint(0, 1)  # случайный выбор фона
        screen = pygame.display.set_mode((x, y))
        pygame.display.set_caption("Тамагочи")

        tamg = MainTamg()

        player = Player(exp=int(input()), lvl=int(input()), walk_right=tamg.run_right(),
                        walk_left=tamg.run_left(), count_kill=int(input()),
                        hp=int(input()), atc=int(input()), CP=int(input()),
                        CP_location=int(input()), location=int(input()))
        player.update_combat_power()

        show_hp = Show_HP_EXP()
        equipment = Equipment()

        clock = pygame.time.Clock()

        running = True  # пока истина - работает

        background = tamg.small_image_to_alpha(idd)  # малый задний фон
        background_full = tamg.full_image_to_alpha(idd)  # большой задний фон
        gameover_small = pygame.image.load("gameover/gameover_small_1.png").convert()
        gameover_full = pygame.image.load("gameover/gameover_full_1.jpg").convert()

        background_event_small = pygame.transform.scale(pygame.image.load("background/special_level.jpg").convert(),
                                                        (571, 321))
        background_event_full = pygame.image.load("background/special_level.jpg")

        image = tamg.image_to_alpha("fox/fox_main_lvl1.png")  # выбери сам если не нравится
        image = pygame.transform.scale(image, (500, 300))  # отформатирование животного, чтоб влезало

        fullscreen = tamg.image_to_alpha("icons/fullscreen.png")
        fullscreen_rect = fullscreen.get_rect(topleft=(547, 296))

        minimise = tamg.image_to_alpha("icons/minimise.png")
        minimise_rect = minimise.get_rect(topleft=(x - 32, 0))

        label = pygame.font.Font(size=40)

        information = Information(label)

        add_enemy5_button = label.render("Добавить 5 врагов", False, "green")
        add_enemy5_button_rect = add_enemy5_button.get_rect(topleft=(446, 340))

        restart_button = label.render("Restart", False, "green")
        restart_button_rect = restart_button.get_rect(topleft=(440, 280))

        equipment_button = label.render("Снаряжение", False, "green")
        equipment_button_rect = equipment_button.get_rect(topleft=(446, 460))

        timer_button_enemy_5 = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_button_enemy_5, 1)

        full = False

        enemies = pygame.sprite.Group()
        enemies_special = pygame.sprite.Group()

        enemies_full = pygame.sprite.Group()

        # input_box_enemies = InputBox(x=446 + 140, y=y - 60, w=10, h=40)
        # input_boxes = [input_box_enemies]

    while running:
        keys = pygame.key.get_pressed()

        if not full:  # Если экран начальный
            information.update_interface(screen, background, image, x, y)  # Отрисовка интерфейса

            # Information
            information.update_information(screen, player, equipment_button, equipment_button_rect, enemies)

            if not global_flag_of_death:
                if not player.location:
                    if True:  # Enemy, Fullscreen, etc
                        """Enemy, Fullscreen, etc{"""
                        screen.blit(add_enemy5_button, add_enemy5_button_rect)

                        if enemies:
                            enemies.draw(screen)
                            enemies.update(player.rect, player)

                        pygame.draw.rect(screen, "white", (539, 288, 32, 32))
                        screen.blit(fullscreen, fullscreen_rect)

                        sprites_attack_fire_1.update(player, enemies)  # отрисовка первой атаки
                        sprites_attack_fire_1.draw(screen)

                        show_hp.update(screen, player)
                        """}Enemy, Fullscreen, etc"""

                    if True:  # Перемещение персонажа
                        """Перемещение персонажа{"""
                        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.rect.x > 30:
                            run_lf = player.run_left()
                            screen.blit(run_lf[0], run_lf[1])
                        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.rect.x < 400:
                            run_rght = player.run_right()
                            screen.blit(run_rght[0], run_rght[1])
                        else:
                            no_move = player.no_movement()
                            screen.blit(no_move[0], no_move[1])
                        """}Перемещение пероснажа"""

                    if True:  # Прыжок
                        """Прыжок{"""
                        if not player.jump_f:
                            if keys[pygame.K_SPACE]:
                                player.jump_f = True
                        else:
                            player.jump()
                        """}Прыжок"""

                    if equipment.show_flag:
                        equipment.show(screen)
                else:
                    screen.blit(background_event_small, (0, 0))
                    if True:  # Enemy, Fullscreen, etc
                        """Enemy, Fullscreen, etc{"""
                        screen.blit(add_enemy5_button, add_enemy5_button_rect)

                        if enemies_special:
                            enemies_special.draw(screen)
                            enemies_special.update(player.rect, player)

                        pygame.draw.rect(screen, "white", (539, 288, 32, 32))
                        screen.blit(fullscreen, fullscreen_rect)

                        sprites_attack_fire_1.update(player, enemies_special)  # отрисовка первой атаки
                        sprites_attack_fire_1.draw(screen)

                        show_hp.update(screen, player)
                        """}Enemy, Fullscreen, etc"""

                    if True:  # Перемещение персонажа
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

                        """}Перемещение пероснажа"""

                    if True:  # Прыжок
                        """Прыжок{"""
                        if not player.jump_f:
                            if keys[pygame.K_SPACE]:
                                player.jump_f = True
                        else:
                            player.jump()
                        """}Прыжок"""
                    
                    if enemies_special:
                        enemies_special.draw(screen)
                        enemies_special.update(player.rect, player)
                    else:
                        enemies_special = pygame.sprite.Group()
                    # else:
                    #     player.location = 0

                    if equipment.show_flag:
                        equipment.show(screen)
            else:
                screen.blit(gameover_small, (0, 0))
                screen.blit(restart_button, restart_button_rect)
        else:  # для full screen
            screen.blit(background_full, (0, 0))  # НЕ ТРОГАТЬ

            if True:  # Передвижение персонажа
                """Передвижение персонажа{"""
                if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.rect.x > 30:
                    run_lf = player.run_left()
                    screen.blit(run_lf[0], run_lf[1])
                elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.rect.x < x - 150:
                    run_rght = player.run_right()
                    screen.blit(run_rght[0], run_rght[1])
                else:
                    # screen.blit(walk[0], (player_x, player_y))
                    no_move = player.no_movement()
                    screen.blit(no_move[0], no_move[1])

                player_rect = player.rect
                """}Передвижение персонажа"""

            if True:  # прыжок
                """Прыжок персонажа{"""
                if not player.jump_f:
                    if keys[pygame.K_SPACE]:
                        player.jump_f = True
                else:
                    player.jump()
                """}Прыжок персонажа"""

            pygame.draw.rect(screen, "white", (x - 32, 0, 32, 32))
            screen.blit(minimise, minimise_rect)

            if enemies_full:  # Enemies
                enemies_full.draw(screen)
                enemies_full.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(player.exp)  # 0
                print(player.lvl)  # 1
                print(player.count_kill)  # 0
                print(player.start_hp)  # 1000
                print(player.start_atc)  # 100
                print(player.CP)  # 300
                print(player.CP_location)   # 0
                print(player.location)  # 0
                running = False
            if event.type == pygame.KEYDOWN:
                if not full:
                    if event.key == pygame.K_f:
                        full = True

                        player = Player(exp=player.exp, lvl=player.lvl, walk_right=tamg.run_right(True),
                                        walk_left=tamg.run_left(True), count_kill=player.count_kill,
                                        hp=player.hp, atc=player.atc, CP=player.CP, x=150, y=y - 150,
                                        jump_count=10, speed=player.speed * 2)
                else:
                    if event.key == pygame.K_f or event.key == pygame.K_ESCAPE:
                        full = False

                        player = Player(exp=player.exp, lvl=player.lvl, walk_right=tamg.run_right(),
                                        walk_left=tamg.run_left(), count_kill=player.count_kill,
                                        hp=player.hp, atc=player.atc, CP=player.CP,
                                        jump_count=8, speed=player.speed // 2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if fullscreen_rect.collidepoint(pos_mouse):
                    """Вывод изображения на фулл экран"""
                    full = True

                    player = Player(exp=player.exp, lvl=player.lvl, walk_right=tamg.run_right(True),
                                    walk_left=tamg.run_left(True), count_kill=player.count_kill,
                                    hp=player.hp, atc=player.atc, CP=player.CP, x=150, y=y - 150,
                                    jump_count=10, speed=player.speed * 2,
                                    CP_location=player.CP_location, location=player.location)
                if add_enemy5_button_rect.collidepoint(pos_mouse) and not player.location:
                    pos_x = 500
                    if player.count_kill % 1000 <= 4:
                        path_of_the_enemy = "enemy/ghost_2_small.png"
                    else:
                        path_of_the_enemy = "enemy/ghost_small.png"
                    for _ in range(5):
                        enemies.add(Enemy(pos_x, y=250, filename=path_of_the_enemy))
                        pos_x -= 50
                if restart_button_rect.collidepoint(pos_mouse):
                    global_flag_of_death = False
                    # player.start_hp -= 300
                    # player.start_atc -= 100
                    player.hp = player.start_hp
                    # player.CP -= 1000
                    player.status = "Alive"
                    if enemies:
                        enemies.update(die=1)
                if minimise_rect.collidepoint(pos_mouse):
                    full = False

                    player = Player(exp=player.exp, lvl=player.lvl, walk_right=tamg.run_right(),
                                    walk_left=tamg.run_left(), count_kill=player.count_kill,
                                    hp=player.hp, atc=player.atc, CP=player.CP,
                                    jump_count=8, speed=player.speed // 2,
                                    CP_location=player.CP_location, location=player.location)
                if equipment_button_rect.collidepoint(pos_mouse):
                    equipment.show_flag = True
                create_particles(pos_mouse)
            if event.type == timer_button_enemy_5:
                if full:
                    for i in range(5):
                        pos_x = x + 500
                        enemies_full.add(Enemy(x=pos_x, y=y - 200, filename="enemy/ghost_full.png"))
                        pos_x -= 200
            if player.location and not enemies_special and not full and timer_button_enemy_5:
                pygame.time.set_timer(timer_button_enemy_5, 100000)
                enemies = pygame.sprite.Group()
                pos_x = 500
                for _ in range(5):
                    enemies_special.add(Enemy(attack=250, health=1000, x=pos_x, 
                                              y=250, filename="enemy/special_ghost_small.png"))
                    pos_x -= 50
            elif not enemies_special:
                player.location = 0


        pygame.display.update()

        clock.tick(15)

    pygame.quit()


if __name__ == "__main__":
    main()
