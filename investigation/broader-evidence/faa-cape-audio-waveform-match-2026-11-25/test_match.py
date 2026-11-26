import os,subprocess,numpy as np
from scipy.signal import fftconvolve
root=os.environ['CAPE_AUDIO_ROOT'].rstrip('/')+'/'
def dec(name, start=None,duration=None):
 c=['ffmpeg','-v','error']
 if start is not None:c+=['-ss',str(start),'-t',str(duration)]
 c+=['-i',root+name,'-ac','1','-ar','2000','-f','f32le','pipe:1']
 return np.frombuffer(subprocess.check_output(c),dtype='<f4').copy()
x=dec('nara-k90-30-7598879.mp3'); q=dec('nara-k90-39-7598886.mp3',1473,10)
control=x[2000000:2020000].copy(); control-=control.mean(); print('positive_control_self_correlation',round(float(np.corrcoef(control,x[2000000:2020000])[0,1]),6)); q-=q.mean(); n=len(q)
print('sample_rate=2000 search_samples=',len(x),'query_samples=',n,'query_file_start=1473')
y=fftconvolve(x,q[::-1],mode='valid')
# Mean-center each rolling search window in the denominator.
sums=np.r_[0.,np.cumsum(x,dtype=np.float64)];squares=np.r_[0.,np.cumsum(x.astype(np.float64)**2)]
energy=squares[n:]-squares[:-n]-(sums[n:]-sums[:-n])**2/n
norm=np.sqrt(np.maximum(energy,0)*np.dot(q,q)); scores=np.divide(y,norm,out=np.zeros_like(y),where=norm>1e-10)
for rank in range(3):
 i=int(np.argmax(np.abs(scores)));print('rank',rank+1,'k90_30_offset_seconds',round(i/2000,4),'signed_pearson',round(float(scores[i]),6));scores[max(0,i-60000):min(len(scores),i+60001)]=0
