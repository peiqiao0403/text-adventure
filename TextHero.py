import sys
import random
import math
import time
import json
from threading import Thread


GREEN = "\033[38;2;0;255;0m"
ITEM_COLOR = "\033[38;2;255;255;0m"  # Yellow
RESET = "\033[38;2;0;255;0m"  # Reset color back to default
BLUE = "\033[38;2;0;255;255m"         # Information, navigation
RED = "\033[38;2;255;0;0m"          # Damage, danger
COMBAT_COLOR = "\033[38;2;255;100;50m"  # Combat, action

class static_slider(Thread):
    def __init__(self, delay: int):
        """A class which runs a visual slider and return a number up to 29. 
        Use .kill variable to end the process, then wait delay + 0.01 to be sure you get a good result."""
        Thread.__init__(self)
        self.daemon = True
        self.delay = delay
        self.kill = False
        self.result = 0
    
    def run(self):
        x = 0
        y = 1
        while True:
            x += y
            if x == 28: y = -1  # noqa: E701
            if x == 1: y = 1  # noqa: E701
            STR = (" " * (x - 1)) + "^" + (" " * (29 - (x + 1)))
            print("\033[101m        \033[103m     \033[102m   \033[103m     \033[101m        \033[0m")
            print(STR)
            time.sleep(self.delay)
            print("\033[F\033[F", end="")
            if self.kill: break  # noqa: E701
        self.result = x

def run_slider(scale: int, offset: int, delay = 0.02):
    """Returns a percentage for scaling numbers.
    Scale is the difference in between 2 spots.
    Offset is a number added to the result to raise the maximum & minimum percent."""
    main = static_slider(delay)
    main.start()
    input(GREEN + "Press Enter to stop the slider!")
    main.kill = True
    time.sleep(delay + 0.01)
    print()
    return round(100 * (1 - abs(main.result - 15) / (100 / scale))) + offset

def save_game():
    """Save the current game state to a file"""
    # Create comprehensive game state dictionary
    game_state = {
        "player": player,
        "inventory": inventory,
        "player_equipment": player_equipment,
        "currentRoom": currentRoom,
        "defeated_bosses": list(defeated_bosses),
        "rooms": rooms,
        "locked_spells": locked_spells.copy(),
    }
    
    # Convert to string using custom serialization
    game_data = str(game_state).replace('\\', '\\\\').replace('\n', '\\n')
    
    # Save to file
    with open("savegame.txt", "w") as f:
        f.write(game_data)
    
    print_slow("Game saved successfully!")

def load_game():
    """Load a saved game state from file"""
    try:
        # Read from file
        with open("savegame.txt", "r") as f:
            save_data = f.read()

        # Convert string back to dictionary
        game_state = eval(save_data)
        
        # Restore game state
        global player, inventory, player_equipment, currentRoom, defeated_bosses, rooms, locked_spells
        player = game_state["player"]
        inventory = game_state["inventory"]
        player_equipment = game_state["player_equipment"]
        currentRoom = game_state["currentRoom"]
        defeated_bosses = set(game_state["defeated_bosses"])
        rooms = game_state["rooms"]
        player["spells"] = game_state["player"]["spells"]
        inventory = game_state["inventory"]
        rooms = game_state["rooms"]
        # Restore spells
        locked_spells = game_state["locked_spells"]
        
        print_slow("Game loaded successfully!")
        return True
    except Exception as e:
        print_slow(f"Error loading game: {str(e)}")
        return False

def count_visible_chars(text):
    count = 0
    in_escape = False
    for char in text:
        if char == '\x1b':
            in_escape = True
        elif in_escape and char == 'm':
            in_escape = False
        elif not in_escape:
            count += 1
    return count

def clear_screen():
    sys.stdout.write("\033[2J\033[H")

