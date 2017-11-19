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
