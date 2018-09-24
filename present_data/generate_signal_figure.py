import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt


data = pd.read_csv('C:/Users/EhudHahamy/Data/2018-09-23-he13-data.csv')
frame = DataFrame(data)

time_stamps = frame['event_timestamp']
bmp_alt = frame['bmp_alt']
gps_alt = frame['gps_alt']

fig = plt.figure()

ax1 = fig.add_subplot(2,1,1)
plt.plot(bmp_alt,'k', label = 'bmp')
plt.plot(gps_alt, 'r', label = 'gps')
ax1.legend()

ax2 = fig.add_subplot(2,1,2)
plt.plot(bmp_alt.T - gps_alt.T)


plt.show()






