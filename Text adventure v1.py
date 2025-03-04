import sys
import random
import math
import time
from threading import Thread


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
            if x == 28: y = -1 
            if x == 1: y = 1
            STR = (" " * (x - 1)) + "^" + (" " * (29 - (x + 1)))
            print("\033[101m        \033[103m     \033[102m   \033[103m     \033[101m        \033[0m")
            print(STR)
            time.sleep(self.delay)
            print("\033[F\033[F", end="")
            if self.kill: break
        self.result = x

def run_slider(scale: int, offset: int, delay = 0.03):
    """Returns a percentage for scaling numbers.
    Scale is the difference in between 2 spots.
    Offset is a number added to the result to raise the maximum & minimum percent."""
    main = static_slider(delay)
    main.start()
    input("Press Enter to stop the slider!")
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

def showStart():
    print('''\nRPG Game\n=========\nCommands:\ngo [direction]\nget [item]\nuse [item]''')
    print('---------------------------')
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

# Define monster types
MONSTER_TYPES = {
    'normal': {
        'health': 50,
        'attack_min': 5,
        'attack_max': 15,
        'gold_drop_range': (10, 30),
        'item_drop_chance': 0.2
    },
    'boss': {
        'health': 200,
        'attack_min': 25,
        'attack_max': 35,
        'gold_drop_range': (100, 150),
        'item_drop_chance': 1
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
            print(f"\n=== Help System ({self.current_page}) ===")
            print(self.pages[self.current_page])
            print("\nAvailable Pages:")
            for p in self.pages.keys():
                status = "*" if p == self.current_page else " "
                print(f"- [{status}] {p}")
            print("- Type 'help <page>' to view a different page")
            print("=============================")

def clear_lines(number):
    sys.stdout.write("\033[2J\033[H")
    for i in range(number):
        sys.stdout.write("\033[F")
    print("         " * 10, end="")
    print()
    sys.stdout.write("\033[F")

def showInstructions():
    """Only shown when help isn't used"""
    print('''\nRPG Game\n=========\nType 'help' for detailed game information\n---------------------------''')

def showHelp(page=None):
    """Global function to interface with the HelpSystem class"""
    global help_system
    help_system.display_help(page)
    return True  # Prevent instructions from showing

def showAvailableDirections(room):
    """Show all available directions for the current room with destination room numbers."""
    directions = []
    if 'north' in room:
        directions.append(f"  north: {room['north']}")
    if 'south' in room:
        directions.append(f"  south: {room['south']}")
    if 'east' in room:
        directions.append(f"  east: {room['east']}")
    if 'west' in room:
        directions.append(f"  west: {room['west']}")
    return "\n".join(directions)

def showStatus():
    print('You are in the ' + currentRoom)
    print('Available directions:')
    print(showAvailableDirections(rooms[currentRoom]))
    print('Health:', player["health"])
    print('Armor:', player["armor"])
    print('Mana:', player["mana"])
    print('Gold:', player["gold"])
    print('Class:', player["class"])
    print('Equipped Armor:')
    for slot, item in player_equipment.items():
        if item:
            print(f'- {slot}: {item}')
    print_list('Inventory', inventory)
    if "item" in rooms[currentRoom]:
        if rooms[currentRoom]['item'] == 'monster':
            print("A fearsome monster awaits you!")
        else:
            print('You see a ' + rooms[currentRoom]['item'])
    print("---------------------------")

def print_list(tag, items):
    print(f"{tag}: {', '.join(map(str, items))}")

def equip_armor(item_type, slot):
    """Equip armor in specified slot"""
    global player_equipment
    if slot not in ARMOR_SLOTS:
        return "Invalid armor slot!"
    # Check if item exists in inventory
    item_name = f"{item_type} {slot}"
    if item_name not in inventory:
        return f"You don't have {item_type} {slot}!"
    # Check if slot is empty or same tier
    current_item = player_equipment[slot]
    if current_item:
        old_tier = current_item.split(' ')[0]
        if old_tier != item_type:
            return f"You must remove {old_tier} {slot} first!"
    # Equip the armor
    player_equipment[slot] = item_name
    inventory.remove(item_name)
    defense_bonus = ARMOR_TIERS[item_type]['defense']
    player["armor"] += defense_bonus
    return f"Equipped {item_type} {slot} (+{defense_bonus} defense)"

def remove_armor(slot):
    """Remove armor from specified slot"""
    global player_equipment
    if slot not in ARMOR_SLOTS:
        return "Invalid armor slot!"
    current_item = player_equipment[slot]
    if not current_item:
        return f"No armor equipped in {slot} slot!"
    # Remove defense bonus
    item_type = current_item.split(' ')[0]
    defense_bonus = ARMOR_TIERS[item_type]['defense']
    player["armor"] -= defense_bonus
    # Return item to inventory
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
        'item': 'iron helmet'
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
        "item": "sword"
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
print("Welcome to the RPG Game!")
print("To start, choose a class: Warrior, Mage, Rogue, Healer, Ranger")
chosen_class = input("> ").capitalize()
clear_lines(100)
if chosen_class not in classes:
    chosen_class = "Warrior"
def use_item_during_combat(item):
    try:
        if item == "health potion" and item in inventory:
            player["health"] = min(classes[player["class"]]["health"], player["health"] + 30)
            inventory.remove("health potion")
            return f"Used health potion! Restored 30 health!"
        elif item == "mana potion" and item in inventory:
            player["mana"] = min(classes[player["class"]]["mana"], player["mana"] + 30)
            inventory.remove("mana potion")
            return f"Used mana potion! Restored 30 mana!"
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

# Initialize player's equipped armor
player_equipment = {
    'helmet': None,
    'chestplate': None,
    'pants': None,
    'boots': None
}

# Initialize inventory
inventory = []

# Track defeated bosses
defeated_bosses = set()


def show_market_items():
    # Print top border
    print("""┌──────────────────────┬────────────┬────────────────────────┐
| Item Name            │ Price      │ Description            |
├──────────────────────┼────────────┼────────────────────────┤
| health potion        │    30 gold │ Restores 30 health     |
| mana potion          │    30 gold │ Restores 30 mana       |
| leather helmet       │    50 gold │ Basic head protection  |
| leather chestplate   │    70 gold │ Basic chest protection |
| leather pants        │    60 gold │ Basic leg protection   |
| leather boots        │    40 gold │ Basic foot protection  |
└──────────────────────┴────────────┴────────────────────────┘""")
    print("---------------------------")
    


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
        clear_lines(100)  # Clear the screen for the new combat turn
        # Determine monster type (boss for room 1-19)
        enemy_type = MONSTER_TYPES['boss'] if currentRoom == '1-19' else MONSTER_TYPES['normal']
        enemy = {
            "name": "Boss Monster" if currentRoom == '1-19' else "Monster",
            "health": enemy_type['health'],
            "attack_min": enemy_type['attack_min'],
            "attack_max": enemy_type['attack_max']
        }
        last_turn_log = ""  # Initialize empty log for the first turn.
        print("A fearsome monster appears!")
        turn = 1
        # Combat loop

        while enemy["health"] > 0 and player["health"] > 0:
            print("---------------------------")
            print(f"Enemy Health: {enemy['health']}")
            print("---------------------------")
            print(f"Your Health: {player['health']}")
            print(f"Your Mana: {player['mana']}")
            print(f"Your Armour: {player['armor']}")

            # Display inventory
            print("\nInventory:")
            if inventory:
                for i, item in enumerate(inventory, 1):
                    print(f"{i}. {item}")
            else:
                print("Empty")
            
            print("---------------------------")
            print("Choose an action: fight, defend, cast [spell], use [item]")
            action = input("> ").lower().split()
            clear_lines(100)  # Clear the screen for the new combat turn
            turn += 1
            valid_action = False
            turn_log = ""  # Log for this turn
            
            if action[0] == "fight":
                valid_action = True
                print("Time your attack! The closer to the green center, the more damage you deal!")
                accuracy_percent = run_slider(5, 35)  # Scale of 5, minimum 50%
                base_damage = player["attack"]
                attack_damage = int(base_damage * (accuracy_percent / 100))
                turn_log += f"You attack with {accuracy_percent}% accuracy for {attack_damage} damage!\n"
                enemy["health"] -= attack_damage
            
            elif action[0] == "defend":
                valid_action = True
                print("Time your defense! Better timing means more protection!")
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
                    print(f"Time your spell casting! Better timing means more effective {spell_name}!")
                    spell_percent = random.randint(40,140)
                    
                    if spell_name == "fireball":
                        base_damage = player["spells"][spell_name][0]
                        damage = int(base_damage * (spell_percent / 100))
                        turn_log += f"You cast {spell_name} with {spell_percent}% efficiency for {damage} damage!\n"
                    elif spell_name == "shadow strike":
                        base_damage = player["spells"][spell_name][0]
                        damage = int(base_damage * (spell_percent / 100))
                        turn_log += f"You cast {spell_name} with {spell_percent}% efficiency for {damage} damage!\n"
                    elif spell_name == "slash":
                        base_damage = player["spells"][spell_name][0]
                        damage = int(base_damage * (spell_percent / 100))
                        turn_log += f"You swing your weapon with {spell_percent}% precision for {damage} damage!\n"
                    elif spell_name == "circle heal":
                        base_healing = player["spells"][spell_name][0]
                        healing_amount = int(base_healing * (spell_percent / 100))
                        player["health"] = min(player["health"] + healing_amount,
                                            classes[player["class"]]["health"])
                        turn_log += f"You cast circle heal with {spell_percent}% efficiency, restoring {healing_amount} health!\n"
                    elif spell_name == "bleeding arrow":
                        base_damage = player["spells"][spell_name][0]
                        damage = int(base_damage * (spell_percent / 100))
                        turn_log += f"You shoot an arrow with {spell_percent}% accuracy for {damage} damage!\n"
                    
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
            

            if valid_action:
                if enemy["health"] <= 0:
                    clear_lines(100)
                    gold_dropped = random.randint(enemy_type['gold_drop_range'][0],
                                                enemy_type['gold_drop_range'][1])
                    player["gold"] = player.get("gold", 0) + gold_dropped
                    if currentRoom == '1-19':
                        defeated_bosses.add(currentRoom)
                    if random.random() < enemy_type['item_drop_chance']:
                        # Drop a random armor piece
                        slot = random.choice(list(ARMOR_SLOTS.keys()))
                        tier = random.choice(['leather', 'chainmail', 'iron'])
                        dropped_item = f"{tier} {slot}"
                        inventory.append(dropped_item)
                        print(f"\nThe monster dropped {dropped_item}!")
                    print(turn_log)
                    print(f"You defeated the monster and earned {gold_dropped} gold!")
                    print("---------------------------")

                    del rooms[currentRoom]["item"]
                    break
            # Monster's turn to attack
            enemy_attack = math.floor(random.randint(enemy["attack_min"], enemy["attack_max"]) *
                                   (1 - player["armor"] / 100))
            player["health"] -= enemy_attack
            turn_log += f"The monster attacks you for {enemy_attack} damage!\n"
            if player["health"] <= 0:
                turn_log += "You died! Game over.\n"
                print(turn_log)
                exit()
            last_turn_log = turn_log
            print(turn_log)
            continue
    # Show current status
    if currentRoom == '1-17':
        print('Shop')
        print("---------------------------")
        show_market_items()
    showStatus()

    move = input('> ').lower().split()
    clear_lines(100)
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
            print(f"Error: You can't go that way: {direction}")
        continue
    # Handle item pickup
    elif move[0] == 'get':
        item_name = " ".join(move[1:])
        if "item" in rooms[currentRoom] and item_name == rooms[currentRoom]['item']:
            inventory.append(item_name)
            print(item_name + ' got!')
            del rooms[currentRoom]['item']
        else:
            print("Can't get " + item_name + "!")
        continue
    # Handle item usage
    elif move[0] == 'use':
        item_name = " ".join(move[1:])
        if item_name in inventory:
            if item_name == "health potion":
                player["health"] = min(classes[player["class"]]["health"], player["health"] + 30)
                inventory.remove("health potion")
                print("You used a health potion and restored 30 health!")
            elif item_name == "mana potion":
                player["mana"] = min(classes[player["class"]]["mana"], player["mana"] + 30)
                inventory.remove("mana potion")
                print("You used a mana potion and restored 30 mana!")
            elif item_name in ARMOR_SLOTS:
                # Handle armor equipping
                slot = item_name.split(' ')[1]
                item_type = item_name.split(' ')[0]
                result = equip_armor(slot, item_type)
                print(result)
            else:
                print("You can't use that item!")
        else:
            print("You don't have that item!")
        continue
    # Handle armor removal
    elif move[0] == 'remove':
        slot = " ".join(move[1:])
        result = remove_armor(slot)
        print(result)
        continue
    # Handle armor equipping
    elif move[0] == 'equip':
        if len(move) >= 3:
            slot = move[1]
            item_type = move[2]
            result = equip_armor(slot, item_type)
            print(result)
        else:
            print("Usage: equip [slot] [type]")
        continue
    elif move[0] == 'buy' and currentRoom == '1-17':
        item_name = " ".join(move[1:])
        result = buy_item(item_name)
        print(result)
        continue
    elif move[0] == 'sell' and currentRoom == '1-17':
        item_name = " ".join(move[1:])
        result = sell_item(item_name)
        print(result)
        continue
    # Handle invalid commands
    else:
        print("Invalid command!")