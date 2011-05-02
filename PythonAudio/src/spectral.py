import math
import numpy as N
import pylab as P

class Spectral:

	def __init__(self,winSize,rate):
	
		self.twoPiJ=2.0*N.pi*complex(0,1)
		self.winSize=winSize

		self.chunkSize=winSize/2
		self.hann=self._hanning()
		self.Hann=P.ifft(self.hann)
		self.rate=float(rate)
		self.freqT=rate/winSize
		self.nyquist=rate/2
		self.binF = N.zeros(self.winSize,N.double)
		self.binF[0:self.winSize] = N.arange(0,rate,self.freqT)
		self.binFW = (self.binF+self.nyquist)%rate-self.nyquist 
		
		
	def _hanning(self):
		
		w = N.zeros(self.winSize,N.double)
		
		for i in range(self.winSize):
			w[i] = 0.5*(1.0-N.cos( (i+0.5)*N.pi*2.0 / self.winSize))
			
		return w		
	
	
	def createBinVect(self):
		return N.zeros(self.winSize,N.cdouble)
	
	
	def createChunkVect(self):
		return N.zeros(self.winSize,N.double) 
	
	
	def freqVect(self,f):
		# FFT of cos(f) by doing FFT(cos(f))  
		
		x = N.zeros(self.winSize,N.double)
		
		for i in range(self.winSize):
			x[i] = N.cos( float(f)*(i+0.5)*N.pi*2.0 / self.freqT / (self.winSize))
		
		X=P.fft(x)
	
		return X
	
	def hanningFT(self,f):
		nf=f/self.freqT
		piJ=self.twoPiJ/2.0
		
		return  0.5*N.sinc(nf)+0.25*(N.sinc(nf+1)*N.exp(-piJ*self.freqT)+N.sinc(nf-1)*N.exp(self.freqT*piJ))
		
	
	def freqVectH(self,f,rads):
		
		# FFT of sin(wt).hann(t)   by explicit FFT(sin(wt).hann(t))
			
		x = N.zeros(self.winSize,N.double)
		
		for i in range(self.winSize):
			x[i] = N.sin(rads+float(f)*(i+0.5)*N.pi*2.0 / self.freqT / (self.winSize))	
		
		X=P.fft(x*self.hann)
	
		return X
		
	def shiftVec(self,T):
		return N.exp(-self.twoPiJ*T*self.binFW)	
		
	def deltaFF(self,freq,dT):
		lam=dT*freq
		X=self.createBinVect()
		nqy=self.winSize/2
		X[1:nqy]=N.exp(self.twoPiJ*lam)
		X[nqy:self.winSize]=N.exp(-self.twoPiJ*lam)
		return X	
		
	
if __name__ == "__main__":
	
	rate=44100.0
	nFFT=64
	fragSize=nFFT/2
	T=nFFT/rate
	
	f=1000.0
	
	s=Spectral(nFFT,rate)
	
	nFrag=7
		
	y=N.zeros(nFrag*fragSize,N.double)
	
	X1=s.freqVectH(f,0)
	D=s.deltaFF(f,T/2.0)
	
	
	for i in range(nFrag-1):
		chunk=N.real(P.ifft(X1))
		y[i*fragSize:i*fragSize+nFFT] += chunk
		X1=X1*D*.8
	
	# X2=s.Hann
	
	
	# X1 *= s.shiftVec(T/2)
	
	
	
	
	from matplotlib.pyplot import * 

	plot(y)
	show()
	
	