def display_credits():
    """Display the end credits when reaching the final room"""
    clear_screen()
    print_credits("\n" + "="*50+"\n")
    print_credits(f"{GREEN}CONGRATULATIONS!{RESET}\n")
    print_credits(f"You've completed Text Hero!\n")
    print_credits("="*50 + "\n")
    print_credits(r'''
      _____         _      _   _
     |_   _|____  _| |_   | | | | ___ _ __ ___
       | |/ _ \ \/ / __|  | |_| |/ _ \ '__/ _ \
       | |  __/>  <| |_   |  _  |  __/ | | (_) |
       |_|\___/_/\_\\__|  |_| |_|\___|_|  \___/'''   
    )
    print()
    # Credits scroll
    f"\n",
    f"{BLUE}Development Team:{RESET}\n",
    f"Lead Developer & Creator: {BLUE}Chales{RESET}\n",
    f"Developer: {BLUE}arnesito{RESET}\n",
    f"Developer & Designer: {BLUE}Moltd{RESET}\n",
    "\n",
    f"{BLUE}DLC Development Team:{RESET}\n",
    f"DLC Developer: {BLUE}arnesito{RESET}\n",
    "\n"
    f"{BLUE}Quality Assurance Team:{RESET}\n",
    f"Bug Finder & Patcher: {BLUE}JayMcCray11{RESET}\n",
    "\n",
    f"{BLUE}Playtesting Team:{RESET}\n",
    f"{GREEN}David Sucks At Life{RESET}\n",
    f"{GREEN}Bee1949{RESET}\n",
    f"{GREEN}Not Guy Stew{RESET}\n",
    f"{GREEN}Vroom Vroom Snail{RESET}\n",
    "\n",
    f"{BLUE}Game Features:{RESET}\n",
    "10 Unique Classes\n",
    "340 Rooms to Explore\n",
    "11 Levels to Defeat\n",
    "50+ Items to Collect\n",
    "200 Monsters to Battle\n",
    "Leveling up system\n",
    "\n",
    f"{BLUE}Technical Details:{RESET}\n",
    "Custom ANSI Color System\n",
    "Dynamic Combat Engine\n",
    "Save/Load System\n",
    "Crafting System\n",
    "\n",
    f"{BLUE}Thanks for Playing!{RESET}\n",
    f"{BLUE}press enter to quit{RESET}"
    input()
    quit()
    
    screen_width = 50
    for line in credits:
        visible_length = count_visible_chars(line)
        padding = " " * ((screen_width - visible_length) // 2)
        centered_line = padding + line
        print_credits(centered_line)
        if line.strip() == "":
            time.sleep(0.5)  # Longer pause for empty lines
        else:
            time.sleep(0.1)
        
def display_DLC_credits():
    """Display the end credits when reaching the final room"""
    clear_screen()
    print_credits("\n" + "="*50+"\n")
    print_credits(f"{GREEN}CONGRATULATIONS!{RESET}\n")
    print_credits(f"You've completed Text Hero!\n")
    print_credits("="*50 + "\n")
    print_credits(r'''
      _____         _      _   _
     |_   _|____  _| |_   | | | | ___ _ __ ___
       | |/ _ \ \/ / __|  | |_| |/ _ \ '__/ _ \
       | |  __/>  <| |_   |  _  |  __/ | | (_) |
       |_|\___/_/\_\\__|  |_| |_|\___|_|  \___/
                  Salvation Edition'''   
    )
    # Credits scroll
    print_credits(f"\n")
    print_credits(f"{BLUE}Development Team:{RESET}\n")
    print_credits(f"Lead Developer & Creator: {BLUE}Chales{RESET}\n")
    print_credits(f"Developer: {BLUE}arnesito{RESET}\n")
    print_credits(f"Developer & Designer: {BLUE}Moltd{RESET}\n")
    print_credits("\n")
    print_credits(f"{BLUE}DLC Development Team:{RESET}\n")
    print_credits(f"DLC Developer: {BLUE}arnesito{RESET}\n")
    print_credits("\n")
    print_credits(f"{BLUE}Quality Assurance Team:{RESET}\n")
    print_credits(f"Bug Finder & Patcher: {BLUE}JayMcCray11{RESET}\n")
    print_credits("\n")
    print_credits(f"{BLUE}Playtesting Team:{RESET}\n")
    print_credits(f"{GREEN}David Sucks At Life{RESET}\n")
    print_credits(f"{GREEN}Bee1949{RESET}\n")
    print_credits(f"{GREEN}Not Guy Stew{RESET}\n")
    print_credits(f"{GREEN}Vroom Vroom Snail{RESET}\n")
    print_credits("\n")
    print_credits(f"{BLUE}Game Features:{RESET}\n")
    print_credits("10 Unique Classes\n")
    print_credits("340 Rooms to Explore\n")
    print_credits("11 Levels to Defeat\n")
    print_credits("50+ Items to Collect\n")
    print_credits("200 Monsters to Battle\n")
    print_credits("Leveling up system\n")
    print_credits("\n")
    print_credits(f"{BLUE}Technical Details:{RESET}\n")
    print_credits("Custom ANSI Color System\n")
    print_credits("Dynamic Combat Engine\n")
    print_credits("Save/Load System\n")
    print_credits("Crafting System\n")
    print_credits("\n")
    print_credits(f"{BLUE}Thanks for Playing!{RESET}\n")
    print_credits(f"{BLUE}press enter to quit{RESET}")
    input()
    quit()
    
    screen_width = 50
    for line in credits:
        visible_length = count_visible_chars(line)
        padding = " " * ((screen_width - visible_length) // 2)
        centered_line = padding + line
        print_credits(centered_line)
        if line.strip() == "":
            time.sleep(0.5)  # Longer pause for empty lines
        else:
            time.sleep(0.1)

# Define armor tiers and their properties
ARMOR_TIERS = {
    'leather': {'defense': 1},
    'chainmail': {'defense': 3},
    'iron': {'defense': 5},
    'mythril': {'defense': 7},
    'adamantite': {'defense': 10},
    'hallowed': {'defense': 12},
    'godslayer': {'defense': 15}
}

# Add sword tiers
SWORD_TIERS = {
    'wooden': {'damage': 5},
    'iron': {'damage': 10},
    'steel': {'damage': 15},
    'mythril': {'damage': 20},
    'adamantite': {'damage': 25},
    'hallowed': {'damage': 35},
    'godslayer': {'damage': 50}
}
def print_credits(text):
    
    # Split text into parts that are either ANSI sequences or regular text
    parts = []
    current_part = ""
    i = 0
    
    while i < len(text):
        # Check if we're at the start of an ANSI sequence
        if text[i:i+2] == "\033[":
            # If we have regular text before this sequence, add it
            if current_part:
                parts.append(current_part)
                current_part = ""
            
            # Find the end of the ANSI sequence
            j = text.find("m", i)
            if j != -1:
                parts.append(text[i:j+1])
                i = j + 1
                continue
        
        # Add the current character to the regular text part
        current_part += text[i]
        i += 1
    
    # Add any remaining regular text
    if current_part:
        parts.append(current_part)
    
    # Print each part slowly, but keep ANSI sequences together
    for part in parts:
        if part.startswith("\033["):
            # ANSI sequence - print all at once
            sys.stdout.write(part)
            sys.stdout.flush()
        else:
            # Regular text - print character by character with proper color
            for char in part:
                sys.stdout.write(char)  # Write the character first
                sys.stdout.flush()
                time.sleep(0.005)
    
    
def print_slow(text):
    
    # Split text into parts that are either ANSI sequences or regular text
    parts = []
    current_part = ""
    i = 0
    
    while i < len(text):
        # Check if we're at the start of an ANSI sequence
        if text[i:i+2] == "\033[":
            # If we have regular text before this sequence, add it
            if current_part:
                parts.append(current_part)
                current_part = ""
            
            # Find the end of the ANSI sequence
            j = text.find("m", i)
            if j != -1:
                parts.append(text[i:j+1])
                i = j + 1
                continue
        
        # Add the current character to the regular text part
        current_part += text[i]
        i += 1
    
    # Add any remaining regular text
    if current_part:
        parts.append(current_part)
    
    # Print each part slowly, but keep ANSI sequences together
    for part in parts:
        if part.startswith("\033["):
            # ANSI sequence - print all at once
            sys.stdout.write(part)
            sys.stdout.flush()
        else:
            # Regular text - print character by character with proper color
            for char in part:
                sys.stdout.write(char)  # Write the character first
                sys.stdout.flush()
                time.sleep(0.00065)
    
    print()  # Add newline at end

MARKET_ITEMS = {
    'health potion': {'price': 30, 'description': 'Restores 30 health'},
    'mana potion': {'price': 30, 'description': 'Restores 30 mana'},
    'leather helmet': {'price': 50, 'description': 'Basic head protection'},
    'leather chestplate': {'price': 70, 'description': 'Basic chest protection'},
    'leather pants': {'price': 60, 'description': 'Basic leg protection'},
    'leather boots': {'price': 40, 'description': 'Basic foot protection'}
}
# Define armor slots and their available items
ARMOR_SLOTS = {
    'helmet': ['leather', 'chainmail', 'iron', 'mythril', 'adamantite', 'hallowed', 'godslayer'],
    'chestplate': ['leather', 'chainmail', 'iron', 'mythril', 'adamantite', 'hallowed', 'godslayer'],
    'pants': ['leather', 'chainmail', 'iron', 'mythril', 'adamantite', 'hallowed', 'godslayer'],
    'boots': ['leather', 'chainmail', 'iron', 'mythril', 'adamantite', 'hallowed', 'godslayer']
}

MONSTER_TYPES = {
    'normal': {
        'names': ['Orc', 'Goblin', 'Zombie', 'Ghoul'],  # List of possible monster names
        'health': 50,
        'attack_min': 5,
        'attack_max': 15,
        'gold_drop_range': (30, 60),
        "exp_drop_range": (3, 5),
        'item_drop_chance': 0.2
    },
    'demon': {
        'names': ['Demon', 'Incubus', 'Succubus', 'Poltergeist', 'Oni', 'Rakshaka'],
        'health': 100,
        'attack_min': 5,
        'attack_max': 15,
        'gold_drop_range': (60, 90),
        "exp_drop_range": (15, 30),
        'item_drop_chance': 0
    },
    'boss': {
        'name': 'Boss Monster',
        'health': 200,
        'attack_min': 25,
        'attack_max': 35,
        'gold_drop_range': (100, 150),
        "exp_drop_range": (25, 50),
        'item_drop_chance': 1
    },
    'vampire': {
        'name': 'Count Dracula',
        'health': 250,
        'attack_min': 35,
        'attack_max': 45,
        'gold_drop_range': (500, 1000),
        'exp_drop_range': (50, 100),
        'item_drop_chance': 1,
        'lifesteal_range': (5, 10)
    },
    'demon king lucifer': {
        'name': 'Demon King Lucifer',
        'health': 300,
        'attack_min': 50,
        'attack_max': 75,
        'gold_drop_range': 1000,
        "exp_drop_range": 500,
        'item_drop_chance': 0
    },
    'demon king asmodeus': {
        'name': 'Demon King Asmodeus',
        'health': 400,
        'attack_min': 50,
        'attack_max': 85,
        'gold_drop_range': 1000,
        "exp_drop_range": 500,
        'item_drop_chance': 0
    },
    'demon king leviathan': {
        'name': 'Demon King Leviathan',
        'health': 500,
        'attack_min': 75,
        'attack_max': 100,
        'gold_drop_range': 1000,
        "exp_drop_range": 500,
        'item_drop_chance': 0
    },
    'demon king belphegor': {
        'name': 'Demon King Belphegor',
        'health': 600,
        'attack_min': 80,
        'attack_max': 100,
        'gold_drop_range': 1000,
        "exp_drop_range": 500,
        'item_drop_chance': 0
    },
    'demon king beelzebub': {
        'name': 'Demon King Beelzebub',
        'health': 750,
        'attack_min': 150,
        'attack_max': 200,
        'gold_drop_range': 1000,
        "exp_drop_range": 500,
        'item_drop_chance': 0
    },
    'demon king mammon': {
        'name': 'Demon King Mammon',
        'health': 1000,
        'attack_min': 175,
        'attack_max': 225,
        'gold_drop_range': 1000,
        "exp_drop_range": 500,
        'item_drop_chance': 0
    },
    'demon king satan': {
        'name': 'Demon King Satan',
        'health': 1000,
        'attack_min': 300,
        'attack_max': 400,
        'gold_drop_range': 1000,
        "exp_drop_range": 1000,
        'item_drop_chance': 0
    }
}

EXP_TO_GET_TO_LEVEL2 = {
    1: 0,
    2: 8,
    3: 16,
    4: 24,
    5: 40,
    6: 48,
    7: 60,
    8: 72,
    9: 84,
    10: 100,
    11: 120,
    12: 140,
    13: 160,
    14: 180,
    15: 240,
    16: 280,
    17: 320,
    18: 380,
    19: 440,
    20: 500,
    21: 600,
    22: 700,
    23: 800,
    24: 900,
    25: 1000,
    26: 1100,
    27: 1200,
    28: 1300,
    29: 1400,
    30: 1500,
    31: 1600,
    32: 1700,
    33: 1800,
    34: 1900,
    35: 2000,
    36: 2100,
    37: 2200,
    38: 2300,
    39: 2400,
    40: 2500,
    41: 2600,
    42: 2700,
    43: 2800,
    44: 2900,
    45: 3000,
    46: 3200,
    47: 3400,
    48: 3600,
    49: 3800,
    50: 4000
}

EXP_TO_GET_TO_LEVEL = {
    0: 1,
    8: 2,
    16: 3,
    26: 4,
    37: 5,
    48: 6,
    60: 7,
    72: 8,
    84: 9,
    100: 10,
    120: 11,
    140: 12,
    160: 13,
    180: 14,
    240: 15,
    280: 16,
    320: 17,
    380: 18,
    440: 19,
    500: 20,
    600: 21,
    700: 22,
    800: 23,
    900: 24,
    1000: 25,
    1100: 26,
    1200: 27,
    1300: 28,
    1400: 29,
    1500: 30,
    1600: 31,
    1700: 32,
    1800: 33,
    1900: 34,
    2000: 35,
    2100: 36,
    2200: 37,
    2300: 38,
    2400: 39,
    2500: 40,
    2600: 41,
    2700: 42,
    2800: 43,
    2900: 44,
    3000: 45,
    3200: 46,
    3400: 47,
    3600: 48,
    3800: 49,
    4000: 50
}

LEVEL_IMPROVEMENTS = {
    1: 1,
    2: 1.05,
    3: 1.1,
    4: 1.15,
    5: 1.2,
    6: 1.25,
    7: 1.3,
    8: 1.35,
    9: 1.4,
    10: 1.45,
    11: 1.5,
    12: 1.55,
    13: 1.6,
    14: 1.65,
    15: 1.7,
    16: 1.75,
    17: 1.8,
    18: 1.85,
    19: 1.9,
    20: 2,
    21: 2.1,
    22: 2.2,
    23: 2.3,
    24: 2.4,
    25: 2.5,
    26: 2.6,
    27: 2.7,
    28: 2.8,
    29: 2.9,
    30: 3,
    31: 3.1,
    32: 3.2,
    33: 3.3,
    34: 3.4,
    35: 3.5,
    36: 3.6,
    37: 3.7,
    38: 3.8,
    39: 3.9,
    40: 4,
    41: 4.1,
    42: 4.2,
    43: 4.3,
    44: 4.4,
    45: 4.5,
    46: 4.6,
    47: 4.7,
    48: 4.8,
    49: 4.9,
    50: 5
}

ARMOR_IMPROVEMENTS = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 7,
    9: 8,
    10: 9,
    11: 10,
    12: 11,
    13: 12,
    14: 13,
    15: 14,
    16: 15,
    17: 16,
    18: 17,
    19: 18,
    20: 20
}

classes = {
    "Warrior": {
        "health": 120, 
        "armor": 0, 
        "mana": 30, 
        "spells": {
            "slash": [15, 20], 
            "mordschlang": [10, 15]
            }, 
        "attack": 25
    },

    "Mage": {
        "health": 80, 
        "armor": 0, 
        "mana": 100, 
        "spells": {
            "fireball": [20, 30], 
            "boulder": [25, 35]
            }, 
        "attack": 20
    },

    "Rogue": {
        "health": 100, 
        "armor": 0, 
        "mana": 50, 
        "spells": {
            "back stab": [20, 25], 
            "knife throw": [10, 15]
            }, 
        "attack": 20
        },

    "Healer": {
        "health": 150, 
        "armor": 0, 
        "mana": 45, 
        "spells": {
            "minor heal": [15, 20], 
            "divine retribution": [20, 30]
            }, 
        "attack": 12
        },

    "Archer": {
        "health": 110, 
        "armor": 0, 
        "mana": 20, 
        "spells": {
            "bleeding arrow": [25, 25], 
            "double shot": [40, 40]
            }, 
        "attack": 20
        },
    
    "Vampire": {
        "health": 120,
        "armor": 0,
        "mana": 100,
        "spells": {
            "lifesteal": [25, 30],
            "blood bomb": [25, 50]
        },
        "attack": 30
    }
}

class_to_get_to_tier_2 = {
    "Warrior": "Paladin",
    "Mage": "Archmage",
    "Rogue": "Assassin",
    "Healer": "Priest",
    "Archer": "Ranger"
}

class_tier_2 = {
    "Paladin": "divine shield",
    "Archmage": "eternity",
    "Assassin": "supernova",
    "Priest": "heal",
    "Ranger": "phantasm"
}

spells_tier_2 = {
    "Paladin": {"divine shield": [0, 15]},
    "Archmage": {"eternity": [20, 90]},
    "Assassin": {"supernova": [20, 25]},
    "Priest": {"heal": [25, 50]},
    "Ranger": {"phantasm": [20, 50]},
    "Vampire": {"blood bomb": [25, 50],"lifesteal": [25, 30]}
}

locked_spells = {
    "Warrior": {'finishing blow': [20, 30], 'stun strike': [15, 20]},
    "Mage": {'water bolt': [15, 10], 'thunder zapper': [20, 15]},
    "Rogue": {'stealth': [0, 10], 'stealth strike': [25, 20]},
    "Healer": {'divine shield': [0, 15], "spear of justice": [20, 35]},
    "Archer": {'bleeding arrow': [30, 20], 'binding shot': [15, 15]},
    "Vampire": {'blood spear': [30, 65], 'haemolacria': [50, 100]},
    "Paladin": {"holy strike": [25, 50], "healing pool": [10, 10]},
    "Archmage": {"tidal wave": [15, 30], "kamehameha": [50, 125]},
    "Assassin": {"Assassinate": [20, 40], "ultrakill": [40, 80]},
    "Priest": {'great heal': [50, 75], "holy cleansing": [20, 10]},
    "Ranger": {"arrow of light": [10, 25], "midas prime": [25, 60]}
}

class HelpSystem:
    def __init__(self):
        self.pages = {
            'commands': '''\nCommands Reference\n=================\nBasic Commands:\n- go [direction]     - Move character\n- get [item]         - Pick up items\n- use [item]         - Use items\n- help              - Show this menu\n- remove [slot]      - Remove armor from slot\n- equip [type] [slot]- Equip armor in slot\n- list              - Show market items\n- buy [item]        - Buy from market\n- sell [item]       - Sell to market\n''',
            'classes': '''\nCharacter Classes\n================\n┌─────────┬───────┬────┬────┬───────────────┬────────┬──────────────┐\n│ Class   │Health │Mana│Atk │Spell          │Effect  │Spell Cost    │\n├─────────┼───────┼────┼────┼───────────────┼────────┼──────────────┤\n│ Warrior │ 120   │ 30 │ 25 │ Slash         │ +10 dmg│ 10 Mana      │\n│ Mage    │ 80    │100 │ 20 │ Fireball      │ +30 dmg│ 40 Mana      │\n│ Rogue   │ 100   │ 50 │ 20 │ back stab     │ +20 dmg│ 25 Mana      │\n│ Healer  │ 150   │ 45 │ 12 │ Circle Heal   │ +30 HP │ 35 Mana      │\n│ Archer  │ 110   │ 20 │ 20 │ Bleeding Arrow│ +25 dmg│ 25 Mana      │\n└─────────┴───────┴────┴────┴───────────────┴────────┴──────────────┘\n''',
            'help': '''\nThe help system provides detailed information about different aspects of the game.\nAvailable commands:\n- help              : Shows this help menu\n- help commands     : Shows basic game commands\n- help classes      : Shows character class information\n- help market       : Shows market commands\nNavigation:\n- Use 'help' alone to see this menu\n- Use 'help <page>' to view a specific page\n- Type 'help' at any time to access the help system\n''',
            'market': '''\nMarket Commands\n==============\n- buy [item]    : Purchase an item from the market\n- sell [item]   : Sell an item to the market\n- list          : Show available items and prices\n'''
        }
        self.current_page = 'help'

    def display_help(self, page=None):
        """Display the help system, optionally showing a specific page"""
        if page is None:
            page = "help"
        if page in self.pages:
            self.current_page = page
            print_slow(f"\n=== Help System ({self.current_page}) ===")
            print_slow(self.pages[self.current_page])
            print_slow("\nAvailable Pages:")
            for p in self.pages.keys():
                status = "*" if p == self.current_page else " "
                print_slow(f"- [{status}] {p}")
            print_slow("- Type 'help <page>' to view a different page")
            print_slow("=============================")

    print()
    sys.stdout.write("\033[F")

def showInstructions():
    """Only shown when help isn't used"""
    print_slow('''\nText Hero\n=========\nType 'help' for detailed game information\n---------------------------''')

def showHelp(page=None):
    """Global function to interface with the HelpSystem class"""
    global help_system
    help_system.display_help(page)
    return True  # Prevent instructions from showing

def showAvailableDirections(room):
    """Show all available directions for the current room with destination room numbers."""
    directions = []
    if 'north' in room:
        directions.append(f"  north: {BLUE}{room['north']}{RESET}")
    if 'south' in room:
        directions.append(f"  south: {BLUE}{room['south']}{RESET}")
    if 'east' in room:
        directions.append(f"  east: {BLUE}{room['east']}{RESET}")
    if 'west' in room:
        directions.append(f"  west: {BLUE}{room['west']}{RESET}")
    if 'down' in room:
        directions.append(f"  down: {BLUE}{room['down']}{RESET}")
    if 'up' in room:
        directions.append(f"  up: {BLUE}{room['up']}{RESET}")
    return "\n".join(directions)

def showStatus():
    print_slow('You are in ' + BLUE+currentRoom+RESET)
    print_slow('Available directions:')
    print_slow(showAvailableDirections(rooms[currentRoom]))
    print_slow(f'Health: {player["health"]}')
    print_slow(f'Armor: {player["armor"]}')
    print_slow(f'Mana: {player["mana"]}')
    print_slow(f'Gold: {player["gold"]}')
    print_slow(f'Class: {BLUE}{player["class"]}{RESET}')
    print_slow(f'Secondary Class: {BLUE}{player["class 2"]}{RESET}')
    print_slow(f'Level: {player["level"]}')
    print_slow(f'Exp: {player["exp"]}')
    print_slow('Equipped Armor:')
    for slot, item in player_equipment.items():
        if item:
            print_slow(f'- {slot}: {ITEM_COLOR}{item}{RESET}')
    show_inventory()
    if "lore" in rooms[currentRoom]:
        print_slow(f"{rooms[currentRoom]['lore']}{RESET}\n")
    if "hint" in rooms[currentRoom]:
        print_slow(f"{BLUE}{rooms[currentRoom]['hint']}{RESET}")
    if "item" in rooms[currentRoom]:
        if isinstance(rooms[currentRoom]["item"], list):
            items = rooms[currentRoom]["item"]
            if len(items) == 1:
                print_slow(f"{GREEN}You see a{RESET} {ITEM_COLOR}{items[0]}{RESET}")
            else:
                formatted_items = [f"{ITEM_COLOR}{item}{RESET}" for item in items]
                if len(formatted_items) == 2:
                    item_str = " and ".join(formatted_items)
                else:
                    item_str = ", ".join(formatted_items[:-1]) + f" and {formatted_items[-1]}"
                print_slow(f"{GREEN}You see{RESET} {item_str}")
        else:
            print_slow(f"{GREEN}You see a{RESET} {ITEM_COLOR}{rooms[currentRoom]['item']}{RESET}")
    print_slow("---------------------------")

def print_slow_list(tag, items):
    print_slow(f"{tag}: {ITEM_COLOR}{', '.join(map(str, items))}{RESET}")

def get_tier_value(tier):
    """Helper function to determine the value/strength of a tier"""
    tier_values = {
        'leather': 1,
        'chainmail': 2,
        'iron': 3,
        'wooden': 1,
        'steel': 2,
        'mythril': 4
    }
    return tier_values.get(tier, 0)

def find_best_equipment(slot=None):
    """Find the best available equipment for given slot or all slots"""
    best_equipment = {}
    
    # Function to find best item for a specific slot
    def find_best_for_slot(slot):
        best_tier = None
        best_tier_value = -1
        
        for item in inventory:
            if slot == 'sword' and item.endswith('sword'):
                tier = item.split(' ')[0]
                tier_value = get_tier_value(tier)
                if tier_value > best_tier_value:
                    best_tier = tier
                    best_tier_value = tier_value
            elif slot != 'sword' and item.endswith(slot):
                tier = item.split(' ')[0]
                tier_value = get_tier_value(tier)
                if tier_value > best_tier_value:
                    best_tier = tier
                    best_tier_value = tier_value
        
        return best_tier

    if slot:
        # Find best equipment for specific slot
        best_tier = find_best_for_slot(slot)
        if best_tier:
            best_equipment[slot] = best_tier
    else:
        # Find best equipment for all slots
        for slot in list(ARMOR_SLOTS.keys()) + ['sword']:
            best_tier = find_best_for_slot(slot)
            if best_tier:
                best_equipment[slot] = best_tier
    
    return best_equipment

def equip_armor(slot=None, item_type=None):
    """Enhanced equip function that can automatically equip best gear"""
    if not slot:
        # Auto-equip best available equipment for all slots
        best_equipment = find_best_equipment()
        if not best_equipment:
            return "No equipment available to equip!"
        results = []
        for slot, tier in best_equipment.items():
            result = equip_armor(slot, tier)
            results.append(result)
        return "\n".join(filter(None, results))  # Filter out None/empty results
    
    if not item_type:
        # Auto-equip best available equipment for specific slot
        best_equipment = find_best_equipment(slot)
        if not best_equipment:
            return f"No equipment available for {slot}!"
        item_type = best_equipment[slot]
    
    # Original equip logic
    if slot not in ARMOR_SLOTS and slot != 'sword':
        return "Invalid equipment slot!"

    # Handle sword equipping
    if slot == 'sword':
        item_name = f"{item_type} sword"
        if item_name not in inventory:
            return f"You don't have {item_name}!"
        
        # Remove old sword's damage bonus if one is equipped
        if player_equipment['sword']:
            old_tier = player_equipment['sword'].split(' ')[0]
            player['attack'] -= SWORD_TIERS[old_tier]['damage']
        
        # Equip new sword
        player_equipment['sword'] = item_name
        inventory.remove(item_name)
        damage_bonus = SWORD_TIERS[item_type]['damage']
        player['attack'] += damage_bonus
        return f"Equipped {item_name} (+{damage_bonus} attack)"

    # Handle armor equipping
    item_name = f"{item_type} {slot}"
    if item_name not in inventory:
        return f"You don't have {item_type} {slot}!"
    current_item = player_equipment[slot]
    if current_item:
        old_tier = current_item.split(' ')[0]
        player["armor"] -= ARMOR_TIERS[old_tier]['defense']
        inventory.append(current_item)
    player_equipment[slot] = item_name
    inventory.remove(item_name)
    defense_bonus = ARMOR_TIERS[item_type]['defense']
    player["armor"] += defense_bonus
    return f"Equipped {item_type} {slot} (+{defense_bonus} defense)"


def remove_armor(slot=None):
    """Remove armor or sword from specified slot, or all slots if none specified"""
    global player_equipment
    
    if slot is None:
        # Remove all equipment
        results = []
        for equipped_slot, item in player_equipment.items():
            if item:  # Only try to remove if there's equipment in the slot
                results.append(remove_armor(equipped_slot))
        return "\n".join(results) if results else "No equipment to remove!"
    
    if slot not in ARMOR_SLOTS and slot != 'sword':
        return "Invalid equipment slot!"

    current_item = player_equipment[slot]
    if not current_item:
        return f"No equipment in {slot} slot!"

    # Handle sword removal
    if slot == 'sword':
        item_type = current_item.split(' ')[0]
        damage_bonus = SWORD_TIERS[item_type]['damage']
        player['attack'] -= damage_bonus
        inventory.append(current_item)
        player_equipment[slot] = None
        return f"Removed {current_item} (-{damage_bonus} attack)"

    # Handle armor removal
    item_type = current_item.split(' ')[0]
    defense_bonus = ARMOR_TIERS[item_type]['defense']
    player["armor"] -= defense_bonus
    inventory.append(current_item)
    player_equipment[slot] = None
    return f"Removed {current_item} (-{defense_bonus} defense)"

rooms = {
    '1-1': {
        "east": '1-2',
        "item": "health potion",
        'lore': 'You have recieved a message: CLEANSE THE TOWER OF DEMONS',
        'hint': 'In this game, you use cardinal directions to travel. There are some keyboard shortcuts. EG - n for north, s for south, e for east, w for west.'
    },
    '1-2': {
        'north': '1-3',
        'west': '1-1',
    },
    '1-3': {
        'west': '1-4',
        'south': '1-2',
        'item': 'wooden sword',
        'hint': 'To equip something, you type in (equip (itemname))'
    },
    '1-4': {
        'east': '1-3',
        'west': '1-15',
        'north': '1-5',
        'item': 'chainmail boots',
        'hint': 'if you have multiple items in your inventory to equip, you can type in (i) to equip the best ones possible'
    },
    '1-5': {
        'south': '1-4',
        'west': '1-6',
        'hint': 'For combat, you have 3 options. Fight, Defend and Cast.\nFight allows you to attack the monster, If you type in (fight) a slider will pop up.\nTry to hit the middle of the slider to most damage possible!\nDefend makes you take less damage from the monsters next attack and allows you to build up mana.\nCast will cast a spell, which will require mana to do.\nHowever, you need to unlock the spell before being able to cast it.\nYou can do this by using spellbooks. To cast a spell, you will type in (cast(spell name))'
    },
    '1-6': {
        'west': '1-7',
        'east': '1-5',
        'monster': "normal",
        "item": "mana potion",
        'hint': 'Mana potions instantly regain mana. You can use them inside our outside of combat by typing (use(mana potion))'
    },
    '1-7': {
        'east': '1-6',
        'west': '1-8',
        'south': '1-15',
        'monster': "normal"
    },
    '1-8': {
        'east': '1-7',
        'west': '1-9',
        'south': '1-14',
        'north': '1-12'
    },
    '1-9': {
        'west': '1-10',
        'south': '1-13',
        'east': '1-8',
        "item": "key fragment",
    },
    '1-10': {
        'south': '1-11',
        'east': '1-9',
        "monster": "normal"
    },
    '1-11': {
        'north': '1-10',
        "item": "leather helmet"
    },
    '1-12': {
        'south': '1-11',
        'monster': 'normal'
    },
    '1-13': {
        'east': '1-16',
        'north': '1-9',
        "item": "mana potion"
    },
    '1-14': {
        'north': '1-8',
        "south": "1-16",
        "item": "leather chestplate"
    },
    '1-15': {
        'east': '1-4',
        'north': '1-7',
        "item": "health potion",
        'hint': 'health potions are used the same way as mana potions, except for the fact that they give health instead of mana. Type in the same command, which was: (use (health potion))'
    },
    '1-16': {
        'east': '1-1',
        'north': '1-14',
        'south': '1-17',
        'west': '1-13',
        'monster': "normal"
    },
    '1-17': {
        'west': '1-18',
        'north': '1-16'
    },
    '1-18': {
        'west': '1-19',
        'east': '1-17'
    },
    '1-19': {
        'west': '1-20',
        'east': '1-18',
        'monster': "boss",
    },
    '1-20': {
        'east': '1-19',
        'up': '2-1'
    },
    'dungeon-1': {
        'up': '1-10',
        'east': 'dungeon-2',
        'monster': "normal"
    },
    'dungeon-2': {
        'west': 'dungeon-1',
        'south': 'dungeon-3',
        'item': 'iron sword'
    },
    'dungeon-3': {
        'north': 'dungeon-2',
        'monster': "vampire",
        'lore': 'SOMETHING FEELS SUCCESFUL IN YOU.'
    },
    '2-1': {
        'west': '1-20',
        "north": '2-2',
        'lore': 'Your sourroundings feel vague.'
    },
    '2-2': {
        'west': '2-3',
        'south': '2-1',
        "item": "mana potion"
    },
    '2-3': {
        'west': '2-4',
        'east': '2-2',
        'item': 'iron sword'
    },
    '2-4': {
        'east': '2-3',
        'south': '2-5',
        'west': '2-15',
        'item': 'mana potion'
    },
    '2-5': {
        'north': '2-4',
        'south': '2-6',
        'monster': 'normal'
    },
    '2-6': {
        'west': '2-7',
        'north': '2-5',
        "item": "mana potion"
    },
    '2-7': {
        'east': '2-6',
        'west': '2-8',
        'south': '2-13',
        'north': '2-15',
        'monster': 'normal'
    },
    '2-8': {
        'east': '2-7',
        'west': '2-9',
    },
    '2-9': {
        'south': '2-10',
        'north': '2-13',
        'east': '2-8',
        'west': '2-10',
        "item": "iron chestplate"
    },
    '2-10': {
        'south': '2-11',
        'north': '2-9',
        "item": "health potion"
    },
    '2-11': {
        'north': '2-10',
        'south': '2-12',
        'monster': 'normal'
    },
    '2-12': {
      'north': '2-11',
      'west': '2-13',
      'monster': 'normal',
    },
    '2-13': {
        'east': '2-12',
        'south': '2-9',
        'north': '2-14',
    },
    '2-14': {
        'south': '2-13',
        "west": "2-16",
        "item": "chainmail pants"
    },
    '2-15': {
        'east': '2-4',
        'north': '2-7',
        "item": "mana potion"
    },
    '2-16': {
        'west': '2-18',
        'south': '2-17',
        'east': '2-14',
        'monster': 'normal'
    },
    '2-17': {
        'north': '2-16',
        'monster': 'normal'
    },
    '2-18': {
        'west': '2-19',
        'east': '2-16',
        'item': 'spellbook'
    },
    '2-19': {
        'north': '2-20',
        'east': '2-18',
        'item': 'health potion'
    },
    '2-20': {
        'south': '2-19'
    },
    '2-21': {
        'south': '2-20',
        'north': '2-22'
    },
    '2-22': {
        'south': '2-21',
        'north': '2-23',
        'east': '2-26'
    },
    '2-23': {
        'south': '2-22',
        'west': '2-24',
        'item': 'mana potion'
    },
    '2-24': {
        'east': '2-23',
        'south': '2-25'
            
    },
    '2-25': {
        'north': '2-24',
        'east': '2-28',
        'item': 'steel sword'
            
    },
    '2-26': {
        'west': '2-23',
        'east': '2-27',
        'monster': 'normal'

    },
    '2-27': {
        'west': '2-26',
        'monster': 'normal'

    },
    '2-28': {
        'west': '2-25',
        'east': '2-29',
        'monster': 'normal'
    },
    '2-29': {
        'west': '2-28',
        'south': '2-30',
        'item': 'iron boots'
    },
    '2-30': {
        'east': '2-29',
        'west': '3-1',
        'monster': 'boss',
        'lore': 'you feel less greedy'
    },
    '3-1': {
        'east': '2-29',
        "north": '3-2'
    },
    '3-2': {
        'east': '3-3',
        'south': '3-1',
        'monster': 'normal'
    },
    '3-3': {
        'west': '3-2',
        'east': '3-4',
        'south': '3-7',
        'item': 'iron pants'
    },
    '3-4': {
        'west': '3-3',
        'east': '3-5',
        'monster': 'normal'
    },
    '3-5': {
        'west': '3-4',
        'north': '3-6'
    },
    '3-6': {
        'west': '3-31',
        'south': '3-5',
        'east': '3-8',
        'north': '3-13',
        "item": "health potion"
    },
    '3-7': {
        'east': '3-10',
        'west': '3-8',
        'south': '3-16',
        'north': '3-3',
        'monster': 'normal'
    },
    '3-8': {
        'east': '3-7',
        'west': '3-6',
        'north': '3-9',
        'item': 'iron boots'
    },
    '3-9': {
        'south': '3-8',
        'east': '3-11',
        'west': '3-10',
        'monster': 'normal'
    },
    '3-10': {
        'east': '3-9',
        "item": "health potion"
    },
    '3-11': {
        'west': '3-9',
        'south': '3-12',
        "item": 'iron sword'
    },
    '3-12': {
      'north': '3-11',
      'monster': 'normal'
    },
    '3-13': {
        'south': '3-6',
        'north': '3-14',
    },
    '3-14': {
        'south': '3-13',
        "west": "3-15",
        'monster': 'normal'
    },
    '3-15': {
        'east': '3-14',
        'north': '3-16',
        "item": "spell"
    },
    '3-16': {
        'west': '3-26',
        'south': '3-15',
        'north': '3-7',
        'monster': 'normal'
    },
    '3-17': {
        'north': '3-31',
        'item': 'health potion'
    },
    '3-18': {
        'south': '3-26',
        'east': '3-19',
        'item': 'health potion'
   },
    '3-19': {
        'north': '3-22',
        'west': '3-18',
        'item': 'health potion'
    },
    '3-20': {
        'south': '3-23',
        'monster': 'normal'
    },
    '3-21': {
        'north': '3-22'
    },
    '3-22': {
        'south': '3-19',
        'north': '3-20',
        'east': '3-32',
        'west': '3-23'
    },
    '3-23': {
        'east': '3-22',
        'west': '3-24',
        'north': '3-20',
        'monster': 'normal'
    },
    '3-24': {
        'east': '3-23',
        'south': '3-25'
            
    },
    '3-25': {
        'north': '3-24',
        'east': '3-31',
        'item': 'health potion'
            
    },
    '3-26': {
        'west': '3-33',
        'monster': 'normal'

    },
    '3-27': {
        'west': '3-32',
        'item': 'health potion'

    },
    '3-28': {
        'north': '3-29',
        'east': '3-34',
        'item': 'health potion'
    },
    '3-29': {
        'west': '3-28',
        'south': '3-30',
        'item': 'mana potion'
    },
    '3-30': {
        'east': '3-29',
        'item': 'health potion',       
    },
    '3-31': {
        'east': '3-6',
        'west': '3-25',
        'monster': 'normal'
            
    },
    '3-32': {
        'east': '3-27',
        'west': '3-22',
        'north': '3-33',
        'item': 'health potion'
            
    },
    '3-33': {
        'south': '3-32',
        'north': '3-34',
        'monster': 'normal'
            
    },
    '3-34': {
        'south': '3-33',
        'west': '3-35',
        'north': '3-36',
        'monster': 'normal'
            
    },
    '3-35': {
        'south': '3-34',
        'west': '3-38',
        'item': 'iron helmet'
            
    },
    '3-36': {
        'south': '3-34',
        'east': '3-37',
        'item': 'health potion'
            
    },
    '3-37': {
        'east': '3-38',
        'west': '3-36',
        'item': 'iron boots'
            
    },
    '3-38': {
        'east': '3-39',
        'west': '3-37',
        'item': 'health potion'
            
    },
    '3-39': {
        'east': '3-40',
        'west': '3-38',
        'item': 'health potion'
            
    },
    '3-40': {
        'east': '4-1',
        'west': '3-39',
        'monster': 'boss',
    },
    '4-1': {
        'east': '3-40',
        "west": '4-2',
    },
    '4-2': {
        'east': '4-1',
        'north': '4-3',
        'item': 'health potion'
        
    },
    '4-3': {
        'west': '4-5',
        'north': '4-4',
        'south': '4-2',
        'item': 'mana potion'
        
    },
    '4-4': {
        'south': '4-3',
        'east': '4-5',
        'monster': 'normal'
        
    },
    '4-5': {
        'west': '4-4',
        'north': '4-6',
        'south': '4-7'
        
    },
    '4-6': {
        'west': '4-47',
        'south': '4-5',
        'east': '4-8',
        'north': '4-15',
        "item": "health potion"
        
    },
    '4-7': {
        'east': '4-8',
        'south': '4-16',
        'north': '4-5',
        'monster': 'normal'
        
    },
    '4-8': {
        'east': '4-10',
        'north': '4-9',
        'item': 'health potion'
        
    },
    '4-9': {
        'south': '4-8',
        'east': '4-15',
        'north': '4-10',
        'monster': 'normal'
        
    },
    '4-10': {
        'south': '4-9',
        'north': '4-11',
        "item": "health potion"
        
    },
    '4-11': {
        'west': '4-12',
        "item": 'iron chestplate'
        
    },
    '4-12': {
      'east': '4-11',
        
    },
    '4-13': {
        'south': '4-15',
        'north': '3-14',
        
    },
    '4-14': {
        'south': '4-13',
        'monster': 'normal'
        
    },
    '4-15': {
        'west': '4-9',
        'north': '3-16',
        'south': '4-6',
        'east': '4-16',
        "item": "health potion"
        
    },
    '4-16': {
        'west': '4-15',
        'south': '4-17',
        'north': '4-7',
        'item': 'mana potion'
        
    },
    '4-17': {
        'north': '4-16',
        'west': '4-18',
        'item': 'health potion'
        
    },
    '4-18': {
        'south': '4-19',
        'east': '4-17',
        'monster': 'normal'
        
    },
    '4-19': {
        'north': '4-18',
        'west': '4-20',
        'item': 'health potion'
        
    },
    '4-20': {
        'east': '4-19',
        'south': '4-21',
        'monster': 'boss',
        
    },
    '4-21': {
        'north': '4-21',
        'south': '4-22',
        'monster': 'normal',
        
    },
    '4-22': {
        'south': '4-29',
        'north': '4-25',
        'east': '4-46',
        'west': '4-23'
        
    },
    '4-23': {
        'east': '4-22',
        'west': '4-24',
        'north': '4-26',
        'monster': 'normal'
        
    },
    '4-24': {
        'east': '4-23',
        'south': '4-25'
           
    },
    '4-25': {
        'north': '4-24',
        'south': '4-22',
        'east': '4-26',
        'west': '4-33',
        'item': 'health potion'
           
    },
    '4-26': {
        'west': '4-25',
        'east': '4-27',
        'monster': 'normal'

    },
    '4-27': {
        'west': '4-26',
        'south': '4-28',
        'item': 'health potion'

    },
    '4-28': {
        'north': '4-27',
        'east': '4-29',
        'monster': 'normal'
    },
    '4-29': {
        'west': '4-28',
        'south': '4-30',
        'item': 'mana potion'
    },
    '4-30': {
        'east': '4-29',
        'north': '4-31',
        'item': 'health potion'
           
    },
    '4-31': {
        'south': '4-30',
        'west': '4-32',
        'monster': 'normal'
           
    },
    '4-32': {
        'east': '4-31',
        'north': '4-33',
        'item': 'health potion'
           
    },
    '4-33': {
        'south': '4-32',
        'east': '4-25',
        'north': '4-34',
        'monster': 'normal'
           
    },
    '4-34': {
        'south': '4-33',
        'west': '4-35',
        'north': '4-36',
        'monster': 'normal'
           
    },
    '4-35': {
        'east': '4-34',
        'west': '4-38',
        'item': 'iron helmet'
           
    },
    '4-36': {
        'south': '4-44',
        'north': '4-38',
        'item': 'health potion'
           
    },
    '4-37': {
        'east': '4-38',
        'south': '4-36',
        'monster': 'normal'
           
    },
    '4-38': {
        'east': '4-39',
        'north': '4-37',
        'item': 'health potion'
           
    },
    '4-39': {
        'east': '4-40',
        'west': '4-38',
        'monster': 'normal'
           
    },
    '4-40': {
        'east': '4-41',
        'west': '4-39',
        'monster': 'normal'
            
           
    },
    '4-41': {
        'east': '4-40',
        'west': '4-42',
        'item': 'mana potion'
            
               
    },
    '4-42': {
        'east': '4-41',
        'north': '4-44',
        'west': '4-43',
        'item': 'mana potion'
            
    },
    '4-43': {
        'east': '4-42',
        'item': 'health potion'
            
               
    },
    '4-44': {
        'east': '4-45',
        'west': '4-43',
        'monster': 'normal'
            

    },
    '4-45': {
        'south': '4-46',
        'west': '4-44'
            

    },
    '4-46': {
        'east': '4-47',
        'north': '4-45'
            

    },
    '4-47': {
        'east': '4-48',
        'north': '4-46',
        'south': '4-49'
            

    },
    '4-48': {
        'west': '4-48',
        'monster': 'normal'
            

    },
    '4-49': {
        'north': '4-47',
        'south': '4-50',
        'item': 'health potion',
        'lore': 'You feel if something terrible is coming...'
        

    },
    '4-50': {
        'north': '4-49',
        'south': '5-1',
        'monster': 'boss',
            
            
    },
    '5-1': {
        'east': '4-50',
        "north": '5-2',
        
    },
    '5-2': {
        'east': '5-1',
        'south': '5-3',
        'west': '5-12',
        'monster': 'normal'
        
    },
    '5-3': {
        'west': '5-5',
        'south': '5-4',
        'north': '5-2',
        'east': '5-17',
        'item': 'health potion'
        
    },
    '5-4': {
        'south': '5-3',
        'east': '5-6',
        'monster': 'normal'
        
    },
    '5-5': {
        'east': '5-3',
        'north': '5-10',
        'monster': 'boss',
        'lore': 'This doesnt feel right.'
        
    },
    '5-6': {
        'west': '5-50',
        'south': '5-7',
        'north': '5-15',
        "monster": "normal"
        
    },
    '5-7': {
        'east': '5-8',
        'north': '5-6',
        'item': 'health potion'
        
    },
    '5-8': {
        'west': '5-7',
        'north': '5-9',
        'monster': 'normal'
        
    },
    '5-9': {
        'south': '5-8',
        'north': '5-10',
        'monster': 'normal'
        
    },
    '5-10': {
        'south': '5-9',
        'north': '5-11',
        "monster": "boss"
        
    },
    '5-11': {
        'west': '5-12',
        'south': '5-10',
        "item": 'mana potion'
        
    },
    '5-12': {
      'east': '5-11',
      'south': '5-13',
      'item': 'health potion'
        
    },
    '5-13': {
        'south': '5-14',
        'north': '5-12',
        'monster': 'normal',
        
    },
    '5-14': {
        'north': '5-13',
        'west': '5-15',
        'monster': 'normal'
        
    },
    '5-15': {
        'south': '5-16',
        'east': '5-14',
        "item": "wooden sword"
        
    },
    '5-16': {
        'west': '4-16',
        'south': '5-59',
        'north': '5-15',
        'east': '5-17',
        'monster': 'normal'
        
    },
    '5-17': {
        'north': '5-18',
        'west': '5-16',
        'monster': 'normal'
        
    },
    '5-18': {
        'south': '5-17',
        'east': '5-19',
        'monster': 'normal'
        
   },
    '5-19': {
        'north': '5-18',
        'west': '5-20',
        'item': 'health potion'
        
    },
    '5-20': {
        'east': '5-19',
        'south': '5-21',
        'monster': 'boss'
        
    },
    '5-21': {
        'north': '5-20',
        'east': '5-22',
        'west': '5-23',
        'monster': 'normal'
        
    },
    '5-22': {
        'south': '5-33',
        'north': '5-32',
        'east': '5-31',
        'west': '5-21'
        
    },
    '5-23': {
        'east': '5-21',
        'west': '5-24',
        'monster': 'normal'
        
    },
    '5-24': {
        'east': '5-23',
        'south': '5-25',
           
    },
    '4-25': {
        'north': '4-24',
        'east': '4-26',
        'monster': 'boss'
           
    },
    '5-26': {
        'west': '5-25',
        'east': '5-27',
        'monster': 'normal'

    },
    '5-27': {
        'west': '5-26',
        'south': '5-28',
        'monster': 'normal'

    },
    '5-28': {
        'north': '5-27',
        'east': '5-29',
        'monster': 'normal'
    },
    '5-29': {
        'west': '5-28',
        'south': '5-30',
        'item': 'mana potion'
    },
    '5-30': {
        'east': '5-29',
        'monster': 'boss',
        'lore': 'you feel sick.'
           
    },
    '5-31': {
        'west': '5-22',
        'west': '5-32',
        'item': 'health potion'
           
    },
    '5-32': {
        'east': '5-31',
        'south': '5-22',
        'north': '5-33',
        'item': 'health potion'
           
    },
    '5-33': {
        'south': '5-32',
        'east': '5-34',
        'north': '5-22',
        'monster': 'normal'
           
    },
    '5-34': {
        'south': '4-33',
        'west': '4-35',
        'monster': 'normal'
           
    },
    '5-35': {
        'easr': '5-34',
        'west': '5-36',
        'monster': 'boss'
           
    },
    '5-36': {
        'south': '5-45',
        'north': '5-37',
        'item': 'health potion'
           
    },
    '5-37': {
        'east': '5-38',
        'south': '5-36',
        'item': 'health potion'
           
    },
    '5-38': {
        'east': '5-39',
        'west': '5-37',
        'item': 'health potion'
           
    },
    '5-39': {
        'east': '5-40',
        'west': '5-38',
        'item': 'health potion'
           
    },
    '5-40': {
        'east': '5-41',
        'west': '5-39',
        'monster': 'boss',
        'lore': 'NOTHING IN THIS WORLD IS RIGHT'
            
           
    },
    '5-41': {
        'east': '5-40',
        'west': '5-42',
        'item': 'mana potion',
        'lore': 'And you must right those wrongs.'
               
    },
    '5-42': {
        'east': '4-41',
        'west': '4-43',
        'item': 'mana potion'
            
    },
    '5-43': {
        'east': '4-42',
        'north': '5-44',
        'item': 'health potion'
            
               
    },
    '5-44': {
        'east': '5-45',
        'west': '5-43',
        'monster': 'normal'
            

    },
    '5-45': {
        'south': '5-46',
        'west': '5-44',
        'monster': 'boss',
        'lore': 'ALL YOUR EFFORTS ARE FOR NOTHING.'
    },
    '5-46': {
        'east': '5-47',
        'north': '5-45',
        'lore': 'Trun back now.'

    },
    '5-47': {
        'east': '5-48',
        'north': '5-46',
        'monster': 'normal',
        'lore': 'You have no place with the gods.'

    },
    '5-48': {
        'west': '5-47',
        'south': '5-49',
        'monster': 'normal'
            

    },
    '5-49': {
        'north': '4-48',
        'south': '4-50',
        'item': 'health potion'
            

    },
    '5-50': {
        'north': '5-49',
        'south': '5-51',
        'monster': 'boss',
        'lore': 'ITS NOT FAIR'
            

    },
    '5-51': {
        'north': '5-50',
        'east': '5-52',
        'monster': 'normal',
        'lore': 'It never was.'

    },
    '5-52': {
        'west': '5-51',
        'east': '5-53',
        'north': '5-59',
        'monster': 'normal',
        'lore': 'A N D  Y O U  K N O W  I T.'

    },
    '5-53': {
        'west': '5-52',
        'south': '5-54',
        'item': 'health potion'
            

    },
    '5-54': {
        'north': '5-53',
        'west': '5-55',
        'item': 'health potion'
            

    },
    '5-55': {
        'east': '5-54',
        'west': '5-56',
        'monster': 'boss'
            

    },
    '5-56': {
        'east': '5-55',
        'west': '5-57',
        'monster': 'normal'
            

    },
    '5-57': {
        'east': '5-56',
        'west': '5-58',
        'item': 'health potion'
            

    },
    '5-58': {
        'west': '5-57',
        'item': 'health potion'
            

    },
    '5-59': {
        'north': '5-52',
        'west': '5-60',
        'item': 'health potion'
    },
    '5-60': {
        'east': '5-59',
        'monster': 'boss',    
    },
        '1~1': {
        'north': '1~2',
        'item': 'health potion',
        'lore': 'hehe, lol jk'
    },
    '1~2': {
        'west': '1~3',
        'south': '1~1',
        'monster': 'demon'
    },
    '1~3': {
        'west': '1~4',
        'east': '1~2',
        'south': '1~8',
        'item': 'mythril pants'
    },
    '1~4': {
        'west': '1~5',
        'east': '1~3',
        'south': '1~7',
        'monster': 'demon'
    },
    '1~5': {
        'south': '1~6',
        'east': '1~4',
        'monster': 'demon'
    },
    '1~6': {
        'east': '1~7',
        'north': '1~5',
        "item": "health potion"
    },
    '1~7': {
        'east': '1~8',
        'west': '1~6',
        'north': '1~4',
        'monster': 'demon'
    },
    '1~8': {
        'south': '1~9',
        'west': '1~7',
        'north': '1~3',
        'item': 'mythril boots'
    },
    '1~9': {
        'south': '1~10',
        'north': '1~8',
        'monster': 'demon'
    },
    '1~10': {
        'east': '1~13',
        'north': '1~9',
        'south': '1~11',
        "item": "health potion"
    },
    '1~11': {
        'north': '1~10',
        'south': '1~12',
        "item": 'mythril sword'
    },
    '1~12': {
      'north': '1~11',
      'monster': 'demon'
    },
    '1~13': {
        'west': '1~14',
        'east': '1~10',
        'monster': 'demon'
    },
    '1~14': {
        'south': '1~15',
        "east": "1~13",
        'monster': 'demon'
    },
    '1~15': {
        'west': '1~15',
        'north': '1~14',
        "item": "health potion"
    },
    '1~16': {
        'east': '1~15',
        'south': '1~18',
        'north': '1~17',
        "item": "mythril helmet"
    },
    '1~17': {
        'south': '1~16',
        "item": "health potion"
    },
    '1~18': {
        'north': '1~16',
        'south': '1~19',
        'monster': 'demon'
    },
    '1~19': {
        'north': '1~18',
        'south': '1~20',
        'item': 'mythril chestplate',
        'lore': "You feel an evil presence watching you..."
    },
    '1~20': {
        'north': '1~19',
        'up': '2~1',
        'monster': 'demon king lucifer'
    },
    '2~1': {
        'down': '1~20',
        'west': '2~2',
        'item': 'health potion',
    },
    '2~2': {
        'east': '2~1',
        'north': '2~3',
        'monster': 'demon'
    },
    '2~3': {
        'west': '2~4',
        'south': '2~2',
        'monster': 'demon'
    },
    '2~4': {
        'west': '2~8',
        'east': '2~3',
        'north': '2~5',
        'monster': 'demon'
    },
    '2~5': {
        'south': '2~4',
        'east': '2~6',
        'monster': 'demon'
    },
    '2~6': {
        'west': '2~5',
        'north': '2~7',
        "item": "health potion"
    },
    '2~7': {
        'south': '2~6',
        'monster': 'demon'
    },
    '2~8': {
        'south': '2~9',
        'east': '2~4',
        'north': '2~14',
        'monster': 'demon'
    },
    '2~9': {
        'east': '2~10',
        'north': '2~8',
        'monster': 'demon'
    },
    '2~10': {
        'east': '2~13',
        'west': '2~9',
        'north': '2~11',
        'monster': 'demon'
    },
    '2~11': {
        'east': '2~12',
        'south': '2~10',
        'warp 1': '2~20',
        'warp 2': '4~20',
        'warp 3': '6~20',
        'item': 'health potion'
    },
    '2~12': {
      'south': '2~13',
      'monster': 'demon'
    },
    '2~13': {
        'west': '2~10',
        'north': '2~12',
        'monster': 'demon'
    },
    '2~14': {
        'south': '2~8',
        "east": "2~15",
        'monster': 'demon'
    },
    '2~15': {
        'west': '2~14',
        'north': '2~16',
        'monster': 'demon'
    },
    '2~16': {
        'north': '2~18',
        'south': '2~15',
        'west': '2~17',
        'item': 'health potion'
    },
    '2~17': {
        'west': '2~16',
        'north': '2~19',
        'monster': 'demon'
    },
    '2~18': {
        'east': '2~20',
        'south': '2~16',
        'item': 'health potion',
        'lore': "You feel vibrations from deep below..."
    },
    '2~19': {
        'south': '2~17',
        'monster': 'demon'
    },
    '2~20': {
        'west': '2~18',
        'up': '3~3',
        'warp 1': '2~11',
        'monster': 'demon king asmodeus'
    },
    '3~1': {
        'north': '3~2',
        'monster': 'demon'
    },
    '3~2': {
        'south': '3~1',
        'east': '3~3',
        'monster': 'demon'
    },
    '3~3': {
        'west': '3~2',
        'down': '2~20',
        'north': '3~4',
        'east': '3~8',
        'south': '3~16',
        'monster': 'demon'
    },
    '3~4': {
        'south': '3~3',
        'east': '3~5',
        'monster': 'demon'
    },
    '3~5': {
        'south': '3~6',
        'west': '3~4',
        'monster': 'demon'
    },
    '3~6': {
        'east': '3~7',
        'north': '3~5',
        'monster': 'demon'
    },
    '3~7': {
        'west': '3~6',
        'monster': 'demon'
    },
    '3~8': {
        'east': '3~7',
        'west': '3~7',
        'monster': 'demon'
    },
    '3~9': {
        'west': '3~10',
        'monster': 'demon'
    },
    '3~10': {
        'east': '3~16',
        'north': '3~9',
        'west': '3~11',
        'monster': 'demon'
    },
    '3~11': {
        'east': '3~10',
        'item': 'health potion'
    },
    '3~12': {
      'south': '3~18',
      'north': '3~16',
      'monster': 'demon'
    },
    '3~13': {
        'west': '3~14',
        'north': '3~19',
        'monster': 'demon'
    },
    '3~14': {
        'south': '3~15',
        "east": "3~13",
        'monster': 'demon'
    },
    '3~15': {
        'north': '3~15',
        'item': 'health potion'
    },
    '3~16': {
        'north': '3~3',
        'south': '3~12',
        'west': '3~10',
        'monster': 'demon'
    },
    '3~17': {
        'west': '3~19',
        'south': '3~20',
        'item': 'health potion',
        'lore': "This is going to be a terrible night..."
    },
    '3~18': {
        'north': '3~12',
        'monster': 'demon'
    },
    '3~19': {
        'east': '3~17',
        'south': '1~13',
        'monster': 'demon'
    },
    '3~20': {
        'north': '3~17',
        'up': '4~1',
        'monster': 'demon king leviathan'
    },
    '4~1': {
        'east': '4~2',
        'south': '4~10',
        'monster': 'demon'
    },
    '4~2': {
        'south': '4~9',
        'west': '4~1',
        'east': '4~3',
        'monster': 'demon'
    },
    '4~3': {
        'south': '4~8',
        'west': '4~2',
        'east': '4~4',
        'monster': 'demon'
    },
    '4~4': {
        'south': '4~7',
        'west': '4~3',
        'east': '4~5',
        'monster': 'demon'
    },
    '4~5': {
        'south': '4~6',
        'west': '4~4',
        'monster': 'demon'
    },
    '4~6': {
        'south': '4~15',
        'west': '4~7',
        'north': '4~5',
        'monster': 'demon'
    },
    '4~7': {
        'west': '4~8',
        'north': '4~4',
        'east': '4~6',
        'south': '4~14',
        'monster': 'demon'
    },
    '4~8': {
        'west': '4~9',
        'north': '4~3',
        'east': '4~7',
        'south': '4~13',
        'monster': 'demon'
    },
    '4~9': {
        'west': '4~10',
        'north': '4~2',
        'east': '4~8',
        'south': '4~12',
        'monster': 'demon'
    },
    '4~10': {
        'north': '4~1',
        'east': '4~9',
        'south': '4~11',
        'monster': 'demon'
    },
    '4~11': {
        'north': '4~10',
        'east': '4~8',
        'south': '4~20',
        'monster': 'demon'
    },
    '4~12': {
        'west': '4~11',
        'north': '4~9',
        'east': '4~13',
        'south': '4~19',
        'monster': 'demon'
    },
    '4~13': {
        'west': '4~12',
        'north': '4~8',
        'east': '4~14',
        'south': '4~18',
        'monster': 'demon'
    },
    '4~14': {
        'west': '4~13',
        'north': '4~7',
        'east': '4~15',
        'south': '4~17',
        'monster': 'demon'
    },
    '4~15': {
        'west': '4~14',
        'north': '4~6',
        'south': '4~16',
        'monster': 'demon'
    },
    '4~16': {
        'north': '4~15',
        'west': '4~17',
        'monster': 'demon'
    },
    '4~17': {
        'west': '4~18',
        'north': '4~14',
        'east': '4~16',
        'item': 'health potion'
    },
    '4~18': {
        'west': '4~19',
        'north': '4~13',
        'east': '4~17',
        'monster': 'demon'
    },
    '4~19': {
        'west': '4~20',
        'north': '4~12',
        'east': '4~18',
        'warp 2': '2~11',
        'item': 'health potion',
        'lore': "The air is getting colder around you..."
    },
    '4~20': {
        'north': '4~11',
        'east': '4~19',
        'up': '5~5',
        'monster': 'demon king belphegor'
    },
    '5~1': {
        'east': '5~5',
        'north': '5~7',
        'south': '5~16',
        'monster': 'demon'
    },
    '5~2': {
        'west': '5~18',
        'monster': 'demon'
    },
    '5~3': {
        'north': '5~17',
        'south': '5~13',
        'monster': 'demon'
    },
    '5~4': {
        'south': '5~11',
        'monster': 'demon'
    },
    '5~5': {
        'west': '5~1',
        'down': '4~20',
        'north': '5~6',
        'east': '5~11',
        'south': '5~18',
        'monster': 'demon'
    },
    '5~6': {
        'west': '5~7',
        'south': '5~5',
        'monster': 'demon'
    },
    '5~7': {
        'east': '5~6',
        'west': '5~10',
        'south': '5~1',
        'monster': 'demon'
    },
    '5~8': {
        'north': '5~19',
        'monster': 'demon'
    },
    '5~9': {
        'east': '5~16',
        'monster': 'demon'
    },
    '5~10': {
        'east': '5~7',
        'south': '5~15',
        'west': '5~14',
        'monster': 'demon'
    },
    '5~11': {
        'west': '5~5',
        'north': '5~4',
        'item': 'health potion'
    },
    '5~12': {
      'north': '5~18',
      'east': '5~17',
      'west': '5~19',
      'monster': 'demon'
    },
    '5~13': {
        'north': '5~3',
        'monster': 'demon'
    },
    '5~14': {
        "east": "5~10",
        'monster': 'demon'
    },
    '5~15': {
        'north': '5~10',
        'item': 'health potion'
    },
    '5~16': {
        'north': '5~1',
        'west': '5~9',
        'monster': 'demon'
    },
    '5~17': {
        'west': '5~12',
        'south': '5~3',
        'item': 'health potion'
    },
    '5~18': {
        'north': '5~5',
        'east': '5~2',
        'south': '5~12',
        'monster': 'demon'
    },
    '5~19': {
        'west': '5~20',
        'south': '5~8',
        'east': '5~12',
        'monster': 'demon',
        'lore': 'What a horrible night to have a curse...'
    },
    '5~20': {
        'east': '5~19',
        'up': '6~1',
        'monster': 'demon king beelzebub'
    },
    '6~1': {
        'east': '6~13',
        'north': '6~2',
        'south': '6~19',
        'monster': 'demon'
    },
    '6~2': {
        'west': '6~3',
        'south': '6~1',
        'monster': 'demon'
    },
    '6~3': {
        'west': '6~4',
        'east': '6~2',
        'monster': 'demon'
    },
    '6~4': {
        'south': '6~5',
        'east': '6~3',
        'monster': 'demon'
    },
    '6~5': {
        'west': '6~6',
        'north': '6~4',
        'monster': 'demon'
    },
    '6~6': {
        'south': '6~7',
        'east': '6~5',
        'north': '6~8',
        'monster': 'demon'
    },
    '6~7': {
        'north': '6~6',
        'monster': 'demon'
    },
    '6~8': {
        'north': '6~9',
        'south': '6~6',
        'monster': 'demon'
    },
    '6~9': {
        'south': '6~8',
        'monster': 'demon'
    },
    '6~10': {
        'south': '6~12',
        'west': '6~11',
        'monster': 'demon'
    },
    '6~11': {
        'east': '6~10',
        'item': 'health potion'
    },
    '6~12': {
      'north': '6~10',
      'south': '6~15',
      'monster': 'demon'
    },
    '6~13': {
        'west': '6~1',
        'east': '6~15',
        'monster': 'demon'
    },
    '6~14': {
        "west": "6~17",
        'monster': 'demon'
    },
    '6~15': {
        'north': '6~12',
        'west': '6~13',
        'south': '6~16',
        'item': 'health potion'
    },
    '6~16': {
        'north': '6~17',
        'monster': 'demon'
    },
    '6~17': {
        'east': '6~14',
        'south': '6~16',
        'north': '6~15',
        'monster': 'demon'
    },
    '6~18': {
        'east': '6~1',
        'monster': 'demon'
    },
    '6~19': {
        'north': '6~1',
        'south': '6~20',
        'monster': 'demon',
        'lore': 'Otherworldly voices linger around you...'
    },
    '6~20': {
        'north': '6~19',
        'up': '7~1',
        'monster': 'demon king beelzebub'
    },
    '7~1': {
        'west': '7~2',
        'monster': 'demon'
    },
    '7~2': {
        'south': '7~3',
        'east': '7~1',
        'monster': 'demon'
    },
    '7~3': {
        'west': '7~4',
        'north': '7~2',
        'monster': 'demon'
    },
    '7~4': {
        'south': '7~5',
        'east': '7~3',
        'monster': 'demon'
    },
    '7~5': {
        'north': '7~4',
        'west': '7~6',
        'monster': 'demon'
    },
    '7~6': {
        'south': '7~7',
        'north': '7~5',
        'monster': 'demon'
    },
    '7~7': {
        'north': '7~6',
        'west': '7~8',
        'monster': 'demon'
    },
    '7~8': {
        'east': '7~7',
        'west': '7~9',
        'monster': 'demon'
    },
    '7~9': {
        'west': '7~10',
        'east': '7~8',
        'monster': 'demon'
    },
    '7~10': {
        'east': '7~9',
        'north': '7~11',
        'monster': 'demon'
    },
    '7~11': {
        'east': '7~12',
        'south': '7~10',
        'monster': 'demon'
    },
    '7~12': {
      'south': '7~13',
      'west': '7~11',
      'monster': 'demon'
    },
    '7~13': {
        'west': '7~14',
        'north': '7~12',
        'monster': 'demon'
    },
    '7~14': {
        'west': '7~15',
        "east": "7~13",
        'monster': 'demon'
    },
    '7~15': {
        'north': '7~16',
        'east': '7~14',
        'monster': 'demon'
    },
    '7~16': {
        'south': '7~15',
        'east': '7~17',
        'monster': 'demon'
    },
    '7~17': {
        'west': '7~16',
        'south': '7~18',
        'monster': 'demon',
    },
    '7~18': {
        'west': '7~19',
        'north': '7~17',
        'monster': 'demon'
    },
    '7~19': {
        'east': '7~19',
        'south': '7~20',
        'monster': 'demon',
        'lore': "Impending doom approaches..."
    },
    '7~20': {
        'north': '7~19',
        'up': '?~??',
        'monster': 'demon king satan'
    },
    '?~??': {}
}

BLACKSMITH_RECIPES = {
    'bleeding key': {
        'materials': {'key fragment': 3},
        'price': 0,
        'description': 'Opens the dungeon entrance'
    },
    'iron sword': {
        'materials': {},
        'price': 200,
        'description': '+10 attack damage'
    },
    'steel sword': {
        'materials': {},
        'price': 300,
        'description': '+15 attack damage'
    },
    'iron helmet': {
        'materials': {},
        'price': 150,
        'description': '+15 defense'
    },
    'iron chestplate': {
        'materials': {},
        'price': 200,
        'description': '+15 defense'
    },
    'iron pants': {
        'materials': {},
        'price': 180,
        'description': '+15 defense'
    },
    'iron boots': {
        'materials': {},
        'price': 120,
        'description': '+15 defense'
    }
}

UPGRADED_BLACKSMITH_RECIPES = {
    'adamantite sword': {
        'materials': {'adamantite bar': 1},
        'price': 300,
        'description': '+25 attack damage'
    },
    'adamantite helmet': {
        'materials': {'adamantite bar': 1},
        'price': 225,
        'description': '+10 defense'
    },
    'adamantite chestplate': {
        'materials': {'adamantite bar': 1},
        'price': 300,
        'description': '+10 defense'
    },
    'adamantite pants': {
        'materials': {'adamantite bar': 1},
        'price': 250,
        'description': '+10 defense'
    },
    'adamantite boots': {
        'materials': {'adamantite bar': 1},
        'price': 200,
        'description': '+10 defense'
    },
    'hallowed sword': {
        'materials': {"hallowed bar": 1},
        'price': 400,
        'description': '+35 attack damage'
    },
    'hallowed helmet': {
        'materials': {"hallowed bar": 1},
        'price': 300,
        'description': '+12 defense'
    },
    'hallowed chestplate': {
        'materials': {"hallowed bar": 1},
        'price': 400,
        'description': '+12 defense'
    },
    'hallowed pants': {
        'materials': {"hallowed bar": 1},
        'price': 300,
        'description': '+12 defense'
    },
    'hallowed boots': {
        'materials': {"hallowed bar": 1},
        'price': 250,
        'description': '+12 defense'
    },
    'godslayer sword': {
        'materials': {'cosmilite bar': 1},
        'price': 500,
        'description': '+50 attack damage'
    },
    'godslayer helmet': {
        'materials': {'cosmilite bar': 1},
        'price': 350,
        'description': '+15 defense'
    },
    'godslayer chestplate': {
        'materials': {'cosmilite bar': 1},
        'price': 500,
        'description': '+15 defense'
    },
    'godslayer pants': {
        'materials': {'cosmilite bar': 1},
        'price': 350,
        'description': '+15 defense'
    },
    'godslayer boots': {
        'materials': {'cosmilite bar': 1},
        'price': 300,
        'description': '+15 defense'
    },
    'health potion': {
        'materials': {},
        'price': 30,
        'description': 'Restores 30 health'
    },
    'mana potion': {
        'materials': {},
        'price': 30,
        'description': 'Restores 30 health'
    }
}

# Game setup
clear_screen()
print(GREEN)
print_slow(r"""
 _____         _      _   _
|_   _|____  _| |_   | | | | ___ _ __ ___
  | |/ _ \ \/ / __|  | |_| |/ _ \ '__/ _ \
  | |  __/>  <| |_   |  _  |  __/ | | (_) |
  |_|\___/_/\_\\__|  |_| |_|\___|_|  \___/
""")

print_slow("Welcome to the Text Hero!")
print_slow("To start, choose a class: Warrior, Mage, Rogue, Healer, Archer")
chosen_class = input(GREEN + "> ").capitalize() 

clear_screen()
DLC_unlocked = "yes"

if chosen_class == "Load":
    load_game()
    BASE_STATS = {
    "health": classes[player["class"]]["health"],
    "armor": classes[player["class"]]["armor"],
    "mana": classes[player["class"]]["mana"],
    "attack": classes[player["class"]]["attack"],
    }
elif chosen_class not in classes and not chosen_class == "Load":
    chosen_class = "Warrior"
    player = {
    "health": classes[chosen_class]["health"],
    "armor": classes[chosen_class]["armor"],
    "mana": classes[chosen_class]["mana"],
    "class": chosen_class,
    "class 2": None,
    "spells": classes[chosen_class]["spells"],
    "attack": classes[chosen_class]["attack"],
    "gold": 0,  # Starting gold
    "level": 1,
    "exp": 0,
    "key_fragment_chance": 0.7  # Starting chance for key fragments
    }
    currentRoom = '1-1'
    classes[player["class"]]
    BASE_STATS = {
    "health": classes[chosen_class]["health"],
    "armor": classes[chosen_class]["armor"],
    "mana": classes[chosen_class]["mana"],
    "attack": classes[chosen_class]["attack"],
    }
else:
    player = {
    "health": classes[chosen_class]["health"],
    "armor": classes[chosen_class]["armor"],
    "mana": classes[chosen_class]["mana"],
    "class": chosen_class,
    "class 2": None,
    "spells": classes[chosen_class]["spells"],
    "attack": classes[chosen_class]["attack"],
    "gold": 0,  # Starting gold
    "level": 1,
    "exp": 0,
    "key_fragment_chance": 0.7  # Starting chance for key fragments
    }
    currentRoom = '1-1'
    classes[player["class"]]
    BASE_STATS = {
    "health": classes[chosen_class]["health"],
    "armor": classes[chosen_class]["armor"],
    "mana": classes[chosen_class]["mana"],
    "attack": classes[chosen_class]["attack"],
    }
def use_item_during_combat(item):
    try:
        # Parse item name and quantity
        item_parts = item.split(' x')
        item_name = item_parts[0].strip()
        quantity = int(item_parts[1]) if len(item_parts) > 1 else 1
        
        # Count how many of the item we have
        item_count = inventory.count(item_name)
        
        if item_count >= quantity:
            if item_name == "health potion":
                heal_amount = 30 * quantity
                player["health"] = min(classes[player["class"]]["health"], player["health"] + heal_amount)
                for _ in range(quantity):
                    inventory.remove("health potion")
                return f"Used {quantity}x health potion! Restored {heal_amount} health!"
            elif item_name == "mana potion":
                mana_amount = 30 * quantity
                player["mana"] = min(classes[player["class"]]["mana"], player["mana"] + mana_amount)
                for _ in range(quantity):
                    inventory.remove("mana potion")
                return f"Used {quantity}x mana potion! Restored {mana_amount} mana!"
            else:
                return f"Cannot use {item} during combat!"
        else:
            return f"Not enough {item_name}! (Have {item_count}, need {quantity})"
    except Exception as e:
        return f"Error using item: {str(e)}"

player_equipment = {
    'helmet': None,
    'chestplate': None,
    'pants': None,
    'boots': None,
    'sword': None  # Add sword slot
}

# Initialize inventory
inventory = ['spell book','spell book','spell book', 'vampire pendant']

# Track defeated bosses
defeated_bosses = set()

def display_table(title, items, columns=None):
    """Display a formatted table with consistent spacing
    title: string for the table header
    items: dictionary of items to display
    columns: list of column names and widths [(name, width)]"""
    
    if columns is None:
        columns = [
            ("Item Name", 23),
            ("Price", 18),
            ("Description", 32)
        ]
    
    # Create the table border and header format
    border = "┌" + "┬".join("─" * width for _, width in columns) + "┐"
    header = "│" + "│".join(f" {name:<{width-2}} " for name, width in columns) + "│"
    separator = "├" + "┼".join("─" * width for _, width in columns) + "┤"
    row_format = "│" + "│".join(f" {{{i}:<{width-2}}} " for i, (_, width) in enumerate(columns)) + "│"
    bottom = "└" + "┴".join("─" * width for _, width in columns) + "┘"

    print_slow(f"\n{GREEN}{title}")
    print_slow(border)
    print_slow(header)
    print_slow(separator)
    
    for item_name, details in items.items():
        if 'materials' in details:  # Blacksmith items
            price = f"{details['price']} gold"
            if details['materials']:
                materials = ", ".join(f"{amt} {mat}" for mat, amt in details['materials'].items())
                price = f"{materials}"
        else:  # Market items
            price = f"{details['price']} gold"
        
        print_slow(row_format.format(
            item_name,
            price,
            details['description']
        ))
    
    print_slow(bottom)
    print_slow("---------------------------")

# Update the existing functions to use the new display_table function
def show_market_items():
    display_table(
        "Market Items",
        MARKET_ITEMS
    )

def show_blacksmith_items():
    display_table(
        "Blacksmith Items",
        BLACKSMITH_RECIPES
    )

def show_mare_items():
    display_table(
        "Mare Items",
        UPGRADED_BLACKSMITH_RECIPES
    )

def forge_item(item_name):
    """Handle crafting items at the blacksmith"""
    if item_name not in BLACKSMITH_RECIPES:
        return "That item isn't available to forge!"
    
    recipe = BLACKSMITH_RECIPES[item_name]
    price = recipe['price']
    
    # Check if player has enough gold
    if player['gold'] < price:
        return f"You don't have enough gold! (Need {price} gold)"
    
    # Check if player has required materials
    for material, amount in recipe['materials'].items():
        count = inventory.count(material)
        if count < amount:
            return f"You need {amount} {material}(s)! (Have {count})"
    
    # Remove materials and gold, add forged item
    for material, amount in recipe['materials'].items():
        for _ in range(amount):
            inventory.remove(material)
    
    player['gold'] -= price
    inventory.append(item_name)
    return f"Forged {item_name} for {price} gold!"

def forge_DLC_item(item_name):
    """Handle crafting items at the blacksmith"""
    if item_name not in UPGRADED_BLACKSMITH_RECIPES:
        return "That item isn't available to forge!"
    
    recipe = UPGRADED_BLACKSMITH_RECIPES[item_name]
    price = recipe['price']
    
    # Check if player has enough gold
    if player['gold'] < price:
        return f"You don't have enough gold! (Need {price} gold)"
    
    # Check if player has required materials
    for material, amount in recipe['materials'].items():
        count = inventory.count(material)
        if count < amount:
            return f"You need {amount} {material}(s)! (Have {count})"
    
    # Remove materials and gold, add forged item
    for material, amount in recipe['materials'].items():
        for _ in range(amount):
            inventory.remove(material)
    
    player['gold'] -= price
    inventory.append(item_name)
    return f"Forged {item_name} for {price} gold!"

def show_inventory():
    print_slow(f"{GREEN}Inventory:{ITEM_COLOR}")
    if not inventory:
        print_slow(f"Empty{GREEN}")
        return
    
    # Count items and display with quantities
    item_counts = {}
    for item in inventory:
        item_counts[item] = item_counts.get(item, 0) + 1
    for item, count in item_counts.items():
        if count > 1:
            print_slow(f"{ITEM_COLOR} - {item} x{count}{GREEN}")
        else:
            print_slow(f"{ITEM_COLOR} - {item}{GREEN}")

# Main game loop
help_system = HelpSystem()

def display_spell_book(player_class, player_class_2):
    """Display a formatted spellbook with all available spells for the class"""
    if player_class_2 == None:
        print_slow(f"\n{GREEN}==== {player_class}'s Spell Book ====")
    else:
        print_slow(f"\n{GREEN}==== {player_class} {player_class_2}'s Spell Book ====")
    print_slow("\nCurrent Spells:")
    
    print_slow("┌────────────────┬─────────────┬────────────┬────────────────────────────────────────────┐")
    print_slow("│ Spell          │ Damage/Eff  │ Mana Cost  │ Special Effect                             │")
    print_slow("├────────────────┼─────────────┼────────────┼────────────────────────────────────────────┤")
    
    # Display current spells
    for spell, values in player['spells'].items():
        effect = values[0]
        cost = values[1]
        special = get_spell_description(spell)
        print_slow(f"│ {spell:<14} │ {effect:<11} │ {cost:<10} │ {special:<42} │")
    if player_class_2 != None:
        for spell, values in locked_spells[player_class_2].items():
            effect = values[0]
            cost = values[1]
            special = get_spell_description(spell)
            print_slow(f"│ {spell:<14} │ {effect:<11} │ {cost:<10} │ {special:<42} │")

    
    print_slow("└────────────────┴─────────────┴────────────┴────────────────────────────────────────────┘")
    
    # Display unlockable spells if any exist
    if locked_spells[player_class]:
        print_slow("\nUnlockable Spells:")
        print_slow("┌────────────────┬─────────────┬────────────┬────────────────────────────────────────────┐")
        print_slow("│ Spell          │ Damage/Eff  │ Mana Cost  │ Special Effect                             │")
        print_slow("├────────────────┼─────────────┼────────────┼────────────────────────────────────────────┤")
        

    # Iterate through both classes' spells
        for spell, values in locked_spells[player_class].items(): 
            effect = values[0] 
            cost = values[1] 
            special = get_spell_description(spell) 
            
            print_slow(f"│ {spell:<14} │ {effect:<11} │ {cost:<10} │ {special:<42} │") 
        if player_class_2 != None:
            for spell, values in locked_spells[player_class_2].items(): 
                effect = values[0] 
                cost = values[1] 
                special = get_spell_description(spell) 
                print_slow(f"│ {spell:<14} │ {effect:<11} │ {cost:<10} │ {special:<42} │")
        print_slow("└────────────────┴─────────────┴────────────┴────────────────────────────────────────────┘")
    else:
        print_slow("\nNo more spells left to learn!")
        print_slow("\nType 'exit' to close the spellbook:")

def get_spell_description(spell_name):
    """Return a short description of what the spell does"""
    descriptions = {
        "slash": "Basic melee attack",
        "finishing blow": "Powerful finishing attack",
        "stun strike": "Chance to stun enemy (2-5 turns)",
        "fireball": "Causes burning for 3 turns",
        "water bolt": "Basic water attack, low cost",
        "thunder zapper": "Chance to stun enemy",
        "back stab": "Basic rogue attack",
        "stealth": "Allows you to exit the battle",
        "stealth strike": "Attack from stealth confusing the enemy",
        "spear of justice": "Attack enemies with a spear of justice",
        "great heal": "Powerful single target heal",
        "divine shield": "Block damage for 3 rounds",
        "minor heal": "Small efficient heal",
        "bleeding arrow": "Causes bleeding damage",
        "binding shot": "Roots enemy in place",
        "holy strike": "Imbue your sword with holy power",
        "healing pool": "A small healing spell",
        "tidal wave": "Summon a tsunami to decimate your enemies",
        "kamehameha": "A legendary attack used by a Turtle Hermit",
        "assassinate": "Catch enemies off guard",
        "ultrakill": "A truly overkill spell",
        "holy cleansing": "Heals a minor amount of HP",
        "arrow of light": "Fire a holy arrow, blinding enemies",
        "marksman": "Bounce an arrow off of a coin",
        "mordshlang": "Attack with the pommel of the sword",
        "boulder": "Throw a boulder at the enemy",
        "knife throw": "Throw a knife",
        "divine retribution": "The wrath of the gods will aid you in battle",
        "double shot": "Shoot 2 arrows at once",
        "blood bomb": "Release an explosive blood sack",
        "lifesteal": "Drain the life force of the enemy", 
        "blood spear": "Shoot a spear of blood at the enemy",
        "haemolacria": "launch a giant bloody tear at the enemy"
    }
    return descriptions.get(spell_name, "")

def buy_item(item_name):
    """Handle purchasing items from the market"""
    if item_name not in MARKET_ITEMS:
        return "That item isn't available in the market!"
    
    price = MARKET_ITEMS[item_name]['price']
    if player['gold'] < price:
        return f"You don't have enough gold! (Need {price} gold)"
    
    player['gold'] -= price
    inventory.append(item_name)
    return f"Bought {item_name} for {price} gold!"

def sell_item(item_name):
    """Handle selling items to the market"""
    if item_name not in inventory:
        return "You don't have that item!"
    
    if item_name in MARKET_ITEMS:
        sell_price = MARKET_ITEMS[item_name]['price'] // 2  # Sell for half the buy price
        inventory.remove(item_name)
        player['gold'] += sell_price
        return f"Sold {item_name} for {sell_price} gold!"
    return "You can't sell that item here!"

# Add this function to generate a random normal monster
def generate_random_monster():
    enemy_type = MONSTER_TYPES['normal']
    enemy_name = random.choice(enemy_type['names'])
    
    # Add some randomness to monster stats
    health_variation = random.uniform(0.8, 1.2)  # 80% to 120% of base health
    attack_variation = random.uniform(0.9, 1.1)  # 90% to 110% of base attack
    
    return {
        "health": int(enemy_type['health'] * health_variation),
        "name": enemy_name,
        "attack_min": int(enemy_type['attack_min'] * attack_variation),
        "attack_max": int(enemy_type['attack_max'] * attack_variation),
        "stunned": 0,
        "blinded": 0
    }

def generate_random_demon():
    enemy_type = MONSTER_TYPES['demon']
    enemy_name = random.choice(enemy_type['names'])
    
    # Add some randomness to monster stats
    health_variation = random.uniform(0.8, 1.2)  # 80% to 120% of base health
    attack_variation = random.uniform(0.9, 1.1)  # 90% to 110% of base attack
    
    return {
        "health": int(enemy_type['health'] * health_variation),
        "name": enemy_name,
        "attack_min": int(enemy_type['attack_min'] * attack_variation),
        "attack_max": int(enemy_type['attack_max'] * attack_variation),
        "stunned": 0,
        "blinded": 0
    }

while True:
    # Add this to your main game loop, right after the room check:
    if currentRoom == '5-60':
        if DLC_unlocked == "yes":
            currentRoom = '1~1'
        else:
            display_credits()
            exit()

    if currentRoom == '?~??':
        display_DLC_credits()
        exit()

    if currentRoom in rooms:
        if "monster" in rooms[currentRoom]:
            clear_screen()
            # Determine monster type
            monster_type = rooms[currentRoom]["monster"]
            
            # Initialize enemies list
            enemies = []
            
            if monster_type == 'boss':
                enemy_type = MONSTER_TYPES['boss']
                enemy = {
                    "health": enemy_type['health'],
                    "name": enemy_type['name'],
                    "attack_min": enemy_type['attack_min'],
                    "attack_max": enemy_type['attack_max'],
                    "stunned": 0,
                    "blinded": 0
                }
                enemies.append(enemy)
                print_slow(f"{enemy['name']} appears!")
            elif monster_type == 'vampire':
                enemy_type = MONSTER_TYPES['vampire']
                enemy = {
                    "health": enemy_type['health'],
                    "name": enemy_type['name'],
                    "attack_min": enemy_type['attack_min'],
                    "attack_max": enemy_type['attack_max'],
                    "stunned": 0,
                    "blinded": 0,
                    "lifesteal_range": enemy_type['lifesteal_range']
                }
                enemies.append(enemy)
                print_slow(f"{enemy['name']} appears!")
            elif monster_type == 'demon king lucifer':
                enemy_type = MONSTER_TYPES['demon king lucife']
                enemy = {
                    "health": enemy_type['health'],
                    "name": enemy_type['name'],
                    "attack_min": enemy_type['attack_min'],
                    "attack_max": enemy_type['attack_max'],
                    "stunned": 0,
                    "blinded": 0
                }
                enemies.append(enemy)
                print_slow(f"{enemy['name']} appears!")
            elif monster_type == 'demon king asmodeus':
                enemy_type = MONSTER_TYPES['demon king asmodeus']
                enemy = {
                    "health": enemy_type['health'],
                    "name": enemy_type['name'],
                    "attack_min": enemy_type['attack_min'],
                    "attack_max": enemy_type['attack_max'],
                    "stunned": 0,
                    "blinded": 0
                }
                enemies.append(enemy)
                print_slow(f"{enemy['name']} appears!")
            elif monster_type == 'demon king leviathan':
                enemy_type = MONSTER_TYPES['demon king leviathan']
                enemy = {
                    "health": enemy_type['health'],
                    "name": enemy_type['name'],
                    "attack_min": enemy_type['attack_min'],
                    "attack_max": enemy_type['attack_max'],
                    "stunned": 0,
                    "blinded": 0
                }
                enemies.append(enemy)
                print_slow(f"{enemy['name']} appears!")
            elif monster_type == 'demon king belphegor':
                enemy_type = MONSTER_TYPES['demon king belphegor']
                enemy = {
                    "health": enemy_type['health'],
                    "name": enemy_type['name'],
                    "attack_min": enemy_type['attack_min'],
                    "attack_max": enemy_type['attack_max'],
                    "stunned": 0,
                    "blinded": 0
                }
                enemies.append(enemy)
                print_slow(f"{enemy['name']} appears!")
            elif monster_type == 'demon king beelzebub':
                enemy_type = MONSTER_TYPES['demon king beelzebub']
                enemy = {
                    "health": enemy_type['health'],
                    "name": enemy_type['name'],
                    "attack_min": enemy_type['attack_min'],
                    "attack_max": enemy_type['attack_max'],
                    "stunned": 0,
                    "blinded": 0
                }
                enemies.append(enemy)
                print_slow(f"{enemy['name']} appears!")
            elif monster_type == 'demon king mammon':
                enemy_type = MONSTER_TYPES['demon king mammon']
                enemy = {
                    "health": enemy_type['health'],
                    "name": enemy_type['name'],
                    "attack_min": enemy_type['attack_min'],
                    "attack_max": enemy_type['attack_max'],
                    "stunned": 0,
                    "blinded": 0
                }
                enemies.append(enemy)
                print_slow(f"{enemy['name']} appears!")
            elif monster_type == 'demon king satan':
                enemy_type = MONSTER_TYPES['demon king satan']
                enemy = {
                    "health": enemy_type['health'],
                    "name": enemy_type['name'],
                    "attack_min": enemy_type['attack_min'],
                    "attack_max": enemy_type['attack_max'],
                    "stunned": 0,
                    "blinded": 0
                }
                enemies.append(enemy)
                print_slow(f"{enemy['name']} appears!")
            elif monster_type == 'demon':
                if player["level"] <= 3:
                    num_monsters = 1
                elif player["level"] <= 5:
                    num_monsters = 2
                elif player["level"] <= 10:
                    num_monsters = 3
                elif player["level"] <= 15:
                    num_monsters = 4
                else:
                    num_monsters = 5
                for i in range(num_monsters):
                    enemies.append(generate_random_demon())
                
                # Announce the encounter
                if num_monsters == 1:
                    print_slow(f"A {enemies[0]['name']} appears!")
                else:
                    monster_names = [f"{enemy['name']}" for enemy in enemies]
                    if len(monster_names) == 2:
                        print_slow(f"A {monster_names[0]} and a {monster_names[1]} appear!")
                    else:
                        print_slow(f"A {', '.join(monster_names[:-1])} and a {monster_names[-1]} appear!")
            else:  # normal monster - generate 1-5 random monsters
                if player["level"] <= 3:
                    num_monsters = 1
                elif player["level"] <= 5:
                    num_monsters = 2
                elif player["level"] <= 10:
                    num_monsters = 3
                elif player["level"] <= 15:
                    num_monsters = 4
                else:
                    num_monsters = 5
                for i in range(num_monsters):
                    enemies.append(generate_random_monster())
                
                # Announce the encounter
                if num_monsters == 1:
                    print_slow(f"A {enemies[0]['name']} appears!")
                else:
                    monster_names = [f"{enemy['name']}" for enemy in enemies]
                    if len(monster_names) == 2:
                        print_slow(f"A {monster_names[0]} and a {monster_names[1]} appear!")
                    else:
                        print_slow(f"A {', '.join(monster_names[:-1])}, and a {monster_names[-1]} appear!")

            last_turn_log = ""  # Initialize empty log for the first turn
            turn = 1
            
            # Combat loop
            original_armor = player["armor"]
            while len(enemies) > 0 and player["health"] > 0:
                print_slow("---------------------------")
                
                # Display all enemy health
                for i, enemy in enumerate(enemies):
                    print_slow(f"Enemy {i+1} ({enemy['name']}): {enemy['health']} HP")
                
                print_slow("---------------------------")
                print_slow(f"Your Health: {player['health']}")
                print_slow(f"Your Mana: {player['mana']}")
                print_slow(f"Your armor: {player['armor']}")

                # Display inventory
                show_inventory()
                print(GREEN)
                print_slow("---------------------------")
                
                if len(enemies) > 1:
                    print_slow("Choose an action: fight [enemy#], defend, cast [spell] [enemy#], use [item]")
                    print_slow("Enemy numbers: " + ", ".join([f"{i+1}: {enemy['name']}" for i, enemy in enumerate(enemies)]))
                else:
                    print_slow("Choose an action: fight, defend, cast [spell], use [item]")
                
                action = input(GREEN + "> ").lower().split()
                clear_screen()  # Clear the screen for the new combat turn
                turn += 1
                valid_action = False
                turn_log = ""  # Log for this turn
                
                # Parse target enemy if specified
                target_idx = 0  # Default to first enemy
                
                if len(action) > 0:
                    # Handle targeting for multiple enemies
                    if len(enemies) > 1 and len(action) > 1:
                        # Check if the last argument is a number for targeting
                        if action[-1].isdigit() and 1 <= int(action[-1]) <= len(enemies):
                            target_idx = int(action[-1]) - 1
                            action = action[:-1]  # Remove the target from action
                    
                    if action[0] == "fight":
                        valid_action = True
                        print(GREEN + "Time your attack! The closer to the green center, the more damage you deal!")
                        accuracy_percent = run_slider(7.5, 35)
                        base_damage = player["attack"]
                        attack_damage = int(base_damage * (accuracy_percent / 100))
                        
                        # Apply damage to targeted enemy
                        enemy = enemies[target_idx]
                        turn_log += f"{GREEN}You attack {enemy['name']} with {accuracy_percent}% accuracy for{COMBAT_COLOR} {attack_damage} damage!{RESET}\n"
                        enemy["health"] -= attack_damage
                        
                        # Check if enemy is defeated
                        if enemy["health"] <= 0:
                            turn_log += f"You defeated {enemy['name']}!\n"
                            # Don't remove enemy yet, do it after all enemies have attacked

                    elif action[0] == "defend":
                        valid_action = True
                        defense_percent = random.randint(40, 140)
                        plus_armor = round((10 * defense_percent) / 100)
                        mana_regen = round((20 * defense_percent) / 100)
                        player["armor"] = min(player["armor"] + plus_armor, 80)
                        player["mana"] += max(0, mana_regen)
                        turn_log += f"You defend with {defense_percent}% efficiency, gaining {plus_armor} armor and {mana_regen} mana!\n"

                    elif action[0] == "cast" and len(action) > 1:
                        valid_action = True
                        # Extract spell name - if target is included, it was already parsed above
                        spell_parts = action[1:]
                        if action[-1].isdigit() and len(enemies) > 1:
                            spell_parts = action[1:-1]
                        
                        spell_name = " ".join(spell_parts)  # Join all remaining words into spell name
                        
                        if spell_name in player["spells"] and player["mana"] >= player["spells"][spell_name][1]:
                            spell_percent = random.randint(40,140)
                            damage = 0  # Initialize damage to 0 by default
                            
                            # Get targeted enemy
                            enemy = enemies[target_idx]

                            # Handle spells - similar to before, but now targeting specific enemy
                            if spell_name == 'divine shield':
                                shield_strength = 2 * player["mana"]
                                player["divine_shield"] = {
                                    "strength": shield_strength,
                                    "rounds": 3,
                                    "mana_cost": player["mana"]
                                }
                                player["mana"] = 0
                                turn_log += f"You cast divine shield, blocking up to {shield_strength} damage for 3 rounds!\n"
                            elif spell_name in ['stun strike', 'thunder zapper', 'binding shot']:
                                stun_chance = spell_percent / 100
                                damage = 0
                                if random.random() < stun_chance:
                                    stun_duration = random.randint(2, 5)
                                    enemy["stunned"] = stun_duration
                                    turn_log += f"You cast {spell_name} with {spell_percent}% efficiency and stunned {enemy['name']} for {stun_duration} turns!\n"
                                else:
                                    turn_log += f"You cast {spell_name} but {enemy['name']} resisted!\n"
                            elif spell_name == 'stealth strike':
                                stun_chance = spell_percent / 100
                                damage = 0
                                if random.random() < stun_chance:
                                    confusion_duration = random.randint(2, 5)
                                    recovery_chance = random.randint(10, 30)
                                    enemy["confused"] = [confusion_duration, recovery_chance]
                                    turn_log += f"You cast {spell_name} with {spell_percent}% efficiency and confused {enemy['name']} for {confusion_duration} turns!\n"
                                else:
                                    turn_log += f"You cast {spell_name} but {enemy['name']} resisted!\n"
                            elif spell_name == "fireball":
                                base_damage = player["spells"][spell_name][0]
                                damage = int(base_damage * (spell_percent / 100))
                                burn_duration = 3
                                burn_damage = int(damage * 0.5)
                                enemy["burning"] = {
                                    "duration": burn_duration,
                                    "damage": burn_damage
                                }
                                turn_log += f"You cast {spell_name} at {enemy['name']} with {spell_percent}% efficiency for{COMBAT_COLOR} {damage} damage{RESET} and {RED}burns{RESET} the enemy!\n"
                                enemy["health"] -= damage
                            elif spell_name in ["back stab", "slash", "water bolt", "bleeding arrow", "eternity", "supernova", "phantasm", "assassinate", "tidal wave", "ultrakill", "midas prime", "kamehameha", "mordschlang", "boulder", "blood bomb", "blood spear", "haemolacria", "spear of justice"]:
                                base_damage = player["spells"][spell_name][0]
                                damage = int(base_damage * (spell_percent / 100))
                                turn_log += f"You cast {spell_name} at {enemy['name']} with {spell_percent}% efficiency for{COMBAT_COLOR} {damage} damage!{RESET}\n"
                                enemy["health"] -= damage
                            elif spell_name == "arrow of light":
                                blind_chance = spell_percent / 100
                                damage = 25
                                if random.random() < blind_chance:
                                    blind_duration = random.randint(2, 5)
                                    enemy["blind"] = blind_duration
                                    turn_log += f"You cast {spell_name} with {spell_percent}% efficiency and blinded {enemy['name']} for {blind_duration} turns!\n"
                                else:
                                    turn_log += f"You cast {spell_name} but {enemy['name']} resisted!\n"
                            elif spell_name == "heal":
                                base_healing = player["spells"][spell_name][0]
                                healing_amount = int(base_healing * (spell_percent / 100))
                                player["health"] = min(player["health"] + healing_amount, classes[player["class"]]["health"])
                                turn_log += f"You cast heal with {spell_percent}% efficiency, restoring {healing_amount} health!\n"
                            elif spell_name == "great heal":
                                base_healing = player["spells"][spell_name][0]
                                healing_amount = int(base_healing * (spell_percent / 100))
                                player["health"] = min(player["health"] + healing_amount, classes[player["class"]]["health"])
                                turn_log += f"You cast great heal with {spell_percent}% efficiency, restoring {healing_amount} health!\n"
                            elif spell_name == "minor heal":
                                base_healing = player["spells"][spell_name][0]
                                healing_amount = int(base_healing * (spell_percent / 100))
                                player["health"] = min(player["health"] + healing_amount, classes[player["class"]]["health"])
                                turn_log += f"You cast minor heal with {spell_percent}% efficiency, restoring {healing_amount} health!\n"
                            elif spell_name == "healing pool":
                                base_healing = player["spells"][spell_name][0]
                                healing_amount = int(base_healing * (spell_percent / 100))
                                player["health"] = min(player["health"] + healing_amount, classes[player["class"]]["health"])
                                turn_log += f"You cast healing pool with {spell_percent}% efficiency, restoring {healing_amount} health!\n"
                            elif spell_name == "life steal":
                                base_damage == player["spells"][spell_name][0]
                                damage = int(base_damage * (spell_percent / 100))
                                healing_amount = damage / 5
                                turn_log += f"You cast {spell_name} at {enemy['name']} with {spell_percent}% efficiency for{COMBAT_COLOR} {damage} damage{RESET} and you heal {healing_amount} health!\n"
                                player["health"] = min(player["health"] + healing_amount, classes[player["class"]]["health"])
                                enemy['health'] -= damage
                            elif spell_name == "finishing blow":
                                base_damage = player["spells"][spell_name][0]
                                
                                # Get enemy's original max health
                                max_enemy_health = MONSTER_TYPES[monster_type]['health'] if monster_type != 'normal' else MONSTER_TYPES['normal']['health']
                                current_health_percent = (enemy["health"] / max_enemy_health) * 100
                                
                                if current_health_percent < 25:
                                    damage_multiplier = 4
                                    turn_log += f"CRITICAL FINISHING BLOW! {enemy['name']} is weakened! \n"
                                elif current_health_percent < 50:
                                    damage_multiplier = 2
                                    turn_log += f"Strong finishing blow on {enemy['name']}! \n"
                                elif current_health_percent < 75:
                                    damage_multiplier = 1
                                    turn_log += f"Effective finishing blow on {enemy['name']}! \n"
                                else:
                                    damage_multiplier = 0.25
                                    turn_log += f"Weak finishing blow on {enemy['name']}! The enemy is too healthy! \n"
                                
                                damage = int(base_damage * (spell_percent / 100) * damage_multiplier)
                                turn_log += f"You deal {spell_percent}% accuracy for{COMBAT_COLOR} {damage} damage!{RESET}\n"
                                enemy["health"] -= damage
                            
                            # Deduct mana cost
                            player["mana"] -= player["spells"][spell_name][1]
                            
                        else:
                            turn_log += f"Not enough mana or invalid spell! (Spell: {spell_name})\n"
                            valid_action = False

                    elif action[0] == "use" and len(action) > 1:
                        valid_action = True
                        item_name = " ".join(action[1:])
                        item_result = use_item_during_combat(item_name)
                        if item_result:
                            turn_log += item_result + "\n"
                        else:
                            turn_log += "Invalid action!\n"
                            valid_action = False
                    else:
                        turn_log += "Invalid action!\n"
                        valid_action = False
                        
                    # Remove any defeated enemies
                    defeated_indices = []
                    for i, enemy in enumerate(enemies):
                        if enemy["health"] <= 0:
                            defeated_indices.append(i)
                    
                    # Remove from highest index to lowest to avoid index issues
                    for idx in sorted(defeated_indices, reverse=True):
                        del enemies[idx]
                    
                    # Check if all enemies are defeated
                    if len(enemies) == 0:
                        clear_screen()
                        print_slow(turn_log)  # Show the combat results first
                        
                        # Handle monster drops and rewards
                        if monster_type == 'boss':
                            # Boss rewards
                            gold_dropped = random.randint(
                                MONSTER_TYPES['boss']['gold_drop_range'][0],
                                MONSTER_TYPES['boss']['gold_drop_range'][1]
                            )
                            exp_earned = random.randint(
                                MONSTER_TYPES['boss']['exp_drop_range'][0],
                                MONSTER_TYPES['boss']['exp_drop_range'][1]
                            ) * int(currentRoom[0])
                            print_slow(f"You defeated the boss!\n You have earned {ITEM_COLOR}{gold_dropped} gold{RESET} and {ITEM_COLOR}{exp_earned} exp{RESET}!")
                            player["gold"] += gold_dropped
                            player["exp"] += exp_earned
                            defeated_bosses.append(currentRoom)

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] >= 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 15 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")

                        elif monster_type == 'vampire':
                            # Vampire rewards
                            gold_dropped = random.randint(
                                MONSTER_TYPES['vampire']['gold_drop_range'][0],
                                MONSTER_TYPES['vampire']['gold_drop_range'][1]
                            )
                            exp_earned = 100
                            inventory.append("vampire pendant")
                            print_slow(f"{RESET}Count Dracula dropped a mysterious {ITEM_COLOR}pendant{RESET}!")
                            print_slow(f"You earned {ITEM_COLOR}{gold_dropped} gold{RESET} and {ITEM_COLOR}100 exp{RESET}!")
                            
                            player["gold"] += gold_dropped
                            player["exp"] += exp_earned
                            defeated_bosses.append("Vampire")

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                        
                        elif monster_type == 'demon king lucifer':
                            # Vampire rewards
                            gold_dropped = random.randint(
                                MONSTER_TYPES['demon king lucifer']['gold_drop_range'][0],
                                MONSTER_TYPES['demon king lucifer']['gold_drop_range'][1]
                            )
                            exp_earned = random.randint(
                                MONSTER_TYPES['lucifer']['exp_drop_range'][0],
                                MONSTER_TYPES['lucifer']['exp_drop_range'][1]
                            )
                            print_slow(f"You earned {ITEM_COLOR}1000 gold{RESET} and {ITEM_COLOR}500 exp{RESET}!")
                            
                            player["gold"] += 1000
                            player["exp"] += 500
                            defeated_bosses.append("Demon King Lucifer")

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")

                        elif monster_type == 'demon king asmodeus':
                            # Boss rewards
                            for i in range(5):
                                inventory.append("adamantite bar")
                            print_slow(f"{RESET}Demon King Asmodeus dropped 5 {ITEM_COLOR}Adamanmtite bars{RESET}!")
                            print_slow(f"You defeated Demon King Asmodeus!\n You have earned {ITEM_COLOR}1000 gold{RESET} and {ITEM_COLOR}500 exp{RESET}!")
                            player["gold"] += 1000
                            player["exp"] += 500
                            defeated_bosses.append("Demon King Asmodeus")

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                        
                        elif monster_type == 'demon king leviathan':
                            # Vampire rewards
                            gold_dropped = random.randint(
                                MONSTER_TYPES['demon king leviathan']['gold_drop_range'][0],
                                MONSTER_TYPES['demon king leviathan']['gold_drop_range'][1]
                            )
                            exp_earned = random.randint(
                                MONSTER_TYPES['leviathan']['exp_drop_range'][0],
                                MONSTER_TYPES['leviathan']['exp_drop_range'][1]
                            )
                            print_slow(f"You earned {ITEM_COLOR}1000 gold{RESET} and {ITEM_COLOR}500 exp{RESET}!")
                            
                            player["gold"] += 1000
                            player["exp"] += 500
                            defeated_bosses.append("Demon King Levianthan")

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")

                        elif monster_type == 'demon king belphegor':
                            # Boss rewards
                            for i in range(5):
                                inventory.append("hallowed bar")
                            print_slow(f"{RESET}Demon King Belphegor dropped 5 {ITEM_COLOR}Hallowed bars{RESET}!")
                            print_slow(f"You defeated Demon King Belphegor!\n You have earned {ITEM_COLOR}1000 gold{RESET} and {ITEM_COLOR}500 exp{RESET}!")
                            player["gold"] += 1000
                            player["exp"] += 500
                            defeated_bosses.append("Demon King Belphegor")

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                        
                        elif monster_type == 'demon king beelzebub':
                            print_slow(f"You earned {ITEM_COLOR}1000 gold{RESET} and {ITEM_COLOR}500 exp{RESET}!")
                            
                            player["gold"] += 1000
                            player["exp"] += 500
                            defeated_bosses.append("Demon King Beelzebub")

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                        
                        elif monster_type == 'demon king mammon':
                            # Boss rewards
                            for i in range(5):
                                inventory.append("cosmilite bar")
                            print_slow(f"{RESET}Demon King Mammon dropped 5 {ITEM_COLOR}Cosmilite bars{RESET}!")
                            print_slow(f"You defeated Demon King Mammon!\n You have earned {ITEM_COLOR}1000 gold{RESET} and {ITEM_COLOR}500 exp{RESET}!")
                            player["gold"] += 1000
                            player["exp"] += 500
                            defeated_bosses.append("Demon King Mammon")

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                        elif monster_type == 'demon king satan':
                            # Boss rewards
                            print_slow(f"You defeated Demon King Satan!\n You have earned {ITEM_COLOR}1000 gold{RESET} and {ITEM_COLOR}1000 exp{RESET}!")
                            player["gold"] += 1000
                            player["exp"] += 1000
                            defeated_bosses.append("Demon King Satan")

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                        elif monster_type == "demon":
                            # Normal monster rewards - based on how many were defeated
                            gold_dropped = random.randint(
                                MONSTER_TYPES['normal']['gold_drop_range'][0],
                                MONSTER_TYPES['normal']['gold_drop_range'][1]
                            )
                            exp_earned = random.randint(
                                MONSTER_TYPES['normal']['exp_drop_range'][0],
                                MONSTER_TYPES['normal']['exp_drop_range'][1]
                            )
                            
                            # Chance for armor drops
                            if random.random() < MONSTER_TYPES['normal']['item_drop_chance']:
                                slot = random.choice(list(ARMOR_SLOTS.keys()))
                                tier = random.choice(['leather', 'chainmail', 'iron'])
                                dropped_item = f"{tier} {slot}"
                                inventory.append(dropped_item)
                                print_slow(f"{RESET}A monster dropped {ITEM_COLOR}{dropped_item}{RESET}!")
                            
                            # Key fragment drop chance
                            if random.random() < player['key_fragment_chance']:
                                inventory.append("key fragment")
                                print_slow(f"{RESET}A monster dropped a {ITEM_COLOR}key fragment{RESET}!")
                            
                            print_slow(f"You defeated all monsters\nYou have earned {ITEM_COLOR}{gold_dropped} gold{RESET} and {ITEM_COLOR}{exp_earned * num_monsters} exp{RESET}!")
                            player["gold"] += gold_dropped
                            player["exp"] += exp_earned * num_monsters

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                        else:
                            # Normal monster rewards - based on how many were defeated
                            gold_dropped = random.randint(
                                MONSTER_TYPES['normal']['gold_drop_range'][0],
                                MONSTER_TYPES['normal']['gold_drop_range'][1]
                            )
                            exp_earned = random.randint(
                                MONSTER_TYPES['normal']['exp_drop_range'][0],
                                MONSTER_TYPES['normal']['exp_drop_range'][1]
                            )* int(currentRoom[0])
                            
                            
                            # Chance for armor drops
                            if random.random() < MONSTER_TYPES['normal']['item_drop_chance']:
                                slot = random.choice(list(ARMOR_SLOTS.keys()))
                                tier = random.choice(['leather', 'chainmail', 'iron'])
                                dropped_item = f"{tier} {slot}"
                                inventory.append(dropped_item)
                                print_slow(f"{RESET}A monster dropped {ITEM_COLOR}{dropped_item}{RESET}!")
                            
                            # Key fragment drop chance
                            if random.random() < player['key_fragment_chance'] and not "bleeding key" in inventory and not inventory.count('key fragment') > 2:
                                inventory.append("key fragment")
                                print_slow(f"{RESET}A monster dropped a {ITEM_COLOR}key fragment{RESET}!")

                            print_slow(f"You defeated all monsters\nYou have earned {ITEM_COLOR}{gold_dropped} gold{RESET} and {ITEM_COLOR}{exp_earned * num_monsters} exp{RESET}!")
                            player["gold"] += gold_dropped
                            player["exp"] += exp_earned * num_monsters

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_GET_TO_LEVEL2[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{RESET}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{RESET}: {ITEM_COLOR}{player['health']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Mana{RESET}: {ITEM_COLOR}{player['mana']}{RESET}")
                                    print_slow(f"{ITEM_COLOR}Attack{RESET}: {ITEM_COLOR}{player['attack']}{RESET}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{RESET}: {ITEM_COLOR}{player['armor']}{RESET}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] == None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{RESET} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{RESET}!")
                        
                        player["armor"] = original_armor
                        del rooms[currentRoom]["monster"]
                        print_slow("---------------------------")
                        break
                    
                    if valid_action:
                        # All enemies attack if not stunned/confused
                        for i, enemy in enumerate(enemies):
                            # Skip defeated enemies
                            if enemy["health"] <= 0:
                                continue
                                
                            # Apply burning damage if active
                            if "burning" in enemy:
                                burn = enemy["burning"]
                                if burn["duration"] > 0:
                                    enemy["health"] -= burn["damage"]
                                    turn_log += f"{enemy['name']} takes {burn['damage']} burning damage! ({burn['duration']} turns remaining)\n"
                                    burn["duration"] -= 1
                                    if burn["duration"] <= 0:
                                        del enemy["burning"]
                                        turn_log += f"The fire consuming {enemy['name']} dies out.\n"
                            
                            # Check if enemy is stunned
                            if enemy["stunned"] > 0:
                                enemy["stunned"] -= 1
                                turn_log += f"{enemy['name']} is stunned and cannot attack! ({enemy['stunned']} turns remaining)\n"
                                if enemy["stunned"] <= 0:
                                    turn_log += f"{enemy['name']} recovers from being stunned!\n"
                                continue
                            
                            # Check if enemy is confused
                            if "confused" in enemy and enemy["confused"][0] > 0:
                                enemy["confused"][0] -= 1
                                turn_log += f"{enemy['name']} is confused and cannot attack! ({enemy['confused'][0]} turns remaining)\n"
                                recovery_chance = enemy["confused"][1]
                                recovery_roll = random.randint(1, 100)
                                if enemy["confused"][0] <= 0 or recovery_roll <= recovery_chance:
                                    del enemy["confused"]
                                    turn_log += f"{enemy['name']} recovers from being confused!\n"
                                continue


                            
                            # Handle vampire lifesteal
                            if monster_type == 'vampire' and "lifesteal_range" in enemy:
                                lifesteal_percent = random.randint(enemy["lifesteal_range"][0], enemy["lifesteal_range"][1])
                                lifesteal_amount = math.floor(player["health"] * (lifesteal_percent / 100))
                                enemy["health"] += lifesteal_amount
                                turn_log += f"{RED}{enemy['name']} drains {lifesteal_amount} health ({lifesteal_percent}% of your current health)!{RESET}\n"
                            
                            # Normal enemy attack
                            enemy_attack = math.floor(random.randint(enemy["attack_min"], enemy["attack_max"]) * (1 - player["armor"] / 100))
                            
                            # Handle divine shield
                            if hasattr(player, "divine_shield") and player["divine_shield"]:
                                shield = player["divine_shield"]
                                if shield["rounds"] > 0:
                                    damage_blocked = min(shield["strength"], enemy_attack)
                                    enemy_attack -= damage_blocked
                                    shield["strength"] -= damage_blocked
                                    shield["rounds"] -= 1
                                    turn_log += f"Divine shield blocks {damage_blocked} damage from {enemy['name']}! ({shield['rounds']} rounds remaining)\n"
                                    
                                    if shield["rounds"] <= 0 or shield["strength"] <= 0:
                                        turn_log += "Divine shield fades away!\n"
                                        player["divine_shield"] = None
                            
                            player["health"] -= enemy_attack
                            turn_log += f"{enemy['name']} attacks you for{RED} {enemy_attack} damage!{RESET}\n"
                        
                        # Check player death
                        if player["health"] <= 0:
                            turn_log += "You died! Game over.\n"
                            print_slow(turn_log)
                            exit()
                        
                        last_turn_log = turn_log
                        print_slow(turn_log)
                    else:
                        print_slow("Invalid action! Try again.")
                    
    # Show current status
    if currentRoom == '1-17':
        print_slow('Shop')
        print_slow("---------------------------")
        show_market_items()
    if currentRoom == '1-13':
        print_slow('Blacksmith')
        print_slow("---------------------------")
        show_blacksmith_items()
        print_slow("Type 'forge [item]' to craft items")
    if currentRoom == '2~11':
        print_slow('Mare')
        print_slow("---------------------------")
        show_mare_items()
        print_slow("Type 'forge [item]' to craft items")
    showStatus()


    move = input(GREEN + "> ").lower().split()
    clear_screen()
    if len(move) > 0:
        # Handle help command
        if move[0] in ['help', 'h']:
            if len(move) > 1:
                showHelp(' '.join(move[1:]))
            else:
                showHelp()
            continue
        # Add to the main game loop command handling
        elif move[0] in ['save']:
            save_game()
            continue
        elif move[0] in ['load', 'l']:
            load_game()
            continue
        # Handle movement - check "go direction", just "direction", or single letter direction
        elif move[0] == 'go' or move[0] in ['north', 'south', 'east', 'west', 'up', 'down', 'n', 's', 'e', 'w', 'u', 'd']:
            # Convert single letter to full direction
            direction_map = {
                'n': 'north', 's': 'south', 'e': 'east', 
                'w': 'west', 'u': 'up', 'd': 'down'
            }
            direction = move[1] if move[0] == 'go' else direction_map.get(move[0], move[0])
            if direction in rooms[currentRoom]:
                currentRoom = rooms[currentRoom][direction]
            else:
                print_slow(f"Error: You can't go that way: {direction}")
            continue
        # Handle item pickup
        elif move[0] in ['get', 'g']:
            if len(move) == 1:  # No specific item specified, get everything
                if "item" in rooms[currentRoom]:
                    if isinstance(rooms[currentRoom]["item"], list):
                        items = rooms[currentRoom]["item"]
                        if items:
                            formatted_items = [f"{ITEM_COLOR}{item}{RESET}" for item in items]
                            if len(formatted_items) == 1:
                                item_str = formatted_items[0]
                            elif len(formatted_items) == 2:
                                item_str = " and ".join(formatted_items)
                            else:
                                item_str = ", ".join(formatted_items[:-1]) + f" and {formatted_items[-1]}"
                            inventory.extend(items)
                            print_slow(f"Got {item_str}!")
                            del rooms[currentRoom]['item']
                        else:
                            print_slow("Nothing to pick up!")
                    else:
                        item = rooms[currentRoom]['item']
                        inventory.append(item)
                        print_slow(f"Got {ITEM_COLOR}{item}{RESET}!")
                        del rooms[currentRoom]['item']
                else:
                    print_slow("Nothing to pick up!")
            else:  # Specific item specified
                item_name = " ".join(move[1:])
                if "item" in rooms[currentRoom]:
                    if isinstance(rooms[currentRoom]["item"], list):
                        if item_name in rooms[currentRoom]["item"]:
                            rooms[currentRoom]["item"].remove(item_name)
                            if not rooms[currentRoom]["item"]:  # If list is empty after removal
                                del rooms[currentRoom]["item"]
                            inventory.append(item_name)
                            print_slow(f"Got {ITEM_COLOR}{item_name}{RESET}!")
                        else:
                            print_slow(f"Can't get {item_name}!")
                    elif item_name == rooms[currentRoom]['item']:
                        inventory.append(item_name)
                        print_slow(f"Got {ITEM_COLOR}{item_name}{RESET}!")
                        del rooms[currentRoom]['item']
                    else:
                        print_slow(f"Can't get {item_name}!")
                else:
                    print_slow(f"Can't get {item_name}!")
            continue
        # Handle item usage
        elif move[0] == 'use':
            try:
                # Parse item name and quantity
                item_parts = " ".join(move[1:]).split(' x')
                item_name = item_parts[0].strip()
                quantity = int(item_parts[1]) if len(item_parts) > 1 else 1
                
                # Count how many of the item we have
                item_count = inventory.count(item_name)

                if item_count >= quantity:
                    for _ in range(quantity):

                        if item_name == "health potion":
                            player["health"] = min(classes[player["class"]]["health"], player["health"] + 30)
                            inventory.remove("health potion")
                            print_slow("Used health potion! Restored 30 health!")
                        elif item_name == "mana potion":
                            player["mana"] = min(classes[player["class"]]["mana"], player["mana"] + 30)
                            inventory.remove("mana potion")
                            print_slow("Used mana potion! Restored 30 mana!")
                        elif item_name == "vampire pendant":
                            if  player['level'] > 10:
                                player["class 2"] = "Vampire"
                                inventory.remove("vampire pendant")
                                player["spells"] = spells_tier_2["Vampire"]
                                print(f"You have become a {ITEM_COLOR}Vampire{RESET} and have learnt {ITEM_COLOR}{', '.join(spells_tier_2['Vampire'].keys())}{RESET}!")
                            else:
                                print_slow("You need to be at least level 10 to use this item!")
                        elif item_name == "spell book":
                            display_spell_book(player["class"], player["class 2"])
                            spell = input(GREEN + "> ").lower()
                            clear_screen()
                            if spell == "exit":
                                print_slow("You close the spell book.")
                            elif spell in locked_spells[player["class"]]:
                                # Add the spell to player's spells
                                player["spells"][spell] = locked_spells[player["class"]][spell]
                                # Remove the spell from locked spells
                                del locked_spells[player["class"]][spell]
                                inventory.remove("spell book")
                                print_slow(f"You learned the {COMBAT_COLOR}{spell}{RESET} spell!")
                            else:
                                if not locked_spells[player["class"]]:
                                    print_slow("You have learned all available spells!")
                                else:
                                    print_slow("That spell isn't available to learn.")
                        elif item_name == "bleeding key" and currentRoom == "1-10":
                            rooms["1-10"]["down"] = "dungeon-1"
                            inventory.remove("bleeding key")
                            print_slow("You unlock the dungeon entrance with the bleeding key!")
                        else:
                            print_slow("You can't use that item!")
                else:
                    print_slow(f"Not enough {item_name}! (Have {item_count}, need {quantity})")
            except Exception as e:
                print_slow(f"Error using item: {str(e)}")
        # Handle armor removal
        elif move[0] in ['remove', 'r']:
            if len(move) == 1:
                # Remove all equipment when no slot specified
                result = remove_armor()
                print_slow(result)
            else:
                # Remove specific slot
                slot = " ".join(move[1:])
                result = remove_armor(slot)
                print_slow(result)
            continue
        # Handle armor equipping
        elif move[0] in ['equip', 'i']:
            if len(move) == 1:
                # Auto-equip best available gear
                result = equip_armor()
                print_slow(result)
            elif len(move) == 2:
                # Auto-equip best available gear for specific slot
                result = equip_armor(move[1])
                print_slow(result)
            elif len(move) == 3:
                # Manual equip specific item to specific slot
                result = equip_armor(move[2], move[1])
                print_slow(result)
            else:
                print_slow("Usage: equip [slot] [type] or equip [slot] or equip")
            continue
        elif move[0] == 'buy' and currentRoom == '1-17':
            item_name = " ".join(move[1:])
            result = buy_item(item_name)
            print_slow(result)
            continue
        elif move[0] == 'sell' and currentRoom == '1-17' or move[0] == 'sell' and currentRoom == '1-13' or move[0] == 'sell' and currentRoom == '2~11':
            item_name = " ".join(move[1:])
            result = sell_item(item_name)
            print_slow(result)
            continue
        elif move[0] == 'forge' and currentRoom == '1-13':
            item_name = " ".join(move[1:])
            result = forge_item(item_name)
            print_slow(result)
            continue
        elif move[0] == 'forge' and currentRoom == '2~11':
            item_name = " ".join(move[1:])
            result = forge_DLC_item(item_name)
            print_slow(result)
            continue

        elif move[0] in ['drop']:
            if len(move) == 1:
                # Drop all items
                if not inventory:
                    print_slow("You have nothing to drop!")
                else:
                    dropped_items = inventory.copy()
                    if "item" not in rooms[currentRoom]:
                        rooms[currentRoom]["item"] = []
                    elif not isinstance(rooms[currentRoom]["item"], list):
                        rooms[currentRoom]["item"] = [rooms[currentRoom]["item"]]
                    rooms[currentRoom]["item"].extend(dropped_items)
                    inventory.clear()
                    print_slow(f"Dropped all items: {ITEM_COLOR}{', '.join(dropped_items)}{RESET}")
            else:
                # Drop specific item
                item_name = " ".join(move[1:])
                if item_name in inventory:
                    inventory.remove(item_name)
                    if "item" not in rooms[currentRoom]:
                        rooms[currentRoom]["item"] = []
                    elif not isinstance(rooms[currentRoom]["item"], list):
                        rooms[currentRoom]["item"] = [rooms[currentRoom]["item"]]
                    rooms[currentRoom]["item"].append(item_name)
                    print_slow(f"Dropped: {ITEM_COLOR}{item_name}{RESET}")
                else:
                    print_slow(f"You don't have {item_name}!")
            continue
        elif move[0].lower() in ["stop", "quit", "exit", "halt", "q"]:
            print("\033[38;2;255;255;255m")
            quit()
        # Handle invalid commands
        else:
            print_slow("Invalid command!")
    else:
        print_slow("Invalid command!")
