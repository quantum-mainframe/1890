import pyglet, configparser, os, glooey, random
from pyglet.window import key, mouse
from fight import fightOutcome

objects = configparser.ConfigParser()
objects.read('assets/objects.ini')
pyglet.font.add_file('assets/font/xkcd-Regular.ttf') #If we include the font in the build, change this line to: "pyglet.resource.add_font('xkcdRegular.ttf')"
#source = pyglet.media.load('animations/xkcdattack_1.mp4') #There's a chance it does support MP4, but we're gonna need FFMPEG
#player = pyglet.media.Player()
window = pyglet.window.Window(1280, 960, "Bull in a Gun Fight")
icon16 = pyglet.image.load('assets/images/icon16.png')
icon32 = pyglet.image.load('assets/images/icon32.png')
icon48 = pyglet.image.load('assets/images/icon48.png')
icon64 = pyglet.image.load('assets/images/icon64.png')
icon72 = pyglet.image.load('assets/images/icon72.png')
icon128 = pyglet.image.load('assets/images/icon128.png')
window.set_icon(icon16, icon32, icon48, icon64, icon72, icon128)
batch = pyglet.graphics.Batch()
group = pyglet.graphics.Group()
gui = glooey.Gui(window, batch, group)
step = 0
pressedLast = ''
events = [0] * 100
inLoop = False
collect_global_mouse_input = False


class MyLabel(glooey.Label):
    custom_font_name = 'xkcd'
    custom_color = '#babdb6'
    custom_font_size = 20
    custom_alignment = 'center'

# If we want another kind of text, for example a bigger font for section
# titles, we just have to derive another class:

class MyTitle(glooey.Label):
    custom_color = '#eeeeec'
    custom_font_size = 12
    custom_alignment = 'center'
    custom_bold = True

class WeaponButton(glooey.Button):
    Label = MyLabel
    custom_alignment = 'fill'

    # More often you'd specify images for the different rollover states, but
    # we're just using colors here so you won't have to download any files
    # if you want to run this code.

    class Base(glooey.Background):
        custom_color = '#204a87'

    class Over(glooey.Background):
        custom_color = '#3465a4'

    class Down(glooey.Background):
        custom_color = '#729fcff'

    # Beyond just setting class variables in our widget subclasses, we can
    # also implement new functionality.  Here we just print a programmed
    # response when the button is clicked.

    def __init__(self, text, response):
        super().__init__(text)
        self.response = response

    def on_click(self, widget):
        global step
        global pressedLast
        pressedLast = self.response
        step += 1

class TempBox(glooey.Placeholder):
    custom_alignment = 'center'
    custom_padding = 10

class WeaponGrid(glooey.Grid):
    custom_alignment = 'fill bottom'
    custom_padding = 10

@window.event
def on_draw():
    gameLoopIdle()
    window.clear()
    gui.on_draw()
    label.draw()
    label2.draw()

#@window.event #probably better to sacrifice keyboard input in favour of it not crashing when anything is pressed?
#def on_key_press(symbol, modifiers):
#    gui.dispatch_event('on_key_press', symbol, modifiers)
#    global step
#    #if symbol == key.A:
#    #    print("The A key was pressed.")
#    #elif symbol == key.LEFT:
#    #    print("The left arrow key was pressed.")
#    #elif symbol == key.ENTER:
#    #    print("The enter key was pressed.")
#    if symbol == key.TAB:
#        step = 0
#        window.clear()
#    elif symbol == key.SPACE:
#        step += 1

@window.event
def on_mouse_press(x, y, button, modifiers):
    gui.dispatch_event('on_mouse_press', x, y, button,modifiers)
    global step
    if button == mouse.LEFT:
        #print('The left mouse button was pressed.')
        if (collect_global_mouse_input):
            step += 1

def getObjectsRandomId(number):
    objectsChosen = []
    for i in range(number):
        obj = random.choice(tuple(objects))
        while obj in objectsChosen:
            obj = random.choice(tuple(objects))
        objectsChosen.append(obj)
    return objectsChosen

