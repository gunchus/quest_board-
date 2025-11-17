from flask import Flask, jsonify, send_file, abort, request, Response
import os
import random

app = Flask(__name__)

# Health and fitness quest templates
QUEST_TEMPLATES = {
    "cardio": [
        {"activity": "Run", "units": "minutes", "range": (10, 30)},
        {"activity": "Walk", "units": "minutes", "range": (15, 45)},
        {"activity": "Jump rope", "units": "minutes", "range": (5, 15)},
        {"activity": "Cycling", "units": "minutes", "range": (15, 40)},
        {"activity": "Swimming", "units": "minutes", "range": (10, 30)},
        {"activity": "Dancing", "units": "minutes", "range": (15, 30)},
    ],
    "strength": [
        {"activity": "Push-ups", "units": "reps", "range": (10, 50)},
        {"activity": "Squats", "units": "reps", "range": (15, 60)},
        {"activity": "Lunges", "units": "reps", "range": (10, 40)},
        {"activity": "Plank hold", "units": "seconds", "range": (30, 120)},
        {"activity": "Wall sits", "units": "seconds", "range": (30, 90)},
        {"activity": "Burpees", "units": "reps", "range": (10, 30)},
        {"activity": "Mountain climbers", "units": "reps", "range": (20, 60)},
        {"activity": "Sit-ups", "units": "reps", "range": (15, 50)},
        {"activity": "Pull-ups", "units": "reps", "range": (5, 20)},
    ],
    "flexibility": [
        {"activity": "Yoga session", "units": "minutes", "range": (10, 30)},
        {"activity": "Stretching routine", "units": "minutes", "range": (10, 20)},
        {"activity": "Foam rolling", "units": "minutes", "range": (5, 15)},
    ],
    "wellness": [
        {"activity": "Drink water", "units": "glasses", "range": (6, 10)},
        {"activity": "Meditate", "units": "minutes", "range": (5, 20)},
        {"activity": "Sleep", "units": "hours", "range": (7, 9)},
        {"activity": "Take deep breaths", "units": "cycles", "range": (5, 15)},
        {"activity": "Go outside for fresh air", "units": "minutes", "range": (10, 30)},
    ]
}

def generate_random_quests(count=5):
    """Generate random health and fitness quests"""
    quests = []
    quest_id = 1
    
    # Randomly select categories to ensure variety
    available_categories = list(QUEST_TEMPLATES.keys())
    random.shuffle(available_categories)
    
    for _ in range(count):
        # Pick a random category
        category = available_categories[_ % len(available_categories)]
        quest_template = random.choice(QUEST_TEMPLATES[category])
        
        # Generate random amount within the range
        amount = random.randint(quest_template["range"][0], quest_template["range"][1])
        
        quest = {
            "quest_id": quest_id,
            "title": f"{quest_template['activity']} Challenge",
            "description": f"Complete {amount} {quest_template['units']} of {quest_template['activity'].lower()}",
            "category": category,
            "status": "active"
        }
        quests.append(quest)
        quest_id += 1
    
    return quests

# Returns the quest board login/starting page
@app.route('/', methods=['GET'])
@app.route('/quest_board', methods=['GET'])
def quest_board_entry():
    return send_file("quest_board.html")

# Returns start html for specific quest
@app.route('/quest_board/quests/<quest_id>', methods=['GET'])
def quest_board_quest_id(quest_id: int):
    return send_file("quest_board.html")

