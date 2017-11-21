import pyglet, configparser, os, glooey, random, sys, pygame
from pyglet.window import key, mouse
from fight import fightOutcome
from playsound import playsound
objects = configparser.ConfigParser()
objects.read('assets/objects.ini')
pyglet.font.add_file('assets/font/xkcd-Regular.ttf') #If we include the font in the build, change this line to: "pyglet.resource.add_font('xkcdRegular.ttf')"


#source = pyglet.media.load('animations/xkcdattack_1.mp4') #There's a chance it does support MP4, but we're gonna need FFMPEG
#player = pyglet.media.Player()
window = pyglet.window.Window(1280, 960, "Bull in a Gun Fight", True)
window.set_minimum_size(960, 720)
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

pygame.mixer.pre_init(44100, 16, 2, 4096) # setup mixer to avoid sound lag
pygame.mixer.init()
pygame.mixer.set_num_channels(4) # set a large number of channels so all the game sounds will play WITHOUT stopping another


step = 0
r = 0
pressedLast = ''
events = [0] * 100
inLoop = False
collect_global_mouse_input = False

try:
    if sys.argv[1] == '1v1':
        modeEndurance = False
        mode1v1 = True
    elif sys.argv[1] == 'endurance':
        modeEndurance = True
        mode1v1 = False
    else:
        modeEndurance = False
        mode1v1 = True
except:
    modeEndurance = False
    mode1v1 = True

class MyLabel(glooey.Label):
    custom_font_name = 'xkcd'
    custom_color = '#babdb6'
    custom_font_size = 32
    custom_alignment = 'left'

class ButtonLabel(glooey.Label):
    custom_font_name = 'xkcd'
    custom_color = '#babdb6'
    custom_font_size = 20
    custom_alignment = 'center'

class PromptBox(glooey.VBox):
    custom_alignment = 'top'
    #custom_top_padding = 150
    custom_padding = 25
    def __init__(self):
        super().__init__()
        self.set_default_cell_size(0)

class FightZone(glooey.HBox):
    custom_alignment = 'center'
    custom_padding = 100

    def __init__(self):
        super().__init__()
        self.set_default_cell_size(0)

class WeaponButton(glooey.Button):
    Label = ButtonLabel
    custom_alignment = 'fill'
    
    class Base(glooey.Background):
        custom_color = '#204a87'

    class Over(glooey.Background):
        custom_color = '#3465a4'

    class Down(glooey.Background):
        custom_color = '#729fcff'

    def __init__(self, text, response):
        super().__init__(text)
        self.response = response

    def on_click(self, widget):
        global step
        global pressedLast
        pressedLast = self.response
        step += 1

class ImageButton(glooey.Button):
    Label = ButtonLabel
    custom_alignment = 'fill'

    class Base(glooey.Background):
        custom_color = '#204a87'

    class Over(glooey.Background):
        custom_color = '#204a87'

    class Down(glooey.Background):
        custom_color = '#204a87'

    def __init__(self, text, response):
        super().__init__(text)
        self.response = response

    def on_click(self, widget):
        global step
        global pressedLast
        pressedLast = self.response
        step += 1

class MyImage(glooey.Image):
    custom_image = None
    custom_alignment = 'center'
'''
    def __init__(self, image=None, sprite=None, texture=None):
        super().__init__()        
        self._image = image or self.custom_image
        self._sprite = sprite
        self._sprite._texture = texture

    def do_claim(self):
        if self._sprite is not None:
            return self._sprite.width, self._sprite.height
        else:
            return 0, 0

    def do_regroup(self):
        if self._sprite is not None:
            self._sprite.group = self.group

    def do_draw(self):
        if self._sprite is None:
            print('No sprite wtf')
            self.do_undraw()
            return
        
        self._sprite.image = self.image

        self._sprite.x = self.rect.left
        self._sprite.y = self.rect.bottom
        self._sprite.draw()
        print("X: {}".format(self._sprite.x))
        print("Y: {}".format(self._sprite.y))
        print("Scale: {}".format(self._sprite.scale))
        print("Opacity: {}".format(self._sprite.opacity))

    def do_undraw(self):
        if self._sprite is not None:
            self._sprite.delete()
            self._sprite = None

    def get_image(self):
        return None

    def set_image(self, new_image):
        pass

    def del_image(self):
        pass

    def get_appearance(self):
        return None

    def set_appearance(self, *, sprite=None):
        pass

    @property
    def is_empty(self):
        return self._sprite is None
'''

