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
window.set_minimum_size(1152, 648)

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
roundsWon = 0
pressedLast = ''
events = [0] * 100
inLoop = False
collect_global_mouse_input = False
win = False         #Quick Hack for preserving the consistency of the GUI process whilst achieving variable end of round prompts
modeSelect = True
choosingMode = False
modeEndurance = False
mode1v1 = False

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

def play_music(MainMenu = True):
    global modeEndurance, mode1v1
    try:
        if MainMenu:
            playTrack1()
        else:
            playTrack2()
    except Exception as e:
        print("\nEverything is lava: media isn't working.\nYou probably need to install some missing dependencies.\nMore information on this should be below.\n{}".format(e))

def playTrack1():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/music/dbgf01.ogg')
    pygame.mixer.music.set_volume(0.75)
    pygame.mixer.music.play(-1) # the music will loop endlessly

def playTrack2():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/music/dbgf02.ogg')
    pygame.mixer.music.set_volume(0.75)
    pygame.mixer.music.play(-1) # the music will loop endlessly
    

class TempBox(glooey.Placeholder):
    custom_alignment = 'center'
    custom_padding = 10

@window.event
def on_draw():
    if modeSelect:
        game_mode_select()
    elif modeEndurance:
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

def getFightImage(imagePath):
    if imagePath == 'None':
        weaponImage = pyglet.image.load('assets/images/objects/Resized/kittenshark_1.png')
    else:
        weaponImage = pyglet.image.load('assets/images/objects/Resized/%s'%imagePath)
    return weaponImage

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

class EndOfRoundButton(glooey.Button):
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
        global collect_global_mouse_input, modeEndurance, mode1v1, modeSelect, choosingMode, roundsWon
        collect_global_mouse_input = False
        if self.response == 'Play Again':
            play_again()
        elif self.response == 'Change Game Mode':
            game_mode_select()
            choosingMode = False
            modeSelect = True
            mode1v1 = False
            modeEndurance = False
        elif self.response == '1v1':
            mode1v1 = True
            modeEndurance = False
            modeSelect = False
            playTrack2()
        elif self.response == 'endurance':
            mode1v1 = False
            modeEndurance = True
            modeSelect = False
            roundsWon = 0
            playTrack2()
        else:
            BorkedError()

def drawPlayAgainGrid():
    grid = ChoiceGrid()
    box = glooey.VBox() #The grid had to be put in a box, because the grid wouldn't stop aligning itself to the left of the screen
    box.alignment = 'fill bottom'
    box.add(grid)
    grid.add(1, 0, EndOfRoundButton("Play Again", 'Play Again'))
    grid.add(1, 1, EndOfRoundButton("Change Game Mode", 'Change Game Mode'))
    gui.add(box)

def play_again():
    ResetRound()
    if mode1v1:
        mode1v1Round()
    elif modeEndurance:
        modeEnduranceRound()
    else:
        BorkedError()
    
def drawGameModeGrid():
    grid = ChoiceGrid()
    box = glooey.VBox() #The grid had to be put in a box, because the grid wouldn't stop aligning itself to the left of the screen
    box.alignment = 'fill bottom'
    box.add(grid)
    grid.add(1, 0, EndOfRoundButton("Local 1v1", '1v1'))
    grid.add(1, 1, EndOfRoundButton("Endurance", 'endurance'))
    gui.add(box)

def game_mode_select():
    global choosingMode
    if not choosingMode:
        ResetRound()
        playTrack1()
        gui.clear()
        gui.add(vbox)
        label.text = "Choose a game mode!"
        label2.text = "...or just listen to the music."
        drawGameModeGrid()
        choosingMode = True

