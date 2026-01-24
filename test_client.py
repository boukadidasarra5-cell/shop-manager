import random
import os

class Client:
    def __init__(self):
        self.image = self._choose_image()
        self.name = self._choose_name()

        # Liste des items possibles
        possible_items = [
            "burger-cheese",
            "burger-double",
            "burger-cheese-double",
            "cookie-chocolate",
            "chinese",
            "corn-dog",
            "fries",
            "maki-vegetable",
            "pizza",
            "cup-tea",
            "cup-coffee",
            "donut",
            "hot-dog",
            "ice-cream",
            "croissant",
            "soda",
            "sundae"
        ]

        # 🌟 RANDOM : 70% de chance d’un seul item, 30% d’un menu
        if random.random() < 0.7:
            # Un seul item
            self.request = [random.choice(possible_items)]
        else:
            # Un menu de 2 à 3 items
            count = random.randint(2, 3)
            self.request = random.sample(possible_items, count)

        # 🌸 Patience
        self.patience = 100

    def _choose_image(self):
        folder = "images/clients"
        images = [f for f in os.listdir(folder) if f.endswith(".png")]
        self.chosen_image = random.choice(images)
        return os.path.join(folder, self.chosen_image)

    def _choose_name(self):
        female_names = ["Alice", "Emna", "Lina", "Sofia", "Maya", "Mouna"]
        male_names = ["Adam", "Leo", "Yanis", "Sami", "Elias", "Macron"]

        if "female" in self.chosen_image:
            return random.choice(female_names)
        else:
            return random.choice(male_names)