def play_music():
    try:
        if modeEndurance:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('assets/music/dbgf01.ogg')
            pygame.mixer.music.set_volume(0.75)
            pygame.mixer.music.play(-1) # the music will loop endlessly
            #playsound('assets/music/dbgf01.wav', False)
        elif mode1v1:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('assets/music/dbgf02.ogg')
            pygame.mixer.music.set_volume(0.75)
            pygame.mixer.music.play(-1) # the music will loop endlessly
            #playsound('assets/music/dbgf02.wav', False)
        else:
            print('There should be no possible way that you\'ve gotten here.')
    except Exception as e:
        print("\nEverything is lava: media isn't working.\nYou probably need to install some missing dependencies.\nMore information on this should be below.\n{}".format(e))


class TempBox(glooey.Placeholder):
    custom_alignment = 'center'
    custom_padding = 10

@window.event
def on_draw():
    global label, label2
    if modeEndurance:
        modeEnduranceRound()
    elif mode1v1:
        mode1v1Round()
    window.clear()
    gui.on_draw()

#@window.event #probably better to sacrifice keyboard input in favour of it not crashing when anything is pressed?
#def on_key_press(symbol, modifiers): #I can probably debug this and fix it, but for the time being, yeah, I agree
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
        #print("The left mouse button was pressed.")
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

def getObjectMostStylish(objs):
    mostStyle = 0
    for obj in objs:
        if int(objects[obj]['style']) > mostStyle:
            mostStyle = int(objects[obj]['style'])
            mostStylish = obj
    return mostStylish

