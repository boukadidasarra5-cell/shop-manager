import pygame
import random

class QTEGame:
    def __init__(self):
        self.active = False
        self.bar_position = 0
        self.bar_speed = 3
        self.target_zone_start = 40
        self.target_zone_end = 60
        self.direction = 1  # 1 = droite, -1 = gauche
        self.result = None  # "perfect", "good", "miss"
        self.font = pygame.font.SysFont("georgia", 18)
        
    def start(self):
        self.active = True
        self.bar_position = 0
        self.direction = 1
        self.result = None
        # Zone aléatoire pour plus de difficulté
        self.target_zone_start = random.randint(30, 50)
        self.target_zone_end = self.target_zone_start + 20
        
    def update(self):
        if not self.active:
            return
            
        self.bar_position += self.bar_speed * self.direction
        
        # Rebond aux extrémités
        if self.bar_position >= 100:
            self.bar_position = 100
            self.direction = -1
        elif self.bar_position <= 0:
            self.bar_position = 0
            self.direction = 1
    
    def check_click(self):
        if not self.active:
            return None
            
        # Zone parfaite (centre de la zone verte)
        perfect_center = (self.target_zone_start + self.target_zone_end) / 2
        perfect_range = 5
        
        if abs(self.bar_position - perfect_center) <= perfect_range:
            self.result = "perfect"
            self.active = False
            return "perfect"  # Bonus x2
        elif self.target_zone_start <= self.bar_position <= self.target_zone_end:
            self.result = "good"
            self.active = False
            return "good"  # Bonus x1.5
        else:
            self.result = "miss"
            self.active = False
            return "miss"  # Pas de bonus
    
    def draw(self, screen, x, y):
        if not self.active and self.result is None:
            return
            
        # Fond du mini-jeu
        bg_width, bg_height = 400, 150
        bg_x = x - bg_width // 2
        bg_y = y - bg_height // 2
        
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (255, 250, 240, 240), (0, 0, bg_width, bg_height), border_radius=20)
        screen.blit(bg_surface, (bg_x, bg_y))
        
        # Titre
        if self.active:
            title = self.font.render("☕ CAFÉ PARFAIT - Clique au bon moment !", True, (100, 70, 50))
        else:
            title = self.font.render(f"Résultat : {self.result.upper()}", True, (100, 70, 50))
        screen.blit(title, (bg_x + bg_width//2 - title.get_width()//2, bg_y + 20))
        
        # Barre de progression
        bar_width = 300
        bar_height = 30
        bar_x = bg_x + (bg_width - bar_width) // 2
        bar_y = bg_y + 70
        
        # Fond de la barre
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), border_radius=15)
        
        # Zone cible (verte)
        target_x = bar_x + int((self.target_zone_start / 100) * bar_width)
        target_width = int(((self.target_zone_end - self.target_zone_start) / 100) * bar_width)
        pygame.draw.rect(screen, (150, 255, 150), (target_x, bar_y, target_width, bar_height), border_radius=15)
        
        # Zone parfaite (or)
        perfect_center = (self.target_zone_start + self.target_zone_end) / 2
        perfect_x = bar_x + int((perfect_center / 100) * bar_width) - 15
        pygame.draw.rect(screen, (255, 215, 0), (perfect_x, bar_y, 30, bar_height), border_radius=15)
        
        # Curseur (position actuelle)
        cursor_x = bar_x + int((self.bar_position / 100) * bar_width)
        pygame.draw.circle(screen, (255, 100, 100), (cursor_x, bar_y + bar_height//2), 12)
        
        # Instructions
        if self.active:
            instruction = self.font.render("Clique maintenant !", True, (100, 70, 50))
            screen.blit(instruction, (bg_x + bg_width//2 - instruction.get_width()//2, bg_y + 115))
        else:
            # Afficher le bonus obtenu
            bonus_text = {
                "perfect": "🌟 PARFAIT ! Bonus x2 🌟",
                "good": "✓ Bien ! Bonus x1.5",
                "miss": "✗ Raté... Pas de bonus"
            }
            result_text = self.font.render(bonus_text.get(self.result, ""), True, (100, 70, 50))
            screen.blit(result_text, (bg_x + bg_width//2 - result_text.get_width()//2, bg_y + 115))
    
    def is_showing_result(self):
        return not self.active and self.result is not None
    
    def reset(self):
        self.active = False
        self.result = None
        self.bar_position = 0