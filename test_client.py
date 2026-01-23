import random
import os

class Client:
    def __init__(self):
        self.image = self._choose_image()
        self.name = self._choose_name()
        self.request = random.choice([
            "burger-cheese",
            "cookie-chocolate",
            "cup-tea",
            "cup-coffee",
            "donut",
            "hot-dog",
            "ice-cream",
            "croissant",
            "soda",
            "sundae"
        ])

    def _choose_image(self):
        folder = "images/clients"
        images = [f for f in os.listdir(folder) if f.endswith(".png")]
        self.chosen_image = random.choice(images)
        return os.path.join(folder, self.chosen_image)

    def _choose_name(self):
        female_names = ["Alice", "Emma", "Lina", "Sofia", "Maya"]
        male_names = ["Adam", "Leo", "Yanis", "Noah", "Elias"]

        if "female" in self.chosen_image:
            return random.choice(female_names)
        else:
            return random.choice(male_names)
