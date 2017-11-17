import configparser
from fight import fightOutcome

objects = configparser.ConfigParser()
objects.read('objects.ini')

p1 = 'gun'
p2 = 'knife'

def runFight(p1, p2):
    o = objects[p1]
    obj1 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':'offense'}
    o = objects[p2]
    obj2 = {'name':o['Name'], 'atk':int(o['Atk']), 'def':int(o['Def']), 'style':int(o['Style']), 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':'defense'}
    
    if obj1['state'] == 'offense' and obj2['state'] == 'defense':
        print("The {0} attacks the {1}!".format(obj1['name'], obj2['name']))
    elif obj1[state] == 'defense' and obj2[state] == 'offense':
        print("The {0} is attacked by the {1}!".format(obj1['name'], obj2['name']))
    elif obj1[state] == 'offense' and obj2[state] == 'offense':
        print("The {0} and {1} fight!".format(obj1['name'], obj2['name']))
    elif obj1[state] == 'defence' and obj2[state] == 'defence':
        print("The {0} and {1} defend the hell out of each other!".format(obj1['name'], obj2['name']))
    winner = fightOutcome(obj1, obj2)
    print("The {} wins!".format(winner['name']))
    print("And the moral of that story is:")
    if winner == obj1:
        print(obj2['textLose'].format(obj1['textWin']))
    elif winner == obj2:
        print(obj1['textLose'].format(obj2['textWin']))

runFight(p1, p2)
