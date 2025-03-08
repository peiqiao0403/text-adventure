import sys
import random
import math
import time
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


# Define armor tiers and their properties
ARMOR_TIERS = {
    'leather': {'defense': 5, 'weight': 1},
    'chainmail': {'defense': 10, 'weight': 2},
    'iron': {'defense': 15, 'weight': 3}
}

# Add sword tiers
SWORD_TIERS = {
    'wooden': {'damage': 5},
    'iron': {'damage': 10},
    'steel': {'damage': 15},
    'mythril': {'damage': 30}
}
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
def showStart():
    print_slow('''\nText Adventure\n=========\nCommands:\ngo [direction]\nget [item]\nuse [item]''')
    print_slow('---------------------------')
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
    'helmet': ['leather', 'chainmail', 'iron'],
    'chestplate': ['leather', 'chainmail', 'iron'],
    'pants': ['leather', 'chainmail', 'iron'],
    'boots': ['leather', 'chainmail', 'iron']
}

MONSTER_TYPES = {
    'normal': {
        'name': 'Monster',
        'health': 50,
        'attack_min': 5,
        'attack_max': 15,
        'gold_drop_range': (10, 30),
        'item_drop_chance': 0.2
    },
    'boss': {
        'name': 'Boss Monster',
        'health': 200,
        'attack_min': 25,
        'attack_max': 35,
        'gold_drop_range': (100, 150),
        'item_drop_chance': 1
    },
    'vampire': {  # Add vampire boss type
        'name': 'Count Dracula',
        'health': 250,
        'attack_min': 35,
        'attack_max': 50,
        'gold_drop_range': (1000, 1500),
        'item_drop_chance': 1,
        'lifesteal_range': (1, 5)  # Percentage range for lifesteal
    }
}

classes = {
    "Warrior": {"health": 120, "armor": 0, "mana": 30, "spells": {"slash": [10, 10]}, "attack": 25},
    "Mage": {"health": 80, "armor": 0, "mana": 100, "spells": {"fireball": [30, 40]}, "attack": 20},
    "Rogue": {"health": 100, "armor": 0, "mana": 50, "spells": {"shadow strike": [20, 25]}, "attack": 20},
    "Healer": {"health": 150, "armor": 0, "mana": 45, "spells": {"circle heal": [30, 35]}, "attack": 12},
    "Ranger": {"health": 110, "armor": 0, "mana": 20, "spells": {"bleeding arrow": [25, 25]}, "attack": 20}
}

