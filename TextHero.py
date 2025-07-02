import sys
import random
import math
import time
from threading import Thread
import keyboard


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
        global player, inventory, player_equipment, currentRoom, rooms, locked_spells
        player = game_state["player"]
        inventory = game_state["inventory"]
        player_equipment = game_state["player_equipment"]
        currentRoom = game_state["currentRoom"]
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


symbols = ['$', '#', '%', '&', '@', '?']
symbol_colors = {
    '$': '\033[38;2;0;255;0m',  # Green
    '#': '\033[94m',  # Blue
    '%': '\033[93m',  # Yellow
    '&': '\033[95m',  # Magenta
    '@': '\033[91m',  # Red
    '?': '\033[96m'   # Cyan
}
RESET = '\033[0m'

symbols = ['$', '#', '%', '&', '@', '?']
symbol_colors = {
    '$': '\033[38;2;0;255;0m',  # Green
    '#': '\033[94m',  # Blue
    '%': '\033[93m',  # Yellow
    '&': '\033[95m',  # Magenta
    '@': '\033[91m',  # Red
    '?': '\033[96m'   # Cyan
}
RESET = '\033[0m'

# Payout values
payouts = {
    '$': 100,
    '#': 75,
    '%': 60,
    '&': 50,
    '@': 40,
    '?': 25  # Only when all 3 are wilds
}

# Weights
symbol_weights = {
    '$': 10,
    '#': 20,
    '%': 30,
    '&': 40,
    '@': 50,
    '?': 150
}
symbol_weights_2 = symbol_weights.copy()

BET_AMOUNT = 5

def colorize(symbol):
    return f"{symbol_colors[symbol]}{symbol}{GREEN}"

def clear():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def print_payout_table():
    print("\033[1mPAYOUT TABLE\033[0m")
    print("\033[38;2;0;255;0m┌─────────┬────────┐")
    print("\033[38;2;0;255;0m| Icon    │ Coins  |")
    print("\033[38;2;0;255;0m├─────────┼────────┤")
    for symbol in symbols:
        payout = payouts[symbol]
        color = colorize(symbol)
        print(f"\033[38;2;0;255;0m│ {color}  {color}  {color} \033[38;2;0;255;0m│  {payout:>4}  \033[38;2;0;255;0m│")
    print("\033[38;2;0;255;0m└─────────┴────────┘")
    print("Note: \033[96m?\033[38;2;0;255;0m is a wildcard and matches any symbol.")

def display_reels(reels):
    rows = get_display_rows(reels)
    print("Slot Machine\n\033[38;2;0;255;0m┌─────┬─────┬─────┐")
    for row in rows:
        print("\033[38;2;0;255;0m│  {}  \033[38;2;0;255;0m│  {}  \033[38;2;0;255;0m│  {}  \033[38;2;0;255;0m│".format(
            *[colorize(s) for s in row]
        ))
    print("\033[38;2;0;255;0m└─────┴─────┴─────┘\n")

def create_reel(spins):
    weights=[symbol_weights[s] for s in symbols]
    return random.choices(symbols, weights=weights, k=spins)

def rotate_reel(reel, history):
    valid_choices = [s for s in symbols if s not in history]
    if not valid_choices:
        valid_choices = symbols
        weights = [symbol_weights[s] for s in symbols]
    else:
        weights = [symbol_weights[s] for s in valid_choices]
    new_symbol = random.choices(valid_choices, weights=weights, k=1)[0]

    reel.insert(0, new_symbol)
    reel.pop()

    history.insert(0, new_symbol)
    if len(history) > 3:
        history.pop()

    return reel, history

def get_display_rows(reels):
    return [[reel[i] for reel in reels] for i in range(3)]  # top, mid, bottom

def check_win(middle_row):
    non_wilds = [s for s in middle_row if s != '?']
    
    if len(non_wilds) == 0:
        return True, payouts['?']
    elif all(s == non_wilds[0] for s in non_wilds):
        return True, payouts[non_wilds[0]]
    return False, 0
def create_reels(num_reels, reel_length=40):
    reels = []
    for _ in range(num_reels):
        reel = create_reel(reel_length)  # generate a full reel with random symbols
        reels.append(reel)
    return reels

def create_final_reel():
    global symbol_weights_2
    eligible_symbols = [s for s in symbols if s != '?']

    reel_weights = [symbol_weights_2[s] for s in eligible_symbols]

    first = random.choices(eligible_symbols, weights=reel_weights, k=1)[0]
    symbol_weights_2[first] += 50

    second = random.choices(eligible_symbols, weights=reel_weights, k=1)[0]

    # Reset the weights of first and second to zero before choosing third
    symbol_weights_2[first] = 0
    symbol_weights_2[second] = 0

    # Check if first two are different and not '?'
    if first != second and first != '?' and second != '?':
        eligible_symbols = symbols  # allow '?'
    else:
        eligible_symbols = [s for s in symbols if s != '?']

    # Prepare adjusted weights for third spin
    reel_weights = [symbol_weights_2[s] for s in eligible_symbols]
    third = random.choices(eligible_symbols, weights=reel_weights, k=1)[0]

    final_reel = [first, second, third]
    symbol_weights_2 = symbol_weights.copy()
    return final_reel


def slot_machine(gold):
    balance = gold
    print_payout_table()

    while True:
        if balance < BET_AMOUNT:
            clear_screen()
            print("Game over.")
            return balance

        print(f"\n\033[1mYour balance: {balance} coins | Bet: {BET_AMOUNT} coins\033[0m")
        move = input("\033[38;2;0;255;0mPress Enter to spin or exit to quit\n")
        if move == 'q' or move == 'exit':
            clear_screen()
            print("Thanks for playing!")
            return balance
        clear()

        # minus bet
        balance -= BET_AMOUNT
        #making it "balanced"
        final_reel = create_final_reel()
        reels = create_reels(3, reel_length=40)
        histories = [[] for _ in range(3)]
        spins_remaining = [20, 30, 40]
        max_spins = max(spins_remaining)

        for frame in range(max_spins+1):
            for i in range(3):
                if spins_remaining[i] > 0:
                    reels[i], histories[i] = rotate_reel(reels[i], histories[i])
                    spins_remaining[i] -= 1
                else:
                    reels[i][1] = final_reel[i]
                
            display_reels(reels)
            print_payout_table()
            time.sleep(0.07)
            clear()

        # final display
        display_reels(reels)
        print_payout_table()

        middle_row = get_display_rows(reels)[1]
        won, payout = check_win(middle_row)
        if won:
            balance += payout
            print(f"\033[1;92mYou WON {payout} coins!\033[0m")
        else:
            print("No win this time. Better luck next spin!")
MAX_SPLITS = 3  # Up to 4 total hands

def get_card():
    return random.choice(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])

def card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)

def hand_value(hand):
    total = sum(card_value(c) for c in hand)
    aces = hand.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21

def print_hand(title, hand):
    print(f"{title}: {' '.join(hand)} (value: {hand_value(hand)})")

def offer_insurance(balance, dealer_card, dealer_hidden):
    if dealer_card != 'A':
        return 0
    if not is_blackjack([dealer_card, dealer_hidden]):
        return 0
    while True:
        choice = input("Dealer shows an Ace. Take insurance for half your bet? (yes/no): ").lower().strip()
        if choice == 'yes':
            return 1
        elif choice == 'no':
            return 0
        else:
            print("Invalid input.")

def resolve_dealer(dealer):
    print_hand("Dealer's hand", dealer)
    while hand_value(dealer) < 17:
        dealer.append(get_card())
        print_hand("Dealer's hand", dealer)
    return hand_value(dealer)

def play_hand(player, dealer_card, balance, bet):
    print_hand("Your hand", player)
    print(f"Dealer shows: {dealer_card} ?")
    doubled = False
    if len(player) == 2 and balance >= bet:
        choice = input("Would you like to double down (yes/no)? ").lower().strip()
        if choice == 'yes':
            bet *= 2
            player.append(get_card())
            print_hand("Your hand after doubling", player)
            return player, bet, True

    while hand_value(player) < 21:
        move = input("Hit or stand? ").lower().strip()
        if move == 'hit':
            player.append(get_card())
            print_hand("Your hand", player)
        elif move == 'stand':
            break
        else:
            print("Invalid input.")
    return player, bet, doubled

def resolve_outcome(player, dealer_hand, bet):
    player_total = hand_value(player)
    dealer_total = hand_value(dealer_hand)
    if player_total > 21:
        print("Bust. You lose.")
        return -bet
    elif dealer_total > 21 or player_total > dealer_total:
        print("You win!")
        return bet
    elif player_total < dealer_total:
        print("Dealer wins.")
        return -bet
    else:
        print("Push.")
        return 0

def play_split_hands(hands, dealer_card, dealer_hidden, balance, bet):
    results = 0
    dealer = [dealer_card, dealer_hidden]
    dealer_blackjack = is_blackjack(dealer)

    for idx, hand in enumerate(hands):
        print(f"\n--- Playing hand {idx + 1} ---")
        if is_blackjack(hand):
            if dealer_blackjack:
                print_hand("Your hand", hand)
                print("Push. Both have blackjack.")
                continue
            else:
                print_hand("Your hand", hand)
                print("Blackjack! You win 3:2.")
                results += int(1.5 * bet)
                continue

        hand, actual_bet, doubled = play_hand(hand, dealer_card, balance, bet)
        if hand_value(hand) > 21:
            results -= actual_bet
            continue

        if not dealer_blackjack:
            result = resolve_outcome(hand, dealer, actual_bet)
            results += result

    return results

def play_round(balance):
    while True:
        bet_input = input("Enter your bet (10–1000) or 'exit': ").strip().lower()
        if bet_input == 'exit' or bet_input == 'q':
            return balance, True
        if not bet_input.isdigit():
            print("Invalid input.")
            continue
        bet = int(bet_input)
        if bet < 10 or bet > 1000:
            print("Bet must be between 10 and 1000.")
            continue
        if bet > balance:
            print("Not enough money.")
            return balance, True
        clear_screen()
        break

    dealer = [get_card(), get_card()]
    player = [get_card(), get_card()]

    # Insurance
    insurance = offer_insurance(balance, dealer[0], dealer[1])
    if insurance == 1:
        insurance_bet = bet // 2
        if is_blackjack(dealer):
            print("Dealer has blackjack! Insurance pays 2:1.")
            balance += insurance_bet
        else:
            print("Dealer does not have blackjack. Insurance lost.")
            balance -= insurance_bet

    # Player blackjack
    if is_blackjack(player):
        print_hand("Your hand", player)
        if is_blackjack(dealer):
            print_hand("Dealer's hand", dealer)
            print_slow("Push. Both have blackjack.")
            return balance, False
        else:
            print_hand("Dealer's hand", dealer)
            print_slow("Blackjack! You win 3:2.")
            return balance + int(1.5 * bet), False

    # Splitting
    hands = [player]
    while len(hands) <= MAX_SPLITS:
        first = hands[-1]
        if len(first) == 2 and card_value(first[0]) == card_value(first[1]) and balance >= (len(hands) + 1) * bet:
            choice = input(f"You have a pair of {first[0]}. Split? (yes/no): ").strip().lower()
            if choice == 'yes':
                hands[-1] = [first[0], get_card()]
                hands.append([first[1], get_card()])
                continue
        break

    result = play_split_hands(hands, dealer[0], dealer[1], balance, bet)
    return balance + result, False

def blackjack(balance):
    sys.stdout.write("\033[2J\033[H")
    exit_game = False
    while balance >= 10 and not exit_game:
        print_slow(f"Current balance: ${balance}")
        balance, exit_game = play_round(balance)
    clear_screen()
    print_slow("\nGame over.")
    return balance
# Constants
RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}
BLACK_NUMBERS = set(range(1, 37)) - RED_NUMBERS

# Player state

def print_intro_bj():
    print_slow("You can bet on:")
    print_slow("- A number (payout: 35 to 1)")
    print_slow("- 'red', 'black' or 'green' (payout: 1 to 1)")
    print_slow("- 'odd' or 'even' (payout: 1 to 1)")
    print_slow("Type 'exit' to quit.\n")

def spin_wheel():
    return random.randint(0, 36)

def get_color(number):
    if number == 0:
        return 'green'
    return 'red' if number in RED_NUMBERS else 'black'

def place_bet(balance):
    print_slow(f"\nCurrent Balance: ${balance}")
    bet_type = input("Bet on a number (0-36), 'red', 'black', 'odd', or 'even': ").lower().strip()
    if bet_type == 'exit':
        return 'exit', 0

    amount_str = input("Enter bet amount: ").strip()
    if not amount_str.isdigit():
        print_slow("Invalid amount.")
        return None, 0

    amount = int(amount_str)
    if amount > balance or amount <= 0:
        print_slow("Invalid bet amount.")
        return None, 0

    return bet_type, amount

