class StoryManager:
    def __init__(self):
        self.day = 1
        self.total_clients_served = 0
        self.story_events = {
            1: {
                "title": "Jour 1 - Ouverture du Café",
                "message": [
                    "Bienvenue dans ton nouveau café !",
                    "Après des années de rêve, c'est enfin le grand jour.",
                    "",
                    "Objectif : Servir 1000 clients satisfaits",
                    "et devenir le Meilleur Café de la Ville !",
                    "",
                    "Bonne chance !"
                ]
            },
            2: {
                "title": "Jour 2 - Nouveau Mini-Jeu",
                "message": [
                    "Bravo pour ton premier jour !",
                    "À partir d'aujourd'hui, tu débloques un nouveau défi :",
                    "",
                    "🎯 Mini-Jeu : Café Parfait",
                    "",
                    "Appuie sur ESPACE pour y jouer.",
                    "Il sera disponible un jour sur deux !"
                ]
            },

            3: {
                "title": "Jour 3 - Premiers Habitués",
                "message": [
                    "Bravo ! Ton café commence à se faire connaître.",
                    "Certains clients deviennent des habitués...",
                    "",
                    "Continue comme ça !"
                ]
            },
            5: {
                "title": "Jour 5 - Nouveau Défi",
                "message": [
                    "Tu progresses bien !",
                    "Mais la concurrence est rude.",
                    "Il va falloir se démarquer !",
                    "",
                ]
            },
            10: {
                "title": "Jour 10 - Réputation Grandissante",
                "message": [
                    "Ton café est de plus en plus populaire !",
                    "Les clients réguliers sont fidèles.",
                    "",
                    "Objectif intermédiaire : 500 clients"
                ]
            },
            15: {
                "title": "Jour 15 - À Mi-Chemin",
                "message": [
                    "Déjà 15 jours que ton café est ouvert !",
                    "Tu es sur la bonne voie.",
                    "",
                    "Continue, la victoire approche !"
                ]
            },
            25: {
                "title": "VICTOIRE - Meilleur Café 2025 !",
                "message": [
                    "FÉLICITATIONS !",
                    "",
                    "Tu as atteint l'objectif de 1000 clients !",
                    "Ton café est désormais le plus réputé de la ville.",
                    "",
                    "🏆 TU AS GAGNÉ ! 🏆",
                    "",
                    "Merci d'avoir joué à Cozy Café !"
                ]
            }
        }
        
        self.regular_clients = {
            "Marc": {
                "name": "Marc le Businessman",
                "dialogues": [
                    "Mon café habituel svp ! J'ai une réunion importante.",
                    "Toujours aussi efficace ! Merci.",
                    "Ce café me sauve la vie chaque matin !"
                ],
                "favorite_items": ["cup-coffee", "croissant"]
            },
            "Lisa": {
                "name": "Lisa l'Étudiante",
                "dialogues": [
                    "Un thé et un cookie... J'ai mes examens demain...",
                    "Merci ! Ça va m'aider à réviser.",
                    "Votre café est mon refuge pendant les révisions !"
                ],
                "favorite_items": ["cup-tea", "cookie-chocolate"]
            },
            "Robert": {
                "name": "Robert le Retraité",
                "dialogues": [
                    "Ah, toujours un plaisir de venir ici !",
                    "Parfait comme d'habitude, merci jeune !",
                    "Votre sourire égaye mes journées !"
                ],
                "favorite_items": ["cup-coffee", "donut"]
            }
        }
    
    def add_client_served(self):
        self.total_clients_served += 1

    # Jour 1 → Jour 2 après 10 clients
        if self.day == 1 and self.total_clients_served >= 10:
            self.day = 2
            return True
    # Jour 2 → Jour 3 après 20 clients
        if self.day == 2 and self.total_clients_served >= 20:
            self.day = 3
            return True

    # Jour 3+ → un jour tous les 30 clients
        if self.day >= 3:
            seuil = 30 * (self.day - 2)  # Jour 3 = 30, Jour 4 = 60, Jour 5 = 90...
            if self.total_clients_served >= seuil:
                self.day += 1
                return True

        return False

    
    def get_current_event(self):
        if self.day in self.story_events:
            return self.story_events[self.day]
        return None
    
    def get_random_regular_dialogue(self, client_name):
        import random
        if client_name in self.regular_clients:
            dialogues = self.regular_clients[client_name]["dialogues"]
            return random.choice(dialogues)
        return None
    
    def is_regular_client_unlocked(self, client_name):
        unlock_days = {
            "Marc": 3,
            "Lisa": 7,
            "Robert": 12
        }
        return self.day >= unlock_days.get(client_name, 999)
    
    def get_progress_percentage(self):
        return min(100, (self.total_clients_served / 1000) * 100)
    
    def has_won(self):
        return self.total_clients_served >= 1000