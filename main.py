import pygame
import random
import sys

pygame.init()

sys.stdin = open("information_about_player.txt", "r+", encoding="UTF-8")
sys.stdout = open("information_about_player.txt", "r+")

global_flag_of_death = False
screen_rect = (0, 0, 571, 321)
screen_rect_full = (0, 0, 1280, 720)
global_SM_enemies = 5  # Summoning_multiple_enemies
x, y = 1280, 720  # размер экрана
FPS = 15
global_flag_information_screen = False

color1 = (0, 0, 255)  # Начальный цвет (синий)
color2 = (255, 0, 0)  # Конечный цвет (красный)

backgrounds_small = {
    0: "background/background_2_small.png",
    1: "background/background_3_small.png",
    2: "background/background_4_small.png"
}

backgrounds_full = {
    0: "background/background_2_full.png",
    1: "background/background_3_full.png",
    2: "background/background_4_full.png"
}


def update_image_background(location, full=False):
        return pygame.image.load(backgrounds_small[location]) if not full else pygame.image.load(backgrounds_full[location])
    

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

    def update(self, pos_player=None, player=None,
               take_hp=None, other_rect=None,
               other=None, die=None):
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

    def update(self, player, enemies, full):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if enemies:
            enemies.update(take_hp=player.atc, player=player, other_rect=self.rect, other=self)
        if not full:
            if not self.rect.colliderect(screen_rect):
                self.kill()
        else:
            if not self.rect.colliderect(screen_rect_full):
                self.kill()


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
        
        self.CP_start = CP
        self.start_session_atc, self.start_session_hp = atc, hp
        self.count_kill_start = count_kill
        self.start_exp = 0
        self.start_lvl = lvl

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
            self.start_exp += self.exp
            self.lvl += 1
            self.exp = 0
        
        if self.CP_location >= 50000 and self.location == 1:
            self.location = 2
            self.CP_location = 0
        elif self.CP_location >= 10000 and not self.location:
            self.location = 1
            self.CP_location = 0
    
    def update_CP_EXP_etc(self):
        self.CP += 5
        self.CP_location += 5
        self.exp += 10
        self.count_kill += 1
    
    def result_after_death(self):
        return {
            "CP": self.CP - self.CP_start,
            "ATC": self.start_atc - self.start_session_atc,
            "HP": self.start_hp - self.start_session_hp,
            "KILL": self.count_kill - self.count_kill_start,
            "EXP": self.start_exp + self.exp,
            "LVL": self.lvl - self.start_lvl
            }


