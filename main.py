import pygame
import sys
import json
import random
from test_client import Client
from story import StoryManager
from qte_minigame import QTEGame
from main_menu import menu_loop
from save_system import save_game, load_game


pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cozy Café - Story Mode")

font = pygame.font.SysFont("georgia", 20)
small_font = pygame.font.SysFont("georgia", 16)


def draw_story_event(event_data):
    """Affiche un événement narratif"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Boîte de dialogue
    box_w, box_h = 600, 400
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2
    
    box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    pygame.draw.rect(box, (255, 250, 240, 250), (0, 0, box_w, box_h), border_radius=25)
    
    # Titre
    title = font.render(event_data["title"], True, (100, 70, 50))
    box.blit(title, (box_w//2 - title.get_width()//2, 30))
    
    # Ligne de séparation
    pygame.draw.line(box, (200, 180, 160), (50, 70), (box_w - 50, 70), 2)
    
    # Messages
    y_offset = 100
    for line in event_data["message"]:
        if line == "":
            y_offset += 15
        else:
            text = small_font.render(line, True, (80, 60, 50))
            box.blit(text, (box_w//2 - text.get_width()//2, y_offset))
            y_offset += 30
    
    # Instruction
    instruction = small_font.render("Clique pour continuer...", True, (150, 130, 110))
    box.blit(instruction, (box_w//2 - instruction.get_width()//2, box_h - 40))
    
    screen.blit(box, (box_x, box_y))

def draw_dialogue_bubble(text, x, y):
    max_width = 250
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if small_font.size(test_line)[0] < max_width - 20:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word + " "
    if current_line:
        lines.append(current_line)
    
    bubble_h = 20 + len(lines) * 22
    bubble_w = max_width
    
    bubble = pygame.Surface((bubble_w, bubble_h), pygame.SRCALPHA)
    pygame.draw.rect(bubble, (255, 255, 230, 240), (0, 0, bubble_w, bubble_h), border_radius=15)
    
    # Petite queue de dialogue
    points = [(10, bubble_h), (20, bubble_h + 10), (30, bubble_h)]
    pygame.draw.polygon(bubble, (255, 255, 230, 240), points)
    
    # Texte
    y_text = 10
    for line in lines:
        txt = small_font.render(line.strip(), True, (60, 50, 40))
        bubble.blit(txt, (10, y_text))
        y_text += 22
    
    screen.blit(bubble, (x, y))

def draw_day_transition(day):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    day_font = pygame.font.SysFont("georgia", 48, bold=True)
    text = day_font.render(f"JOUR {day}", True, (255, 240, 200))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 30))
    
    sub_text = font.render("Nouveau jour au café...", True, (220, 200, 180))
    screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2 + 30))

def draw_tutorial():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    lines = [
        "Bienvenue dans Cozy Café !",
        "",
        "- Regarde les commandes des clients",
        "- Ouvre le menu des objets pour choisir un item",
        "- Glisse l'item sur le client pour le servir",
        "- Améliore ton café dans le shop",
        "- Appuie sur ESPACE pour le mini-jeu Café Parfait",
        "",
        "Objectif : 1000 clients satisfaits !",
        "",
        "Clique n'importe où pour commencer !"
    ]

    y = 100
    for line in lines:
        txt = font.render(line, True, (255, 255, 255))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, y))
        y += 35

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

def draw_header(score, money, day, progress):
    block_w = 120
    block_h = 45
    y = 10
    
    # Day
    x1 = 20
    day_block = pygame.Surface((block_w, block_h), pygame.SRCALPHA)
    pygame.draw.rect(day_block, (255, 235, 205, 230), (0, 0, block_w, block_h), border_radius=18)
    day_text = font.render(f"Jour {day}", True, (100, 80, 60))
    day_block.blit(day_text, (block_w//2 - day_text.get_width()//2,
                              block_h//2 - day_text.get_height()//2))
    screen.blit(day_block, (x1, y))
    
    # Shop
    x2 = 160
    shop_block = pygame.Surface((block_w, block_h), pygame.SRCALPHA)
    pygame.draw.rect(shop_block, (245, 225, 255, 230), (0, 0, block_w, block_h), border_radius=18)
    shop_text = font.render("Shop", True, (80, 60, 80))
    shop_block.blit(shop_text, (block_w//2 - shop_text.get_width()//2,
                                block_h//2 - shop_text.get_height()//2))
    screen.blit(shop_block, (x2, y))
    shop_rect = pygame.Rect(x2, y, block_w, block_h)

    # Score
    x3 = WIDTH//2 - block_w//2
    score_block = pygame.Surface((block_w, block_h), pygame.SRCALPHA)
    pygame.draw.rect(score_block, (225, 245, 255, 230), (0, 0, block_w, block_h), border_radius=18)
    score_text = font.render(f"{score}", True, (60, 70, 90))
    score_block.blit(score_text, (block_w//2 - score_text.get_width()//2,
                                  block_h//2 - score_text.get_height()//2))
    screen.blit(score_block, (x3, y))

    # Money
    x4 = WIDTH - block_w - 20
    money_block = pygame.Surface((block_w, block_h), pygame.SRCALPHA)
    pygame.draw.rect(money_block, (255, 240, 220, 230), (0, 0, block_w, block_h), border_radius=18)
    money_text = font.render(f"{money}€", True, (90, 70, 60))
    money_block.blit(money_text, (block_w//2 - money_text.get_width()//2,
                                  block_h//2 - money_text.get_height()//2))
    screen.blit(money_block, (x4, y))

    # Progress bar
    bar_w, bar_h = 300, 20
    bar_x = WIDTH//2 - bar_w//2
    bar_y = 65
    
    bar_bg = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
    pygame.draw.rect(bar_bg, (200, 200, 200, 200), (0, 0, bar_w, bar_h), border_radius=10)
    
    progress_w = int((progress / 100) * (bar_w - 4))
    pygame.draw.rect(bar_bg, (150, 220, 150, 230), (2, 2, progress_w, bar_h - 4), border_radius=8)
    
    screen.blit(bar_bg, (bar_x, bar_y))
    
    progress_text = small_font.render(f"{int(progress)}% vers l'objectif", True, (80, 80, 80))
    screen.blit(progress_text, (WIDTH//2 - progress_text.get_width()//2, bar_y + 25))

        # Pause + Menu côte à côte
    btn_w, btn_h = 120, 40
    spacing = 20

    # Pause à gauche du centre
    pause_x = WIDTH//2 - btn_w - spacing//2
    pause_y = 120

    pause_block = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
    pygame.draw.rect(pause_block, (230, 230, 255, 230), (0, 0, btn_w, btn_h), border_radius=16)
    pause_text = small_font.render("Pause", True, (60, 60, 90))
    pause_block.blit(pause_text, (btn_w//2 - pause_text.get_width()//2,
                                  btn_h//2 - pause_text.get_height()//2))
    screen.blit(pause_block, (pause_x, pause_y))
    pause_rect = pygame.Rect(pause_x, pause_y, btn_w, btn_h)

    # Menu à droite du centre
    menu_x = WIDTH//2 + spacing//2
    menu_y = pause_y

    menu_block = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
    pygame.draw.rect(menu_block, (255, 220, 220, 230), (0, 0, btn_w, btn_h), border_radius=16)
    menu_text = small_font.render("Menu", True, (120, 40, 40))
    menu_block.blit(menu_text, (btn_w//2 - menu_text.get_width()//2,
                                btn_h//2 - menu_text.get_height()//2))
    screen.blit(menu_block, (menu_x, menu_y))
    menu_rect = pygame.Rect(menu_x, menu_y, btn_w, btn_h)

    return shop_rect, pause_rect, menu_rect





def draw_items_button():
    w, h = 130, 40
    x, y = WIDTH//2 - w//2, HEIGHT - 160

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

def spawn_client(upgrades, story_manager):
    # Chance de spawner un client régulier
    is_regular = False
    regular_name = None
    favorite_items = None
    dialogue = None
    
    if random.random() < 0.3:  # 30% de chance
        regulars = ["Marc", "Lisa", "Robert"]
        for name in regulars:
            if story_manager.is_regular_client_unlocked(name):
                if random.random() < 0.5:  # 50% si débloqué
                    is_regular = True
                    regular_name = name
                    regular_data = story_manager.regular_clients[name]
                    favorite_items = regular_data["favorite_items"]
                    dialogue = story_manager.get_random_regular_dialogue(name)
                    break
    
    client = Client(is_regular=is_regular, regular_name=regular_name, favorite_items=favorite_items)
    client.patience = min(100, client.patience + upgrades["decor"]["level"] * 5)
    client.dialogue = dialogue
    img = pygame.transform.scale(pygame.image.load(client.image), (230, 320))
    return client, img

def draw_drag_bubble(item_img, mouse_pos):
    size = 80
    bubble = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(bubble, (230, 255, 240, 230), (size//2, size//2), size//2)
    img = pygame.transform.scale(item_img, (50, 50))
    bubble.blit(img, (size//2 - 25, size//2 - 25))
    screen.blit(bubble, (mouse_pos[0] - size//2, mouse_pos[1] - size//2))
def main():
    score, money, upgrades, day, total_clients = load_game()
    
    # Initialiser le système d'histoire
    story_manager = StoryManager()
    story_manager.day = day
    story_manager.total_clients_served = total_clients
    
    # Initialiser le QTE
    qte_game = QTEGame()
    qte_result_timer = 0

    # États du jeu
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

    paused = False
    show_tutorial = True
    show_story_event = False
    current_story_event = None
    show_day_transition = False
    day_transition_timer = 0

    auto_timer = pygame.time.get_ticks()

    # Chargement des assets
    background = pygame.image.load("images/backgrounds/cafe1.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    happy_img = pygame.transform.scale(
        pygame.image.load("images/ui/emote_faceHappy.png"), (50, 50)
    )
    angry_img = pygame.transform.scale(
        pygame.image.load("images/ui/emote_faceAngry.png"), (50, 50)
    )

    # Position des clients (corrigée)
    clients = []
    client_imgs = []
    client_positions = [(120, 260), (370, 260), (650, 260)]

    for _ in range(3):
        c, img = spawn_client(upgrades, story_manager)
        clients.append(c)
        client_imgs.append(img)

    item_images = load_item_images()

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()
        
        screen.blit(background, (0, 0))

        # Tutorial
        if show_tutorial:
            draw_tutorial()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    show_tutorial = False
                    event_data = story_manager.get_current_event()
                    if event_data:
                        show_story_event = True
                        current_story_event = event_data
            continue

        # Story Event
        if show_story_event and current_story_event:
            draw_story_event(current_story_event)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game(score, money, upgrades, {
                        "day": story_manager.day,
                        "total_clients": story_manager.total_clients_served
                    })
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    show_story_event = False
                    current_story_event = None
            continue

        # Day Transition
        if show_day_transition:
            if now - day_transition_timer < 2000:
                draw_day_transition(story_manager.day)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                continue
            else:
                show_day_transition = False
                event_data = story_manager.get_current_event()
                if event_data:
                    show_story_event = True
                    current_story_event = event_data

        progress = story_manager.get_progress_percentage()
        shop_rect, pause_rect, menu_rect = draw_header(score, money, story_manager.day, progress)

        # Pause
        if paused:
            pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 120))
            screen.blit(pause_overlay, (0, 0))

            pause_text = font.render("PAUSE", True, (255, 255, 255))
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2,
                                     HEIGHT//2 - pause_text.get_height()//2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game(score, money, upgrades, {
                        "day": story_manager.day,
                        "total_clients": story_manager.total_clients_served
                    })
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        paused = False
            continue

        # Update QTE
        if qte_game.active:
            qte_game.update()
        
        if qte_game.is_showing_result():
            if now - qte_result_timer > 2000:
                qte_game.reset()

        # Patience decay
        base_decay = 0.05
        decay_bonus = 0.01 * upgrades["fridge"]["level"]
        decay = max(0.01, base_decay - decay_bonus)

        client_rects = []

        # Update clients
        for i, client in enumerate(clients):
            if not qte_game.active:
                client.patience -= decay
            if client.patience <= 0:
                client.patience = 0
                result_message = "bad"
                feedback_timer = now
                clients[i], client_imgs[i] = spawn_client(upgrades, story_manager)

        # Draw clients
        for i, client in enumerate(clients):
            x, y = client_positions[i]
            img = client_imgs[i]
            screen.blit(img, (x, y))
            rect = pygame.Rect(x, y, img.get_width(), img.get_height())
            client_rects.append(rect)

            draw_patience_bar(client.patience, x + 20, y - 10)
            draw_request_bubble(client.request, x + 40, y - 70, item_images)

            if client.dialogue and client.is_regular:
                draw_dialogue_bubble(client.dialogue, x + 10, y - 140)

        # Feedback icons
        if result_message == "good":
            screen.blit(happy_img, (WIDTH - 90, 140))
        elif result_message == "bad":
            screen.blit(angry_img, (WIDTH - 90, 140))

        btn_rect = draw_items_button()

        items_menu_rect = None
        item_rects = {}

        if items_open:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 80))
            screen.blit(overlay, (0, 0))
            items_menu_rect, item_rects = draw_items_dropdown(item_images, mouse_pos, scroll_offset)

        if shop_open:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))
            shop_box = draw_shop_menu(upgrades, money)
        else:
            shop_box = None

        # Auto service
        if upgrades["employee"]["level"] > 0 and not items_open and not shop_open and not dragging_item and not qte_game.active:
            delay = max(2000, 5000 - upgrades["employee"]["level"] * 800)
            if now - auto_timer > delay:
                target_index = 0
                score += 1
                gain = 5 + 2 * upgrades["stock"]["level"]
                money += gain
                result_message = "good"
                feedback_timer = now
                
                new_day = story_manager.add_client_served()
                if new_day:
                    show_day_transition = True
                    day_transition_timer = now
                
                clients[target_index], client_imgs[target_index] = spawn_client(upgrades, story_manager)
                auto_timer = now

        # Draw QTE
        if qte_game.active or qte_game.is_showing_result():
            qte_game.draw(screen, WIDTH//2, HEIGHT//2)

        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(score, money, upgrades, {
                    "day": story_manager.day,
                    "total_clients": story_manager.total_clients_served
                })
                running = False

            if event.type == pygame.MOUSEWHEEL and items_open and not dragging_item:
                scroll_offset += event.y * 30
                scroll_offset = max(-120, min(scroll_offset, 0))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
        # Mini-jeu tous les 2 jours (jours pairs)
                    if story_manager.day % 2 == 0:
                        if not qte_game.active and not qte_game.is_showing_result():
                            if not items_open and not shop_open and not dragging_item:
                                qte_game.start()



            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Retour au menu
                if menu_rect.collidepoint(pos):
                    save_game(score, money, upgrades, {
                        "day": story_manager.day,
                        "total_clients": story_manager.total_clients_served
                    })
                    choice = menu_loop(screen)

                    if choice == "quit":
                        pygame.quit()
                        sys.exit()

                    if choice == "new":
                        score = 0
                        money = 0
                        upgrades = {
                            "stock": {"price": 20, "level": 0},
                            "decor": {"price": 30, "level": 0},
                            "fridge": {"price": 40, "level": 0},
                            "employee": {"price": 60, "level": 0}
                        }
                        save_game(score, money, upgrades, {"day": 1, "total_clients": 0})
                        return main()

                # Click QTE
                if qte_game.active:
                    result = qte_game.check_click()
                    qte_result_timer = now
                    continue

                if pause_rect.collidepoint(pos):
                    paused = True
                    continue

                if btn_rect.collidepoint(pos) and not shop_open and not dragging_item:
                    items_open = not items_open
                    continue

                if shop_rect.collidepoint(pos) and not items_open and not dragging_item:
                    shop_open = not shop_open
                    continue

                # Fermeture du menu des items
                if items_open and not dragging_item and items_menu_rect:
                    if not items_menu_rect.collidepoint(pos) and not btn_rect.collidepoint(pos):
                        items_open = False
                        continue

                # Fermeture du shop
                if shop_open and shop_box:
                    if not shop_box.collidepoint(pos) and not shop_rect.collidepoint(pos):
                        shop_open = False
                        continue

                # Achat shop
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

                # Drag item
                if items_open and not dragging_item and items_menu_rect and items_menu_rect.collidepoint(pos):
                    for name, r in item_rects.items():
                        if r.collidepoint(pos):
                            dragging_item = True
                            dragged_item_name = name
                            dragged_item_img = item_images[name]
                            items_open = False
                            scroll_offset = 0
                            break

            # DROP ITEM
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

                                    qte_bonus = 1
                                    if qte_game.result == "perfect":
                                        qte_bonus = 2
                                    elif qte_game.result == "good":
                                        qte_bonus = 1.5
                                    
                                    gain = int((5 + 2 * upgrades["stock"]["level"]) * qte_bonus)
                                    money += gain
                                    result_message = "good"
                                    feedback_timer = pygame.time.get_ticks()
                                    
                                    new_day = story_manager.add_client_served()
                                    if new_day:
                                        show_day_transition = True
                                        day_transition_timer = now
                                    
                                    if story_manager.has_won():
                                        show_story_event = True
                                        current_story_event = story_manager.get_current_event()
                                    
                                    clients[i], client_imgs[i] = spawn_client(upgrades, story_manager)
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

        # FEEDBACK 
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
    choice = menu_loop(screen)

    if choice == "quit":
        pygame.quit()
        sys.exit()

    if choice == "new":
        # Reset complet
        score = 0
        money = 0
        upgrades = {
            "stock": {"price": 20, "level": 0},
            "decor": {"price": 30, "level": 0},
            "fridge": {"price": 40, "level": 0},
            "employee": {"price": 60, "level": 0}
        }

        save_game(score, money, upgrades, {"day": 1, "total_clients": 0})
        main()

    if choice == "continue":
        main()
