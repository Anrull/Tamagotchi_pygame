import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

hello_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 275), (100, 50)),
    text='Say Hello',
    manager=manager
)


text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((350, 350), (100, 50)),
    text="Information",
    manager=manager
)

buy_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 425), (100, 50)),
    text='Say Buy',
    manager=manager
)

clock = pygame.time.Clock()
is_running = True

manager2 = pygame_gui.UIManager((800, 600))

hello_button2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 275), (100, 50)),
    text='Say Hello',
    manager=manager2
)


text2 = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((350, 350), (100, 50)),
    text="Information",
    manager=manager2
)

buy_button2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 425), (100, 50)),
    text='Say Buy',
    manager=manager2
)


while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('Hello World!')
            if event.ui_element == buy_button:
                print("Buy")
            if event.ui_element == hello_button2:
                print('Hello World!')
            if event.ui_element == buy_button2:
                print("Buy")
    if False:
        manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
    else:
        manager2.process_events(event)

        manager2.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager2.draw_ui(window_surface)
    pygame.display.update()
