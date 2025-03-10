# Text Adventure Documentation

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
-   **Ranger**
    -   Health: 110
    -   Attack: 20
    -   Spell: Bleeding Arrow (+25 damage)
    -   Mana: 20

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

## Inventory and Equipment System

### Armor System

The game features a comprehensive armor system with multiple slots and tiers:

-   **Armor Slots**: helmet, chestplate, pants, boots
-   **Armor Tiers**:
    -   Leather: Basic protection (5 defense)
    -   Chainmail: Medium protection (10 defense)
    -   Iron: Maximum protection (15 defense)

### Market System

The market (located in room 1-17) allows you to:

-   Buy items and equipment
-   Sell unwanted gear
-   View available items and prices

## Commands Reference

Basic movement and interaction:
```text
go [direction]     - Move character (or n,s,e,w,u,d)
get [item]         - Pick up items (or g)
use [item] [qty]   - Use items with optional quantity
help              - Show help menu
remove [slot]      - Remove armor from slot (or r)
equip [type] [slot]- Equip armor in slot (or i)
list              - Show market items
buy [item]        - Buy from market
sell [item]       - Sell to market
drop [item]       - Drop items in current room
quit              - Exit the game (or q)
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

Three types of enemies:

-   **Normal Monsters**:
    -   Health: 50
    -   Attack range: 5-15
    -   Gold drop: 10-30
    -   Item drop chance: 20%
-   **Boss Monsters**:
    -   Health: 200
    -   Attack range: 25-35
    -   Gold drop: 100-150
    -   Item drop chance: 100%
-   **Vampire Boss**:
    -   Health: 250
    -   Attack range: 35-45
    -   Gold drop: 500-1000
    -   Item drop chance: 100%
    -   Special: Life drain ability

This documentation covers all major aspects of the game. Please use the help system during gameplay for additional details about specific mechanics or commands.