class HelpSystem:

    def __init__(self):
        self.pages = {
            'commands': '''\nCommands Reference\n=================\nBasic Commands:\n- go [direction]     - Move character\n- get [item]         - Pick up items\n- use [item]         - Use items\n- help              - Show this menu\n- remove [slot]      - Remove armor from slot\n- equip [type] [slot]- Equip armor in slot\n- list              - Show market items\n- buy [item]        - Buy from market\n- sell [item]       - Sell to market\n''',
            'classes': '''\nCharacter Classes\n================\n┌─────────┬───────┬────┬────┬───────────────┬────────┬──────────────┐\n│ Class   │Health │Mana│Atk │Spell          │Effect  │Spell Cost    │\n├─────────┼───────┼────┼────┼───────────────┼────────┼──────────────┤\n│ Warrior │ 120   │ 30 │ 25 │ Slash         │ +10 dmg│ 10 Mana      │\n│ Mage    │ 80    │100 │ 20 │ Fireball      │ +30 dmg│ 40 Mana      │\n│ Rogue   │ 100   │ 50 │ 20 │ Shadow Strike │ +20 dmg│ 25 Mana      │\n│ Healer  │ 150   │ 45 │ 12 │ Circle Heal   │ +30 HP │ 35 Mana      │\n│ Ranger  │ 110   │ 20 │ 20 │ Bleeding Arrow│ +25 dmg│ 25 Mana      │\n└─────────┴───────┴────┴────┴───────────────┴────────┴──────────────┘\n''',
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

def clear_lines(number):
    sys.stdout.write("\033[2J\033[H")
    for i in range(number):
        sys.stdout.write("\033[F")
    print("         " * 10, end="")
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
    return "\n".join(directions)

def showStatus():
    print_slow('You are in the ' + BLUE+currentRoom+RESET)
    print_slow('Available directions:')
    print_slow(showAvailableDirections(rooms[currentRoom]))
    print_slow(f'Health: {player["health"]}')
    print_slow(f'Armor: {player["armor"]}')
    print_slow(f'Mana: {player["mana"]}')
    print_slow(f'Gold: {player["gold"]}')
    print_slow(f'Class: {BLUE}{player["class"]}{RESET}')
    print_slow('Equipped Armor:')
    for slot, item in player_equipment.items():
        if item:
            print_slow(f'- {slot}: {ITEM_COLOR}{item}{RESET}')
    print_slow_list('Inventory', inventory)
    if "item" in rooms[currentRoom]:
        if rooms[currentRoom]['item'] == 'monster':
            print_slow("A fearsome monster awaits you!")
        else:
            print_slow(f"{GREEN}You see a{RESET} {ITEM_COLOR}{rooms[currentRoom]['item']}{RESET}")
    print_slow("---------------------------")

def print_slow_list(tag, items):
    print_slow(f"{tag}: {ITEM_COLOR}{', '.join(map(str, items))}{RESET}")

def equip_armor(item_type, slot):
    """Equip armor or sword in specified slot"""
    global player_equipment
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

    # Handle armor equipping (existing code)
    item_name = f"{item_type} {slot}"
    if item_name not in inventory:
        return f"You don't have {item_type} {slot}!"
    current_item = player_equipment[slot]
    if current_item:
        old_tier = current_item.split(' ')[0]
        if old_tier != item_type:
            return f"You must remove {old_tier} {slot} first!"
    player_equipment[slot] = item_name
    inventory.remove(item_name)
    defense_bonus = ARMOR_TIERS[item_type]['defense']
    player["armor"] += defense_bonus
    return f"Equipped {item_type} {slot} (+{defense_bonus} defense)"


def remove_armor(slot):
    """Remove armor or sword from specified slot"""
    global player_equipment
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

    # Handle armor removal (existing code)
    item_type = current_item.split(' ')[0]
    defense_bonus = ARMOR_TIERS[item_type]['defense']
    player["armor"] -= defense_bonus
    inventory.append(current_item)
    player_equipment[slot] = None
    return f"Removed {current_item} (-{defense_bonus} defense)"


# Room layout with armor items
rooms = {
    '1-1': {
        "east": '1-2',
        "item": "health potion"
    },
    '1-2': {
        'north': '1-3',
        'west': '1-1',
        "item": "monster"
    },
    '1-3': {
        'west': '1-4',
        'south': '1-2',
        'item': 'iron sword'
    },
    '1-4': {
        'east': '1-3',
        'west': '1-15',
        'north': '1-5',
        'item': 'chainmail boots'
    },
    '1-5': {
        'south': '1-4',
        'west': '1-6',
        'item': 'monster'
    },
    '1-6': {
        'west': '1-7',
        'east': '1-5',
        "item": "mana potion"
    },
    '1-7': {
        'east': '1-6',
        'west': '1-8',
        'south': '1-15',
        'item': 'monster'
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
        "item": "key"
    },
    '1-10': {
        'south': '1-11',
        'east': '1-9',
        "item": "monster"
    },
    '1-11': {
        'north': '1-10',
        "item": "leather helmet"
    },
    '1-12': {
        'south': '1-11',
        'item': 'monster'
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
        "item": "health potion"
    },
    '1-16': {
        'east': '1-1',
        'north': '1-14',
        'south': '1-17',
        'west': '1-13',
        'item': 'monster'
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
        'item': 'monster'
    },
    '1-20': {
        'east': '1-19'
    }
}



# Game setup
clear_lines(100)
print(GREEN)
print_slow(r"""
 _____         _      _   _
|_   _|____  _| |_   | | | | ___ _ __ ___
  | |/ _ \ \/ / __|  | |_| |/ _ \ '__/ _ \
  | |  __/>  <| |_   |  _  |  __/ | | (_) |
  |_|\___/_/\_\\__|  |_| |_|\___|_|  \___/
""")

print_slow("Welcome to the Text Hero!")
print_slow("To start, choose a class: Warrior, Mage, Rogue, Healer, Ranger")
chosen_class = input(GREEN + "> ").capitalize()
clear_lines(100)
if chosen_class not in classes:
    chosen_class = "Warrior"
def use_item_during_combat(item):
    try:
        if item == "health potion" and item in inventory:
            player["health"] = min(classes[player["class"]]["health"], player["health"] + 30)
            inventory.remove("health potion")
            return "Used health potion! Restored 30 health!"
        elif item == "mana potion" and item in inventory:
            player["mana"] = min(classes[player["class"]]["mana"], player["mana"] + 30)
            inventory.remove("mana potion")
            return "Used mana potion! Restored 30 mana!"
        else:
            return f"Cannot use {item} during combat!"
    except Exception as e:
        return f"Error using item: {str(e)}"
player = {
    "health": classes[chosen_class]["health"],
    "armor": classes[chosen_class]["armor"],
    "mana": classes[chosen_class]["mana"],
    "class": chosen_class,
    "spells": classes[chosen_class]["spells"],
    "attack": classes[chosen_class]["attack"],
    "gold": 0  # Starting gold
}

player_equipment = {
    'helmet': None,
    'chestplate': None,
    'pants': None,
    'boots': None,
    'sword': None  # Add sword slot
}

# Initialize inventory
inventory = []

# Track defeated bosses
defeated_bosses = set()


def show_market_items():
    # print_slow top border
    print_slow("""┌──────────────────────┬────────────┬────────────────────────┐
| Item Name            │ Price      │ Description            |
├──────────────────────┼────────────┼────────────────────────┤
| health potion        │    30 gold │ Restores 30 health     |
| mana potion          │    30 gold │ Restores 30 mana       |
| leather helmet       │    50 gold │ Basic head protection  |
| leather chestplate   │    70 gold │ Basic chest protection |
| leather pants        │    60 gold │ Basic leg protection   |
| leather boots        │    40 gold │ Basic foot protection  |
└──────────────────────┴────────────┴────────────────────────┘""")
    print_slow("---------------------------")
    


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

# Main game loop
currentRoom = '1-1'
help_system = HelpSystem()

while True:
    # Automatic combat initiation when a monster is present
    if "item" in rooms[currentRoom] and rooms[currentRoom]["item"] == "monster":
        clear_lines(100)
        # Determine monster type
        if currentRoom == '1-19':
            enemy_type = MONSTER_TYPES['boss']
        elif currentRoom == '1-10':
            enemy_type = MONSTER_TYPES['vampire']
        else:
            enemy_type = MONSTER_TYPES['normal']
        
        enemy = {
            "health": enemy_type['health'],
            "name": enemy_type['name'],
            "attack_min": enemy_type['attack_min'],
            "attack_max": enemy_type['attack_max']
        }

        # Add vampire-specific attributes if applicable
        if currentRoom == '1-10':
            enemy["lifesteal_range"] = enemy_type['lifesteal_range']

        last_turn_log = ""  # Initialize empty log for the first turn.
        print_slow(f"A {enemy['name']} appears!")
        turn = 1
        # Combat loop
        original_armor = player["armor"]
        while enemy["health"] > 0 and player["health"] > 0:
            print_slow("---------------------------")
            print_slow(f"Enemy Health: {enemy['health']}")
            print_slow("---------------------------")
            print_slow(f"Your Health: {player['health']}")
            print_slow(f"Your Mana: {player['mana']}")
            print_slow(f"Your Armour: {player['armor']}")

            # Display inventory
            print_slow("\nInventory:")
            if inventory:
                for i, item in enumerate(inventory, 1):
                    print_slow(f"{i}. {item}")
            else:
                print_slow("Empty")
            
            print_slow("---------------------------")
            print_slow("Choose an action: fight, defend, cast [spell], use [item]")
            action = input(GREEN + "> ").lower().split()
            clear_lines(100)  # Clear the screen for the new combat turn
            turn += 1
            valid_action = False
            turn_log = ""  # Log for this turn
            if len(action) > 0:
                if action[0] == "fight":
                    valid_action = True
                    print(GREEN + "Time your attack! The closer to the green center, the more damage you deal!")
                    accuracy_percent = run_slider(7.5, 35)
                    base_damage = player["attack"]
                    attack_damage = int(base_damage * (accuracy_percent / 100))
                    turn_log += f"{GREEN}You attack with {accuracy_percent}% accuracy for{COMBAT_COLOR} {attack_damage} damage!{RESET}\n"
                    enemy["health"] -= attack_damage

                elif action[0] == "defend":
                    valid_action = True
                    defense_percent = random.randint(40, 140)
                    plus_armour = round((10 * defense_percent) / 100)
                    mana_regen = round((20 * defense_percent) / 100)
                    player["armor"] += plus_armour
                    player["mana"] += mana_regen
                    turn_log += f"You defend with {defense_percent}% efficiency, gaining {plus_armour} armor and {mana_regen} mana!\n"

                elif action[0] == "cast" and len(action) > 1:
                    valid_action = True
                    spell_name = " ".join(action[1:])  # Join all remaining words into spell name
                    if spell_name in player["spells"] and player["mana"] >= player["spells"][spell_name][1]:
                        spell_percent = random.randint(40,140)

                        if spell_name == "fireball":
                            base_damage = player["spells"][spell_name][0]
                            damage = int(base_damage * (spell_percent / 100))
                            turn_log += f"You cast {spell_name} with {spell_percent}% efficiency for{COMBAT_COLOR} {damage} damage{RESET}!\n"
                        elif spell_name == "shadow strike":
                            base_damage = player["spells"][spell_name][0]
                            damage = int(base_damage * (spell_percent / 100))
                            turn_log += f"You cast {spell_name} with {spell_percent}% efficiency for{COMBAT_COLOR} {damage} damage!{RESET}\n"
                        elif spell_name == "slash":
                            base_damage = player["spells"][spell_name][0]
                            damage = int(base_damage * (spell_percent / 100))
                            turn_log += f"You swing your weapon with {spell_percent}% precision for{COMBAT_COLOR} {damage} damage!{RESET}\n"
                        elif spell_name == "circle heal":
                            base_healing = player["spells"][spell_name][0]
                            healing_amount = int(base_healing * (spell_percent / 100))
                            player["health"] = min(player["health"] + healing_amount,
                                                classes[player["class"]]["health"])
                            turn_log += f"You cast circle heal with {spell_percent}% efficiency, restoring {healing_amount} health!\n"
                        elif spell_name == "bleeding arrow":
                            base_damage = player["spells"][spell_name][0]
                            damage = int(base_damage * (spell_percent / 100))
                            turn_log += f"You shoot an arrow with {spell_percent}% accuracy for{COMBAT_COLOR} {damage} damage!{RESET}\n"

                        enemy["health"] -= damage
                        player["mana"] -= player["spells"][spell_name][1]
                    else:
                        turn_log += "Not enough mana or invalid spell!\n"
                elif action[0] == "use" and len(action) > 1:
                    valid_action = True
                    item_name = " ".join(action[1:])
                    item_result = use_item_during_combat(item_name)
                    if item_result:
                        turn_log += item_result + "\n"
                    else:
                        turn_log += "Invalid action!\n"

            else:
                turn_log += "Invalid action!\n"
                continue
            if valid_action:
                if enemy["health"] <= 0:
                    clear_lines(100)
                    gold_dropped = random.randint(enemy_type['gold_drop_range'][0],
                                                enemy_type['gold_drop_range'][1])
                    player["gold"] = player.get("gold", 0) + gold_dropped
                    
                    # Special drops for specific bosses
                    if currentRoom == '1-10':  # Vampire boss
                        inventory.append("vampire pendant")
                        print_slow(f"\n{RESET}Count Dracula dropped a mysterious {ITEM_COLOR}vampire pendant{RESET}!")
                    if random.random() < enemy_type['item_drop_chance']:
                        # Drop a random armor piece
                        slot = random.choice(list(ARMOR_SLOTS.keys()))
                        tier = random.choice(['leather', 'chainmail', 'iron'])
                        dropped_item = f"{tier} {slot}"
                        inventory.append(dropped_item)
                        print_slow(f"\n{RESET}{enemy['name']} dropped {dropped_item}!")
                    print_slow(turn_log)
                    print_slow(f"You defeated {enemy['name']} and earned{ITEM_COLOR} {gold_dropped} gold{RESET}!")
                    print_slow("---------------------------")
                    player["armor"] = original_armor
                    del rooms[currentRoom]["item"]
                    break
            # Monster's turn to attack
            if currentRoom == '1-10' and "lifesteal_range" in enemy:
                lifesteal_percent = random.randint(enemy["lifesteal_range"][0], enemy["lifesteal_range"][1])
                lifesteal_amount = math.floor(player["health"] * (lifesteal_percent / 100))
                enemy["health"] += lifesteal_amount
                turn_log += f"{RED}Count Dracula drains {lifesteal_amount} health ({lifesteal_percent}% of your current health)!{RESET}\n"
            enemy_attack = math.floor(random.randint(enemy["attack_min"], enemy["attack_max"]) * (1 - player["armor"] / 100))
            player["health"] -= enemy_attack
            turn_log += f"{enemy['name']} attacks you for{RED} {enemy_attack} damage!{RESET}\n"
            
            # Add vampire lifesteal


            if player["health"] <= 0:
                turn_log += "You died! Game over.\n"
                print_slow(turn_log)
                exit()
            last_turn_log = turn_log
            print_slow(turn_log)
            continue
    # Show current status
    if currentRoom == '1-17':
        print_slow('Shop')
        print_slow("---------------------------")
        show_market_items()
    showStatus()

    move = input(GREEN + "> ").lower().split()
    clear_lines(100)
    if len(move) > 0:
    # Handle help command
        if move[0] == 'help':
            if len(move) > 1:
                showHelp(' '.join(move[1:]))
            else:
                showHelp()
            continue
        # Handle movement
        elif move[0] == 'go':
            direction = move[1]
            if direction in rooms[currentRoom]:
                currentRoom = rooms[currentRoom][direction]
            else:
                print_slow(f"Error: You can't go that way: {direction}")
            continue
        # Handle item pickup
        elif move[0] == 'get':
            item_name = " ".join(move[1:])
            if "item" in rooms[currentRoom] and item_name == rooms[currentRoom]['item']:
                inventory.append(item_name)
                print_slow(item_name + ' got!')
                del rooms[currentRoom]['item']
            else:
                print_slow("Can't get " + item_name + "!")
            continue
        # Handle item usage
        elif move[0] == 'use':
            item_name = " ".join(move[1:])
            if item_name in inventory:
                if item_name == "health potion":
                    player["health"] = min(classes[player["class"]]["health"], player["health"] + 30)
                    inventory.remove("health potion")
                    print_slow("You used a health potion and restored 30 health!")
                elif item_name == "mana potion":
                    player["mana"] = min(classes[player["class"]]["mana"], player["mana"] + 30)
                    inventory.remove("mana potion")
                    print_slow("You used a mana potion and restored 30 mana!")
                elif item_name in ARMOR_SLOTS:
                    # Handle armor equipping
                    slot = item_name.split(' ')[1]
                    item_type = item_name.split(' ')[0]
                    result = equip_armor(slot, item_type)
                    print_slow(result)
                else:
                    print_slow("You can't use that item!")
            else:
                print_slow("You don't have that item!")
            continue
        # Handle armor removal
        elif move[0] == 'remove':
            slot = " ".join(move[1:])
            result = remove_armor(slot)
            print_slow(result)
            continue
        # Handle armor equipping
        elif move[0] == 'equip':
            if len(move) >= 3:
                slot = move[1]
                item_type = move[2]
                result = equip_armor(slot, item_type)
                print_slow(result)
            else:
                print_slow("Usage: equip [slot] [type]")
            continue
        elif move[0] == 'buy' and currentRoom == '1-17':
            item_name = " ".join(move[1:])
            result = buy_item(item_name)
            print_slow(result)
            continue
        elif move[0] == 'sell' and currentRoom == '1-17':
            item_name = " ".join(move[1:])
            result = sell_item(item_name)
            print_slow(result)
            continue
        # Handle invalid commands
        else:
            print_slow("Invalid command!")
    else:
        print_slow("Invalid command!")
