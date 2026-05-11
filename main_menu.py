import pygame
from save_system import save_game, load_game  # On va créer ce fichier juste après

WIDTH, HEIGHT = 800, 600

def draw_main_menu(screen):
    screen.fill((240, 220, 200))

    title_font = pygame.font.SysFont("georgia", 48, bold=True)
    btn_font = pygame.font.SysFont("georgia", 28)

    title = title_font.render("Cozy Café", True, (100, 70, 50))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

    buttons = {
        "new": pygame.Rect(WIDTH//2 - 150, 250, 300, 60),
        "continue": pygame.Rect(WIDTH//2 - 150, 330, 300, 60),
        "quit": pygame.Rect(WIDTH//2 - 150, 410, 300, 60)
    }

    for rect in buttons.values():
        pygame.draw.rect(screen, (255, 240, 220), rect, border_radius=20)
        pygame.draw.rect(screen, (180, 150, 130), rect, 3, border_radius=20)

    new_txt = btn_font.render("Nouvelle Partie", True, (80, 50, 40))
    cont_txt = btn_font.render("Continuer", True, (80, 50, 40))
    quit_txt = btn_font.render("Quitter", True, (80, 50, 40))

    screen.blit(new_txt, (WIDTH//2 - new_txt.get_width()//2, 265))
    screen.blit(cont_txt, (WIDTH//2 - cont_txt.get_width()//2, 345))
    screen.blit(quit_txt, (WIDTH//2 - quit_txt.get_width()//2, 425))

    return buttons


def menu_loop(screen):
    """Boucle du menu principal. Retourne 'new', 'continue' ou 'quit'."""
    running = True

    while running:
        buttons = draw_main_menu(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if buttons["new"].collidepoint(pos):
                    return "new"

                if buttons["continue"].collidepoint(pos):
                    return "continue"

                if buttons["quit"].collidepoint(pos):
                    return "quit"
