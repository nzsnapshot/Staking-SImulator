import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager
import random
import csv
data = []
# Settings combat stats for the players

Att, Str, Def, Hits = 99, 99, 99, 99

def changeStance(stance):
    """Calculates effective att/str/def levels based on stance"""
    # Controlled Stance | Aka Str = +1 to all 3 skills
    # Agressive stance + 3 to respective skill
    flick, lash, deflect = Att+8, Str+8, Def+8

    if stance == 'flick':
        flick, lash, deflect = (Att+3, Str, Def)
    elif stance == 'lash':
        flick, lash, deflect = (Att+1, Str+1, Def+1)
    elif stance == 'deflect':
        flick, lash, deflect = (Att, Str, Def+3)
    else:
        pass
    return(flick, lash, deflect)

def calcMaxRolls(stance):
    """Calculates max rolls for Att/Str/Def"""
    flick, lash, deflect = changeStance(stance)
    attBonus = 90 # Attack bonus for the tent whip
    strBonus = 86 # Str bonus for the tent whip
    defBonus = 0 # Defence bonus for the whip
    lashMax = np.floor(0.5 + lash*(strBonus+64)/640)
    flickMax = flick*(attBonus+64)
    deflectMax = deflect*(defBonus+64)
    return(flickMax, lashMax, deflectMax)


def calcHit(stance):
    flickMax, lashMax, deflectMax = calcMaxRolls(stance)
    if flickMax > deflectMax:
        hitChance = (1 - (deflectMax+2.)/(2*(flickMax+1)))
    else:
        hitChance =  flickMax/(2.*(deflectMax+1))
    roll = np.random.rand(1)[0]

    if roll < hitChance: # Hit Splash!
        dmg = np.random.randint(0,26,size=1)[0]
    else:
        dmg = 0
    return dmg


def writeToCsv(filename, string):
    with open(filename, 'a') as f:
        f.write(string)        


def duel(styles=('flick','flick'),runs=100,info=True):
    """ Run duels """
    P1win,P2win = 0,0 # number of wins
    pid1, pid2 = 0,0
    t1 = 100
    t2 = 100
    x1 = []
    y1 = []
    filename = "data.csv"
    wincsv = "win.csv"

    data = []
    x2 = []
    y2 = []
    counter = 0
    for i in range(runs+1):
        print ('Duel %s/%s' % (str(i),str(runs)))
        P1hp,P2hp = 100, 100 # set health
        pid = np.round(np.random.rand(1)[0])
  
        # if pid:
        #     pid1 +=1
        # else:
        #     pid2 +=1
        while True:
            # calculate player hits
            P1dmg = calcHit(styles[0])
            P2dmg = calcHit(styles[0])	
            if pid: # player 1 wins pid
                # calculate player hp after hit
                P2hp-=P1dmg
                if P2hp <= 0:
                    P1win+=1
                    t1 += 10
                    t2 -= 10
                    counter += 1
                    x1.append(counter)
                    y1.append(t1)
                    x2.append(counter)
                    y2.append(t2)
                    # if info: print ('(P1) hp:%s dmg:%s | (P2) hp:%s dmg%s' % (str(P1hp),str(P1dmg),str(P2hp),str(P2dmg)))
                    print('Player1 Won!')
                    writeToCsv(filename, 'Player1 Won!\n')    
                    writeToCsv(wincsv, '1,0\n')      
                    break
                P1hp -= P2dmg
                if P1hp <= 0:
                    P2win+=1
                    counter += 1
                    t1 -= 10
                    t2 += 10
                    x1.append(counter)
                    y1.append(t1)
                    x2.append(counter)
                    y2.append(t2)
                    # if info: print ('(P1) hp:%s dmg:%s | (P2) hp:%s dmg%s' % (str(P1hp),str(P1dmg),str(P2hp),str(P2dmg)))
                    print('Player2 Won!')
                    writeToCsv(filename, 'Player2 Won!\n')    
                    writeToCsv(wincsv, '0,1\n')      
                    break
            # if info: print ('(P1) hp:%s dmg:%s | (P2) hp:%s dmg:%s' %(str(P1hp),str(P1dmg),str(P2hp),str(P2dmg)))
            else: # player 2 wins pid
            # calculate player hp after hit
                P1hp-=P2dmg
                if P1hp <= 0:
                    P2win+=1
                    t1 -= 10
                    t2 += 10
                    counter += 1
                    x1.append(counter)
                    y1.append(t1)
                    x2.append(counter)
                    y2.append(t2)
                    # if info: print ('(P1) hp:%s dmg:%s | (P2) hp:%s dmg%s' % (str(P1hp),str(P1dmg),str(P2hp),str(P2dmg)))
                    print('Player2 Won!')
                    writeToCsv(filename, 'Player2 Won!\n')    
                    writeToCsv(wincsv, '0,1\n')      
                    break
                P2hp -= P1dmg
                if P2hp <= 0:
                    P1win+=1
                    t1 += 10
                    t2 -= 10
                    counter += 1
                    x1.append(counter)
                    y1.append(t1)
                    x2.append(counter)
                    y2.append(t2)
                    # if info: print ('(P1) hp:%s dmg:%s | (P2) hp:%s dmg%s' % (str(P1hp),str(P1dmg),str(P2hp),str(P2dmg)))
                    print('Player1 Won!')    
                    writeToCsv(wincsv, '1,0\n')
                    writeToCsv(filename, 'Player1 Won!\n')      
                    break
            with open(filename, 'a') as f:
                f.write('(P1) hp:%s dmg:%s | (P2) hp:%s dmg:%s\n' % (str(P1hp),str(P1dmg),str(P2hp),str(P2dmg)))   
            if info: print ('(P1) hp:%s dmg:%s | (P2) hp:%s dmg:%s' %(str(P1hp),str(P1dmg),str(P2hp),str(P2dmg)))


            # offt = '(P1) hp:%s dmg:%s | (P2) hp:%s dmg:%s' %(str(P1hp),str(P1dmg),str(P2hp),str(P2dmg))
        

        runs = runs + 0.0	
    # print(pid1, pid2)
    print(P1win/runs,P2win/runs)

    plt.figure(figsize=(15,5))

    plt.plot(x1, y1)
    plt.xticks(np.arange(min(x1), max(x1)+1, 5.0))

    plt.show()
    plt.figure(figsize=(15,5))

    plt.plot(x2,y2)
    plt.xticks(np.arange(min(x2), max(x2)+1, 5.0))

    plt.show()
    return 	(P1win/runs,P2win/runs)




