import pygame

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
        return (30, 200)
    
    def add_CP(self):
        """Добавление Боевой Мощи"""
        self.combat_power += 10
    
    def min_CP(self):
        """Вычитание БМ"""
        self.combat_power -= 10
    
    def show_CP(self):
        """Получение БМ"""
        return self.combat_power
      

def main():
    x, y = 1280, 720    
    screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Тамагочи")
    
    clock = pygame.time.Clock()
    
    tamg = MainTamg(x, y)
    
    running = True
    
    background = pygame.image.load("background_1.jpg").convert()
    image = tamg.image_to_alpha("fox/fox_main_lvl1.png") # выбери сам если не нравится
    image = pygame.transform.scale(image, (500, 300))
    
    walk_right = tamg.run_right()
    walk_left = tamg.run_left()
    
    walk_count = 0
    
    player_x, player_y = tamg.start_coords()
    player_speed = 7
    
    jump_f = False
    jump_count = 8
    
    walk = walk_right[:]
    
    while running:
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
        
        
        pygame.draw.line(screen, "black", (500, 300), (x, 300), 2)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
               
        clock.tick(15)


if __name__ == "__main__":
    main()