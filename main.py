import pygame
import sys
from test_client import Client

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Jeu de Magasin")

font = pygame.font.SysFont("georgia", 20)

def draw_boxed_text(text, x, y, text_color=(30, 50, 30), bg=(180, 240, 200, 200)):
    text_surface = font.render(text, True, text_color)
    w, h = text_surface.get_width() + 16, text_surface.get_height() + 8
    box = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(box, bg, (0, 0, w, h), border_radius=14)
    box.blit(text_surface, (8, 4))
    screen.blit(box, (x, y))

def draw_score_bar(score):
    bg_color = (180, 240, 200, 200)
    text_color = (30, 50, 30)
    bar_width, bar_height = 150, 40
    bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
    pygame.draw.rect(bar_surface, bg_color, (0, 0, bar_width, bar_height), border_radius=18)
    text_surface = font.render(f"Score : {score}", True, text_color)
    x = (bar_width - text_surface.get_width()) // 2
    y = (bar_height - text_surface.get_height()) // 2
    bar_surface.blit(text_surface, (x, y))
    screen.blit(bar_surface, (WIDTH - bar_width - 20, 20))

def draw_items_button():
    w, h = 130, 40
    x, y = WIDTH - w - 20, 80
    bg = (180, 240, 200, 200)
    btn = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(btn, bg, (0, 0, w, h), border_radius=16)
    text = font.render("Objets ▼", True, (30, 50, 30))
    btn.blit(text, (18, 8))
    screen.blit(btn, (x, y))
    return pygame.Rect(x, y, w, h)

def draw_items_dropdown(item_images, mouse_pos):
    w, h = 700, 240
    x = (WIDTH - w) // 2
    y = 140
    bg = (180, 240, 200, 200)

    box = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(box, bg, (0, 0, w, h), border_radius=22)

    positions = []
    col = 0
    row = 0

    for item, (img, rect) in item_images.items():
        px = x + 40 + col * 120
        py = y + 20 + row * 110

        rect.topleft = (px, py)

        hover = rect.collidepoint(mouse_pos)

        if hover:
            pygame.draw.circle(box, (200, 255, 220), (px - x + 35, py - y + 35), 45)

        box.blit(img, (px - x, py - y))

        col += 1
        if col == 5:
            col = 0
            row += 1

    screen.blit(box, (x, y))

def load_item_images():
    items = [
        "burger-cheese",
        "burger-double",
        "cookie-chocolate",
        "cup-tea",
        "cup-coffee",
        "donut",
        "hot-dog",
        "ice-cream",
        "croissant",
        "soda",
        "sundae"
    ]

    images = {}
    for item in items:
        img = pygame.image.load(f"images/items/{item}.png")
        img = pygame.transform.scale(img, (70, 70))
        rect = img.get_rect()
        images[item] = (img, rect)
    return images

def main():
    score = 0
    items_open = False

    background = pygame.image.load("images/backgrounds/cafe1.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    happy_img = pygame.image.load("images/ui/emote_faceHappy.png")
    happy_img = pygame.transform.scale(happy_img, (50, 50))

    angry_img = pygame.image.load("images/ui/emote_faceAngry.png")
    angry_img = pygame.transform.scale(angry_img, (50, 50))

    client = Client()
    client_img = pygame.image.load(client.image)
    client_img = pygame.transform.scale(client_img, (230, 320))

    item_images = load_item_images()
    result_message = ""

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))
        screen.blit(client_img, (275, 190))

        draw_boxed_text(f"Client : {client.name}", 30, 20)
        draw_boxed_text(f"Demande : {client.request}", 30, 60)
        draw_score_bar(score)

        if result_message == "good":
            screen.blit(happy_img, (WIDTH - 90, 130))
        elif result_message == "bad":
            screen.blit(angry_img, (WIDTH - 90, 130))

        btn_rect = draw_items_button()

        if items_open:
            draw_items_dropdown(item_images, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if btn_rect.collidepoint(pos):
                    items_open = not items_open

                if items_open:
                    for item, (_, rect) in item_images.items():
                        if rect.collidepoint(pos):
                            if item == client.request:
                                score += 1
                                result_message = "good"
                            else:
                                result_message = "bad"

                            pygame.display.flip()
                            pygame.time.delay(900)
                            result_message = ""
                            items_open = False

                            client = Client()
                            client_img = pygame.image.load(client.image)
                            client_img = pygame.transform.scale(client_img, (230, 320))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
