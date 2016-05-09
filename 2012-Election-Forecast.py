# Copyright 2016, Chau Pham

import math
import numpy as np, pandas as pd, scipy as sp, seaborn as sns
from matplotlib import pyplot as plt
get_ipython().magic('matplotlib inline')
from polling_data import States
from ec_votes import Electoral_College

def getState(name): 
    data = []

    dempercent = States[name][0][1]
    reppercent = States[name][0][2]
    marginoferror = States[name][0][3]
        
    edge = (50 + (dempercent - reppercent)/2)/100
        
    d = np.random.normal(edge,(marginoferror/2)/100)
        
    data.append(d)
    
    return np.array(data)

def getVotes():
    demvotes = 0
    repvotes = 0
    
    for name in States:
        ecvotes = Electoral_College[name][1]
        votes = getState(name)
    
        if votes > .5:
            demvotes += ecvotes
        else:
            repvotes += ecvotes
  
    return [demvotes, repvotes]

demwin = [getVotes()[0] for i in range(1000)]
repwin = [getVotes()[1] for i in range(1000)]

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()
line1, = ax1.plot(demwin,'b')
line2, = ax2.plot(repwin,'r')

plt.legend((line1, line2), ('Dem', 'Rep'))
plt.show()

# Histogram courtesy of Michael Lerner (https://github.com/mglerner)
dem_win_pct = 100*(np.array(demwin) >= 270).sum()/len(np.array(demwin))
n, bins, patches = plt.hist(np.array(demwin),bins=50)
plt.title('Dem win {d:.1f}%'.format(d=dem_win_pct))

bin_centers = 0.5 * (bins[:-1] + bins[1:])
colors = []
for c in bin_centers:
    if c < 270: 
        colors.append('red')
    else: 
        colors.append('blue')
for c, p in zip(colors, patches):
    plt.setp(p, 'facecolor', c)
