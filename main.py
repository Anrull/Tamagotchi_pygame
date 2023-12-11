import pygame

pygame.init()


class MainTamg:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def image_to_alpha(self):
        image = pygame.image.load("fox/fox_main_lvl1.png").convert_alpha()
        return image
    
    def run_right(self):
        walk = [
            pygame.image.load("fox/fox_right/fox_right_1.png").convert_alpha(),
            pygame.image.load("fox/fox_right/fox_right_2.png").convert_alpha(),
            pygame.image.load("fox/fox_right/fox_right_3.png").convert_alpha()
        ]
        return walk
    
    def run_left(self):
        walk = [
            pygame.image.load("fox/fox_left/fox_left_1.png").convert_alpha(),
            pygame.image.load("fox/fox_left/fox_left_2.png").convert_alpha(),
            pygame.image.load("fox/fox_left/fox_left_3.png").convert_alpha()
        ]
        return walk

    def start_coords(self):
        return (30, 30)
      

def main():
    x, y = 1280, 720    
    screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Тамагочи")
    
    tamg = MainTamg(x, y)
    
    running = True
    
    background = pygame.image.load("background_1.jpg").convert()
    image = tamg.image_to_alpha() # выбери сам если не нравится
    image = pygame.transform.scale(image, (500, 300))
    
    walk_right = tamg.run_right()
    walk_left = tamg.run_left()
    
    walk_count = 0
    
    player_x, player_y = tamg.start_coords()
    
    while running:
        screen.fill((52, 64, 52)) # (65, 138, 65) / (92, 163, 92) / (54, 92, 54) / выбери сам
        screen.blit(background, (0, 0))
        screen.blit(image, (x // 2, 0))
        
        keys = pygame.key.get_pressed()
        
        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


if __name__ == "__main__":
    main()