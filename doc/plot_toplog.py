import numpy as np
import matplotlib.pyplot as plt
import sys

narg = len(sys.argv)


if narg != 3:
    print("Pass file and pid as arguments")
    exit()
#if

filer = sys.argv[1] # "20250915-memory.txt"

pid = sys.argv[2] #"3135646"
Idr = open(filer,"r")

yy = np.array([] )

for line in Idr:
    if pid in line:
        y_str = line.split()[5]
        y_str = y_str.replace("m","").replace("g","E3")
        yy = np.append( yy,  float( y_str ) )      
#for
    
n = yy.shape[0]

At = 60 #seconds
tt = np.linspace(0,n*At,n)

plt.plot(tt/3600,yy)
plt.xlabel("Time (hours)")
plt.ylabel("Memory (MB)")
plt.title("Nodered")

plt.show()

# Print Leak Rate
# Ath = 10
# Ai = int( Ath*3600/At ) # Number of elements

# leak = (yy[-1]-yy[-Ai])/(Ath)
# print(f"{leak:.2f} MB/h")

