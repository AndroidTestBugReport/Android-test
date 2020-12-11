'''
import matplotlib.pyplot as plt
import calendar
x=[1,2,3,4,5]
y=[3,6,7,9,2]
 
fig = plt.figure(figsize =(10, 7)) 

#fig,ax=plt.subplots(1,1)
plt.plot(x,y,label='trend')
plt.title('Interesting Graph',loc ='left')

plt.xticks(x, calendar.month_name[1:13],color='blue',rotation=60)

#ax.set_title('title test',fontsize=12,color='r')
plt.show()
'''


import matplotlib.pyplot as plt 
import numpy as np 
import calendar

  
# Creating dataset 
np.random.seed(10) 
  
data_1 = np.random.normal(100, 10, 200) 
data_2 = np.random.normal(90, 20, 200) 
data_3 = np.random.normal(80, 30, 200) 
data_4 = np.random.normal(70, 40, 200) 
data = [data_1, data_2, data_3, data_4] 
  
fig = plt.figure(figsize =(10, 7)) 
#ax=plt.subplots(1)
#ax = fig.add_axes([0, 0, 1, 1]) 
#bp = ax.boxplot(data) 
#fig.boxplot(data)

f=plt.boxplot(data, showmeans=True) 

#https://www.jianshu.com/p/b2f70f867a4a
'''
for mean in f['mean']:
    mean.set( color='#7570b3', linewidth=2)
'''

for means in f['means']:
    means.set(marker="x", color='#7570b3',markersize=20)

for whisker in f['whiskers']:
    whisker.set(color='r', linewidth=2)

for cap in f['caps']:
    cap.set(color='g', linewidth=3)

plt.xticks([1,2,3,4], ["aa","bb","cc","dd"],color='blue',rotation=60)

plt.yticks([0,40,80,120], ["qwe","basd","zxc","fdgfdg"],color='blue',rotation=60)

# Creating plot 
#bp = ax.boxplot(data) 
  
# show plot 
plt.show() 