def runFight(p1, p2, p1s, p2s):
    o = objects[p1]
    obj1 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'image':o['Image'], 'state':p1s}
    o = objects[p2]
    obj2 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'image':o['Image'], 'state':p2s}
    out = []
    
    if obj1['state'] == 'offense' and obj2['state'] == 'defense':
        out.append("The {0} attacks the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defense' and obj2['state'] == 'offense':
        out.append("The {0} is attacked by the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'offense' and obj2['state'] == 'offense':
        out.append("The {0} and {1} fight!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defense' and obj2['state'] == 'defense':
        out.append("The {0} and {1} defend the hell out of each other!".format(obj1['name'], obj2['name']))
    winner = fightOutcome(obj1, obj2)
    out.append("The {} wins!".format(winner['name']))
    out.append("And the moral of that story is:")
    if winner == obj1:
        out.append(obj2['textLose'].format(obj1['textWin']))
        out.append(p1)
    elif winner == obj2:
        out.append(obj1['textLose'].format(obj2['textWin']))
        out.append(p2)
    out.append(obj1['image'])
    out.append(obj2['image'])
    return out

class ChoiceGrid(glooey.Grid):
    custom_alignment = 'fill'
    custom_padding = 10
    custom_height_hint = 200

def drawWeaponGrid(rows, columns, objs):
    x = 0
    grid = ChoiceGrid()
    box = glooey.VBox() #The grid had to be put in a box, because the grid wouldn't stop aligning itself to the left of the screen
    box.alignment = 'fill bottom'
    box.add(grid)
    for i in range(rows):
        for j in range(columns):
            grid.add(i, j, WeaponButton(objects[objs[x]]['name'], objs[x]))
            x += 1
    gui.add(box)

def drawADGrid(rows, columns):
    grid = ChoiceGrid()
    box = glooey.VBox() #The grid had to be put in a box, because the grid wouldn't stop aligning itself to the left of the screen
    box.alignment = 'fill bottom'
    box.add(grid)
    grid.add(1, 0, WeaponButton("Offensively", 'offense'))
    grid.add(1, 1, WeaponButton("Defensively", 'defense'))
    gui.add(box)

def getFightImage(imagePath):
    if imagePath == 'None':
        weaponImage = pyglet.image.load('assets/images/objects/Resized/kittenshark_1.png')
    else:
        weaponImage = pyglet.image.load(imagePath)
    return weaponImage


def mode1v1Round():
    global events, step, collect_global_mouse_input, label, label2
    if (events[step]):
        return
    events[step] = True
    gui.clear()
    gui.add(vbox)
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
        global obj1
        obj1 = pressedLast
        label.text = "Player 1, how would you like to use your {}?".format(objects[obj1]['name'])
        drawADGrid(1, 2)
    elif step == 3:
        global state1
        state1 = pressedLast
        collect_global_mouse_input = True
        label.text = "Player 1, look away."
        label2.text = "Player 2, click anywhere to continue."
    elif step == 4:
        collect_global_mouse_input = False
        label.text = "Player 2, what do you want to bring?"
        label2.text = ""
        drawWeaponGrid(2, 4, objs)
    elif step == 5:
        global obj2
        obj2 = pressedLast
        label.text = "Player 2, how would you like to use your {}?".format(objects[obj2]['name'])
        drawADGrid(1, 2)
    elif step == 6: #Pre-Fight
        global state2
        global outputFight
        state2 = pressedLast
        collect_global_mouse_input = True
        label.text = "Both players can look."
        label2.text = "The fight is about to begin."
        outputFight = runFight(obj1, obj2, state1, state2)
    elif step == 7: #Fight
        label.text = outputFight[0]
        label2.text = ""
        fightScene = FightZone()
        img = MyImage(getFightImage(outputFight[5]))
        img2 = MyImage(getFightImage(outputFight[6]))
        fightScene.add(img)
        fightScene.add(img2)
        gui.add(fightScene)
    elif step == 8: #Outcome
        fightScene = FightZone()
        img = MyImage(getFightImage(outputFight[5]))
        img2 = MyImage(getFightImage(outputFight[6]))
        fightScene.add(img)
        fightScene.add(img2)
        gui.add(fightScene)
        label2.text = outputFight[1]
    elif step == 9: #Conclusion
        label.text = outputFight[2]
        label2.text = outputFight[3]
    elif step == 10:#Prompt for Replay
        label.text = "Click anywhere to play again."
        label2.text = ""
    elif step == 11:#Reset values
        step = 0
        window.clear()
        gui.clear()
        events = [0] * 100

def modeEnduranceRound():
    global step
    global r
    global collect_global_mouse_input
    global events
    if (events[step]):
        return
    events[step] = True
    if step == 0:
        collect_global_mouse_input = True
        label.text = "Round {}".format(r + 1)
        label2.text = "Click anywhere to begin."
    elif step == 1:
        global objs
        collect_global_mouse_input = False
        label.text = "What do you want to bring to the fight?"
        label2.text = ""
        objs = getObjectsRandomId(8)
        drawWeaponGrid(2, 4, objs)
    elif step == 2:
        global obj1
        obj1 = pressedLast
        label.text = "How would you like to use your {}?".format(objects[obj1]['name'])
        drawADGrid(1, 2)
    elif step == 3:
        global state1
        global state2
        global outputFight
        state1 = pressedLast
        if random.randint(1,10) == 1:
            obj2 = random.choice(objs)
        else:
            obj2 = getObjectMostStylish(objs)
        state2 = random.choice(['offense', 'defense'])
        gui.clear()
        collect_global_mouse_input = True
        label.text = "The CPU brought {}.".format(objects[obj2]['name'])
        label2.text = "Click to begin the fight."
        outputFight = runFight(obj1, obj2, state1, state2)
    elif step == 4:
        label.text = outputFight[0]
        label2.text = ""
    elif step == 5:
        label2.text = outputFight[1]
    elif step == 6:
        label.text = outputFight[2]
        label2.text = outputFight[3]
    elif step == 7:
        if outputFight[4] == obj1:
            modeEnduranceRun(False)
        else:
            modeEnduranceRun(True)
        events = [0] * 100

def modeEnduranceRun(loss = False):
    global r
    global modeEndurance
    global step
    if loss:
        label.text = "You lose!"
        label2.text = "You survived {} rounds.".format(r + 1)
        modeEndurance = False
    else:
        r += 1
        modeEndurance = True
        step = 0
        #window.clear()
        modeEnduranceRound()

label = MyLabel("Also arbitrary 1", line_wrap = 900)
label2 = MyLabel("Also arbitrary", line_wrap = 900)
vbox = PromptBox()
vbox.add(label)
vbox.add(label2)

play_music()

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
