import json

def save_game(score, money, upgrades, story_data):
    data = {
        "score": score,
        "money": money,
        "upgrades": upgrades,
        "story": {
            "day": story_data["day"],
            "total_clients": story_data["total_clients"]
        }
    }
    with open("save.json", "w") as f:
        json.dump(data, f)


def load_game():
    try:
        with open("save.json", "r") as f:
            data = json.load(f)
            story_data = data.get("story", {"day": 1, "total_clients": 0})
            return (data["score"], data["money"], data["upgrades"],
                    story_data["day"], story_data["total_clients"])
    except:
        return 0, 0, {
            "stock": {"price": 20, "level": 0},
            "decor": {"price": 30, "level": 0},
            "fridge": {"price": 40, "level": 0},
            "employee": {"price": 60, "level": 0}
        }, 1, 0
