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