def resolve_bet(bet_type, amount, result, balance):
    win = False
    winnings = 0
    result_color = get_color(result)

    if bet_type.isdigit():
        if int(bet_type) == result:
            win = True
            winnings = amount * 35
    elif bet_type == 'red' and result_color == 'red':
        win = True
        winnings = amount
    elif bet_type == 'black' and result_color == 'black':
        win = True
        winnings = amount
    elif bet_type == 'green' and result_color == 'green':
        win = True
        winnings = amount * 35
    elif bet_type == 'odd' and result != 0 and result % 2 == 1:
        win = True
        winnings = amount
    elif bet_type == 'even' and result != 0 and result % 2 == 0:
        win = True
        winnings = amount

    balance -= amount
    if win:
        print_slow(f"You won! Number: {result} ({result_color})")
        balance += amount + winnings
    else:
        print_slow(f"You lost. Number: {result} ({result_color})")
    print_slow(f"New balance: ${balance}\n")
    return balance


def roulette(balance):
    print_intro_bj()
    while balance > 0:
        bet_type, amount = place_bet(balance)
        if bet_type == 'exit':
            break
        elif bet_type is None:
            continue

        result = spin_wheel()
        balance = resolve_bet(bet_type, amount, result, balance)
    clear_screen()
    print_slow("Game over.")
    return balance

def clear_screen():
    sys.stdout.write("\033[2J\033[H")

def display_credits():
    """Display the end credits when reaching the final room"""
    clear_screen()
    print_credits("\n" + "="*50+"\n")
    print_credits(f"{GREEN}CONGRATULATIONS!{GREEN}\n")
    print_credits("You've completed Text Hero!\n")
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
    "\n",
    f"{BLUE}Development Team:{GREEN}\n",
    f"Lead Developer & Creator: {BLUE}Chales{GREEN}\n",
    f"Developer: {BLUE}arnesito{GREEN}\n",
    f"Developer & Designer: {BLUE}Moltd{GREEN}\n",
    "\n",
    f"{BLUE}DLC Development Team:{GREEN}\n",
    f"DLC Developer: {BLUE}arnesito{GREEN}\n",
    "\n"
    f"{BLUE}Quality Assurance Team:{GREEN}\n",
    f"Bug Finder & Patcher: {BLUE}JayMcCray11{GREEN}\n",
    "\n",
    f"{BLUE}Playtesting Team:{GREEN}\n",
    f"{GREEN}David Sucks At Life{GREEN}\n",
    f"{GREEN}Bee1949{GREEN}\n",
    f"{GREEN}Not Guy Stew{GREEN}\n",
    f"{GREEN}Vroom Vroom Snail{GREEN}\n",
    "\n",
    f"{BLUE}Game Features:{GREEN}\n",
    "10 Unique Classes\n",
    "340 Rooms to Explore\n",
    "11 Levels to Defeat\n",
    "50+ Items to Collect\n",
    "200 Monsters to Battle\n",
    "Leveling up system\n",
    "\n",
    f"{BLUE}Technical Details:{GREEN}\n",
    "Custom ANSI Color System\n",
    "Dynamic Combat Engine\n",
    "Save/Load System\n",
    "Crafting System\n",
    "\n",
    f"{BLUE}Thanks for Playing!{GREEN}\n",
    f"{BLUE}press enter to quit{GREEN}"
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
    print_credits(f"{GREEN}CONGRATULATIONS!{GREEN}\n")
    print_credits("You've completed Text Hero!\n")
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
    print_credits("\n")
    print_credits(f"{BLUE}Development Team:{GREEN}\n")
    print_credits(f"Lead Developer & Creator: {BLUE}Chales{GREEN}\n")
    print_credits(f"Developer: {BLUE}arnesito{GREEN}\n")
    print_credits(f"Developer & Designer: {BLUE}Moltd{GREEN}\n")
    print_credits("\n")
    print_credits(f"{BLUE}DLC Development Team:{GREEN}\n")
    print_credits(f"DLC Developer: {BLUE}arnesito{GREEN}\n")
    print_credits("\n")
    print_credits(f"{BLUE}Quality Assurance Team:{GREEN}\n")
    print_credits(f"Bug Finder & Patcher: {BLUE}JayMcCray11{GREEN}\n")
    print_credits("\n")
    print_credits(f"{BLUE}Playtesting Team:{GREEN}\n")
    print_credits(f"{GREEN}David Sucks At Life{GREEN}\n")
    print_credits(f"{GREEN}Bee1949{GREEN}\n")
    print_credits(f"{GREEN}Not Guy Stew{GREEN}\n")
    print_credits(f"{GREEN}Vroom Vroom Snail{GREEN}\n")
    print_credits("\n")
    print_credits(f"{BLUE}Game Features:{GREEN}\n")
    print_credits("10 Unique Classes\n")
    print_credits("340 Rooms to Explore\n")
    print_credits("11 Levels to Defeat\n")
    print_credits("50+ Items to Collect\n")
    print_credits("200 Monsters to Battle\n")
    print_credits("Leveling up system\n")
    print_credits("\n")
    print_credits(f"{BLUE}Technical Details:{GREEN}\n")
    print_credits("Custom ANSI Color System\n")
    print_credits("Dynamic Combat Engine\n")
    print_credits("Save/Load System\n")
    print_credits("Crafting System\n")
    print_credits("\n")
    print_credits(f"{BLUE}Thanks for Playing!{GREEN}\n")
    print_credits(f"{BLUE}press enter to quit{GREEN}")
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
    
def print_slow_intro(text):
    
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
                time.sleep(0.01)
    
    print()  # Add newline at end
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
        'health': 150,
        'attack_min': 15,
        'attack_max': 30,
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