class Information:
    def __init__(self, label):
        self.label = label
        self.info = label.render("Information", False, "green")
        self.info_rect = self.info.get_rect(topleft=(870, 340))
        self.gameover_small = pygame.image.load("gameover/gameover_small_1.png").convert()
        self.gameover_full = pygame.image.load("gameover/gameover_full_1.jpg").convert()

    def update_interface(self, screen, background, image, x, y, start_screen):
        screen.fill((255, 255, 255))
        if not start_screen:
            screen.blit(background, (0, 0))
        else:
            screen.fill((255, 255, 255))
        screen.blit(image, (571, 0))

        pygame.draw.line(screen, "black", (0, 317), (x, 317), 3)
        pygame.draw.line(screen, "black", (426, 320), (426, y), 2)
        pygame.draw.line(screen, "black", (853, 320), (853, y), 2)
        pygame.draw.line(screen, "black", (571, 0), (571, 317), 2)

    def update_information(self, screen, player, enemies):
        if player.status != "Alive":
            grey_button = self.label.render("Добавить 5 врагов", False, "grey")
            grey_button_rect = grey_button.get_rect(topleft=(446, 340))
            screen.blit(grey_button, grey_button_rect)
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

    def deathscreen(self, screen, player, full=False):
        dict_results = player.result_after_death()
        
        label_CP = self.label.render(f"БМ: {dict_results['CP']}", False, "green")
        label_atc = self.label.render(f"ATC: {dict_results['ATC']}", False, "green")
        label_hp = self.label.render(f"HP: {dict_results['HP']}", False, "green")
        label_kill = self.label.render(f"KILL: {dict_results['KILL']}", False, "green")
        label_exp = self.label.render(f"EXP: {dict_results['EXP']}", False, "green")
        label_lvl = self.label.render(f"LVL: {dict_results['LVL']}", False, "green")
        if not full:
            screen.blit(self.gameover_small, (0, 0))
            
            label_CP_rect = label_CP.get_rect(topleft=(10, 10))
            label_atc_rect = label_atc.get_rect(topleft=(10, 60))
            label_hp_rect = label_hp.get_rect(topleft=(10, 110))
            label_kill_rect = label_kill.get_rect(topleft=(10, 160))
            label_exp_rect = label_exp.get_rect(topleft=(10, 210))
            label_lvl_rect = label_lvl.get_rect(topleft=(10, 260))
        else:
            screen.blit(self.gameover_full, (0, 0))
            
            label_CP_rect = label_CP.get_rect(topleft=(10, y - 260 - 40))
            label_atc_rect = label_atc.get_rect(topleft=(10, y - 210 - 40))
            label_hp_rect = label_hp.get_rect(topleft=(10, y - 160 - 40))
            label_kill_rect = label_kill.get_rect(topleft=(10, y - 110 - 40))
            label_exp_rect = label_exp.get_rect(topleft=(10, y - 60 - 40))
            label_lvl_rect = label_lvl.get_rect(topleft=(10, y - 10 - 40))

        screen.blit(label_CP, label_CP_rect)
        screen.blit(label_atc, label_atc_rect)
        screen.blit(label_hp, label_hp_rect)
        screen.blit(label_kill, label_kill_rect)
        screen.blit(label_exp, label_exp_rect)
        screen.blit(label_lvl, label_lvl_rect)
    
    def information_screen(self, screen):
        for y in range(720):
            for x in range(1280):
                # Вычисление текущего цвета на основе градиента
                color = (
                    int(color1[0] + (color2[0] - color1[0]) * (x / 1280)),
                    int(color1[1] + (color2[1] - color1[1]) * (y / 720)),
                    int(color1[2] + (color2[2] - color1[2]) * (y / 720))
                )

                # Установка цвета пикселя на экране
                screen.set_at((x, y), color)
        
        # color = (39, 192, 245)
        color = "white"
        
        info_game1 = self.label.render("Эта игра была создана в рамках презентации навыков pygame", False, color)
        info_game2 = self.label.render("Управление персонажем происходит по средством следующих кнопок:", False, color)
        info_game3 = self.label.render(" - передвижение игрока влево", False, color)
        info_game4 = self.label.render(" - передвижение игрока вправо", False, color)
        info_game5 = self.label.render(" - прыжок игрока", False, color)
        
        info_game6 = self.label.render("Взаимодействие c врагами:", False, color)
        info_game7 = self.label.render(" - создание врагов", False, color)
        info_game8 = self.label.render(" - (клик по экрану) атака по врагам", False, color)

        image_a = pygame.image.load("icons/a.png").convert_alpha()
        image_d = pygame.image.load("icons/d.png").convert_alpha()
        image_r = pygame.image.load("icons/right.png").convert_alpha()
        image_l = pygame.image.load("icons/left.png").convert_alpha()
        image_space = pygame.image.load("icons/space.png").convert_alpha()
        image_shift = pygame.image.load("icons/shift.png").convert_alpha()
        image_click = pygame.image.load("icons/click.png").convert_alpha()

        info_game1_rect = info_game1.get_rect(topleft=(60, 60))
        info_game2_rect = info_game2.get_rect(topleft=(60, 100))
        info_game3_rect = info_game3.get_rect(topleft=(75 + 48 + 48, 140 + 8))
        info_game4_rect = info_game4.get_rect(topleft=(75 + 48 + 48, 140 + 56))
        info_game5_rect = info_game5.get_rect(topleft=(75 + 48 + 5, 140 + 56 + 48))
        info_game6_rect = info_game6.get_rect(topleft=(60, 140 + 56 + 48 + 48))
        info_game7_rect = info_game7.get_rect(topleft=(75 + 48, 140 + 56 + 48 + 48 + 48))
        info_game8_rect = info_game8.get_rect(topleft=(75 + 48, 140 + 56 + 48 + 48 + 48 + 48))

        screen.blit(info_game1, info_game1_rect)
        screen.blit(info_game2, info_game2_rect)
        screen.blit(info_game3, info_game3_rect)
        screen.blit(info_game4, info_game4_rect)
        screen.blit(info_game5, info_game5_rect)
        screen.blit(info_game6, info_game6_rect)
        screen.blit(info_game7, info_game7_rect)
        screen.blit(info_game8, info_game8_rect)

        screen.blit(image_a, (75, 140))
        screen.blit(image_d, (75, 140 + 48))
        screen.blit(image_l, (75 + 48, 140))
        screen.blit(image_r, (75 + 48, 140 + 48))
        screen.blit(image_space, (75 + 5, 140 + 48 + 48))
        screen.blit(image_shift, (75, 140 + 56 + 48 + 48 + 36))
        screen.blit(image_click, (75, 140 + 56 + 48 + 48 + 48 + 36))