# Shop items data
SHOP_ITEMS = {
    "avatars": [
        {"id": "avatar_1", "name": "Fitness Pro", "emoji": "🏋️", "price": 50, "type": "avatar"},
        {"id": "avatar_2", "name": "Yoga Master", "emoji": "🧘", "price": 50, "type": "avatar"},
        {"id": "avatar_3", "name": "Runner", "emoji": "🏃", "price": 50, "type": "avatar"},
        {"id": "avatar_4", "name": "Cyclist", "emoji": "🚴", "price": 75, "type": "avatar"},
        {"id": "avatar_5", "name": "Swimmer", "emoji": "🏊", "price": 75, "type": "avatar"},
        {"id": "avatar_6", "name": "Champion", "emoji": "🏆", "price": 100, "type": "avatar"},
        {"id": "avatar_7", "name": "Martial Artist", "emoji": "🥋", "price": 100, "type": "avatar"},
        {"id": "avatar_8", "name": "Boxer", "emoji": "🥊", "price": 100, "type": "avatar"},
    ],
    "cosmetics": [
        {"id": "border_1", "name": "Gold Border", "emoji": "✨", "price": 30, "type": "border", "color": "#ffd700"},
        {"id": "border_2", "name": "Silver Border", "emoji": "⭐", "price": 20, "type": "border", "color": "#c0c0c0"},
        {"id": "border_3", "name": "Bronze Border", "emoji": "🔶", "price": 10, "type": "border", "color": "#cd7f32"},
        {"id": "border_4", "name": "Rainbow Border", "emoji": "🌈", "price": 150, "type": "border", "color": "linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #8b00ff)"},
        {"id": "title_1", "name": "Beginner", "emoji": "🌱", "price": 5, "type": "title"},
        {"id": "title_2", "name": "Warrior", "emoji": "⚔️", "price": 50, "type": "title"},
        {"id": "title_3", "name": "Legend", "emoji": "👑", "price": 100, "type": "title"},
        {"id": "title_4", "name": "Master", "emoji": "🎖️", "price": 200, "type": "title"},
    ],
    "vip_crates": [
        {"id": "bronze_crate", "name": "Bronze VIP Crate", "emoji": "📦", "price": 100, "type": "crate", "vip_required": 1, "description": "Basic VIP crate with common rewards"},
        {"id": "silver_crate", "name": "Silver VIP Crate", "emoji": "🎁", "price": 250, "type": "crate", "vip_required": 2, "description": "Advanced VIP crate with uncommon and rare rewards"},
        {"id": "gold_crate", "name": "Gold VIP Crate", "emoji": "🏆", "price": 500, "type": "crate", "vip_required": 3, "description": "Premium VIP crate with epic and legendary rewards"},
        {"id": "platinum_crate", "name": "Platinum VIP Crate", "emoji": "💫", "price": 1000, "type": "crate", "vip_required": 5, "description": "Ultimate VIP crate with guaranteed legendary rewards"},
    ]
}

# VIP Crate system with probability-based rewards
VIP_CRATES = {
    "bronze_crate": {
        "id": "bronze_crate",
        "name": "Bronze VIP Crate",
        "emoji": "📦",
        "description": "Basic VIP crate with common rewards",
        "vip_level_required": 1,
        "cost": 100,
        "rewards": [
            {"item": "Common Avatar", "type": "avatar", "emoji": "👤", "probability": 0.50, "rarity": "common"},
            {"item": "Basic Border", "type": "border", "emoji": "⬜", "probability": 0.30, "rarity": "common"},
            {"item": "50 Bonus Points", "type": "points", "emoji": "💰", "value": 50, "probability": 0.15, "rarity": "uncommon"},
            {"item": "Epic Title", "type": "title", "emoji": "🎯", "probability": 0.05, "rarity": "rare"}
        ]
    },
    "silver_crate": {
        "id": "silver_crate",
        "name": "Silver VIP Crate",
        "emoji": "🎁",
        "description": "Advanced VIP crate with uncommon and rare rewards",
        "vip_level_required": 2,
        "cost": 250,
        "rewards": [
            {"item": "Rare Avatar", "type": "avatar", "emoji": "🦸", "probability": 0.40, "rarity": "uncommon"},
            {"item": "Premium Border", "type": "border", "emoji": "🔷", "probability": 0.30, "rarity": "uncommon"},
            {"item": "150 Bonus Points", "type": "points", "emoji": "💎", "value": 150, "probability": 0.20, "rarity": "rare"},
            {"item": "Legendary Title", "type": "title", "emoji": "👑", "probability": 0.08, "rarity": "epic"},
            {"item": "Mystery Reward", "type": "special", "emoji": "❓", "probability": 0.02, "rarity": "legendary"}
        ]
    },
    "gold_crate": {
        "id": "gold_crate",
        "name": "Gold VIP Crate",
        "emoji": "🏆",
        "description": "Premium VIP crate with epic and legendary rewards",
        "vip_level_required": 3,
        "cost": 500,
        "rewards": [
            {"item": "Epic Avatar", "type": "avatar", "emoji": "🌟", "probability": 0.35, "rarity": "rare"},
            {"item": "Diamond Border", "type": "border", "emoji": "💠", "probability": 0.25, "rarity": "epic"},
            {"item": "300 Bonus Points", "type": "points", "emoji": "🔥", "value": 300, "probability": 0.20, "rarity": "epic"},
            {"item": "Ultimate Title", "type": "title", "emoji": "⚡", "probability": 0.15, "rarity": "epic"},
            {"item": "Exclusive Avatar Pack", "type": "avatar_pack", "emoji": "🎭", "probability": 0.04, "rarity": "legendary"},
            {"item": "Jackpot 1000 Points", "type": "points", "emoji": "💸", "value": 1000, "probability": 0.01, "rarity": "legendary"}
        ]
    },
    "platinum_crate": {
        "id": "platinum_crate",
        "name": "Platinum VIP Crate",
        "emoji": "💫",
        "description": "Ultimate VIP crate with guaranteed legendary rewards",
        "vip_level_required": 5,
        "cost": 1000,
        "rewards": [
            {"item": "Legendary Avatar", "type": "avatar", "emoji": "🔱", "probability": 0.30, "rarity": "legendary"},
            {"item": "Cosmic Border", "type": "border", "emoji": "🌌", "probability": 0.25, "rarity": "legendary"},
            {"item": "500 Bonus Points", "type": "points", "emoji": "💵", "value": 500, "probability": 0.20, "rarity": "legendary"},
            {"item": "Divine Title", "type": "title", "emoji": "✨", "probability": 0.15, "rarity": "legendary"},
            {"item": "Ultimate Pack", "type": "ultimate_pack", "emoji": "🎪", "probability": 0.08, "rarity": "mythic"},
            {"item": "MEGA JACKPOT 5000 Points", "type": "points", "emoji": "🏅", "value": 5000, "probability": 0.02, "rarity": "mythic"}
        ]
    }
}

