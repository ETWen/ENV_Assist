import matplotlib.pyplot as plt
import numpy as np
import random

plt.ion() ## Note this correction
plt.xlabel('Item (s)')
plt.ylabel('Value')
plt.title('Python Line Chart: Plotting numbers')
plt.grid(True)

i=0
while i <100:
    plt.clf() # clear plot
    t = np.arange(0.0, 100.0, 1) # range 0~100, step = 1

    s = []
    for idx in range(100):
        s.append(random.randint(1,100))
    plt.plot(t,s)
    i+=1;
    plt.show()
    plt.pause(0.001) #Note this correction