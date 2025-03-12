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
        'east': '1-19',
        'north': '2-1'
    },    
    '2-1': {
        'west': '1-20',
        "north": '2-2'
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
        'item': 'monster'
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
        'item': 'monster'
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
        "item": 'monster'
    },
    '2-12': {
      'north': '2-11',
      'item': 'monster'
    },
    '2-13': {
        'east': '2-12',
        'south': '2-9',
        'north': '2-14',
    },
    '2-14': {
        'south': '2-13',
        "west": "2-16",
        "item": "chainmail leggings"
    },
    '2-15': {
        'east': '2-4',
        'north': '2-7',
        "item": "mythril boots"
    },
    '2-16': {
        'west': '2-18',
        'south': '2-17',
        'east': '2-14',
        'item': 'monster'
    },
    '2-17': {
        'north': '2-16',
        'item': 'monster'
    },
    '2-18': {
        'west': '2-19',
        'east': '2-16',
        'item': 'spell'
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
        'item': 'monster'

    },
    '2-27': {
        'west': '2-26',
        'item': 'monster'

    },
    '2-28': {
        'west': '2-25',
        'east': '2-29',
        'item': 'monster'
    },
    '2-29': {
        'west': '2-28',
        'south': '2-30',
        'item': 'iron boots'
    },
    '2-30': {
        'east': '2-29',
        'west': '3-1',
        'item': 'health potion'

    '3-1': {
        'east': '2-29',
        "north": '3-2'
    },
    '3-2': {
        'east': '3-3',
        'south': '3-1',
        "item": "monster"
    },
    '3-3': {
        'west': '3-2',
        'east': '3-4',
        'south': '3-7',
        'item': 'mythril leggings'
    },
    '3-4': {
        'west': '3-3',
        'east': '3-5',
        'item': 'monster'
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
        'item': 'monster'
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
        "item": "monster"
    },
    '3-10': {
        'east': '3-9',
        "item": "health potion"
    },
    '3-11': {
        'west': '3-9',
        'south': '3-12',
        "item": 'steel sword'
    },
    '3-12': {
      'north': '3-11',
      'item': 'monster'
    },
    '3-13': {
        'south': '3-6',
        'north': '3-14',
    },
    '3-14': {
        'south': '3-13',
        "west": "3-15",
        "item": "monster"
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
        'item': 'monster'
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
        'item': 'monster'
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
        'item': 'monster'
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
        'item': 'monster'

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
        'item': 'health potion'
            }
    },
    '3-31': {
        'east': '3-6',
        'west': '3-25',
        'item': 'monster'
            }
    },
    '3-32': {
        'east': '3-27',
        'west': '3-22',
        'north': '3-33',
        'item': 'health potion'
            }
    },
    '3-33': {
        'south': '3-32',
        'north': '3-34',
        'item': 'monster'
            }
    },
    '3-34': {
        'south': '3-33',
        'west': '3-35',
        'north': '3-36',
        'item': 'monster'
            }
    },
    '3-35': {
        'south': '3-34',
        'west': '3-38',
        'item': 'steel helmet'
            }
    },
    '3-36': {
        'south': '3-34',
        'east': '3-37',
        'item': 'health potion'
            }
    },
    '3-37': {
        'east': '3-38',
        'west': '3-36',
        'item': 'steel boots'
            }
    },
    '3-38': {
        'east': '3-39',
        'west': '3-37',
        'item': 'health potion'
            }
    },
    '3-39': {
        'east': '3-40',
        'west': '3-38',
        'item': 'health potion'
            }
    },
    '3-40': {
        'east': '4-1',
        'west': '3-39',
        'item': 'monster'
            }
}

# Mapping for reverse directions
reverse_direction = {"north": "south", "south": "north", "east": "west", "west": "east"}

def connect_rooms(rooms_dict):
    # Iterate over each room and its connections
    for room_id, data in rooms_dict.items():
        for direction, target in data.items():
            # Process only valid directional keys
            if direction in reverse_direction:
                # Check if the target room exists
                if target in rooms_dict:
                    rev_dir = reverse_direction[direction]
                    # Add the reverse connection if it's not already set
                    if rev_dir not in rooms_dict[target]:
                        rooms_dict[target][rev_dir] = room_id
    return rooms_dict

# Update rooms dictionary with reverse connections
rooms = connect_rooms(rooms)

# Print out updated rooms for verification
print(rooms)
