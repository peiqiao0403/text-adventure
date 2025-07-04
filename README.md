## Text Adventure Documentation

## Overview

This text-based RPG features character classes, combat mechanics, inventory management, and a market system. The game combines traditional RPG elements with unique timing-based combat mechanics and an extensive help system.

## Character Classes

The game offers five distinct character classes, each with unique abilities and attributes:

-   **Warrior**
    -   Health: 120
    -   Attack: 25
    -   Spell: Slash (+10 damage)
    -   Mana: 30
-   **Mage**
    -   Health: 80
    -   Attack: 20
    -   Spell: Fireball (+30 damage)
    -   Mana: 100
-   **Rogue**
    -   Health: 100
    -   Attack: 20
    -   Spell: Shadow Strike (+20 damage)
    -   Mana: 50
-   **Healer**
    -   Health: 150
    -   Attack: 12
    -   Spell: Circle Heal (+30 HP)
    -   Mana: 45
-   **Archer**
    -   Health: 110
    -   Attack: 20
    -   Spell: Bleeding Arrow (+25 damage)
    -   Mana: 20
 
## Tier 2 Classes

In addition to these classes, once you reach level 20, you will become one of these classes, depending on the class you first chose:

-   **Paladin**
    -   Health: 204
    -   Attack: 43
    -   Spell: Divine Shield
    -   Mana: 60
-   **Archmage**
    -   Health: 136
    -   Attack: 34
    -   Spell: Infinity (+45 damage)
    -   Mana: 170
-   **Assassin**
    -   Health: 170
    -   Attack: 34
    -   Spell: Supernova (+25 damage)
    -   Mana: 85
-   **Priest**
    -   Health: 255
    -   Attack: 20
    -   Spell: Heal (+50 HP)
    -   Mana: 77
-   **Ranger**
    -   Health: 187
    -   Attack: 34
    -   Spell: Phantasm (+50 damage)
    -   Mana: 34

## Combat Mechanics

Combat in the game is turn-based with timing-based elements for attacks and spells. The combat system follows this structure:

1.  **Combat Flow**
    -   Combat begins when encountering a monster
    -   Take turns making actions
    -   Each action has specific effects and requirements
    -   Combat continues until either side is defeated
2.  **Player Actions**
    -   **Attack**
        -   Uses timing slider for accuracy
        -   Base damage varies by class
        -   Higher timing accuracy increases damage dealt
        -   Accuracy ranges from 35% to 100%
    -   **Defend**
        -   Provides 40-140% defense efficiency
        -   Successful defense provides temporary armor bonus
        -   Also regenerates mana based on defense efficiency
    -   **Cast Spell**
        -   Each class has unique spells
        -   Spell effectiveness ranges from 40-140%
        -   Consumes mana based on spell type
        -   Special effects like burning, stunning, or lifesteal
    -   **Use Item**
        -   Can use health or mana potions during combat
        -   Multiple items can be used with "use [item] [quantity]"
        -   Items provide immediate effects
3.  **Leveling Up**
    -   You can level up after obtaining enough exp, your stats will increase and the exp required for the next level will too

## Inventory and Equipment System

### Armor System

The game features a comprehensive armor system with multiple slots and tiers:

-   **Armor Slots**: helmet, chestplate, pants, boots
-   **Armor Tiers**:
    -   Leather: Low protection (1 defense)
    -   Chainmail: Basic protection (3 defense)
    -   Iron: Moderate protection (5 defense)
    -   Mythril: Medium Protection (7 defense)
    -   Adamantite: Good Protection (10 defense)
    -   Hallowed: High Protection (12 defense)
    -   God Slayer: Maximum defense (15 defense)

### Market System

The market (located in room 1-17) allows you to:

-   Buy items and equipment
-   Sell unwanted gear
-   View available items and prices

## Commands Reference

Basic movement and interaction:
```text
go [direction]      - Move character (or n,s,e,w,u,d)
get [item]          - Pick up items (or g)
use [item] [qty]    - Use items with optional quantity
help                - Show help menu
remove [slot]       - Remove armor from slot (or r)
equip [type] [slot] - Equip armor in slot (or i)
list                - Show market items
buy [item]          - Buy from market
sell [item]         - Sell to market
drop [item]         - Drop items in current room
quit                - Exit the game (or q)
```

## Advanced Features

### Help System

The game includes an extensive help system that provides detailed information about:

-   Commands and controls
-   Character classes and abilities
-   Market system
-   Game mechanics

### Room Layout

The game world is divided into rooms, each with:

-   Multiple exits (north, south, east, west)
-   Potential items or monsters
-   Special locations (market, boss fights)

### Monster Types

Eleven types of enemies:

-   **Normal Monsters**:
    -   Health: 50
    -   Attack range: 5-15
    -   Gold drop: 10-30
    -   EXP drop: 3-5
    -   Item drop chance: 20%
-   **Boss Monsters**:
    -   Health: 200
    -   Attack range: 25-35
    -   Gold drop: 100-150
    -   EXP drop: 5-10
    -   Item drop chance: 100%
-   **Count Dracula**:
    -   Health: 250
    -   Attack range: 35-45
    -   Gold drop: 500-1000
    -   EXP drop: 50-100
    -   Item drop chance: 100%
    -   Special: Life drain ability
-   **Demon**:
    -   Health: 100
    -   Attack range: 25-35
    -   Gold drop: 50-100
    -   EXP drop: 20-30
    -   Item drop chance: 0%
-   **Demon King Lucifer**
    -   Health: 300
    -   Attack range: 50-75
    -   Gold drop: 1000
    -   EXP drop: 500
    -   Item drop chance: 0%
-   **Demon King Asmodeus**:
    -   Health: 400
    -   Attack range: 50-85
    -   Gold drop: 1000
    -   EXP drop: 500
    -   Item drop chance: 0%
-   **Demon King Leviathan**:
    -   Health: 500
    -   Attack range: 75-100
    -   Gold drop: 1000
    -   EXP drop: 500
    -   Item drop chance: 0%
-   **Demon King Belphegor**:
    -   Health: 600
    -   Attack range: 80-100
    -   Gold drop: 1000
    -   EXP drop: 500
    -   Item drop chance: 0%
-   **Demon King Beelzebub**:
    -   Health: 750
    -   Attack range: 150-200
    -   Gold drop: 1000
    -   EXP drop: 500
    -   Item drop chance: 0%
-   **Demon King Mammon**:
    -   Health: 1000
    -   Attack range: 175-225
    -   Gold drop: 1000
    -   EXP drop: 500
    -   Item drop chance: 0%
-   **Demon King Satan**:
    -   Health: 1000
    -   Attack range: 300-400
    -   Gold drop: 1000
    -   EXP drop: 500
    -   Item drop chance: 0%

This documentation covers all major aspects of the game. Please use the help system during gameplay for additional details about specific mechanics or commands.
