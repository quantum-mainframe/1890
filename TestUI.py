import pyglet, configparser, os, glooey
from pyglet.window import key, mouse
from fight import fightOutcome

objects = configparser.ConfigParser()
objects.read('objects.ini')
pyglet.font.add_file('xkcd-Regular.ttf') #If we include the font in the build, change this line to: "pyglet.resource.add_font('xkcdRegular.ttf')"
#source = pyglet.media.load('animations/xkcdattack_1.mp4') #There's a chance it does support MP4, but we're gonna need FFMPEG
#player = pyglet.media.Player()
window = pyglet.window.Window()
step = 0

@window.event
def on_draw():
    pass

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
    if button == mouse.LEFT:
        print('The left mouse button was pressed.')
    gameLoop()

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

def gameLoop():
    global step
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
    step += 1
    window.clear()
    label.draw()


label = pyglet.text.Label('This is a truly arbitrary string',
                          font_name='xkcd',
                          font_size=12,
                          x=window.width//2, y=window.height//1,
                          anchor_x='center', anchor_y='top')
pyglet.app.run()


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