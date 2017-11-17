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
        if obj1['def'] == obj2['def']:
            if obj1['style'] > obj2['style']:
                return obj1
            else:
                return obj2
        elif obj1['def'] > obj2['def']:
            return obj1
        else:
            return obj2
    print("Everything is lava: No outcome.")
