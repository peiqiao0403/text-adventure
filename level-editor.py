rooms = {
    '1-1': {
        "east": '1-2',
        "item": "health potion"
    },
    '1-2': {
        'north': '1-3',
        'west': '1-1',
        "monster": "normal"
    },
    '1-3': {
        'west': '1-4',
        'south': '1-2',
        'item': 'wooden sword'
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
        'monster': "normal"
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
        "item": "key fragment"
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
        'monster': "boss"
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
        'monster': "vampire"
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
      'monster': 'normal'
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
        'monster': 'boss'
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
        'item': 'iron leggings'
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
        'item': 'health potion'
            
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
        'monster': 'boss'
            }
        },
    '3-1': {
        'east': '3-39',
        "west": '4-2'
    },
    '3-2': {
        'east': '4-1',
        'north': '4-3',
        'item': 'health potion'
    },
    '3-3': {
        'west': '4-5',
        'north': '4-4',
        'south': '4-2',
        'item': 'mana potion'
    },
    '3-4': {
        'south': '4-3',
        'east': '4-5',
        'monster': 'normal'
    },
    '3-5': {
        'west': '4-4',
        'north': '4-6',
        'east': '4-7'
    },
    '3-6': {
        'west': '4-47',
        'south': '4-5',
        'east': '4-8',
        'north': '4-13',
        "item": "health potion"
    },
    '3-7': {
        'east': '3-10',
        'west': '3-8',
        'south': '3-16',
        'north': '4-5',
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
        'item': 'health potion'
            
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
        'monster': 'normal'
            
    },
    '3-39': {
        'east': '3-40',
        'west': '3-38',
        'item': 'health potion'
            
    },
    '3-40': {
        'east': '4-1',
        'west': '3-39',
        'monster': 'boss'
            
    },
    '4-1': {
        'east': '3-40',
        "west": '4-2'
        
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
        'monster': 'boss'
        
    },
    '4-21': {
        'north': '4-21',
        'south': '4-22',
        'monster': 'normal'
        
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
            }
           
    },
    '4-41': {
        'east': '4-40',
        'west': '4-42',
        'item': 'mana potion'
            }
               
    },
    '4-42': {
        'east': '4-41',
        'north': '4-44',
        'west': '4-43',
        'item': 'mana potion'
            }
    },
    '4-43': {
        'east': '4-42',
        'item': 'health potion'
            }
               
    },
    '4-44': {
        'east': '4-45',
        'west': '4-43',
        'monster': 'normal'
            }

    },
    '4-45': {
        'south': '4-46',
        'west': '4-44'
            }

    },
    '4-46': {
        'east': '4-47',
        'north': '4-45'
            }

    },
    '4-47': {
        'east': '4-48',
        'north': '4-46',
        'south': '4-49'
            }

    },
    '4-48': {
        'west': '4-48',
        'monster': 'normal'
            }

    },
    '4-49': {
        'north': '4-47',
        'south': '4-50',
        'item': 'health potion'
            }

    },
    '4-50': {
        'north': '4-49',
        'south': '5-1',
        'monster': 'boss'
            }
            
    },
    '5-1': {
        'east': '4-50',
        "north": '5-2'
        
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
        'monster': 'boss'
        
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
        'monster': 'boss'
        #print('wow you really went here and now you have to backtrack fucker.')
           
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
        'monster': 'boss'
            }
           
    },
    '5-41': {
        'east': '5-40',
        'west': '5-42',
        'item': 'mana potion'
            }
               
    },
    '5-42': {
        'east': '4-41',
        'west': '4-43',
        'item': 'mana potion'
            }
    },
    '5-43': {
        'east': '4-42',
        'north': '5-44',
        'item': 'health potion'
            }
               
    },
    '5-44': {
        'east': '5-45',
        'west': '5-43',
        'monster': 'normal'
            }

    },
    '5-45': {
        'south': '5-46',
        'west': '5-44',
        'monster': 'boss'
            }

    },
    '5-46': {
        'east': '5-47',
        'north': '5-45'
            }

    },
    '5-47': {
        'east': '5-48',
        'north': '5-46',
        'monster': 'normal'
            }

    },
    '5-48': {
        'west': '5-47',
        'south': '5-49',
        'monster': 'normal'
            }

    },
    '5-49': {
        'north': '4-48',
        'south': '4-50',
        'item': 'health potion'
            }

    },
    '5-50': {
        'north': '5-49',
        'south': '5-51',
        'monster': 'boss'
            }

    },
    '5-51': {
        'north': '5-50',
        'east': '5-52',
        'monster': 'normal'
            }

    },
    '5-52': {
        'west': '5-51',
        'east': '5-53',
        'north': '5-59',
        'monster': 'normal'
            }

    },
    '5-53': {
        'west': '5-52',
        'south': '5-54',
        'item': 'health potion'
            }

    },
    '5-54': {
        'north': '5-53',
        'west': '5-55',
        'item': 'health potion'
            }

    },
    '5-55': {
        'east': '5-54',
        'west': '5-56',
        'monster': 'boss'
            }

    },
    '5-56': {
        'east': '5-55',
        'west': '5-57',
        'monster': 'normal'
            }

    },
    '5-57': {
        'east': '5-56',
        'west': '5-58',
        'item': 'health potion'
            }

    },
    '5-58': {
        'west': '5-57',
        'item': 'health potion'
            }

    },
    '5-59': {
        'north': '5-52',
        'west': '5-60',
        'item': 'health potion'
            }

    },
    '5-60': {
        'east': '5-59',
        'monster': 'boss'
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
