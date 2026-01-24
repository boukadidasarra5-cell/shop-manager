import pygame
import sys
from test_client import Client

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Jeu de Magasin")

font = pygame.font.SysFont("georgia", 20)

# UI 

def draw_request_bubble(request_list, x, y, item_images):
    if not request_list:
        return

    spacing = 45
    bubble_w = 20 + len(request_list) * spacing
    bubble_h = 55

    bubble = pygame.Surface((bubble_w, bubble_h), pygame.SRCALPHA)
    pygame.draw.rect(bubble, (255, 240, 250, 220), (0, 0, bubble_w, bubble_h), border_radius=18)

    for i, item in enumerate(request_list):
        if item in item_images:
            img = pygame.transform.scale(item_images[item], (40, 40))
            bubble.blit(img, (10 + i * spacing, 7))

    screen.blit(bubble, (x, y))


def draw_header(score, money):
    block_w = 160
    block_h = 45
    y = 10

    pastel_shop = (245, 225, 255, 230)
    pastel_score = (225, 245, 255, 230)
    pastel_money = (255, 240, 220, 230)

    x1 = 20
    shop_block = pygame.Surface((block_w, block_h), pygame.SRCALPHA)
    pygame.draw.rect(shop_block, pastel_shop, (0, 0, block_w, block_h), border_radius=18)
    shop_text = font.render("Shop", True, (80, 60, 80))
    shop_block.blit(shop_text, (block_w//2 - shop_text.get_width()//2,
                                block_h//2 - shop_text.get_height()//2))
    screen.blit(shop_block, (x1, y))
    shop_rect = pygame.Rect(x1, y, block_w, block_h)

    x2 = WIDTH//2 - block_w//2
    score_block = pygame.Surface((block_w, block_h), pygame.SRCALPHA)
    pygame.draw.rect(score_block, pastel_score, (0, 0, block_w, block_h), border_radius=18)
    score_text = font.render(f"{score}", True, (60, 70, 90))
    score_block.blit(score_text, (block_w//2 - score_text.get_width()//2,
                                  block_h//2 - score_text.get_height()//2))
    screen.blit(score_block, (x2, y))

    x3 = WIDTH - block_w - 20
    money_block = pygame.Surface((block_w, block_h), pygame.SRCALPHA)
    pygame.draw.rect(money_block, pastel_money, (0, 0, block_w, block_h), border_radius=18)
    money_text = font.render(f"{money}€", True, (90, 70, 60))
    money_block.blit(money_text, (block_w//2 - money_text.get_width()//2,
                                  block_h//2 - money_text.get_height()//2))
    screen.blit(money_block, (x3, y))

    return shop_rect


def draw_items_button():
    w, h = 130, 40
    x, y = WIDTH//2 - w//2, HEIGHT - 200
    bg = (180, 240, 200, 220)
    btn = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(btn, bg, (0, 0, w, h), border_radius=16)
    text = font.render("Objets ▼", True, (30, 50, 30))
    btn.blit(text, (18, 8))
    screen.blit(btn, (x, y))
    return pygame.Rect(x, y, w, h)


def draw_items_dropdown(item_images, mouse_pos, scroll_offset):
    w, h = 700, 400
    x = (WIDTH - w) // 2
    y = HEIGHT - 260
    bg = (180, 240, 200, 230)

    box = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(box, bg, (0, 0, w, h), border_radius=30)

    col = 0
    row = 0
    item_rects = {}

    for item, img in item_images.items():
        px = x + 40 + col * 120
        py = y + 20 + row * 110 + scroll_offset

        rect = img.get_rect(topleft=(px, py))
        hover = rect.collidepoint(mouse_pos)

        if hover:
            pygame.draw.circle(box, (200, 255, 220), (px - x + 35, py - y + 35), 45)

        box.blit(img, (px - x, py - y))
        item_rects[item] = rect

        col += 1
        if col == 5:
            col = 0
            row += 1

    screen.blit(box, (x, y))
    return pygame.Rect(x, y, w, h), item_rects


def draw_shop_menu(upgrades, money):
    w, h = 400, 300
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2

    box = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(box, (255, 230, 240, 230), (0, 0, w, h), border_radius=20)

    title = font.render("Boutique d'améliorations", True, (120, 60, 80))
    box.blit(title, (60, 20))

    y_offset = 80
    for name, data in upgrades.items():
        label = {"stock": "Stock", "decor": "Décor", "fridge": "Frigo", "employee": "Employé"}[name]
        text = f"{label} (Lvl {data['level']}) - {data['price']}€"
        txt = font.render(text, True, (80, 40, 40))
        box.blit(txt, (40, y_offset))
        y_offset += 50

    money_txt = font.render(f"Argent : {money}€", True, (80, 40, 40))
    box.blit(money_txt, (40, h - 50))

    screen.blit(box, (x, y))
    return pygame.Rect(x, y, w, h)

def load_item_images():
    items = [
        "burger-cheese", "burger-double", "burger-cheese-double", "maki-vegetable", "chinese",
        "hot-dog", "fries", "pizza", "corn-dog", "cup-tea", "cup-coffee", "sundae", "soda",
        "cookie-chocolate", "donut", "ice-cream", "croissant"
    ]

    images = {}
    for item in items:
        img = pygame.image.load(f"images/items/{item}.png").convert_alpha()
        img = pygame.transform.scale(img, (50, 50))
        images[item] = img
    return images


def draw_patience_bar(value, x, y):
    bg = pygame.Surface((160, 22), pygame.SRCALPHA)
    pygame.draw.rect(bg, (255, 220, 230, 220), (0, 0, 160, 22), border_radius=12)

    width = int(150 * (value / 100))
    color = (255, 120, 150) if value > 40 else (255, 80, 80)

    pygame.draw.rect(bg, color, (5, 5, width, 12), border_radius=10)

    heart = font.render("♡", True, (255, 100, 140))
    bg.blit(heart, (135, 2))

    screen.blit(bg, (x, y))


def buy_upgrade(name, upgrades, money):
    upgrade = upgrades[name]
    if money >= upgrade["price"]:
        money -= upgrade["price"]
        upgrade["level"] += 1
        upgrade["price"] = int(upgrade["price"] * 1.5)
        return money, True
    return money, False


def spawn_client(upgrades):
    client = Client()
    client.patience = min(100, client.patience + upgrades["decor"]["level"] * 5)
    img = pygame.transform.scale(pygame.image.load(client.image), (230, 320))
    return client, img


def draw_drag_bubble(item_img, mouse_pos):
    size = 80
    bubble = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(bubble, (230, 255, 240, 230), (size//2, size//2), size//2)
    img = pygame.transform.scale(item_img, (50, 50))
    bubble.blit(img, (size//2 - 25, size//2 - 25))
    screen.blit(bubble, (mouse_pos[0] - size//2, mouse_pos[1] - size//2))

# MAIN LOOP

def main():
    score = 0
    money = 0
    items_open = False
    shop_open = False
    scroll_offset = 0
    result_message = ""
    feedback_timer = 0

    shop_message = ""
    shop_message_timer = 0

    dragging_item = False
    dragged_item_name = None
    dragged_item_img = None

    upgrades = {
        "stock": {"price": 20, "level": 0},
        "decor": {"price": 30, "level": 0},
        "fridge": {"price": 40, "level": 0},
        "employee": {"price": 60, "level": 0}
    }

    auto_timer = pygame.time.get_ticks()

    background = pygame.image.load("images/backgrounds/cafe1.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    happy_img = pygame.transform.scale(pygame.image.load("images/ui/emote_faceHappy.png"), (50, 50))
    angry_img = pygame.transform.scale(pygame.image.load("images/ui/emote_faceAngry.png"), (50, 50))

    clients = []
    client_imgs = []
    client_positions = [(80, 200), (285, 200), (490, 200)]

    for _ in range(3):
        c, img = spawn_client(upgrades)
        clients.append(c)
        client_imgs.append(img)

    item_images = load_item_images()

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        shop_rect = draw_header(score, money)

        base_decay = 0.05
        decay_bonus = 0.01 * upgrades["fridge"]["level"]
        decay = max(0.01, base_decay - decay_bonus)

        now = pygame.time.get_ticks()

        client_rects = []

        for i, client in enumerate(clients):
            client.patience -= decay
            if client.patience <= 0:
                client.patience = 0
                result_message = "bad"
                feedback_timer = now
                clients[i], client_imgs[i] = spawn_client(upgrades)

        for i, client in enumerate(clients):
            x, y = client_positions[i]
            img = client_imgs[i]
            screen.blit(img, (x, y))
            rect = pygame.Rect(x, y, img.get_width(), img.get_height())
            client_rects.append(rect)

            draw_patience_bar(client.patience, x + 20, y - 30)
            draw_request_bubble(client.request, x + 40, y - 70, item_images)

        if result_message == "good":
            screen.blit(happy_img, (WIDTH - 90, 130))
        elif result_message == "bad":
            screen.blit(angry_img, (WIDTH - 90, 130))

        btn_rect = draw_items_button()

        menu_rect = None
        item_rects = {}

        if items_open:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 80))
            screen.blit(overlay, (0, 0))
            menu_rect, item_rects = draw_items_dropdown(item_images, mouse_pos, scroll_offset)

        if shop_open:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))
            shop_box = draw_shop_menu(upgrades, money)
        else:
            shop_box = None

        if upgrades["employee"]["level"] > 0 and not items_open and not shop_open and not dragging_item:
            delay = max(2000, 5000 - upgrades["employee"]["level"] * 800)
            if now - auto_timer > delay:
                target_index = 0
                score += 1
                gain = 5 + 2 * upgrades["stock"]["level"]
                money += gain
                result_message = "good"
                feedback_timer = now
                clients[target_index], client_imgs[target_index] = spawn_client(upgrades)
                auto_timer = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL and items_open and not dragging_item:
                scroll_offset += event.y * 30
                scroll_offset = max(-120, min(scroll_offset, 0))

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if btn_rect.collidepoint(pos) and not shop_open and not dragging_item:
                    items_open = not items_open
                    continue

                if shop_rect.collidepoint(pos) and not items_open and not dragging_item:
                    shop_open = not shop_open
                    continue

                if items_open and not dragging_item and menu_rect:
                    if not menu_rect.collidepoint(pos) and not btn_rect.collidepoint(pos):
                        items_open = False
                        continue

                if shop_open and shop_box:
                    if not shop_box.collidepoint(pos) and not shop_rect.collidepoint(pos):
                        shop_open = False
                        continue

                if shop_open and shop_box and shop_box.collidepoint(pos):
                    w, h = shop_box.width, shop_box.height
                    x, y = shop_box.topleft
                    names = list(upgrades.keys())
                    for i, name in enumerate(names):
                        r = pygame.Rect(x + 40, y + 80 + i * 50, 320, 40)
                        if r.collidepoint(pos):
                            money, ok = buy_upgrade(name, upgrades, money)
                            if ok:
                                shop_message = f"{name.capitalize()} amélioré !"
                            else:
                                shop_message = "Pas assez d'argent !"
                            shop_message_timer = pygame.time.get_ticks()
                            break

                if items_open and not dragging_item and menu_rect and menu_rect.collidepoint(pos):
                    for name, r in item_rects.items():
                        if r.collidepoint(pos):
                            dragging_item = True
                            dragged_item_name = name
                            dragged_item_img = item_images[name]
                            items_open = False
                            scroll_offset = 0
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if dragging_item:
                    pos = pygame.mouse.get_pos()
                    served = False

                    for i, rect in enumerate(client_rects):
                        if rect.collidepoint(pos):
                            if dragged_item_name in clients[i].request:
                                clients[i].request.remove(dragged_item_name)

                                if len(clients[i].request) == 0:
                                    score += 1
                                    gain = 5 + 2 * upgrades["stock"]["level"]
                                    money += gain
                                    result_message = "good"
                                    feedback_timer = pygame.time.get_ticks()
                                    clients[i], client_imgs[i] = spawn_client(upgrades)
                                else:
                                    result_message = "good"
                                    feedback_timer = pygame.time.get_ticks()

                                served = True
                            else:
                                result_message = "bad"
                                feedback_timer = pygame.time.get_ticks()
                            break

                    if not served:
                        result_message = "bad"
                        feedback_timer = pygame.time.get_ticks()

                    dragging_item = False
                    dragged_item_name = None
                    dragged_item_img = None
                    items_open = False

        if result_message:
            if pygame.time.get_ticks() - feedback_timer > 900:
                result_message = ""

        if shop_message:
            if pygame.time.get_ticks() - shop_message_timer < 1200:
                txt = font.render(shop_message, True, (80, 40, 40))
                screen.blit(txt, (260, 520))
            else:
                shop_message = ""

        if dragging_item and dragged_item_img is not None:
            draw_drag_bubble(dragged_item_img, mouse_pos)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