EXP_TO_LEVEL = {
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
    "Vampire": {'blood spear': [30, 60], 'haemolacria': [80, 100]},
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
        directions.append(f"{GREEN}  north: {BLUE}{room['north']}{GREEN}")
    if 'south' in room:
        directions.append(f"{GREEN}  south: {BLUE}{room['south']}{GREEN}")
    if 'east' in room:
        directions.append(f"{GREEN}  east: {BLUE}{room['east']}{GREEN}")
    if 'west' in room:
        directions.append(f"{GREEN}  west: {BLUE}{room['west']}{GREEN}")
    if 'down' in room:
        directions.append(f"{GREEN}  down: {BLUE}{room['down']}{GREEN}")
    if 'up' in room:
        directions.append(f"{GREEN}  up: {BLUE}{room['up']}{GREEN}")
    return "\n".join(directions)

def showStatus():
    print_slow(f'{GREEN}You are in ' + BLUE+currentRoom+RESET)
    print_slow(f'{GREEN}Available directions:')
    print_slow(showAvailableDirections(rooms[currentRoom]))
    print_slow(f'{GREEN}Health: {player["health"]}')
    print_slow(f'{GREEN}Armor: {player["armor"]}')
    print_slow(f'{GREEN}Mana: {player["mana"]}')
    print_slow(f'{GREEN}Gold: {player["gold"]}')
    print_slow(f'{GREEN}Class: {BLUE}{player["class"]}{GREEN}')
    print_slow(f'{GREEN}Secondary Class: {BLUE}{player["class 2"]}{GREEN}')
    print_slow(f'{GREEN}Level: {player["level"]}')
    print_slow(f'{GREEN}Exp: {player["exp"]}')
    print_slow(f'{GREEN}Equipped Armor:')
    for slot, item in player_equipment.items():
        if item:
            print_slow(f'- {slot}: {ITEM_COLOR}{item}{GREEN}')
    show_inventory()
    if "lore" in rooms[currentRoom]:
        print_slow(f"{rooms[currentRoom]['lore']}{GREEN}\n")
    if "hint" in rooms[currentRoom]:
        print_slow(f"{BLUE}{rooms[currentRoom]['hint']}{GREEN}")
    if "item" in rooms[currentRoom]:
        if isinstance(rooms[currentRoom]["item"], list):
            items = rooms[currentRoom]["item"]
            if len(items) == 1:
                print_slow(f"{GREEN}You see a{GREEN} {ITEM_COLOR}{items[0]}{GREEN}")
            else:
                formatted_items = [f"{ITEM_COLOR}{item}{GREEN}" for item in items]
                if len(formatted_items) == 2:
                    item_str = " and ".join(formatted_items)
                else:
                    item_str = ", ".join(formatted_items[:-1]) + f" and {formatted_items[-1]}"
                print_slow(f"{GREEN}You see{GREEN} {item_str}")
        else:
            print_slow(f"{GREEN}You see a{GREEN} {ITEM_COLOR}{rooms[currentRoom]['item']}{GREEN}")
    print_slow(f"{GREEN}---------------------------")

def print_slow_list(tag, items):
    print_slow(f"{tag}: {ITEM_COLOR}{', '.join(map(str, items))}{GREEN}")

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
    "1-1": {
        "east": "1-2",
        "item": "health potion",
        "lore": "You have received a message: CLEANSE THE TOWER OF DEMONS",
        "hint": "In this game, you use cardinal directions to travel. There are some keyboard shortcuts. EG - n for north, s for south, e for east, w for west.",
        "description": "Levitation platforms hover silently. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "1-2": {
        "north": "1-3",
        "west": "1-1",
        "description": "Calendar pages turn themselves."
    },
    "1-3": {
        "west": "1-4",
        "south": "1-2",
        "item": "wooden sword",
        "hint": "To equip something, you type in (equip (itemname))",
        "description": "Seasons cycle within single rooms. You see a sword with a leather wrap providing additional grip, sitting atop the woven basket."
    },
    "1-4": {
        "east": "1-3",
        "west": "1-15",
        "north": "1-5",
        "item": "chainmail boots",
        "hint": "if you have multiple items in your inventory to equip, you can type in (i) to equip the best ones possible",
        "description": "Parchments flutter without wind. You notice boots whose mail is shaped to allow natural foot movement, leaning against the pillar."
    },
    "1-5": {
        "south": "1-4",
        "west": "1-6",
        "hint": "For combat, you have 3 options. Fight, Defend and Cast.\nFight allows you to attack the monster, If you type in (fight) a slider will pop up.\nTry to hit the middle of the slider to most damage possible!\nDefend makes you take less damage from the monsters next attack and allows you to build up mana.\nCast will cast a spell, which will require mana to do.\nHowever, you need to unlock the spell before being able to cast it.\nYou can do this by using spellbooks. To cast a spell, you will type in (cast(spell name))",
        "description": "Raw magical force seeps from cracks."
    },
    "1-6": {
        "west": "1-7",
        "east": "1-5",
        "monster": "normal",
        "item": "mana potion",
        "hint": "Mana potions instantly regain mana. You can use them inside our outside of combat by typing (use(mana potion))",
        "description": "A dark shape blocks the path ahead, its presence making the air colder. You see a potion from which tiny sparks dance within its depths, sitting atop the pile of ancient scrolls."
    },
    "1-7": {
        "east": "1-6",
        "west": "1-8",
        "south": "1-15",
        "item": "iron chestplate",
        "monster": "normal",
        "description": "Eyes reflect the torchlight from multiple impossible angles. You see a chestplate whose metal has a deep, rich color, resting on the wooden chest."
    },
    "1-8": {
        "east": "1-7",
        "west": "1-9",
        "south": "1-14",
        "item": "iron pants",
        "north": "1-12",
        "description": "Floating orbs of light drift aimlessly. Before you rest pants with rivets marking the joints for maximum flexibility, sitting on the display stand."
    },
    "1-9": {
        "west": "1-10",
        "south": "1-13",
        "east": "1-8",
        "item": "key fragment",
        "description": "Moss creeps along the walls, softening the dungeon's menace. You notice a fragment whose intricate teeth seem to shift and change when viewed from different angles, leaning against the wall."
    },
    "1-10": {
        "south": "1-11",
        "east": "1-9",
        "monster": "normal",
        "description": "The creature's presence makes the torches flicker with fear."
    },
    "1-11": {
        "north": "1-10",
        "item": "leather helmet",
        "description": "Windows filled with stained glass cast kaleidoscopic patterns. You see a helmet with a thin layer of metal reinforcement lining its inside, sitting atop the treasure pile."
    },
    "1-12": {
        "south": "1-11",
        "monster": "normal",
        "description": "A dark shape blocks the path ahead, its presence making the air colder."
    },
    "1-13": {
        "east": "1-16",
        "north": "1-9",
        "item": "mana potion",
        "description": "Time echoes replay historical events. You find a vial that seems to absorb and reflect light simultaneously, partially hidden behind the tattered curtain."
    },
    "1-14": {
        "north": "1-8",
        "south": "1-16",
        "item": "leather chestplate",
        "description": "Diary pages turn themselves. You see a chestplate with a small emblem pressed into its center, sitting atop the display pedestal."
    },
    "1-15": {
        "east": "1-4",
        "north": "1-7",
        "item": "health potion",
        "hint": "health potions are used the same way as mana potions, except for the fact that they give health instead of mana. Type in the same command, which was: (use (health potion))",
        "description": "Spaces seem larger inside than outside. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "1-16": {
        "east": "1-1",
        "north": "1-14",
        "south": "1-17",
        "west": "1-13",
        "monster": "normal",
        "description": "The ground shudders beneath the approach of something massive."
    },
    "1-17": {
        "west": "1-18",
        "north": "1-16",
        "description": "Weather patterns repeat in cycles."
    },
    "1-18": {
        "west": "1-19",
        "east": "1-17",
        "description": "Ancient scrolls unfurl themselves."
    },
    "1-19": {
        "west": "1-20",
        "east": "1-18",
        "monster": "boss",
        "item": "spell book",
        "description": "The throne of skulls creaks as a skeletal form rises, its very presence causing time to unravel; its voice is the whisper of forgotten graves."
    },
    "1-20": {
        "east": "1-19",
        "up": "2-1",
        "description": "Arcane energies swirl like visible currents."
    },
    "dungeon-1": {
        "up": "1-10",
        "east": "dungeon-2",
        "monster": "normal",
        "description": "Something moves with unnatural grace, its form unclear."
    },
    "dungeon-2": {
        "west": "dungeon-1",
        "south": "dungeon-3",
        "item": "iron sword",
        "description": "Reliquaries contain mysterious substances. You see a sword that has been balanced for perfect swing, resting on the metal stand."
    },
    "dungeon-3": {
        "north": "dungeon-2",
        "monster": "vampire",
        "lore": "SOMETHING FEELS SUCCESSFUL IN YOU.",
        "description": "Doors lead to impossible places."
    },
    "2-1": {
        "west": "1-20",
        "north": "2-2",
        "lore": "Your surroundings feel vague.",
        "description": "Sand timers flow upward."
    },
    "2-2": {
        "west": "2-3",
        "south": "2-1",
        "item": "mana potion",
        "description": "Raw magical force seeps from cracks. Before you sits a potion that pulses with an inner rhythm matching your heartbeat, perched precariously on the edge of the broken table."
    },
    "2-3": {
        "west": "2-4",
        "east": "2-2",
        "item": "iron sword",
        "description": "Residual magic crackles in the air. You find a sword that feels solid and dependable, hanging from the iron hook."
    },
    "2-4": {
        "east": "2-3",
        "south": "2-5",
        "west": "2-15",
        "item": "mana potion",
        "description": "Ghostly servants continue eternal duties. Before you sits a potion that pulses with an inner rhythm matching your heartbeat, perched precariously on the edge of the broken table."
    },
    "2-5": {
        "north": "2-4",
        "south": "2-6",
        "monster": "normal",
        "description": "A twisted form writhes in the corner, its eyes glowing with unnatural hunger."
    },
    "2-6": {
        "west": "2-7",
        "north": "2-5",
        "item": "mana potion",
        "description": "Pedestals await artifacts yet to be placed. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "2-7": {
        "east": "2-6",
        "west": "2-8",
        "south": "2-13",
        "north": "2-15",
        "monster": "normal",
        "description": "The ground shudders beneath the approach of something massive."
    },
    "2-8": {
        "east": "2-7",
        "west": "2-9",
        "description": "Ethereal dancers perform endless routines."
    },
    "2-9": {
        "south": "2-10",
        "north": "2-13",
        "east": "2-8",
        "west": "2-10",
        "item": "iron chestplate",
        "description": "Ripples disturb the air like water. You see a chestplate whose edges are reinforced with additional strips, sitting atop the treasure pile."
    },
    "2-10": {
        "south": "2-11",
        "north": "2-9",
        "item": "health potion",
        "description": "Natural phenomena defy physics. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "2-11": {
        "north": "2-10",
        "south": "2-12",
        "monster": "normal",
        "description": "A creature that seems to be crafted from nightmares watches you."
    },
    "2-12": {
        "north": "2-11",
        "west": "2-13",
        "monster": "normal",
        "description": "A dark shape blocks the path ahead, its presence making the air colder."
    },
    "2-13": {
        "east": "2-12",
        "south": "2-9",
        "north": "2-14",
        "description": "Residual magic crackles in the air."
    },
    "2-14": {
        "south": "2-13",
        "west": "2-16",
        "item": "chainmail pants",
        "description": "Shadows move independently of light sources. You find pants whose joints are protected by small rings of leather, hanging from the hook."
    },
    "2-15": {
        "east": "2-4",
        "north": "2-7",
        "item": "mana potion",
        "description": "Astrolabes track impossible celestial movements. Before you sits a potion that pulses with an inner rhythm matching your heartbeat, perched precariously on the edge of the broken table."
    },
    "2-16": {
        "west": "2-18",
        "south": "2-17",
        "east": "2-14",
        "monster": "normal",
        "description": "A creature that seems to be made of living shadow moves closer."
    },
    "2-17": {
        "north": "2-16",
        "monster": "normal",
        "description": "The creature's very presence seems to corrupt the air around it."
    },
    "2-18": {
        "west": "2-19",
        "east": "2-16",
        "item": "spellbook",
        "description": "Runes pulse with inner fire."
    },
    "2-19": {
        "north": "2-20",
        "east": "2-18",
        "item": "health potion",
        "description": "Children's toys lie abandoned in dark corners. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "2-20": {
        "south": "2-19",
        "description": "Bubbles rise through solid stone."
    },
    "2-21": {
        "south": "2-20",
        "north": "2-22",
        "description": "Echoes repeat unheard phrases."
    },
    "2-22": {
        "south": "2-21",
        "north": "2-23",
        "east": "2-26",
        "description": "Spectral guards patrol forgotten corridors."
    },
    "2-23": {
        "south": "2-22",
        "west": "2-24",
        "item": "mana potion",
        "description": "Arcane energies swirl like visible currents. You find a vial that seems to absorb and reflect light simultaneously, partially hidden behind the tattered curtain."
    },
    "2-24": {
        "east": "2-23",
        "south": "2-25",
        "description": "Energy signatures persist in patterns."
    },
    "2-25": {
        "north": "2-24",
        "east": "2-28",
        "item": "steel sword",
        "description": "Ancient scrolls unfurl when approached. You see a sword whose steel has been folded countless times, leaning against the nearby pillar."
    },
    "2-26": {
        "west": "2-23",
        "east": "2-27",
        "monster": "normal",
        "description": "A creature that seems to be made of living shadow moves closer."
    },
    "2-27": {
        "west": "2-26",
        "monster": "normal",
        "description": "The shadows seem to coalesce into something that shouldn't exist."
    },
    "2-28": {
        "west": "2-25",
        "east": "2-29",
        "monster": "normal",
        "description": "The shadows seem to coalesce into something that shouldn't exist."
    },
    "2-29": {
        "west": "2-28",
        "south": "2-30",
        "item": "iron boots",
        "description": "Shadows cast by invisible objects. You see boots whose metal has developed a subtle sheen, resting on the display pedestal."
    },
    "2-30": {
        "east": "2-29",
        "west": "3-1",
        "monster": "boss",
        "lore": "you feel less greedy",
        "description": "Through swirling mists emerges a colossal dragon, scales shimmering like fallen stars; its roar shakes the very foundations of reality."
    },
    "3-1": {
        "east": "2-29",
        "north": "3-2",
        "description": "Dream creatures manifest briefly."
    },
    "3-2": {
        "east": "3-3",
        "south": "3-1",
        "monster": "normal",
        "description": "The air grows colder as an unseen presence draws near."
    },
    "3-3": {
        "west": "3-2",
        "east": "3-4",
        "south": "3-7",
        "down": "casino",
        "item": "iron pants",
        "description": "Running water masks hidden dangers. You see pants whose edges are rounded to prevent catching, resting against the wall."
    },
    "casino": {
        "up": "3-3",
        "description": "Memory spirits relive final moments."
    },
    "3-4": {
        "west": "3-3",
        "east": "3-5",
        "monster": "normal",
        "description": "A mass of writhing tendrils reaches out from the darkness."
    },
    "3-5": {
        "west": "3-4",
        "north": "3-6",
        "description": "Memory spirits relive final moments."
    },
    "3-6": {
        "west": "3-31",
        "south": "3-5",
        "east": "3-8",
        "north": "3-13",
        "item": "health potion",
        "description": "Time echoes replay historical events. You notice a vial whose liquid inside seems to breathe with its own rhythm, visible in the partially filled container that rests against the wall."
    },
    "3-7": {
        "east": "3-10",
        "west": "3-8",
        "south": "3-16",
        "north": "3-3",
        "monster": "normal",
        "description": "The creature's presence makes your skin crawl with primal fear."
    },
    "3-8": {
        "east": "3-7",
        "west": "3-6",
        "north": "3-9",
        "item": "iron boots",
        "description": "Runes pulse with inner fire. Before you sit boots that are heavy but balanced, perfect for charging into battle, resting on the welcome mat."
    },
    "3-9": {
        "south": "3-8",
        "east": "3-11",
        "west": "3-10",
        "monster": "normal",
        "description": "A creature that defies mortal comprehension moves through the darkness."
    },
    "3-10": {
        "east": "3-9",
        "item": "health potion",
        "description": "Ghostly apparitions fade in and out of visibility. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "3-11": {
        "west": "3-9",
        "south": "3-12",
        "item": "iron sword",
        "description": "Shadows cast by invisible objects. You see a sword whose hilt is wrapped in worn leather, sitting atop the wooden chest."
    },
    "3-12": {
        "north": "3-11",
        "monster": "normal",
        "description": "A twisted form writhes in the corner, its eyes glowing with unnatural hunger."
    },
    "3-13": {
        "south": "3-6",
        "north": "3-14",
        "description": "Ancient scrolls unfurl when approached."
    },
    "3-14": {
        "south": "3-13",
        "west": "3-15",
        "monster": "normal",
        "description": "A creature that seems to be made of pure malevolence watches you."
    },
    "3-15": {
        "east": "3-14",
        "north": "3-16",
        "item": "spell",
        "description": "A withered banner hangs limply from the ceiling, its emblem unrecognizable."
    },
    "3-16": {
        "west": "3-26",
        "south": "3-15",
        "north": "3-7",
        "monster": "normal",
        "description": "A creature that seems to be made of pure malevolence watches you."
    },
    "3-17": {
        "north": "3-31",
        "item": "health potion",
        "description": "Abandoned armor stands vigil in corners. You see a glass vial filled with swirling crimson liquid that pulses gently on the nearby pedestal."
    },
    "3-18": {
        "south": "3-26",
        "east": "3-19",
        "item": "health potion",
        "description": "Parchments flutter without wind. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "3-19": {
        "north": "3-22",
        "west": "3-18",
        "item": "health potion",
        "description": "Footsteps echo from corridors yet to be discovered. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "3-20": {
        "south": "3-23",
        "monster": "normal",
        "description": "Something massive shifts in the darkness, its full form unseen."
    },
    "3-21": {
        "north": "3-22",
        "description": "Mechanical devices count backward."
    },
    "3-22": {
        "south": "3-19",
        "north": "3-20",
        "east": "3-32",
        "west": "3-23",
        "description": "Doors open onto different locations each time."
    },
    "3-23": {
        "east": "3-22",
        "west": "3-24",
        "north": "3-20",
        "monster": "normal",
        "description": "A creature that seems to be made of living shadow moves closer."
    },
    "3-24": {
        "east": "3-23",
        "south": "3-25",
        "description": "Children's toys lie abandoned in dark corners."
    },
    "3-25": {
        "north": "3-24",
        "east": "3-31",
        "item": "health potion",
        "description": "Architecture defies physical laws. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "3-26": {
        "west": "3-33",
        "monster": "normal",
        "description": "A creature that defies mortal comprehension moves through the darkness."
    },
    "3-27": {
        "west": "3-32",
        "item": "health potion",
        "description": "Projected illusions serve as guides. You notice a vial whose liquid inside seems to breathe with its own rhythm, visible in the partially filled container that rests against the wall."
    },
    "3-28": {
        "north": "3-29",
        "east": "3-34",
        "item": "health potion",
        "description": "Raw magical force seeps from cracks. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "3-29": {
        "west": "3-28",
        "south": "3-30",
        "item": "mana potion",
        "description": "Smells shift and change without apparent source. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "3-30": {
        "east": "3-29",
        "item": "health potion",
        "description": "Family portraits with scratched-out faces. You see a glass vial filled with swirling crimson liquid that pulses gently on the nearby pedestal."
    },
    "3-31": {
        "east": "3-6",
        "west": "3-25",
        "monster": "normal",
        "description": "A creature that seems to be made of pure malevolence watches you."
    },
    "3-32": {
        "east": "3-27",
        "west": "3-22",
        "north": "3-33",
        "item": "health potion",
        "description": "Architecture defies physical laws. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "3-33": {
        "south": "3-32",
        "north": "3-34",
        "monster": "normal",
        "description": "A twisted form writhes in the corner, its eyes glowing with unnatural hunger."
    },
    "3-34": {
        "south": "3-33",
        "west": "3-35",
        "north": "3-36",
        "monster": "normal",
        "description": "Something ancient and evil stirs in the depths of the room."
    },
    "3-35": {
        "south": "3-34",
        "west": "3-38",
        "item": "iron helmet",
        "description": "Ancient scrolls unfurl when approached. You see a helmet with a decorative crest running along its center, resting on the wooden peg."
    },
    "3-36": {
        "south": "3-34",
        "east": "3-37",
        "item": "health potion",
        "description": "Enchantment residue clings to surfaces. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "3-37": {
        "east": "3-38",
        "west": "3-36",
        "item": "spell book",
        "description": "Textures feel different from appearance. Before you sit boots that are heavy but balanced, perfect for charging into battle, resting on the welcome mat."
    },
    "3-38": {
        "east": "3-39",
        "west": "3-37",
        "item": "health potion",
        "description": "Pedestals await artifacts yet to be placed. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "3-39": {
        "east": "3-40",
        "west": "3-38",
        "item": "health potion",
        "description": "Wind chimes ring from unknown heights. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "3-40": {
        "east": "4-1",
        "west": "3-39",
        "monster": "boss",
        "description": "Through swirling mists emerges a colossal dragon, scales shimmering like fallen stars; its roar shakes the very foundations of reality."
    },
    "4-1": {
        "east": "3-40",
        "west": "4-2",
        "description": "Stone tablets bear eroding inscriptions."
    },
    "4-2": {
        "east": "4-1",
        "north": "4-3",
        "item": "health potion",
        "description": "Sounds echo differently depending on position. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "4-3": {
        "west": "4-5",
        "north": "4-4",
        "south": "4-2",
        "item": "mana potion",
        "description": "Pedestals await artifacts yet to be placed. You see a potion from which tiny sparks dance within its depths, sitting atop the pile of ancient scrolls."
    },
    "4-4": {
        "south": "4-3",
        "east": "4-5",
        "monster": "normal",
        "description": "The air seems to ripple with malevolent presence."
    },
    "4-5": {
        "west": "4-4",
        "north": "4-6",
        "south": "4-7",
        "description": "Ancient calendars display impossible dates."
    },
    "4-6": {
        "west": "4-47",
        "south": "4-5",
        "east": "4-8",
        "north": "4-15",
        "item": "health potion",
        "description": "Residual magic crackles in the air. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "4-7": {
        "east": "4-8",
        "south": "4-16",
        "north": "4-5",
        "monster": "normal",
        "description": "A horror beyond human comprehension moves closer."
    },
    "4-8": {
        "east": "4-10",
        "north": "4-9",
        "item": "health potion",
        "description": "Phantom musicians play silent instruments. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "4-9": {
        "south": "4-8",
        "east": "4-15",
        "north": "4-10",
        "monster": "normal",
        "description": "Eyes reflect the torchlight from multiple impossible angles."
    },
    "4-10": {
        "south": "4-9",
        "north": "4-11",
        "item": "health potion",
        "description": "Ancient stonework bears the marks of long-forgotten construction techniques. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "4-11": {
        "west": "4-12",
        "item": "iron chestplate",
        "description": "Running water masks hidden dangers. You notice a chestplate whose plates are shaped to deflect blows, leaning against the pillar."
    },
    "4-12": {
        "east": "4-11",
        "description": "Absolute silence feels oppressive."
    },
    "4-13": {
        "south": "4-15",
        "north": "3-14",
        "description": "Rooms exist in multiple places simultaneously."
    },
    "4-14": {
        "south": "4-13",
        "monster": "normal",
        "description": "The sound of scraping bone echoes through the chamber."
    },
    "4-15": {
        "west": "4-9",
        "north": "3-16",
        "south": "4-6",
        "east": "4-16",
        "item": "health potion",
        "description": "Rusty keys hang from hooks labeled in forgotten languages. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "4-16": {
        "west": "4-15",
        "south": "4-17",
        "north": "4-7",
        "item": "mana potion",
        "description": "Timepieces run in reverse. You see a vial containing liquid that seems to capture starlight, resting in the corner."
    },
    "4-17": {
        "north": "4-16",
        "west": "4-18",
        "item": "health potion",
        "description": "Time echoes replay historical events. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "4-18": {
        "south": "4-19",
        "east": "4-17",
        "monster": "normal",
        "description": "The sound of scraping bone echoes through the chamber."
    },
    "4-19": {
        "north": "4-18",
        "west": "4-20",
        "item": "health potion",
        "description": "Colors seem more vivid near certain walls. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "4-20": {
        "east": "4-19",
        "south": "4-21",
        "monster": "boss",
        "description": "Where light dare not tread, an elder beast stirs, its presence warping space; the dragon's gaze turns heroes to stone."
    },
    "4-21": {
        "north": "4-21",
        "south": "4-22",
        "monster": "normal",
        "description": "A horror beyond human comprehension moves closer."
    },
    "4-22": {
        "south": "4-29",
        "north": "4-25",
        "east": "4-46",
        "west": "4-23",
        "description": "Whispers seem to come from behind."
    },
    "4-23": {
        "east": "4-22",
        "west": "4-24",
        "north": "4-26",
        "monster": "normal",
        "description": "The ground shudders beneath the approach of something massive."
    },
    "4-24": {
        "east": "4-23",
        "south": "4-25",
        "description": "Stone pillars support impossible geometries."
    },
    "4-25": {
        "north": "4-24",
        "east": "4-26",
        "monster": "boss",
        "description": "Stars die in the void left by the presence; its whispered name causes sanity to fray."
    },
    "4-26": {
        "west": "4-25",
        "east": "4-27",
        "monster": "normal",
        "description": "A dark form moves with jerky, unnatural movements."
    },
    "4-27": {
        "west": "4-26",
        "south": "4-28",
        "item": "health potion",
        "description": "Messages scrawled in blood remain legible. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "4-28": {
        "north": "4-27",
        "east": "4-29",
        "monster": "normal",
        "description": "A twisted form writhes in the corner, its eyes glowing with unnatural hunger."
    },
    "4-29": {
        "west": "4-28",
        "south": "4-30",
        "item": "mana potion",
        "description": "Timepieces run in reverse. You see a vial containing liquid that seems to capture starlight, resting in the corner."
    },
    "4-30": {
        "east": "4-29",
        "north": "4-31",
        "item": "health potion",
        "description": "Bioluminescent fungi cast an ethereal blue glow. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "4-31": {
        "south": "4-30",
        "west": "4-32",
        "monster": "normal",
        "description": "A creature that seems to be made of pure malevolence watches you."
    },
    "4-32": {
        "east": "4-31",
        "north": "4-33",
        "item": "health potion",
        "description": "Children's toys lie abandoned in dark corners. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "4-33": {
        "south": "4-32",
        "east": "4-25",
        "north": "4-34",
        "monster": "normal",
        "description": "A horror beyond human comprehension moves closer."
    },
    "4-34": {
        "south": "4-33",
        "west": "4-35",
        "north": "4-36",
        "monster": "normal",
        "description": "The sound of scraping bone echoes through the chamber."
    },
    "4-35": {
        "east": "4-34",
        "west": "4-38",
        "item": "iron helmet",
        "description": "Corridors stretch further than physically possible. You see a helmet with a decorative crest running along its center, resting on the wooden peg."
    },
    "4-36": {
        "south": "4-44",
        "north": "4-38",
        "item": "health potion",
        "description": "Water clocks measure something other than time. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "4-37": {
        "east": "4-38",
        "south": "4-36",
        "monster": "normal",
        "description": "The shadows seem to coalesce into something that shouldn't exist."
    },
    "4-38": {
        "east": "4-39",
        "north": "4-37",
        "item": "health potion",
        "description": "You hear distant music, eerie and slow, with no source in sight. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "4-39": {
        "east": "4-40",
        "west": "4-38",
        "monster": "normal",
        "description": "The creature's very presence seems to corrupt the air around it."
    },
    "4-40": {
        "east": "4-41",
        "west": "4-39",
        "monster": "normal",
        "description": "Something ancient and evil stirs in the depths of the room."
    },
    "4-41": {
        "east": "4-40",
        "west": "4-42",
        "item": "mana potion",
        "description": "Levitation platforms hover silently. You see a potion from which tiny sparks dance within its depths, sitting atop the pile of ancient scrolls."
    },
    "4-42": {
        "east": "4-41",
        "north": "4-44",
        "west": "4-43",
        "item": "mana potion",
        "description": "Bioluminescent fungi cast an ethereal blue glow. You notice a vial whose liquid shifts between colors like a sunset in miniature, reflecting off the potion that sits in the beam of light."
    },
    "4-43": {
        "east": "4-42",
        "item": "health potion",
        "description": "Colors seem more vivid in certain chambers. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "4-44": {
        "east": "4-45",
        "west": "4-43",
        "monster": "normal",
        "description": "Something massive shifts in the darkness, its full form unseen."
    },
    "4-45": {
        "south": "4-46",
        "west": "4-44",
        "description": "Memory echoes replay ancient rituals."
    },
    "4-46": {
        "east": "4-47",
        "north": "4-45",
        "description": "Ancient calendars display impossible dates."
    },
    "4-47": {
        "east": "4-48",
        "north": "4-46",
        "south": "4-49",
        "description": "Running water masks hidden dangers."
    },
    "4-48": {
        "west": "4-48",
        "monster": "normal",
        "description": "A dark form moves with jerky, unnatural movements."
    },
    "4-49": {
        "north": "4-47",
        "south": "4-50",
        "item": "health potion",
        "lore": "You feel if something terrible is coming...",
        "description": "Moss creeps along the walls, softening the dungeon's menace. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "4-50": {
        "north": "4-49",
        "south": "5-1",
        "monster": "boss",
        "description": "Reality tears apart as a deity of darkness manifests, its true form hidden behind veils of madness-inducing horror."
    },
    "5-1": {
        "east": "4-50",
        "north": "5-2",
        "description": "Colors seem more vivid near certain walls."
    },
    "5-2": {
        "east": "5-1",
        "south": "5-3",
        "west": "5-12",
        "monster": "normal",
        "description": "The ground trembles beneath the feet of an unseen horror."
    },
    "5-3": {
        "west": "5-5",
        "south": "5-4",
        "north": "5-2",
        "east": "5-17",
        "item": "health potion",
        "description": "Projected illusions serve as guides. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "5-4": {
        "south": "5-3",
        "east": "5-6",
        "monster": "normal",
        "description": "A twisted abomination emerges from the darkness."
    },
    "5-5": {
        "east": "5-3",
        "north": "5-10",
        "monster": "boss",
        "lore": "This doesn't feel right.",
        "description": "Where light dare not tread, an elder beast stirs, its presence warping space; the dragon's gaze turns heroes to stone."
    },
    "5-6": {
        "west": "5-50",
        "south": "5-7",
        "north": "5-15",
        "monster": "normal",
        "description": "The shadows seem to coalesce into something that shouldn't exist."
    },
    "5-7": {
        "east": "5-8",
        "north": "5-6",
        "item": "health potion",
        "description": "Pressure waves ripple through standing water. You notice a vial whose liquid inside seems to breathe with its own rhythm, visible in the partially filled container that rests against the wall."
    },
    "5-8": {
        "west": "5-7",
        "north": "5-9",
        "monster": "normal",
        "description": "The ground seems to writhe beneath the feet of an approaching horror."
    },
    "5-9": {
        "south": "5-8",
        "north": "5-10",
        "monster": "normal",
        "description": "The creature's very presence seems to corrupt the air around it."
    },
    "5-10": {
        "south": "5-9",
        "north": "5-11",
        "monster": "boss",
        "description": "Amidst swirling necromantic energies stands a figure of pure bone, crowned with dark crystal; death itself seems to bend to its will."
    },
    "5-11": {
        "west": "5-12",
        "south": "5-10",
        "item": "mana potion",
        "description": "Fog banks move with purpose. You see a potion from which tiny sparks dance within its depths, sitting atop the pile of ancient scrolls."
    },
    "5-12": {
        "east": "5-11",
        "south": "5-13",
        "item": "health potion",
        "description": "Metallic scraping tracks movement. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "5-13": {
        "south": "5-14",
        "north": "5-12",
        "monster": "normal",
        "description": "The air grows colder as an unseen presence draws near."
    },
    "5-14": {
        "north": "5-13",
        "west": "5-15",
        "monster": "normal",
        "description": "Eyes reflect the torchlight from multiple impossible angles."
    },
    "5-15": {
        "south": "5-16",
        "east": "5-14",
        "item": "wooden sword",
        "description": "Ripples disturb the air like water. You notice a sword whose wood has been treated with protective oils, hanging from the leather strap."
    },
    "5-16": {
        "west": "4-16",
        "south": "5-59",
        "north": "5-15",
        "east": "5-17",
        "monster": "normal",
        "description": "Something massive shifts in the darkness, its full form unseen."
    },
    "5-17": {
        "north": "5-18",
        "west": "5-16",
        "monster": "normal",
        "description": "A creature that seems to be made of living shadow moves closer."
    },
    "5-18": {
        "south": "5-17",
        "east": "5-19",
        "monster": "normal",
        "description": "The air seems to ripple with malevolent presence."
    },
    "5-19": {
        "north": "5-18",
        "west": "5-20",
        "item": "health potion",
        "description": "Colors seem more vivid in certain chambers. You notice a vial whose liquid inside seems to breathe with its own rhythm, visible in the partially filled container that rests against the wall."
    },
    "5-20": {
        "east": "5-19",
        "south": "5-21",
        "monster": "boss",
        "description": "Amidst swirling necromantic energies stands a figure of pure bone, crowned with dark crystal; death itself seems to bend to its will."
    },
    "5-21": {
        "north": "5-20",
        "east": "5-22",
        "west": "5-23",
        "monster": "normal",
        "description": "A creature that defies mortal comprehension moves through the darkness."
    },
    "5-22": {
        "south": "5-33",
        "north": "5-32",
        "east": "5-31",
        "west": "5-21",
        "description": "Mana pools collect in low areas."
    },
    "5-23": {
        "east": "5-21",
        "west": "5-24",
        "monster": "normal",
        "description": "A twisted abomination emerges from the darkness."
    },
    "5-24": {
        "east": "5-23",
        "south": "5-25",
        "description": "Salt deposits crystallize in delicate patterns."
    },
    "5-26": {
        "west": "5-25",
        "east": "5-27",
        "monster": "normal",
        "description": "Something ancient and evil stirs in the depths of the room."
    },
    "5-27": {
        "west": "5-26",
        "south": "5-28",
        "monster": "normal",
        "description": "The air seems to ripple with malevolent presence."
    },
    "5-28": {
        "north": "5-27",
        "east": "5-29",
        "monster": "normal",
        "description": "The sound of wet flesh slapping against stone echoes through the chamber."
    },
    "5-29": {
        "west": "5-28",
        "south": "5-30",
        "item": "mana potion",
        "description": "Vaulted ceilings disappear into darkness. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "5-30": {
        "east": "5-29",
        "monster": "boss",
        "lore": "you feel sick.",
        "description": "Amidst swirling necromantic energies stands a figure of pure bone, crowned with dark crystal; death itself seems to bend to its will."
    },
    "5-31": {
        "west": "5-32",
        "item": "health potion",
        "description": "Calendar pages turn themselves. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "5-32": {
        "east": "5-31",
        "south": "5-22",
        "north": "5-33",
        "item": "health potion",
        "description": "Time flows at varying rates. You notice a vial whose liquid inside seems to breathe with its own rhythm, visible in the partially filled container that rests against the wall."
    },
    "5-33": {
        "south": "5-32",
        "east": "5-34",
        "north": "5-22",
        "monster": "normal",
        "description": "The ground shudders beneath the approach of something massive."
    },
    "5-34": {
        "south": "4-33",
        "west": "4-35",
        "monster": "normal",
        "description": "A creature that defies nature watches you from the darkness."
    },
    "5-35": {
        "east": "5-34",
        "west": "5-36",
        "monster": "boss",
        "description": "Reality tears apart as a deity of darkness manifests, its true form hidden behind veils of madness-inducing horror."
    },
    "5-36": {
        "south": "5-45",
        "north": "5-37",
        "item": "health potion",
        "description": "Clockwork mechanisms mark impossible hours. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "5-37": {
        "east": "5-38",
        "south": "5-36",
        "item": "health potion",
        "description": "Messages scrawled in blood remain legible. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "5-38": {
        "east": "5-39",
        "west": "5-37",
        "item": "health potion",
        "description": "Vaulted ceilings disappear into darkness. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "5-39": {
        "east": "5-40",
        "west": "5-38",
        "item": "health potion",
        "description": "Ripples disturb the air like water. You see a glass vial filled with swirling crimson liquid that pulses gently on the nearby pedestal."
    },
    "5-40": {
        "east": "5-41",
        "west": "5-39",
        "monster": "boss",
        "item": "spell book",
        "lore": "NOTHING IN THIS WORLD IS RIGHT",
        "description": "The fabric of reality screams as the emergence occurs, dimensions bleeding at its presence."
    },
    "5-41": {
        "east": "5-40",
        "west": "5-42",
        "item": "mana potion",
        "lore": "And you must right those wrongs.",
        "description": "Books whisper contents to nearby listeners. You notice a vial whose liquid shifts between colors like a sunset in miniature, reflecting off the potion that sits in the beam of light."
    },
    "5-42": {
        "east": "4-41",
        "west": "4-43",
        "item": "mana potion",
        "description": "Whispers seem to come from just behind you. Before you sits a potion that pulses with an inner rhythm matching your heartbeat, perched precariously on the edge of the broken table."
    },
    "5-43": {
        "east": "4-42",
        "north": "5-44",
        "item": "health potion",
        "description": "Arcane energies swirl like visible currents. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "5-44": {
        "east": "5-45",
        "west": "5-43",
        "monster": "normal",
        "description": "A twisted form writhes in the corner, its eyes glowing with unnatural hunger."
    },
    "5-45": {
        "south": "5-46",
        "west": "5-44",
        "monster": "boss",
        "lore": "ALL YOUR EFFORTS ARE FOR NOTHING.",
        "description": "Where light never reached, a terrible divinity awakens, its power warping the laws of existence."
    },
    "5-46": {
        "east": "5-47",
        "north": "5-45",
        "lore": "Turn back now.",
        "description": "Magical mirrors show paths yet untaken."
    },
    "5-47": {
        "east": "5-48",
        "north": "5-46",
        "monster": "normal",
        "lore": "You have no place with the gods.",
        "description": "Something moves with unnatural grace, its form unclear."
    },
    "5-48": {
        "west": "5-47",
        "south": "5-49",
        "monster": "normal",
        "description": "A creature that defies nature watches you from the darkness."
    },
    "5-49": {
        "north": "4-48",
        "south": "4-50",
        "item": "health potion",
        "description": "Ancient calendars display impossible dates. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "5-50": {
        "north": "5-49",
        "south": "5-51",
        "monster": "boss",
        "lore": "ITS NOT FAIR",
        "description": "The throne of skulls creaks as a skeletal form rises, its very presence causing time to unravel; its voice is the whisper of forgotten graves."
    },
    "5-51": {
        "north": "5-50",
        "east": "5-52",
        "monster": "normal",
        "lore": "It never was.",
        "description": "The ground shudders beneath the approach of something massive."
    },
    "5-52": {
        "west": "5-51",
        "east": "5-53",
        "north": "5-59",
        "monster": "normal",
        "lore": "A N D  Y O U  K N O W  I T.",
        "description": "A creature that seems to be made of pure malevolence watches you."
    },
    "5-53": {
        "west": "5-52",
        "south": "5-54",
        "item": "health potion",
        "description": "Stone tablets bear eroding inscriptions. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "5-54": {
        "north": "5-53",
        "west": "5-55",
        "item": "health potion",
        "description": "Mosaic floors depict scenes of ancient battles. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "5-55": {
        "east": "5-54",
        "west": "5-56",
        "monster": "boss",
        "description": "Between realms of life and death stands the master of undeath, its cold calculation weighing the worth of all souls."
    },
    "5-56": {
        "east": "5-55",
        "west": "5-57",
        "monster": "normal",
        "description": "A creature that defies nature watches you from the darkness."
    },
    "5-57": {
        "east": "5-56",
        "west": "5-58",
        "item": "health potion",
        "description": "Transparent figures study ancient texts. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "5-58": {
        "west": "5-57",
        "item": "health potion",
        "description": "Diaries written in invisible ink. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "5-59": {
        "north": "5-52",
        "west": "5-60",
        "item": "health potion",
        "description": "Timepieces run in reverse. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "5-60": {
        "east": "5-59",
        "monster": "boss",
        "description": "The air distorts around a serpentine form of impossible scale; dragonfire crackles between teeth older than mountains."
    },
    "1~1": {
        "north": "1~2",
        "item": "health potion",
        "lore": "hehe, lol jk",
        "description": "Mushrooms grow in concentric circles, their caps pulsing gently. You see a glass vial filled with swirling crimson liquid that pulses gently on the nearby pedestal."
    },
    "1~2": {
        "west": "1~3",
        "south": "1~1",
        "monster": "demon",
        "description": "Cobwebs hang heavy with secrets; unseen wings flutter in darkness."
    },
    "1~3": {
        "west": "1~4",
        "east": "1~2",
        "south": "1~8",
        "item": "mythril pants",
        "description": "Lightning flashes within rooms. You find pants whose ancient runes pulse with faint light along the seams, sitting atop the magical platform."
    },
    "1~4": {
        "west": "1~5",
        "east": "1~3",
        "south": "1~7",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "1~5": {
        "south": "1~6",
        "east": "1~4",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "1~6": {
        "east": "1~7",
        "north": "1~5",
        "item": "health potion",
        "description": "Raw magical force seeps from cracks. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "1~7": {
        "east": "1~8",
        "west": "1~6",
        "north": "1~4",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "1~8": {
        "south": "1~9",
        "west": "1~7",
        "north": "1~3",
        "item": "mythril boots",
        "description": "The floor tiles are uneven, shifting subtly underfoot as if alive. You see boots that leave no footprints in the dust, standing on the ancient floor."
    },
    "1~9": {
        "south": "1~10",
        "north": "1~8",
        "monster": "demon",
        "description": "Cobwebs hang heavy with secrets; unseen wings flutter in darkness."
    },
    "1~10": {
        "east": "1~13",
        "north": "1~9",
        "south": "1~11",
        "item": "health potion",
        "description": "Mechanical devices count backward. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "1~11": {
        "north": "1~10",
        "south": "1~12",
        "item": "mythril sword",
        "description": "Rooms exist in multiple places simultaneously. You find a sword that feels alive in your hand, sitting atop the treasure pile."
    },
    "1~12": {
        "north": "1~11",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "1~13": {
        "west": "1~14",
        "east": "1~10",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "1~14": {
        "south": "1~15",
        "east": "1~13",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "1~15": {
        "west": "1~15",
        "north": "1~14",
        "item": "health potion",
        "description": "Arcane energies swirl like visible currents. You see a glass vial filled with swirling crimson liquid that pulses gently on the nearby pedestal."
    },
    "1~16": {
        "east": "1~15",
        "south": "1~18",
        "north": "1~17",
        "item": "mythril helmet",
        "description": "Living vines snake through ancient stonework. You see a helmet that feels strangely light, sitting atop the treasure pile."
    },
    "1~17": {
        "south": "1~16",
        "item": "health potion",
        "description": "Musical instruments play themselves. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "1~18": {
        "north": "1~16",
        "south": "1~19",
        "monster": "demon",
        "description": "The air is thick with malice; something snarls from the shadows."
    },
    "1~19": {
        "north": "1~18",
        "south": "1~20",
        "item": "mythril chestplate",
        "lore": "You feel an evil presence watching you...",
        "description": "Ancient stonework bears the marks of long-forgotten construction techniques. You see a chestplate whose protective glyphs pulse with inner light, resting on the magical platform."
    },
    "1~20": {
        "north": "1~19",
        "up": "2~1",
        "monster": "demon king lucifer",
        "description": "Dark flames dance across the floor\u2014Lucifer himself awaits."
    },
    "2~1": {
        "down": "1~20",
        "west": "2~2",
        "item": "health potion",
        "description": "Sand timers flow upward. You notice a vial whose liquid inside seems to breathe with its own rhythm, visible in the partially filled container that rests against the wall."
    },
    "2~2": {
        "east": "2~1",
        "north": "2~3",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "2~3": {
        "west": "2~4",
        "south": "2~2",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "2~4": {
        "west": "2~8",
        "east": "2~3",
        "north": "2~5",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "2~5": {
        "south": "2~4",
        "east": "2~6",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "2~6": {
        "west": "2~5",
        "north": "2~7",
        "item": "health potion",
        "description": "Ice formations defy the dungeon's temperature. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "2~7": {
        "south": "2~6",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "2~8": {
        "south": "2~9",
        "east": "2~4",
        "north": "2~14",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "2~9": {
        "east": "2~10",
        "north": "2~8",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "2~10": {
        "east": "2~13",
        "west": "2~9",
        "north": "2~11",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "2~11": {
        "east": "2~12",
        "south": "2~10",
        "warp 1": "2~20",
        "warp 2": "4~20",
        "warp 3": "6~20",
        "item": "health potion",
        "description": "Abandoned armor stands vigil in corners. You see a glass vial filled with swirling crimson liquid that pulses gently on the nearby pedestal."
    },
    "2~12": {
        "south": "2~13",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "2~13": {
        "west": "2~10",
        "north": "2~12",
        "monster": "demon",
        "description": "Flickering shadows dance upon walls; the sound of scuttling grows near."
    },
    "2~14": {
        "south": "2~8",
        "east": "2~15",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "2~15": {
        "west": "2~14",
        "north": "2~16",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "2~16": {
        "north": "2~18",
        "south": "2~15",
        "west": "2~17",
        "item": "health potion",
        "description": "Residual magic crackles in the air. You see a glass vial filled with swirling crimson liquid that pulses gently on the nearby pedestal."
    },
    "2~17": {
        "west": "2~16",
        "north": "2~19",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "2~18": {
        "east": "2~20",
        "south": "2~16",
        "item": "health potion",
        "lore": "You feel vibrations from deep below...",
        "description": "Messages scrawled in blood remain legible. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "2~19": {
        "south": "2~17",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "2~20": {
        "west": "2~18",
        "up": "3~3",
        "warp 1": "2~11",
        "monster": "demon king asmodeus",
        "description": "Everything seems to rot and decay in Asmodeus's presence."
    },
    "3~1": {
        "north": "3~2",
        "monster": "demon",
        "description": "The air is thick with malice; something snarls from the shadows."
    },
    "3~2": {
        "south": "3~1",
        "east": "3~3",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "3~3": {
        "west": "3~2",
        "down": "2~20",
        "north": "3~4",
        "east": "3~8",
        "south": "3~16",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "3~4": {
        "south": "3~3",
        "east": "3~5",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "3~5": {
        "south": "3~6",
        "west": "3~4",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "3~6": {
        "east": "3~7",
        "north": "3~5",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "3~7": {
        "west": "3~6",
        "monster": "demon",
        "description": "The air is thick with malice; something snarls from the shadows."
    },
    "3~8": {
        "east": "3~7",
        "west": "3~7",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "3~9": {
        "west": "3~10",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "3~10": {
        "east": "3~16",
        "north": "3~9",
        "west": "3~11",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "3~11": {
        "east": "3~10",
        "item": "health potion",
        "description": "Clouds form and dissipate indoors. You notice a vial whose liquid inside seems to breathe with its own rhythm, visible in the partially filled container that rests against the wall."
    },
    "3~12": {
        "south": "3~18",
        "north": "3~16",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "3~13": {
        "west": "3~14",
        "north": "3~19",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "3~14": {
        "south": "3~15",
        "east": "3~13",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "3~15": {
        "north": "3~15",
        "item": "health potion",
        "description": "Spell residue crackles in the air. You find a vial with a delicate silver cap sealing in its precious contents, leaning against the stone pillar."
    },
    "3~16": {
        "north": "3~3",
        "south": "3~12",
        "west": "3~10",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "3~17": {
        "west": "3~19",
        "south": "3~20",
        "item": "health potion",
        "lore": "This is going to be a terrible night...",
        "description": "Timepieces run in reverse. You notice a vial whose liquid inside seems to breathe with its own rhythm, visible in the partially filled container that rests against the wall."
    },
    "3~18": {
        "north": "3~12",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "3~19": {
        "east": "3~17",
        "south": "1~13",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "3~20": {
        "north": "3~17",
        "up": "4~1",
        "monster": "demon king leviathan",
        "description": "A deep rumble echoes\u2014Leviathan stirs in his watery tomb."
    },
    "4~1": {
        "east": "4~2",
        "south": "4~10",
        "monster": "demon",
        "description": "Cobwebs hang heavy with secrets; unseen wings flutter in darkness."
    },
    "4~2": {
        "south": "4~9",
        "west": "4~1",
        "east": "4~3",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "4~3": {
        "south": "4~8",
        "west": "4~2",
        "east": "4~4",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "4~4": {
        "south": "4~7",
        "west": "4~3",
        "east": "4~5",
        "monster": "demon",
        "description": "Cobwebs hang heavy with secrets; unseen wings flutter in darkness."
    },
    "4~5": {
        "south": "4~6",
        "west": "4~4",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "4~6": {
        "south": "4~15",
        "west": "4~7",
        "north": "4~5",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "4~7": {
        "west": "4~8",
        "north": "4~4",
        "east": "4~6",
        "south": "4~14",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "4~8": {
        "west": "4~9",
        "north": "4~3",
        "east": "4~7",
        "south": "4~13",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "4~9": {
        "west": "4~10",
        "north": "4~2",
        "east": "4~8",
        "south": "4~12",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "4~10": {
        "north": "4~1",
        "east": "4~9",
        "south": "4~11",
        "monster": "demon",
        "description": "Flickering shadows dance upon walls; the sound of scuttling grows near."
    },
    "4~11": {
        "north": "4~10",
        "east": "4~8",
        "south": "4~20",
        "monster": "demon",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "4~12": {
        "west": "4~11",
        "north": "4~9",
        "east": "4~13",
        "south": "4~19",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "4~13": {
        "west": "4~12",
        "north": "4~8",
        "east": "4~14",
        "south": "4~18",
        "monster": "demon",
        "description": "Flickering shadows dance upon walls; the sound of scuttling grows near."
    },
    "4~14": {
        "west": "4~13",
        "north": "4~7",
        "east": "4~15",
        "south": "4~17",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "4~15": {
        "west": "4~14",
        "north": "4~6",
        "south": "4~16",
        "monster": "demon",
        "description": "Cobwebs hang heavy with secrets; unseen wings flutter in darkness."
    },
    "4~16": {
        "north": "4~15",
        "west": "4~17",
        "monster": "demon",
        "description": "Flickering shadows dance upon walls; the sound of scuttling grows near."
    },
    "4~17": {
        "west": "4~18",
        "north": "4~14",
        "east": "4~16",
        "item": "health potion",
        "description": "Natural phenomena defy physics. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "4~18": {
        "west": "4~19",
        "north": "4~13",
        "east": "4~17",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "4~19": {
        "west": "4~20",
        "north": "4~12",
        "east": "4~18",
        "warp 2": "2~11",
        "item": "health potion",
        "lore": "The air is getting colder around you...",
        "description": "Windows show impossible views. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "4~20": {
        "north": "4~11",
        "east": "4~19",
        "up": "5~5",
        "monster": "demon king belphegor",
        "description": "Everything here sags under invisible weight\u2014Belphegor dreams."
    },
    "5~1": {
        "east": "5~5",
        "north": "5~7",
        "south": "5~16",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "5~2": {
        "west": "5~18",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "5~3": {
        "north": "5~17",
        "south": "5~13",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "5~4": {
        "south": "5~11",
        "monster": "demon",
        "description": "Cobwebs hang heavy with secrets; unseen wings flutter in darkness."
    },
    "5~5": {
        "west": "5~1",
        "down": "4~20",
        "north": "5~6",
        "east": "5~11",
        "south": "5~18",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "5~6": {
        "west": "5~7",
        "south": "5~5",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "5~7": {
        "east": "5~6",
        "west": "5~10",
        "south": "5~1",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "5~8": {
        "north": "5~19",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "5~9": {
        "east": "5~16",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "5~10": {
        "east": "5~7",
        "south": "5~15",
        "west": "5~14",
        "monster": "demon",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "5~11": {
        "west": "5~5",
        "north": "5~4",
        "item": "health potion",
        "description": "Chalk drawings of runes and figures cover one wall, still smudged with fresh marks. You see a glass vial filled with swirling crimson liquid that pulses gently on the nearby pedestal."
    },
    "5~12": {
        "north": "5~18",
        "east": "5~17",
        "west": "5~19",
        "monster": "demon",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "5~13": {
        "north": "5~3",
        "monster": "demon",
        "description": "Flickering shadows dance upon walls; the sound of scuttling grows near."
    },
    "5~14": {
        "east": "5~10",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "5~15": {
        "north": "5~10",
        "item": "health potion",
        "description": "Storms rage within single chambers. On the floor lies a potion surrounded by a protective circle of ash."
    },
    "5~16": {
        "north": "5~1",
        "west": "5~9",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "5~17": {
        "west": "5~12",
        "south": "5~3",
        "item": "health potion",
        "description": "A withered banner hangs limply from the ceiling, its emblem unrecognizable. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "5~18": {
        "north": "5~5",
        "east": "5~2",
        "south": "5~12",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "5~19": {
        "west": "5~20",
        "south": "5~8",
        "east": "5~12",
        "monster": "demon",
        "lore": "What a horrible night to have a curse...",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "5~20": {
        "east": "5~19",
        "up": "6~1",
        "monster": "demon king beelzebub",
        "description": "Insects skitter at the edges of your vision\u2014Beelzebub watches."
    },
    "6~1": {
        "east": "6~13",
        "north": "6~2",
        "south": "6~19",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "6~2": {
        "west": "6~3",
        "south": "6~1",
        "monster": "demon",
        "description": "Cobwebs hang heavy with secrets; unseen wings flutter in darkness."
    },
    "6~3": {
        "west": "6~4",
        "east": "6~2",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "6~4": {
        "south": "6~5",
        "east": "6~3",
        "monster": "demon",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "6~5": {
        "west": "6~6",
        "north": "6~4",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "6~6": {
        "south": "6~7",
        "east": "6~5",
        "north": "6~8",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "6~7": {
        "north": "6~6",
        "monster": "demon",
        "description": "The air is thick with malice; something snarls from the shadows."
    },
    "6~8": {
        "north": "6~9",
        "south": "6~6",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "6~9": {
        "south": "6~8",
        "monster": "demon",
        "description": "The air is thick with malice; something snarls from the shadows."
    },
    "6~10": {
        "south": "6~12",
        "west": "6~11",
        "monster": "demon",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "6~11": {
        "east": "6~10",
        "item": "health potion",
        "description": "Residual magic crackles in the air. You see a potion from which small bubbles rise and pop in perfect synchronization, sitting atop the ancient crate."
    },
    "6~12": {
        "north": "6~10",
        "south": "6~15",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "6~13": {
        "west": "6~1",
        "east": "6~15",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "6~14": {
        "west": "6~17",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "6~15": {
        "north": "6~12",
        "west": "6~13",
        "south": "6~16",
        "item": "health potion",
        "description": "Ethereal dancers perform endless routines. Before you sits a potion that glows with a soft light, as if imbued with a heartbeat, resting alone on the dusty shelf."
    },
    "6~16": {
        "north": "6~17",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "6~17": {
        "east": "6~14",
        "south": "6~16",
        "north": "6~15",
        "monster": "demon",
        "description": "Cobwebs hang heavy with secrets; unseen wings flutter in darkness."
    },
    "6~18": {
        "east": "6~1",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "6~19": {
        "north": "6~1",
        "south": "6~20",
        "monster": "demon",
        "lore": "Otherworldly voices linger around you...",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "6~20": {
        "north": "6~19",
        "up": "7~1",
        "monster": "demon king beelzebub",
        "description": "Insects skitter at the edges of your vision\u2014Beelzebub watches."
    },
    "7~1": {
        "west": "7~2",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "7~2": {
        "south": "7~3",
        "east": "7~1",
        "monster": "demon",
        "description": "Rustling cloth whispers ancient tales; footsteps echo where none walk."
    },
    "7~3": {
        "west": "7~4",
        "north": "7~2",
        "monster": "demon",
        "description": "The air is thick with malice; something snarls from the shadows."
    },
    "7~4": {
        "south": "7~5",
        "east": "7~3",
        "monster": "demon",
        "description": "The air is thick with malice; something snarls from the shadows."
    },
    "7~5": {
        "north": "7~4",
        "west": "7~6",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "7~6": {
        "south": "7~7",
        "north": "7~5",
        "monster": "demon",
        "description": "Flickering shadows dance upon walls; the sound of scuttling grows near."
    },
    "7~7": {
        "north": "7~6",
        "west": "7~8",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "7~8": {
        "east": "7~7",
        "west": "7~9",
        "monster": "demon",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "7~9": {
        "west": "7~10",
        "east": "7~8",
        "monster": "demon",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "7~10": {
        "east": "7~9",
        "north": "7~11",
        "monster": "demon",
        "description": "A chill wind stirs dust of ages; whispers echo through forgotten chambers."
    },
    "7~11": {
        "east": "7~12",
        "south": "7~10",
        "monster": "demon",
        "description": "Damp earth smells of decay; distant growling grows louder still."
    },
    "7~12": {
        "south": "7~13",
        "west": "7~11",
        "monster": "demon",
        "description": "Flickering shadows dance upon walls; the sound of scuttling grows near."
    },
    "7~13": {
        "west": "7~14",
        "north": "7~12",
        "monster": "demon",
        "description": "Shadows writhe across ancient stone; malevolent eyes gleam in darkness."
    },
    "7~14": {
        "west": "7~15",
        "east": "7~13",
        "monster": "demon",
        "description": "Flickering shadows dance upon walls; the sound of scuttling grows near."
    },
    "7~15": {
        "north": "7~16",
        "east": "7~14",
        "monster": "demon",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "7~16": {
        "south": "7~15",
        "east": "7~17",
        "monster": "demon",
        "description": "Icy drafts carry forgotten screams; darkness pulses with hungry life."
    },
    "7~17": {
        "west": "7~16",
        "south": "7~18",
        "monster": "demon",
        "description": "Torchlight flickers wildly; something massive shifts beyond the flame's reach."
    },
    "7~18": {
        "west": "7~19",
        "north": "7~17",
        "monster": "demon",
        "description": "Cobwebs hang heavy with secrets; unseen wings flutter in darkness."
    },
    "7~19": {
        "east": "7~19",
        "south": "7~20",
        "monster": "demon",
        "lore": "Impending doom approaches...",
        "description": "Mold-covered walls seem to breathe; faint scratching echoes through corridors."
    },
    "7~20": {
        "north": "7~19",
        "up": "?~??",
        "monster": "demon king satan",
        "description": "The very fabric of reality seems to tear apart\u2014Satan awaits."
    },
    "?~??": {
        "description": "Seasons cycle within single rooms."
    }
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
print(GREEN)
clear_screen()

print_slow(r"""
 _____         _      _   _
|_   _|____  _| |_   | | | | ___ _ __ ___
  | |/ _ \ \/ / __|  | |_| |/ _ \ '__/ _ \
  | |  __/>  <| |_   |  _  |  __/ | | (_) |
  |_|\___/_/\_\\__|  |_| |_|\___|_|  \___/
            Salvation Edition
""")
def print_intro():
    print_slow_intro(f"\n{GREEN}Long ago, the Island of Rhyvannar fell to darkness.\n")
    time.sleep(1)
    print_slow_intro("Count Dracula’s army of demons swept across the land.\n")
    time.sleep(1)
    print_slow_intro("The war lasted thousands of years, costing trillions of lives. \n")
    time.sleep(1)
    print_slow_intro("Until one man, Xyron of Varyndor, turned the tide with a single act: ")
    time.sleep(1)
    print_slow_intro("\nHe tore the Cloak of Kadulom from Dracula’s shoulders, sealing his power.\n")
    time.sleep(1)
    print_slow_intro("In victory, Xyron was crowned Great Hari and built Castle Archmoltry atop the battlefield.\n")
    time.sleep(1)
    print_slow_intro("But victory bred pride. Pride bred corruption.\n")
    time.sleep(1)
    print_slow_intro("The Cloak’s curse took root, consuming Xyron and the castle.\n")
    time.sleep(1)
    print_slow_intro("Now, darkness stirs beneath the ruins.\n")
    time.sleep(1)
    print_slow_intro("The spirits of the fallen haunt the crypts.")
    time.sleep(1)
    print_slow_intro("\nThe Cloak beats with unnatural life.\n")
    time.sleep(1)
    print_slow_intro("And you, the lone survivor, are trapped within.\n")
    time.sleep(1)
    print_slow_intro(f"{BLUE}Press enter to continue")
    input("")
# Game setup
print_intro()
print_slow(GREEN)
clear_screen()
print_slow(r"""
 _____         _      _   _
|_   _|____  _| |_   | | | | ___ _ __ ___
  | |/ _ \ \/ / __|  | |_| |/ _ \ '__/ _ \
  | |  __/>  <| |_   |  _  |  __/ | | (_) |
  |_|\___/_/\_\\__|  |_| |_|\___|_|  \___/
            Salvation Edition
""")

def clear_lines(number: int, LEN = 100):
    for i in range(number):
        print("\033[F" + (" " * LEN), end="")
    print("\033[F")

class keyboard_handler(object):
    def __init__(self):
        self.clicked = []
        keyboard.hook(lambda e: self.key_event(e))
    def key_event(self, event):
        if event.event_type == keyboard.KEY_UP:
            self.key_release(event)
        elif event.event_type == keyboard.KEY_DOWN:
            self.key_press(event)
    def key_press(self, event):
        tag = str(event.name).lower()
        if tag.startswith('Shift'):
            tag = 'Shift'
        elif tag.startswith('Alt'):
            tag = 'Alt'
        elif tag.startswith('Control'):
            tag = 'Control'
        elif tag == '\t':
            tag = 'Tab'
        elif tag == '\b':
            tag = 'BackSpace'
        elif tag in ['\r', '\n', '\r\n']:
            tag = 'Enter'
        elif tag == 'Escape':
            tag = "Esc"
        elif tag == '\x1b':
            tag = 'Esc'
        elif tag == ' ':
            tag = 'Space'
        if tag not in self.clicked:
            self.clicked.append(tag)
    def key_release(self, event):
        tag = str(event.name).lower()
        if tag.startswith('Shift'):
            tag = 'Shift'
        elif tag.startswith('Alt'):
            tag = 'Alt'
        elif tag.startswith('Control'):
            tag = 'Control'
        elif tag == '\t':
            tag = 'Tab'
        elif tag == '\b':
            tag = 'BackSpace'
        elif tag in ['\r', '\n', '\r\n']:
            tag = 'Enter'
        elif tag == 'Escape':
            tag = "Esc"
        elif tag == '\x1b':
            tag = 'Esc'
        elif tag == ' ':
            tag = 'Space'
        try:
            self.clicked.remove(tag)
        except ValueError:
            pass
    def is_pressed(self, char):
        if char in self.clicked:
            return True
        else:
            return False

class selection_menu(object):
    def __init__(self, *items, indent_size = 2):
        self.Runner = self.runner(items, indent_size)
    def run(self):
        self.Runner.start()
        input()
        self.Runner.stop = True
        time.sleep(0.01)
        clear_lines(len(self.Runner.print_order) + 2, self.Runner.clear_len)
        return self.Runner.cursor_pos
    class runner(Thread):
        def __init__(self, items, indent_size):
            self.max_cursor_pos = 0
            self.states = []
            self.print_order = []
            for item in items:
                if item[0] == 'text': self.print_order.append(item)  # noqa: E701
                elif item[0] == 'option':
                    self.print_order.append(['option', '{0}' + item[1]])
                    self.states.append(0)
                    self.max_cursor_pos += 1
            self.stop = False
            Thread.__init__(self)
        def run(self):
            cursor_pos = 0
            was_going = None
            selected = 0
            clear_len = 0
            to_print = ""
            for item in self.print_order:
                if item[0] == 'text':
                    to_print += item[1] + '\n'
                    if len(item[1]) > clear_len:
                        clear_len = len(item[1])
                elif item[0] == 'option':
                    tmp = len((item[1].format(['[ ]', '[*]'][int(selected == cursor_pos)]) + '\n'))
                    if tmp > clear_len:
                        clear_len = tmp
                    to_print += (item[1].format(['[ ]', '[*]'][int(selected == cursor_pos)])) + '\n'
                    selected += 1
            print("\n" + to_print, end='')
            time.sleep(0.01)
            while True:
                to_print = False
                if Input.is_pressed('down') and was_going != 'down':
                    to_print = "\n"
                    cursor_pos += 1
                    if cursor_pos > self.max_cursor_pos - 1:
                        cursor_pos = 0
                    was_going = 'down'
                elif Input.is_pressed('up') and was_going != 'up':
                    to_print = "\n"
                    cursor_pos -= 1
                    if cursor_pos < 0:
                        cursor_pos = self.max_cursor_pos - 1
                    was_going = 'up'
                elif not Input.is_pressed('up') and not Input.is_pressed('down'):
                    was_going = None
                if to_print:
                    clear_lines(len(self.print_order) + 1, clear_len)
                    selected = 0
                    for item in self.print_order:
                        if item[0] == 'text':
                            to_print += item[1] + '\n'
                        elif item[0] == 'option': 
                            to_print += (item[1].format(['[ ]', '[*]'][int(selected == cursor_pos)])) + '\n'
                            selected += 1
                    print(to_print, end=' ')
                time.sleep(0.01)
                if self.stop:
                    self.clear_len = clear_len
                    self.cursor_pos = cursor_pos
                    break

Input = keyboard_handler() # Keep and use this variable. Input.is_pressed("w") for example.

print("To start choose a class:")
menu = selection_menu(['option', 'Warrior'], ['option', 'Rogue'], ['option', 'Mage'], ['option', 'Archer'], ['option', 'Load']) # Formatted [type, text_content], [type, text_content]
# menu = selection_menu(['option', 'Warrior'], ['option', 'Rogue'], ["text", "Random text in the middle. :)"], ['option', 'Mage'], ['option', 'Ranger'], ['option', 'Load']) # An example, uncomment and run to see how it works.
chosen_class = ['Warrior', 'Rogue', 'Mage', 'Archer', 'Load'][menu.run()]


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
inventory = []

# Track defeated bosses

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
    print_slow(f"{GREEN}---------------------------")
# Define the data for the casino games
casino_games = {
    "Blackjack": {
        "description": "Test your luck and skill—get 21 or bust!",
        "price": "10 to 1000"
    },
    "Roulette": {
        "description": "Place your bets on red, black, or numbers!",
        "price": "25 to 5000"
    },
    "Slot Machine": {
        "description": "Spin the reels and hit the jackpot",
        "price": "5"
    }
}

# Define the column headers
casino_columns = [
    ("Game", 20),
    ("Cost", 20),
    ("Description", 45)
]


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
def Show_casino_games():
    display_table(
        "Casino Royale",
        casino_games,
        casino_columns
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
    if player_class_2 is None:
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
    if player_class_2 is not None:
        for spell, values in locked_spells[player_class_2].items():
            effect = values[0]
            cost = values[1]
            special = get_spell_description(spell)
            print_slow(f"│ {spell:<14} │ {effect:<11} │ {cost:<10} │ {special:<42} │")

    
    print_slow("└────────────────┴─────────────┴────────────┴────────────────────────────────────────────┘")
    
    # Display unlockable spells if any exist
    if locked_spells[player_class]:
        print_slow(f"\n{GREEN}Unlockable Spells:")
        print_slow("┌────────────────┬─────────────┬────────────┬────────────────────────────────────────────┐")
        print_slow("│ Spell          │ Damage/Eff  │ Mana Cost  │ Special Effect                             │")
        print_slow("├────────────────┼─────────────┼────────────┼────────────────────────────────────────────┤")
        

    # Iterate through both classes' spells
        for spell, values in locked_spells[player_class].items(): 
            effect = values[0] 
            cost = values[1] 
            special = get_spell_description(spell) 
            
            print_slow(f"│ {spell:<14} │ {effect:<11} │ {cost:<10} │ {special:<42} │") 
        if player_class_2 is not None:
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
        f"{GREEN}slash": "Basic melee attack",
        f"{GREEN}finishing blow": "Powerful finishing attack",
        f"{GREEN}stun strike": "Chance to stun enemy (2-5 turns)",
        f"{GREEN}fireball": "Causes burning for 3 turns",
        f"{GREEN}water bolt": "Basic water attack, low cost",
        f"{GREEN}thunder zapper": "Chance to stun enemy",
        f"{GREEN}back stab": "Basic rogue attack",
        f"{GREEN}stealth": "Allows you to exit the battle",
        f"{GREEN}stealth strike": "Attack from stealth confusing the enemy",
        f"{GREEN}spear of justice": "Attack enemies with a spear of justice",
        f"{GREEN}great heal": "Powerful single target heal",
        f"{GREEN}divine shield": "Block damage for 3 rounds",
        f"{GREEN}minor heal": "Small efficient heal",
        f"{GREEN}bleeding arrow": "Causes bleeding damage",
        f"{GREEN}binding shot": "Roots enemy in place",
        f"{GREEN}holy strike": "Imbue your sword with holy power",
        f"{GREEN}healing pool": "A small healing spell",
        f"{GREEN}tidal wave": "Summon a tsunami to decimate your enemies",
        f"{GREEN}kamehameha": "A legendary attack used by a Turtle Hermit",
        f"{GREEN}assassinate": "Catch enemies off guard",
        f"{GREEN}ultrakill": "A truly overkill spell",
        f"{GREEN}holy cleansing": "Heals a minor amount of HP",
        f"{GREEN}arrow of light": "Fire a holy arrow, blinding enemies",
        f"{GREEN}marksman": "Bounce an arrow off of a coin",
        f"{GREEN}mordschlang": "Attack with the pommel of the sword",
        f"{GREEN}boulder": "Throw a boulder at the enemy",
        f"{GREEN}knife throw": "Throw a knife",
        f"{GREEN}divine retribution": "The wrath of the gods will aid you in battle",
        f"{GREEN}double shot": "Shoot 2 arrows at once",
        f"{GREEN}blood bomb": "Release an explosive blood sack",
        f"{GREEN}lifesteal": "Drain the life force of the enemy", 
        f"{GREEN}blood spear": "Shoot a spear of blood at the enemy",
        f"{GREEN}haemolacria": "launch a giant bloody tear at the enemy"
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
                enemy_type = MONSTER_TYPES['demon king lucifer']
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
                print_slow(f"{GREEN}---------------------------")
                
                # Display all enemy health
                for i, enemy in enumerate(enemies):
                    print_slow(f"Enemy {i+1} ({enemy['name']}): {enemy['health']} HP")
                
                print_slow(f"{GREEN}---------------------------")
                print_slow(f"Your Health: {player['health']}")
                print_slow(f"Your Mana: {player['mana']}")
                print_slow(f"Your armor: {player['armor']}")

                # Display inventory
                show_inventory()
                print(GREEN)
                print_slow(f"{GREEN}---------------------------")
                
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
                        turn_log += f"{GREEN}You attack {enemy['name']} with {accuracy_percent}% accuracy for{COMBAT_COLOR} {attack_damage} damage!{GREEN}\n"
                        enemy["health"] -= attack_damage
                        
                        # Check if enemy is defeated
                        if enemy["health"] <= 0:
                            turn_log += f"{GREEN}you defeated {enemy['name']}!\n"
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
                                turn_log += f"You cast {spell_name} at {enemy['name']} with {spell_percent}% efficiency for{COMBAT_COLOR} {damage} damage{GREEN} and {RED}burns{GREEN} the enemy!\n"
                                enemy["health"] -= damage
                            elif spell_name in ["back stab", "slash", "water bolt", "bleeding arrow", "eternity", "supernova", "phantasm", "assassinate", "tidal wave", "ultrakill", "midas prime", "kamehameha", "mordschlang", "boulder", "blood bomb", "blood spear", "haemolacria", "spear of justice"]:
                                base_damage = player["spells"][spell_name][0]
                                damage = int(base_damage * (spell_percent / 100))
                                turn_log += f"You cast {spell_name} at {enemy['name']} with {spell_percent}% efficiency for{COMBAT_COLOR} {damage} damage!{GREEN}\n"
                                enemy["health"] -= damage
                            elif spell_name == "life steal":
                                base_damage == player["spells"][spell_name][0]
                                damage = int(base_damage * (spell_percent / 100))
                                healing_amount = damage / 5
                                turn_log += f"You cast {spell_name} at {enemy['name']} with {spell_percent}% efficiency for{COMBAT_COLOR} {damage} damage{GREEN} and you heal {healing_amount} health!\n"
                                player["health"] = min(player["health"] + healing_amount, classes[player["class"]]["health"])
                                enemy['health'] -= damage
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
                                turn_log += f"You cast {spell_name} at {enemy['name']} with {spell_percent}% efficiency for{COMBAT_COLOR} {damage} damage{GREEN} and you heal {healing_amount} health!\n"
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
                                turn_log += f"You deal {spell_percent}% accuracy for{COMBAT_COLOR} {damage} damage!{GREEN}\n"
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
                            print_slow(f"{GREEN}you defeated the boss!\n You have earned {ITEM_COLOR}{gold_dropped} gold{GREEN} and {ITEM_COLOR}{exp_earned} exp{GREEN}!")
                            player["gold"] += gold_dropped
                            player["exp"] += exp_earned

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] >= 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 15 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")

                        elif monster_type == 'vampire':
                            # Vampire rewards
                            gold_dropped = random.randint(
                                MONSTER_TYPES['vampire']['gold_drop_range'][0],
                                MONSTER_TYPES['vampire']['gold_drop_range'][1]
                            )
                            exp_earned = 100
                            inventory.append("vampire pendant")
                            print_slow(f"{GREEN}Count Dracula dropped a mysterious {ITEM_COLOR}pendant{GREEN}!")
                            print_slow(f"You earned {ITEM_COLOR}{gold_dropped} gold{GREEN} and {ITEM_COLOR}100 exp{GREEN}!")
                            
                            player["gold"] += gold_dropped
                            player["exp"] += exp_earned

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                        
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
                            print_slow(f"You earned {ITEM_COLOR}1000 gold{GREEN} and {ITEM_COLOR}500 exp{GREEN}!")
                            
                            player["gold"] += 1000
                            player["exp"] += 500

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")

                        elif monster_type == 'demon king asmodeus':
                            # Boss rewards
                            for i in range(5):
                                inventory.append("adamantite bar")
                            print_slow(f"{GREEN}Demon King Asmodeus dropped 5 {ITEM_COLOR}Adamantite bars{GREEN}!")
                            print_slow(f"{GREEN}you defeated Demon King Asmodeus!\n You have earned {ITEM_COLOR}1000 gold{GREEN} and {ITEM_COLOR}500 exp{GREEN}!")
                            player["gold"] += 1000
                            player["exp"] += 500

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                        
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
                            print_slow(f"You earned {ITEM_COLOR}1000 gold{GREEN} and {ITEM_COLOR}500 exp{GREEN}!")
                            
                            player["gold"] += 1000
                            player["exp"] += 500

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")

                        elif monster_type == 'demon king belphegor':
                            # Boss rewards
                            for i in range(5):
                                inventory.append("hallowed bar")
                            print_slow(f"{GREEN}Demon King Belphegor dropped 5 {ITEM_COLOR}Hallowed bars{GREEN}!")
                            print_slow(f"{GREEN}you defeated Demon King Belphegor!\n You have earned {ITEM_COLOR}1000 gold{GREEN} and {ITEM_COLOR}500 exp{GREEN}!")
                            player["gold"] += 1000
                            player["exp"] += 500
                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                        
                        elif monster_type == 'demon king beelzebub':
                            print_slow(f"You earned {ITEM_COLOR}1000 gold{GREEN} and {ITEM_COLOR}500 exp{GREEN}!")
                            
                            player["gold"] += 1000
                            player["exp"] += 500

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                        
                        elif monster_type == 'demon king mammon':
                            # Boss rewards
                            for i in range(5):
                                inventory.append("cosmilite bar")
                            print_slow(f"{GREEN}Demon King Mammon dropped 5 {ITEM_COLOR}Cosmilite bars{GREEN}!")
                            print_slow(f"{GREEN}you defeated Demon King Mammon!\n You have earned {ITEM_COLOR}1000 gold{GREEN} and {ITEM_COLOR}500 exp{GREEN}!")
                            player["gold"] += 1000
                            player["exp"] += 500
                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                        elif monster_type == 'demon king satan':
                            # Boss rewards
                            print_slow(f"{GREEN}you defeated Demon King Satan!\n You have earned {ITEM_COLOR}1000 gold{GREEN} and {ITEM_COLOR}1000 exp{GREEN}!")
                            player["gold"] += 1000
                            player["exp"] += 1000


                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
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
                                print_slow(f"{GREEN}A monster dropped {ITEM_COLOR}{dropped_item}{GREEN}!")
                            
                            # Key fragment drop chance
                            if random.random() < player['key_fragment_chance']:
                                inventory.append("key fragment")
                                print_slow(f"{GREEN}A monster dropped a {ITEM_COLOR}key fragment{GREEN}!")
                            
                            print_slow(f"{GREEN}you defeated all monsters\nYou have earned {ITEM_COLOR}{gold_dropped} gold{GREEN} and {ITEM_COLOR}{exp_earned * num_monsters} exp{GREEN}!")
                            player["gold"] += gold_dropped
                            player["exp"] += exp_earned * num_monsters

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                        else:
                            # Normal monster rewards - based on how many were defeated
                            gold_dropped = random.randint(
                                MONSTER_TYPES['normal']['gold_drop_range'][0],
                                MONSTER_TYPES['normal']['gold_drop_range'][1]
                            )
                            try:
                                exp_earned = random.randint(
                                    MONSTER_TYPES['normal']['exp_drop_range'][0],
                                    MONSTER_TYPES['normal']['exp_drop_range'][1]
                                )* int(currentRoom[0])
                            except ValueError:
                                exp_earned = random.randint(
                                    MONSTER_TYPES['normal']['exp_drop_range'][0],
                                    MONSTER_TYPES['normal']['exp_drop_range'][1]
                                )* 10
                            
                            # Chance for armor drops
                            if random.random() < MONSTER_TYPES['normal']['item_drop_chance']:
                                slot = random.choice(list(ARMOR_SLOTS.keys()))
                                tier = random.choice(['leather', 'chainmail', 'iron'])
                                dropped_item = f"{tier} {slot}"
                                inventory.append(dropped_item)
                                print_slow(f"{GREEN}A monster dropped {ITEM_COLOR}{dropped_item}{GREEN}!")
                            
                            # Key fragment drop chance
                            if random.random() < player['key_fragment_chance'] and "bleeding key" not in inventory and not inventory.count('key fragment') > 2:
                                inventory.append("key fragment")
                                print_slow(f"{GREEN}A monster dropped a {ITEM_COLOR}key fragment{GREEN}!")

                            print_slow(f"{GREEN}you defeated all monsters\nYou have earned {ITEM_COLOR}{gold_dropped} gold{GREEN} and {ITEM_COLOR}{exp_earned * num_monsters} exp{GREEN}!")
                            player["gold"] += gold_dropped
                            player["exp"] += exp_earned * num_monsters

                            for i in range(2, 51):
                                if player["exp"] >= EXP_TO_LEVEL[i] and i > player["level"]:
                                    player["level"] = i
                                    player["health"] = math.ceil(BASE_STATS["health"] * LEVEL_IMPROVEMENTS[i])
                                    player["attack"] = math.ceil(BASE_STATS["attack"] * LEVEL_IMPROVEMENTS[i])
                                    player["mana"] = math.ceil(BASE_STATS["mana"] * LEVEL_IMPROVEMENTS[i])
                                    if player["level"] > 20:
                                        player["armor"] = 20
                                    else:
                                        player["armor"] = ARMOR_IMPROVEMENTS[player["level"]]
                                    print_slow(f"You have reached {ITEM_COLOR}level {player['level']}{GREEN}!")
                                    print_slow("Your stats have improved!")
                                    print_slow(f"{ITEM_COLOR}Health{GREEN}: {ITEM_COLOR}{player['health']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Mana{GREEN}: {ITEM_COLOR}{player['mana']}{GREEN}")
                                    print_slow(f"{ITEM_COLOR}Attack{GREEN}: {ITEM_COLOR}{player['attack']}{GREEN}")
                                    if not player["armor"] == 20:
                                        print_slow(f"{ITEM_COLOR}Armor{GREEN}: {ITEM_COLOR}{player['armor']}{GREEN}")
                                else:
                                    pass
                            if player["level"] >= 20 and player["class 2"] is None:
                                player["class 2"] = class_to_get_to_tier_2[player["class"]]
                                player["spells"] = spells_tier_2[player["class 2"]]
                                if player["class"] == "Rogue" or player["class"] == "Mage":
                                    print_slow(f"You have become an {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                                else:
                                    print_slow(f"You have become a {ITEM_COLOR}{player['class 2']}{GREEN} and have learnt {ITEM_COLOR}{class_tier_2[player['class 2']]}{GREEN}!")
                        
                        player["armor"] = original_armor
                        del rooms[currentRoom]["monster"]
                        print_slow(f"{GREEN}---------------------------")
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
                                turn_log += f"{RED}{enemy['name']} drains {lifesteal_amount} health ({lifesteal_percent}% of your current health)!{GREEN}\n"
                            
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
                            turn_log += f"{GREEN}{enemy['name']} attacks you for{RED} {enemy_attack} damage!{GREEN}\n"
                        
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
        print_slow(f"{GREEN}---------------------------")
        show_market_items()
    if currentRoom == '1-13':
        print_slow('Blacksmith')
        print_slow(f"{GREEN}---------------------------")
        show_blacksmith_items()
        print_slow("Type 'forge [item]' to craft items")
    if currentRoom == 'casino':
        Show_casino_games()
        print_slow("Type 'play [game]' to start gambling")
    if currentRoom == '2~11':
        print_slow('Mare')
        print_slow(f"{GREEN}---------------------------")
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
        elif move[0] in ['look']:
            print_slow(f'{rooms[currentRoom]["description"]}\n')
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
                            formatted_items = [f"{ITEM_COLOR}{item}{GREEN}" for item in items]
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
                        print_slow(f"Got {ITEM_COLOR}{item}{GREEN}!")
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
                            print_slow(f"Got {ITEM_COLOR}{item_name}{GREEN}!")
                        else:
                            print_slow(f"Can't get {item_name}!")
                    elif item_name == rooms[currentRoom]['item']:
                        inventory.append(item_name)
                        print_slow(f"Got {ITEM_COLOR}{item_name}{GREEN}!")
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
                                print(f"You have become a {ITEM_COLOR}Vampire{GREEN} and have learnt {ITEM_COLOR}{', '.join(spells_tier_2['Vampire'].keys())}{GREEN}!")
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
                                print_slow(f"You learned the {COMBAT_COLOR}{spell}{GREEN} spell!")
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
        elif move[0] == 'play' and currentRoom == 'casino':
            if " ".join(move[1:]) == "slot machine":
                slot_machine(player["gold"])
            elif " ".join(move[1:]) == "blackjack":
                player["gold"] = blackjack(player["gold"])
            elif "".join(move[1:]) == "roulette":
                roulette(player["gold"])
            else:
                print("".join(move[1:]))
                print_slow("Invalid game choice!")
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
                    print_slow(f"Dropped all items: {ITEM_COLOR}{', '.join(dropped_items)}{GREEN}")
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
                    print_slow(f"Dropped: {ITEM_COLOR}{item_name}{GREEN}")
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
