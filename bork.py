current_area = None
inventory = []

class Area():
  def __init__(self, opts):
    self.name = opts['name']
    self.desc = opts['desc']
    self.objs = opts['objs']
    self.data = opts['data']

  def enter(self):
    global current_area
    current_area = self

    print(self.name + '\n')
    print('-' * len(self.name))
    print('\n' + self.getDescription() + '\n')

  def find(self, thing):
    # find an object with 'thing' as its name
    for i in self.objs:
      obj = self.objs[i]
      if thing in obj.names:
        return obj

    return None
  
  def getDescription(self):
    return self.desc(inventory)

class Object():
  def __init__(self, opts):
    self.names = opts['names']
    self.commands = opts['commands']

  def find_command(self, action):
    for cmd in self.commands:
      if action in cmd.names:
        return cmd

    return None

class Command():
  def __init__(self, names, fn):
    self.names = names
    self.fn = fn

  def do(self):
    self.fn()

def basement_light_off():
  print('You turn off the light.')
  
def read_paper():
  print('Welcome to bork. A text based adventure game, written fully in python')
  
def open_door():
  if current_area.data['door_is_open'] == True:
    print('You go back to the kitchen.')
    return areas['kitchen'].enter()

  if 'a crowbar' in inventory:
    print('You force open the door using the crowbar and go through it and up the stairs.')
    areas['kitchen'].enter()
  else:
    print('You can\'t do that - the door is firmly bolted shut.')
    
def open_study_door():
  if current_area.data['study_door_is_open'] == True:
    print('You go through to the study.')
    return areas['study'].enter()

  if 'a crowbar' in inventory:
    print('You force open the door using the crowbar and go through it.')
    areas['study'].enter()
  else:
    print('You can\'t do that - the door is nailed shut.')    
  
def floorboard_up():
  print('You lift up the floorboard, and there is a crowbar.')

  current_area.objs['crowbar'] = Object({
    'names': [ 'crowbar', 'bar' ],
    'commands': [
      Command([ 'pick up', 'take' ], crowbar_taken)
    ]
  })
  
def to_basement():
  print('You go through the open door and down the stairs.')
  areas['basement'].enter()
  
def to_kitchen():
  print('You go through the door and enter the kitchen')
  areas['kitchen'].enter()

def open_fridge():
  print('You open the fridge, and there is a bottle of water.')
  # TODO: fix below line
  ##current_area.desc = 'You are in a large kitchen, there is an open fridge with a bottle inside, and a dining table with a sandwich on top, there is a locked door and a window which is boarded up.'
  
  current_area.objs['water'] = Object({
    'names': [ 'water', 'bottle' ],
    'commands': [
      Command([ 'pick up', 'take', 'pick up bottle of', 'take bottle of' ], water_taken)
    ]
  })
  
def crowbar_taken():
  print('You pick up the crowbar.')
  del current_area.objs['crowbar']
  #current_area.desc = 'In this small basement is a door faintly lit by a hanging light. A floorboard has been forced open.'

  inventory.append('a crowbar')
  
def water_taken():
  print('You have taken the bottle of water.')
  del current_area.objs['water']
  current_area.desc = 'You are in a large kitchen, there is an empty fridge, and a dining table with a sandwich on top, there is a locked door and a window which is boarded up.'

  inventory.append('a bottle of water')

def basement_desc(inv):
  desc = "In this small basement is a door faintly lit by a hanging light. A floorboard looks loose, clearly it needs some attention."
  if current_area.data['door_is_open'] == True:
    desc = desc + " The door is unlocked; leading upstairs into the kitchen."
  return desc

def kitchen_desc(inv):
  return "You are in a large kitchen, there is a fridge, and a dining table. An open door leads downstairs into the basement, and a locked door next to the fridge."
  
def study_desc(inv):
  return "You are in a small study, there is a pen and a piece of paper on the desk. There is an open door leading through to the kitchen and a locked door."
  

areas = {
  'basement': Area({
    'name': "Basement",
    'desc': basement_desc,
    'data': { 'door_is_open': False },
    'objs': {
      'light': Object({
        'names': [ 'light', 'lamp' ],
        'commands': [
          Command([ 'switch off', 'turn off' ], basement_light_off)
        ]
      }),
      'floorboard': Object({
        'names': [ 'board', 'floorboard' ],
        'commands': [
          Command([ 'lift up', 'open', 'lift' ], floorboard_up)
        ]
      }),
       'door': Object({
        'names': [ 'door'],
        'commands': [
          Command([ 'open' ], open_door)
        ]
      })
    }
  }),
  'kitchen': Area({
    'name': "kitchen",
    'desc': kitchen_desc,
    'data': {},
    'objs': {
       'fridge': Object({
          'names': [ 'fridge', 'refrigerator' ],
          'commands': [
            Command([ 'open' ], open_fridge)
          ]
        }),
        'downstairs': Object({
          'names': [ 'downstairs', 'basement' ],
          'commands': [
            Command([ 'go', 'go to', 'go into', 'go to the', 'enter' ], to_basement)
          ]
        })
      }
    }),
    'Study': Area({
    'name': "study",
    'desc': study_desc,
    'data': {},
    'objs': {
       'paper': Object({
          'names': [ 'paper', 'report' ],
          'commands': [
            Command([ 'read' ], read_paper)
          ]
        }),
        'kitchen': Object({
          'names': [ 'door', 'kitchen' ],
          'commands': [
            Command([ 'go', 'go to', 'go into', 'go to the', 'enter', 'go through' ], to_kitchen)
          ]
        }),
        'study_door': Object({
          'names': [ 'door','studydoor', 'study'],
          'commands': [
            Command([ 'open study','open', 'force open', 'go to', 'go to the' ], open_study_door)
        ]
      })
      }
    })  
}

def look():
  current_area.enter()

def inv():
  if len(inventory) == 0:
   print('You don\'t have anything in your inventory.')
  else:
   print('You have ' + ' and '.join(inventory) + ' in your inventory.')

global_commands = [
  Command([ 'look' ], look),
  Command([ 'inventory', 'holding', 'inv' ], inv)
]

def get_command():
  split = input('>').split()

  if len(split) == 0:
    return
  if len(split) == 1:
    # global command
    for cmd in global_commands:
      if split[0] in cmd.names:
        cmd.do()
        return
    
    print('You can\'t do that.')
    return

  thing = split.pop()
  action = ' '.join(split)

  # find the thing in the current area
  obj = current_area.find(thing)

  if obj == None:
    # cant find it
    print("There is no " + thing + " here.")
    return

  # find the action!
  a = obj.find_command(action)

  if a == None:
    print("You can't do that.")
    return

  # do action
  a.do()


areas['basement'].enter()
while True:
  get_command()
