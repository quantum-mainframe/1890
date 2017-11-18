import pyglet, configparser, os, glooey
from pyglet.window import key, mouse
from fight import fightOutcome

objects = configparser.ConfigParser()
objects.read('assets/objects.ini')
pyglet.font.add_file('assets/font/xkcd-Regular.ttf') #If we include the font in the build, change this line to: "pyglet.resource.add_font('xkcdRegular.ttf')"
#source = pyglet.media.load('animations/xkcdattack_1.mp4') #There's a chance it does support MP4, but we're gonna need FFMPEG
#player = pyglet.media.Player()
window = pyglet.window.Window()
batch = pyglet.graphics.Batch()
group = pyglet.graphics.Group()
gui = glooey.Gui(window, batch, group)
game_loop = pyglet.app.EventLoop()
step = 0


class MyLabel(glooey.Label):
    custom_color = '#babdb6'
    custom_font_size = 10
    custom_alignment = 'center'

# If we want another kind of text, for example a bigger font for section
# titles, we just have to derive another class:

class MyTitle(glooey.Label):
    custom_color = '#eeeeec'
    custom_font_size = 12
    custom_alignment = 'center'
    custom_bold = True

class MyButton(glooey.Button):
    Label = MyLabel
    custom_alignment = 'fill bottom'

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
        print(self.response)

class MyBox(glooey.Placeholder):
    custom_alignment = 'center'
    #custom_padding = 10

@window.event
def on_draw():
    gameLoopIdle()
    window.clear()
    gui.on_draw()
    label.draw()

@window.event
def on_key_press(symbol, modifiers):
    global step
    if symbol == key.A:
        print('The "A" key was pressed.')
    elif symbol == key.LEFT:
        print('The left arrow key was pressed.')
    elif symbol == key.ENTER:
        print('The enter key was pressed.')
    elif symbol == key.TAB:
        step = 0
        window.clear()

@window.event
def on_mouse_press(x, y, button, modifiers):
    global step
    if button == mouse.LEFT:
        print('The left mouse button was pressed.')
    step += 1

def runFight(p1, p2, p1s, p2s):
    o = objects[p1]
    obj1 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':p1s}
    o = objects[p2]
    obj2 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':p2s}
    
    if obj1['state'] == 'offense' and obj2['state'] == 'defense':
        print("The {0} attacks the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defense' and obj2['state'] == 'offense':
        print("The {0} is attacked by the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'offense' and obj2['state'] == 'offense':
        print("The {0} and {1} fight!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defence' and obj2['state'] == 'defence':
        print("The {0} and {1} defend the hell out of each other!".format(obj1['name'], obj2['name']))
    winner = fightOutcome(obj1, obj2)
    print("The {} wins!".format(winner['name']))
    print("And the moral of that story is:")
    if winner == obj1:
        print(obj2['textLose'].format(obj1['textWin']))
    elif winner == obj2:
        print(obj1['textLose'].format(obj2['textWin']))

def gameLoopIdle():
    if step == 0:
        label.text = 'Enter the id of the object player 1 wants to use: '
    elif step == 1:
        label.text = 'Does player 1 want to play offensively or defensively? '
    elif step == 2:
        label.text = 'Enter the id of the object player 2 wants to use: '
    elif step == 3:
        label.text = 'Does player 2 want to play offensively or defensively? '
    elif step == 4:
        label.text = 'OK. Stop clicking now.'
        #player.queue(source)
        #player.play()
    elif step == 10:
        label.text = 'Please...'
    


label = pyglet.text.Label('This is a truly arbitrary string',
                          font_name='xkcd',
                          font_size=12,
                          x=window.width//2, y=window.height//1,
                          anchor_x='center', anchor_y='top')


grid = glooey.Grid()
for i in range(2):
    for j in range(4):
        grid.add(i, j, MyBox(100,100))

grid.custom_alignment = 'bottom'
gui.add(grid)

label.draw()

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
