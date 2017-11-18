import configparser, random, os

OBJECTSFILE = 'assets/objects.ini'

def fightOutcome(obj1, obj2):
    if obj1['state'] == 'offense' and obj2['state'] == 'defense':
        if obj1['atk'] == obj2['def']:
            if obj1['style'] > obj2['style']: #The style for each object should be a unique number out of 100 so that there can never be a tie.
                return obj1
            else:
                return obj2
        elif obj1['atk'] > obj2['def']:
            return obj1
        else:
            return obj2
    elif obj1['state'] == 'defense' and obj2['state'] == 'offense':
        if obj2['atk'] == obj1['def']:
            if obj2['style'] > obj1['style']:
                return obj2
            else:
                return obj1
        elif obj2['atk'] > obj1['def']:
            return obj2
        else:
            return obj1
    elif obj1['state'] == 'offense' and obj2['state'] == 'offense':
        if obj1['atk'] == obj2['atk']:
            if obj1['style'] > obj2['style']:
                return obj1
            else:
                return obj2
        elif obj1['atk'] > obj2['atk']:
            return obj1
        else:
            return obj2
    elif obj1['state'] == 'defense' and obj2['state'] == 'defense':
        if obj1['style'] > obj2['style']:
            return obj1
        else:
            return obj2
    print("Everything is lava: No outcome.")

def getObjectsRandom(number):
    objects = configparser.ConfigParser()
    objects.read(OBJECTSFILE)
    
    objectsChosen = []
    for i in range(number):
        obj = random.choice(list(objects.items()))
        while obj[1] in objectsChosen:
            obj = random.choice(list(objects.items()))
        objectsChosen.append(obj[1])
    return objectsChosen

def askObjectsSelection(objects):
    for num, obj in enumerate(objects):
        #print(obj)
        print("{0}. {1}".format(num + 1, obj['name']))
    try:
        objSelect = input("Which object would you like to select? ")
        return objects[int(objSelect) - 1]
    except Exception as ex:
        print("Everything is lava: {}".format(ex))
        return askObjectsSelection(objects)

def getObjectMostStylish(objects):
    mostStyle = 0
    for obj in objects:
        #print(obj)
        if int(obj['style']) > mostStyle:
            #print(obj)
            mostStyle = int(obj['style'])
            mostStylish = obj
    return mostStylish

def getObjectsPlayerAndCPU():
    objs = getObjectsRandom(8)
    obj1 = askObjectsSelection(objs)
    if random.randint(1,10) == 1:
        obj2 = random.choice(objs)
    else:
        obj2 = getObjectMostStylish(objs)
    return (obj1, obj2)
    
def getObjectsPlayerAndPlayer():
    objs = getObjectsRandom(8)
    print("Player 1:")
    obj1 = askObjectsSelection(objs)
    os.system('clear')
    print("Player 2:")
    obj2 = askObjectsSelection(objs)
    return (obj1, obj2)

def demoRunFight(obj1, obj2, p1s, p2s):
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
        return True
    elif winner == obj2:
        print(obj1['textlose'].format(obj2['textwin']))
        return False

def modeEnduranceRun():
    loss = False
    r = 1
    while not loss:
        print("\n== ROUND {} ==\n".format(r))
        objs = getObjectsPlayerAndCPU()
        p1s = input("Do you want to play offensively or defensively? ")
        if p1s[0] == 'o':
            p1s = 'offense'
        else:
            p1s = 'defense'
        p2s = random.choice(['offense', 'defense'])
        winner = demoRunFight(objs[0], objs[1], p1s, p2s)
        if not winner:
            loss = True
        r += 1
    print("oh no, you lost")
    print("you did survive {} round(s), though".format(r - 1))
    return r

def mode1v1Run():
    while True:
        print()
        objs = getObjectsPlayerAndPlayer()
        os.system('clear')
        p1s = input("Does Player 1 want to play offensively or defensively? ")
        if p1s[0] == 'o':
            p1s = 'offense'
        else:
            p1s = 'defense'
        os.system('clear')
        p2s = input("Does Player 2 want to play offensively or defensively? ")
        if p2s[0] == 'o':
            p2s = 'offense'
        else:
            p2s = 'defense'
        demoRunFight(objs[0], objs[1], p1s, p2s)
        print()