def runFight(p1, p2, p1s, p2s):
    o = objects[p1]
    obj1 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':p1s}
    o = objects[p2]
    obj2 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':p2s}
    
    out = []
    
    if obj1['state'] == 'offense' and obj2['state'] == 'defense':
        out.append("The {0} attacks the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defense' and obj2['state'] == 'offense':
        out.append("The {0} is attacked by the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'offense' and obj2['state'] == 'offense':
        out.append("The {0} and {1} fight!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defence' and obj2['state'] == 'defence':
        out.append("The {0} and {1} defend the hell out of each other!".format(obj1['name'], obj2['name']))
    winner = fightOutcome(obj1, obj2)
    out.append("The {} wins!".format(winner['name']))
    out.append("And the moral of that story is:")
    if winner == obj1:
        out.append(obj2['textLose'].format(obj1['textWin']))
    elif winner == obj2:
        out.append(obj1['textLose'].format(obj2['textWin']))
    return out

def drawWeaponGrid(rows, columns, objs):
    gui.clear()
    x = 0
    grid = WeaponGrid()
    for i in range(rows):
        for j in range(columns):
            grid.add(i, j, WeaponButton(objects[objs[x]]['name'], objects[objs[x]]))
            x += 1
    gui.add(grid)

def drawADGrid(rows, columns):
    gui.clear()
    grid = WeaponGrid()
    grid.add(1, 0, WeaponButton("Offensively", 'offense'))
    grid.add(1, 1, WeaponButton("Defensively", 'defense'))
    gui.add(grid)

def gameLoopIdle():
    if (events[step]):
        return
    events[step] = True
    global collect_global_mouse_input
    if step == 0:
        collect_global_mouse_input = True
        label.text = "Player 2, look away."
        label2.text = "Player 1, click anywhere to continue."
    elif step == 1:
        global objs
        collect_global_mouse_input = False
        label.text = "Player 1, what do you want to bring?"
        label2.text = ""
        objs = getObjectsRandomId(8)
        drawWeaponGrid(2, 4, objs)
    elif step == 2:
        obj1 = pressedLast
        label.text = "Player 1, how would you like to use your {}?".format(obj1['name'])
        drawADGrid(1, 2)
    elif step == 3:
        state1 = pressedLast
        gui.clear()
        collect_global_mouse_input = True
        label.text = "Player 1, look away."
        label2.text = "Player 2, click anywhere to continue."
    elif step == 4:
        collect_global_mouse_input = False
        label.text = "Player 2, what do you want to bring?"
        label2.text = ""
        drawWeaponGrid(2, 4, objs)
    elif step == 5:
        obj2 = pressedLast
        label.text = "Player 2, how would you like to use your {}?".format(pressedLast['name'])
        drawADGrid(1, 2)
    elif step == 6:
        state2 = pressedLast
        gui.clear()
        collect_global_mouse_input = True
        label.text = "OK. Stop clicking now."
        #player.queue(source)
        #player.play()
    elif step == 10:
        label.text = "Please..."

label = pyglet.text.Label("This is a truly arbitrary string",
                          font_name='xkcd',
                          font_size=32,
                          x=window.width/2, y=window.height/2 + 64,
                          anchor_x='center', anchor_y='top')
label2 = pyglet.text.Label("This is also a truly arbitrary string",
                          font_name='xkcd',
                          font_size=32,
                          x=window.width/2, y=window.height/2,
                          anchor_x='center', anchor_y='top')

pyglet.app.run()
'''
while True:
    pyglet.clock.tick()

    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()

'''
'''
p1 = input("Enter the id of the object player 1 wants to use: ")
p1s = input("Does player 1 want to play offensively or defensively? ")
if p1s[0] == 'o':
    p1s = 'offense'
else:
    p1s = 'defense'
os.system('clear')
p2 = input("Enter the id of the object player 2 wants to use: ")
p2s = input("Does player 2 want to play offensively or defensively? ")
if p2s[0] == 'o':
    p2s = 'offense'
else:
    p2s = 'defense'

runFight(p1, p2, p1s, p2s)

input("Press ENTER to continue...")
'''
