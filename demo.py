import configparser
from fight import fightOutcome

objects = configparser.ConfigParser()
objects.read('objects.ini')

p1 = 'gun'
p2 = 'knife'

def runFight(p1, p2):
    o = objects[p1]
    obj1 = {'name':o['Name'], 'atk':o['Atk'], 'def':o['Def'], 'style':o['Style'], 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':'offense'}
    o = objects[p1]
    obj2 = {'name':o['Name'], 'atk':o['Atk'], 'def':o['Def'], 'style':o['Style'], 'textLose':o['TextLose'], 'textWin':o['TextWin'], 'state':'defense'}
    print(fightOutcome(obj1, obj2))

runFight(p1, p2)
