current_area = None
inventory = []

class Area():
  def __init__(self, opts):
    self.name = opts['name']
    self.desc = opts['desc']
    self.objs = opts['objs']

  def enter(self):
    global current_area

    print(self.name + '\n')
    print('-' * len(self.name))
    print('\n' + self.desc + '\n')
    current_area = self

  def find(self, thing):
    # find an object with 'thing' as its name
    for i in self.objs:
      obj = self.objs[i]
      if thing in obj.names:
        return obj

    return None

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
  
def floorboard_up():
  print('You lift up the floorboard, and there is a crowbar.')
  current_area.desc = 'In this small basement is a door faintly lit by a hanging light. A floorboard has been forced open, and there is a crowbar below it.'
  
  current_area.objs['crowbar'] = Object({
    'names': [ 'crowbar', 'bar' ],
    'commands': [
      Command([ 'pick up', 'take' ], crowbar_taken)
    ]
  })
  
def crowbar_taken():
  print('You pick up the crowbar.')
  del current_area.objs['crowbar']
  current_area.desc = 'In this small basement is a door faintly lit by a hanging light. A floorboard has been forced open.'

  inventory.append('a crowbar')

areas = {
  'basement': Area({
    'name': "Basement",
    'desc': "In this small basement is a door faintly lit by a hanging light. A floorboard looks loose, clearly it needs some attention.",
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
          Command([ 'lift up', 'open' ], floorboard_up)
        ]
      })
    }
  }),
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

