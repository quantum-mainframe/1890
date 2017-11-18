import configparser, os, random
from fight import fightOutcome, getObjectsPlayerAndCPU, modeEnduranceRun

objects = configparser.ConfigParser()
objects.read('assets/objects.ini')

def runFight(obj1, obj2, p1s, p2s):
    o = objects.index(p1)
    obj1 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':p1s}
    o = objects.index(p2)
    obj2 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':p2s}
    
    if obj1['state'] == 'offense' and obj2['state'] == 'defense':
        print("The {0} attacks the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defense' and obj2['state'] == 'offense':
        print("The {0} is attacked by the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'offense' and obj2['state'] == 'offense':
        print("The {0} and {1} fight!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defense' and obj2['state'] == 'defense':
        print("The {0} and {1} defend the hell out of each other!".format(obj1['name'], obj2['name']))
    winner = fightOutcome(obj1, obj2)
    print("The {} wins!".format(winner['name']))
    print("And the moral of that story is:")
    if winner == obj1:
        print(obj2['textLose'].format(obj1['textWin']))
    elif winner == obj2:
        print(obj1['textLose'].format(obj2['textWin']))

def runFight2(obj1, obj2, p1s, p2s):
    obj1 = dict(obj1)
    obj2 = dict(obj2)
    obj1['state'] = p1s
    obj2['state'] = p2s
    
    if obj1['state'] == 'offense' and obj2['state'] == 'defense':
        print("The {0} attacks the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defense' and obj2['state'] == 'offense':
        print("The {0} is attacked by the {1}!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'offense' and obj2['state'] == 'offense':
        print("The {0} and {1} fight!".format(obj1['name'], obj2['name']))
    elif obj1['state'] == 'defense' and obj2['state'] == 'defense':
        print("The {0} and {1} defend the hell out of each other!".format(obj1['name'], obj2['name']))
    winner = fightOutcome(obj1, obj2)
    print("The {} wins!".format(winner['name']))
    print("And the moral of that story is:")
    if winner == obj1:
        print(obj2['textlose'].format(obj1['textwin']))
    elif winner == obj2:
        print(obj1['textlose'].format(obj2['textwin']))

def demoRun():
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
    runFight(objects[p1], objects[p2], p1s, p2s)
    input()

def demo2Run():
    objs = getObjectsPlayerAndCPU()
    runFight2(objs[0], objs[1], random.choice(['offense','defense']), random.choice(['offense','defense']))

modeEnduranceRun()
