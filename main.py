import pygame
import random

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
    
    def run_right(self):
        """Получение списка движения вправо"""
        walk = [
            pygame.image.load("fox/fox_right/fox_right_1.png").convert_alpha(),
            pygame.image.load("fox/fox_right/fox_right_2.png").convert_alpha(),
            pygame.image.load("fox/fox_right/fox_right_3.png").convert_alpha()
        ]
        return walk
    
    def run_left(self):
        """Получение списка движения влево"""
        walk = [
            pygame.image.load("fox/fox_left/fox_left_1.png").convert_alpha(),
            pygame.image.load("fox/fox_left/fox_left_2.png").convert_alpha(),
            pygame.image.load("fox/fox_left/fox_left_3.png").convert_alpha()
        ]
        return walk

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

def main():
    x, y = 1280, 720
    idd = random.randint(0, 1)
    print(idd)  
    screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Тамагочи")
    
    clock = pygame.time.Clock()
    
    tamg = MainTamg(x, y)
    
    running = True
    
    background = tamg.image_to_alpha("background/background_1_new.png")
    image = tamg.image_to_alpha("fox/fox_main_lvl1.png") # выбери сам если не нравится
    image = pygame.transform.scale(image, (500, 300))
    
    fullscreen = tamg.image_to_alpha("icons/fullscreen.png")
    fullscreen_rect = fullscreen.get_rect(topleft=(547, 296))
    
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
    
    full = False
    
    while running:
        if not full:
            screen.fill((255, 255, 255)) # (65, 138, 65) / (92, 163, 92) / (54, 92, 54) / выбери сам / (52, 64, 52)
            screen.blit(background, (0, 0)) # НЕ ТРОГАТЬ
            screen.blit(image, (x // 2, 0))
            
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
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT] and player_x < 400:
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
                if jump_count >= -8:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 1
                else:
                    jump_f = False
                    jump_count = 8
            
            """Information"""
            pygame.draw.line(screen, "black", (571, 317), (x, 317), 3)
            pygame.draw.line(screen, "black", (426, 320), (426, y), 2)
            pygame.draw.line(screen, "black", (853, 320), (853, y), 2)
            
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
            """Information finish"""
            
            
            """Fullscreen, Enemy, etc"""
            pygame.draw.rect(screen, "white", (539, 288, 32, 32))
            screen.blit(fullscreen, fullscreen_rect)
            
            mouse = pygame.mouse.get_pos()
            
            if fullscreen_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                full = True
                
                # player_x, player_y = 
            
            """Fullscreen, Enemy, etc finish"""
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
               
        clock.tick(15)


if __name__ == "__main__":
    main()