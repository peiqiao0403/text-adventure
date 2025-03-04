# Preset rooms dictionary with one-way connections
rooms = {
    '1-1': {
        'east': '1-2',
        'west': '1-16'
    },
    '1-2': {
        'north': '1-3',
        'west': '1-1'
    },
    '1-3': {
        'west': '1-4',
        'south': '1-2',
        'item': 'monster'
    },
    '1-4': {
        'east': '1-3',
        'west': '1-15',
        'north': '1-5',
        "item":"armor"
    },
    '1-5': {
        'south': '1-4',
        'west': '1-6'
    },
    '1-6': {
        'west': '1-7',
        'east': '1-5',
        "item":"mana potion"
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
        "item":"key"

    },
    '1-10': {
        'south': '1-11',
        'east': '1-9',
        "item":"sword"
    },
    '1-11': {
        'north': '1-10',
        "item":"armor"
    },
    '1-12': {
        'south': '1-11'
    },
    '1-13': {
        'south': '1-16',
        'north': '1-9',
        "item":"mana potion"
    },
    '1-14': {
        'north': '1-8',
        "item":"armor"
    },
    '1-15': {
        'east': '1-4',
        'north': '1-7',
        "item":"health potion"
    },
    '1-16': {
        'east': '1-1',
        'west': '1-17',
        'north': '1-13',
        'item': 'monster'
    },
    '1-17': {
        'west': '1-18',
        'east': '1-16'
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