def mode1v1Round():
    global events, step, collect_global_mouse_input, label, label2
    if (events[step]):
        return
    events[step] = True
    gui.clear()
    gui.add(vbox)
    if step == 0: #Welcome Screen
        collect_global_mouse_input = True
        label.text = "Player 2, look away."
        label2.text = "Player 1, click anywhere to continue."
    elif step == 1: #Prompt Player 1 for weapon choice
        global objs
        collect_global_mouse_input = False
        label.text = "Player 1, what do you want to bring?"
        label2.text = ""
        objs = getObjectsRandomId(8)
        drawWeaponGrid(2, 4, objs)
    elif step == 2: #Prompt Player 1 for attack/defense
        global obj1
        obj1 = pressedLast
        label.text = "Player 1, how would you like to use your {}?".format(objects[obj1]['name'])
        drawADGrid(1, 2)
    elif step == 3: #Switch Players
        global state1
        state1 = pressedLast
        collect_global_mouse_input = True
        label.text = "Player 1, look away."
        label2.text = "Player 2, click anywhere to continue."
    elif step == 4: #Prompt Player 2 for weapon choice
        collect_global_mouse_input = False
        label.text = "Player 2, what do you want to bring?"
        label2.text = ""
        drawWeaponGrid(2, 4, objs)
    elif step == 5: #Prompt Player 2 for attack/defense
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
        collect_global_mouse_input = False
        label.text = "Play Again?"
        label2.text = ""
        drawPlayAgainGrid()

def modeEnduranceRound():
    global events, step, collect_global_mouse_input, label, label2, roundsWon, win
    if (events[step]):
        return
    events[step] = True
    gui.clear()
    gui.add(vbox)
    if step == 0: #Welcome Screen
        collect_global_mouse_input = True
        win = False
        label.text = "Round {}".format(roundsWon + 1)
        label2.text = "Click anywhere to begin."
    elif step == 1: #Prompt for weapon choice
        global objs
        collect_global_mouse_input = False
        label.text = "What do you want to bring to the fight?"
        label2.text = ""
        objs = getObjectsRandomId(8)
        drawWeaponGrid(2, 4, objs)
    elif step == 2: #Prompt for attack/defense
        global obj1
        obj1 = pressedLast
        label.text = "How would you like to use your {}?".format(objects[obj1]['name'])
        drawADGrid(1, 2)
    elif step == 3: #Choice results
        global state1
        global state2
        global outputFight
        state1 = pressedLast
        if random.randint(1,10) == 1:
            obj2 = random.choice(objs)
        else:
            obj2 = getObjectMostStylish(objs)
        state2 = random.choice(['offense', 'defense'])
        collect_global_mouse_input = True
        label.text = "The CPU brought {}.".format(objects[obj2]['name'])
        label2.text = "Click to begin the fight."
        outputFight = runFight(obj1, obj2, state1, state2)
    elif step == 4: #Fight
        label.text = outputFight[0]
        label2.text = ""
        fightScene = FightZone()
        img = MyImage(getFightImage(outputFight[5]))
        img2 = MyImage(getFightImage(outputFight[6]))
        fightScene.add(img)
        fightScene.add(img2)
        gui.add(fightScene)
    elif step == 5: #Outcome
        fightScene = FightZone()
        img = MyImage(getFightImage(outputFight[5]))
        img2 = MyImage(getFightImage(outputFight[6]))
        fightScene.add(img)
        fightScene.add(img2)
        gui.add(fightScene)
        label2.text = outputFight[1]
    elif step == 6: #Conclusion
        label.text = outputFight[2]
        label2.text = outputFight[3]
    elif step == 7: #Results
        collect_global_mouse_input = True
        if outputFight[4] == obj1: #If the human player won this round
            win = True
            label.text = "You won this round!"
            label2.text = "Click to continue."
            roundsWon += 1
        else:
            win = False
            label.text = "You lost!"
            label2.text = "You survived {} rounds.".format(roundsWon + 1)
            roundsWon = 0
    elif step == 8: #Restart Round / Prompt for Play Again or Change Game Mode
        collect_global_mouse_input = False
        if win:
            ResetRound()
            modeEnduranceRound()
        else:
            label.text = "Play Again?"
            label2.text = ""
            drawPlayAgainGrid()

def ResetRound():
    global step, events
    step = 0
    window.clear()
    gui.clear()
    events = [0] * 100

def BorkedError():
    gui.clear()
    label.text = "Something is borked. Tell the developers."
    label2.text = "Please."

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
