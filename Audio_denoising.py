#HAAR Wavelet to denoise the signal

import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from scipy.io import wavfile
import soundfile as sf

def downsample(data,noise,M):
    
    dm = np.zeros(len(data)//M)
    for i in range(0,len(dm)):
        dm[i] = data[i*M]

    nm = np.zeros(len(noise)//M)
    for i in range(0,len(nm)):
        nm[i] = noise[i*M]
        
    return dm,nm

def upsample(data,noise,L):
    
    dli = np.zeros(len(data)*L)
    for i in range(0,len(dli)):
        if i%L == 0:
            dli[i] = data[i//L]
        else:
            dli[i] = 0 

    nli = np.zeros(len(noise)*L)
    for i in range(0,len(nli)):
        if i%L == 0:
            nli[i] = noise[i//L]
        else:
            nli[i] = 0
    return dli,nli
    

ao=AudioSegment.from_wav(r"paste ur file directory here")

sound=wavfile.read(r"paste ur file directory here")
print(sound)

arr=np.array(sound[1])
print(arr)
a=np.reshape(arr,arr.size)

print("Array after extraction from .wav file",a)
plt.plot(a)
plt.title("Original Audio")
plt.show()


#Filter equations
coeff=1/(2**0.5)
h=[coeff,coeff]
g=[-coeff,coeff]

#Computing for the very first branch

d0=np.convolve(a,h)
n0=np.convolve(a,g)

print(d0)
print(n0)
#downsampling followed by upsampling
di,ni=downsample(d0,n0,2)

plt.plot(d0)
plt.title("Denoised Signal")
plt.show()

plt.plot(n0)
plt.title("Intermediate Noise component")
plt.show()

#upsampling the audio
di1,ni1=upsample(di,ni,2)

#Passing through another filter
h1=[coeff,coeff]
g1=[coeff,-coeff]

#Final data part of the audio is recovered
df=np.convolve(di1,h1)
#Noisy part of the Audio is recovered
nf=np.convolve(ni1,g1)

#adding together the Data and Noise to ensure there is no loss from the original audio
final=np.add(df,nf)

print(final)

plt.plot(final)
plt.title("Final")
plt.show()

plt.plot(df)
plt.title("Data")
plt.show()

#Denoised audio file
sf.write(r'paste ur file directory here',df, 98000)

#Other components not reqd in Denoising but essential in reconstruction of original signal
sf.write(r'paste ur file directory here', 98000)
sf.write(r'paste ur file directory here',final,98000)