def open_crate(crate_id, user_vip_level):
    """Open a VIP crate and return a random reward based on probability"""
    if crate_id not in VIP_CRATES:
        return {"error": "Invalid crate ID"}
    
    crate = VIP_CRATES[crate_id]
    
    # Check VIP level requirement
    if user_vip_level < crate["vip_level_required"]:
        return {
            "error": f"VIP level {crate['vip_level_required']} required. Your level: {user_vip_level}",
            "required_level": crate["vip_level_required"],
            "current_level": user_vip_level
        }
    
    # Select reward based on probability
    rewards = crate["rewards"]
    random_value = random.random()
    cumulative_probability = 0.0
    
    for reward in rewards:
        cumulative_probability += reward["probability"]
        if random_value <= cumulative_probability:
            return {
                "success": True,
                "crate": crate["name"],
                "reward": reward,
                "message": f"You received: {reward['emoji']} {reward['item']}!"
            }
    
    # Fallback to last reward if somehow none selected
    return {
        "success": True,
        "crate": crate["name"],
        "reward": rewards[-1],
        "message": f"You received: {rewards[-1]['emoji']} {rewards[-1]['item']}!"
    }

# API endpoint to get randomly generated quests
@app.route('/api/quests', methods=['GET'])
def api_quests():
    # Generate random quests each time this endpoint is called
    count = request.args.get('count', default=5, type=int)
    count = min(count, 20)  # Limit to maximum 20 quests
    quests = generate_random_quests(count)
    return jsonify(quests)

# API endpoint to get shop items
@app.route('/api/shop', methods=['GET'])
def api_shop():
    return jsonify(SHOP_ITEMS)

# API endpoint to get VIP crates
@app.route('/api/vip/crates', methods=['GET'])
def api_vip_crates():
    return jsonify(VIP_CRATES)

# API endpoint to open a VIP crate
@app.route('/api/vip/crates/<crate_id>/open', methods=['POST'])
def api_open_crate(crate_id):
    data = request.get_json() or {}
    user_vip_level = data.get('vip_level', 0)  # Default to 0 if not provided
    
    result = open_crate(crate_id, user_vip_level)
    
    if "error" in result:
        return jsonify(result), 403
    
    return jsonify(result), 200

# API endpoint to get crate details
@app.route('/api/vip/crates/<crate_id>', methods=['GET'])
def api_crate_details(crate_id):
    if crate_id not in VIP_CRATES:
        return jsonify({"error": "Crate not found"}), 404
    
    return jsonify(VIP_CRATES[crate_id]), 200

# Serve static files - images
@app.route('/images/<image_name>', methods=['GET'])
def serve_images(image_name: str):
    image_type = image_name.split(".")[-1]
    current_path = os.getcwd()
    full_path = current_path + "/client/images/" + image_name
    if os.path.exists(full_path):
        return send_file(full_path, mimetype="image/" + image_type)
    abort(404, description=image_name + " not found")

# Serve static files - styles
@app.route('/styles/<style_name>', methods=['GET'])
def serve_styles(style_name: str):
    current_path = os.getcwd()
    full_path = current_path + "/client/styles/" + style_name
    if os.path.exists(full_path):
        return send_file(full_path, mimetype="text/css")
    abort(404, description=style_name + " not found")

# Serve static files - scripts
@app.route('/scripts/<script_name>', methods=['GET'])
def serve_scripts(script_name: str):
    current_path = os.getcwd()
    full_path = current_path + "/client/scripts/" + script_name
    if os.path.exists(full_path):
        return send_file(full_path, mimetype="application/javascript")
    abort(404, description=script_name + " not found")

if __name__ == '__main__':
    app.run(port=5002, debug=True)