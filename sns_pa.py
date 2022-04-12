import matplotlib.pyplot as plt
import cmath 
from pandas import *
import numpy as np
  
# reading CSV file
data = read_csv("data.csv")
  
# converting column data to list
y = data['y[n]'].tolist()
x = data['x[n]'].tolist()

# now defining h[n]
h=[1/16,1/4,3/8,1/4,1/16]

#now defining denoising
def denoising(a):
    c=[]
    c.append((a[0]+a[1]+a[2]+a[3]+a[4])/5)
    c.append((a[0]+a[1]+a[2]+a[3]+a[4])/5)
    c.append((a[0]+a[1]+a[2]+a[3]+a[4])/5)
    for i in range(3,190):
        c.append((a[i-3]+a[i-2]+a[i-1]+a[i]+a[i+1]+a[i+2]+a[i+3])/7) #taken average of seven nearby terms
    c.append((a[188]+a[189]+a[190]+a[191]+a[192])/5)
    c.append((a[188]+a[189]+a[190]+a[191]+a[192])/5)
    c.append((a[188]+a[189]+a[190]+a[191]+a[192])/5)
    return c 
 
#now defining Deblurring
def deblur(y):
    
    # dtft of y[n]
    dtft =[]
    for i in range(0,193):
        k=0
        for j in range(0,193):
            k=k+(y[j]*(cmath.exp(complex(0,(-2)*cmath.pi*i*(j/193)))))
        dtft.append(k)
   

    # dtft of h[n]
    dtft1=[]
    for i in range(193):
        d=0
        for j in range(5):
           d+=(h[j]*(cmath.exp(complex(0,(-2)*cmath.pi*i*((j-2)/193)))))
        if d.real<=0.4:
            d=0.4
            
        dtft1.append(dtft[i]/d)  # dividing dtft of y[n] by h[n] 
        
    # finally inverse dtft
    x1=[]
    for i in range(193):
        k=0
        for j in range(193):
            k+=(dtft1[j]*(cmath.exp(complex(0,2*cmath.pi*i*(j/193)))))
        x1.append(k/193)
    return x1

# original x -- blue
plt.plot(x)

# first denoising and then debluurring -- orange
denoised_y=denoising(y)
x1=deblur(denoised_y)
plt.plot(x1)

# first deblurring and then denoising -- green 
deblurred_y=deblur(y)
x2=denoising(deblurred_y)
plt.plot(x2)     

plt.show()

# difference between both methods

# mean squared error of x1-x ( denoise then deblur)
x1_x= np.array(x1)- np.array(x)
MSE1 = np.square(np.subtract(x1,x)).mean()
print(abs(MSE1))
 
# mean squared error of x2-x ( deblur then denoise)
x2_x= np.array(x2)- np.array(x)
MSE2 = np.square(np.subtract(x2,x)).mean()
print(abs(MSE2))

# compare the values. (lesser mse is better)