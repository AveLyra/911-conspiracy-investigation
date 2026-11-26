import os,subprocess,numpy as np
from scipy import signal,fft
root=os.environ['CAPE_AUDIO_ROOT'].rstrip('/')+'/'
def dec(name,start=None,duration=None):
 c=['ffmpeg','-v','error']
 if start is not None:c+=['-ss',str(start),'-t',str(duration)]
 c+=['-i',root+name,'-ac','1','-ar','2000','-f','f32le','pipe:1']
 return np.frombuffer(subprocess.check_output(c),dtype='<f4')
def features(x):
 _,_,z=signal.stft(x,fs=2000,nperseg=256,noverlap=56,boundary=None,padded=False)
 v=fft.dct(np.log1p(np.abs(z)*10000),type=2,axis=0,norm='ortho')[1:17].astype('float32')
 v-=v.mean(axis=0,keepdims=True)
 return v
def search(q,x,exclusion=None):
 n=q.shape[1]; q=q-q.mean(axis=1,keepdims=True)
 cor=signal.fftconvolve(x,q[::-1,::-1],mode='valid')[0]
 s=np.pad(np.cumsum(x,axis=1,dtype='float64'),((0,0),(1,0)));s2=np.pad(np.cumsum(x*x,axis=1,dtype='float64'),((0,0),(1,0)))
 e=(s2[:,n:]-s2[:,:-n]-(s[:,n:]-s[:,:-n])**2/n).sum(axis=0)
 score=np.divide(cor,np.sqrt(np.maximum(e,0)*np.sum(q*q)),out=np.zeros_like(cor),where=e>0)
 if exclusion is not None: score[max(0,exclusion-300):min(len(score),exclusion+301)]=0
 i=int(np.argmax(score));return round(i/10,1),round(float(score[i]),6)
x=features(dec('nara-k90-30-7598879.mp3'))
for offset in (1453,1463,1473,1483,1493):
 q=features(dec('nara-k90-39-7598886.mp3',offset,10)); peak,score=search(q,x)
 print('query_offset',offset,'reference_peak',peak,'implied_shift',round(peak-offset,1),'score',score,flush=True)