def create_particles(position):
    # количество создаваемых частиц
    particle_count = 6
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def main():
    global global_flag_of_death, global_flag_information_screen

    if True:  # чисто для того, чтоб скрыть создание переменных. Можно удалить
        idd = random.randint(0, 1)  # случайный выбор фона
        screen = pygame.display.set_mode((x, y))
        pygame.display.set_caption("Тамагочи")
        
        start_screen = True
        
        pygame.mixer.init()
        pygame.mixer.music.load("music/Serious_Sam_The_Second_Encounter_Corridor_of_Death_Saferty_Cover.mp3")
        pygame.mixer.music.play(-1)

        tamg = MainTamg()

        player = Player(exp=int(input()), lvl=int(input()), walk_right=tamg.run_right(),
                        walk_left=tamg.run_left(), count_kill=int(input()),
                        hp=int(input()), atc=int(input()), CP=int(input()),
                        CP_location=int(input()), location=int(input()))
        player.update_combat_power()

        show_hp = Show_HP_EXP()

        clock = pygame.time.Clock()

        running = True  # пока истина - работает

        background = tamg.small_image_to_alpha(idd)  # малый задний фон
        background_full = tamg.full_image_to_alpha(idd)  # большой задний фон

        # image = tamg.image_to_alpha("fox/fox_main_lvl1.png")  # выбери сам если не нравится
        # image = pygame.transform.scale(image, (500, 300))  # отформатирование животного, чтоб влезало
        image = pygame.image.load("fox/fox_main_version3.png")
        image = pygame.transform.scale(image, (x - 571, 317))

        fullscreen = tamg.image_to_alpha("icons/fullscreen.png")
        fullscreen_rect = fullscreen.get_rect(topleft=(547, 296))

        minimise = tamg.image_to_alpha("icons/minimise.png")
        minimise_rect = minimise.get_rect(topleft=(x - 32, 0))
        
        information_button = tamg.image_to_alpha("icons/information.png")
        information_button_rect = information_button.get_rect(topleft=(x - 32, y - 32))
        
        escape_button = tamg.image_to_alpha("icons/escape.png")
        escape_button_rect = escape_button.get_rect(topleft=(0, 0))

        label = pygame.font.Font(size=40)

        information = Information(label)

        add_enemy5_button = label.render("Добавить 5 врагов", False, "green")
        add_enemy5_button_rect = add_enemy5_button.get_rect(topleft=(446, 340))

        restart_button = label.render("Restart", False, "green")
        restart_button_rect = restart_button.get_rect(topleft=(440, 280))
        restart_button_rect_full = restart_button.get_rect(topleft=(x - 150, y - 100))
        
        start_button = label.render("Start", True, "red")
        start_button_rect = start_button.get_rect(topleft=(235, 145))
        start_button_rect_full = start_button.get_rect(topleft=(x // 2 - 40, y // 2 - 40))

        timer_button_enemy_5 = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_button_enemy_5, 5000)

        full = False

        enemies = pygame.sprite.Group()

        enemies_full = pygame.sprite.Group()

    while running:
        keys = pygame.key.get_pressed()
        
        if not global_flag_information_screen:
            if not full:  # Если экран начальный
                background = update_image_background(player.location)
                information.update_interface(screen, background, image, x, y, start_screen)  # Отрисовка интерфейса
                if start_screen:
                    screen.blit(start_button, start_button_rect)

                # Information
                information.update_information(screen, player, enemies)

                if not global_flag_of_death:
                    if True:  # Enemy, Fullscreen, etc
                        """Enemy, Fullscreen, etc{"""
                        screen.blit(add_enemy5_button, add_enemy5_button_rect)
                        screen.blit(information_button, information_button_rect)

                        if not start_screen:
                            if enemies:
                                enemies.draw(screen)
                                enemies.update(player.rect, player)

                            pygame.draw.rect(screen, "white", (539, 288, 32, 32))
                            screen.blit(fullscreen, fullscreen_rect)

                            sprites_attack_fire_1.update(player, enemies, full)  # отрисовка первой атаки
                            sprites_attack_fire_1.draw(screen)

                            show_hp.update(screen, player)
                        """}Enemy, Fullscreen, etc"""

                    if not start_screen:  # Перемещение персонажа
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
                else:
                    information.deathscreen(screen, player)
                    screen.blit(restart_button, restart_button_rect)
            else:  # для fullscreen
                background_full = update_image_background(player.location, True)
                screen.blit(background_full, (0, 0))  # НЕ ТРОГАТЬ

                if not start_screen:  # Передвижение персонажа
                    if not global_flag_of_death:
                        if True:
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
                            """}Передвижение персонажа"""

                        if True:  # прыжок
                            """Прыжок персонажа{"""
                            if not player.jump_f:
                                if keys[pygame.K_SPACE]:
                                    player.jump_f = True
                            else:
                                player.jump()
                            """}Прыжок персонажа"""

                        if enemies_full:
                            enemies_full.draw(screen)
                            enemies_full.update(player.rect, player)
                        
                        sprites_attack_fire_1.update(player, enemies_full, full)  # отрисовка первой атаки
                        sprites_attack_fire_1.draw(screen)
                        
                        show_hp.update(screen, player)
                    else:
                        information.deathscreen(screen, player, full)
                        screen.blit(restart_button, restart_button_rect_full)
                else:
                    screen.fill("WHITE")
                    screen.blit(start_button, start_button_rect_full)
                pygame.draw.rect(screen, "white", (x - 32, 0, 32, 32))
                screen.blit(minimise, minimise_rect)
        else:
            information.information_screen(screen)
            screen.blit(escape_button, escape_button_rect)

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
                if event.key == pygame.K_SPACE and start_screen:
                    start_screen = False
                if event.key == pygame.K_ESCAPE and global_flag_information_screen:
                    global_flag_information_screen = False
                if not full:
                    if event.key == pygame.K_f:
                        full = True

                        player = Player(exp=player.exp, lvl=player.lvl, walk_right=tamg.run_right(True),
                                        walk_left=tamg.run_left(True), count_kill=player.count_kill,
                                        hp=player.hp, atc=player.atc, CP=player.CP, x=150, y=y - 150,
                                        jump_count=10, speed=player.speed * 2)
                    if event.key == pygame.K_LSHIFT and not global_flag_of_death:
                        pos_x = 500
                        # if player.count_kill % 1000 <= 4:
                        #     path_of_the_enemy = "enemy/ghost_2_small.png"
                        # else:
                        #     
                        path_of_the_enemy = "enemy/ghost_small.png"
                        for _ in range(5):
                            enemies.add(Enemy(pos_x, y=250, attack=100 * (player.location + 1) + 100,
                                            health=100 * (player.location + 1), filename=path_of_the_enemy))
                            pos_x -= 50
                else:
                    if event.key == pygame.K_f or event.key == pygame.K_ESCAPE:
                        full = False

                        player = Player(exp=player.exp, lvl=player.lvl, walk_right=tamg.run_right(),
                                        walk_left=tamg.run_left(), count_kill=player.count_kill,
                                        hp=player.hp, atc=player.atc, CP=player.CP,
                                        jump_count=8, speed=player.speed // 2)
                    
                    if event.key == pygame.K_LSHIFT and not global_flag_of_death:
                        pos_x = x - 250
                        for _ in range(3):
                            enemies_full.add(Enemy(x=pos_x, y=y - 200, attack=100 * (player.location + 1) + 100, 
                                                   health=100 * (player.location + 1), filename="enemy/ghost_full.png"))
                            pos_x -= 200
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
                elif add_enemy5_button_rect.collidepoint(pos_mouse) and not global_flag_of_death:
                    pos_x = 500
                    # if player.count_kill % 1000 <= 4:
                    #     path_of_the_enemy = "enemy/ghost_2_small.png"
                    # else:
                    #     
                    path_of_the_enemy = "enemy/ghost_small.png"
                    for _ in range(5):
                        enemies.add(Enemy(pos_x, y=250, attack=100 * (player.location + 1) + 100,
                                          health=100 * (player.location + 1), filename=path_of_the_enemy))
                        pos_x -= 50
                elif restart_button_rect.collidepoint(pos_mouse) or restart_button_rect_full.collidepoint(pos_mouse):
                    global_flag_of_death = False
                    # player.start_hp -= 300
                    # player.start_atc -= 100
                    player.hp = player.start_hp
                    # player.CP -= 1000
                    player.status = "Alive"
                    if enemies:
                        enemies.update(die=1)
                    if enemies_full:
                        enemies_full.update(die=1)
                elif start_button_rect.collidepoint(pos_mouse) or start_button_rect_full.collidepoint(pos_mouse):
                    start_screen = False
                elif minimise_rect.collidepoint(pos_mouse):
                    full = False

                    player = Player(exp=player.exp, lvl=player.lvl, walk_right=tamg.run_right(),
                                    walk_left=tamg.run_left(), count_kill=player.count_kill,
                                    hp=player.hp, atc=player.atc, CP=player.CP,
                                    jump_count=8, speed=player.speed // 2,
                                    CP_location=player.CP_location, location=player.location)
                elif information_button_rect.collidepoint(pos_mouse):
                    global_flag_information_screen = True
                elif escape_button_rect.collidepoint(pos_mouse):
                    global_flag_information_screen = False
                create_particles(pos_mouse)
            if event.type == timer_button_enemy_5:
                if full:
                    pos_x = x - 250
                    for _ in range(3):
                        enemies_full.add(Enemy(x=pos_x, y=y - 200, attack=100 * (player.location + 1) + 100, 
                                                health=100 * (player.location + 1), filename="enemy/ghost_full.png"))
                        pos_x -= 200


        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
    
# 0
# 1
# 0
# 1000
# 100
# 300
# 0
# 0