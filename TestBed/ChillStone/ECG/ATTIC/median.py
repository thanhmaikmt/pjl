#!/bin/env python

import numpy as np

def medfilt1(x=None,L=None):

    '''
    a simple median filter for 1d numpy arrays.

    performs a discrete one-dimensional median filter with window
    length L to input vector x. produces a vector the same size 
    as x. boundaries handled by shrinking L at edges; no data
    outside of x used in producing the median filtered output.
    (upon error or exception, returns None.)

    inputs:
        x, Python 1d list or tuple or Numpy array
        L, median filter window length
    output:
        xout, Numpy 1d array of median filtered result; same size as x
    
    bdj, 5-jun-2009
    '''

    # input checks and adjustments --------------------------------------------
    try:
        N = len(x)
        if N < 2:
            print 'Error: input sequence too short: length =',N
            return None
        elif L < 2:
            print 'Error: input filter window length too short: L =',L
            return None
        elif L > N:
            print 'Error: input filter window length too long: L = %d, len(x) = %d'%(L,N)
            return None
    except:
        print 'Exception: input data must be a sequence'
        return None

    xin = np.array(x)
    if xin.ndim != 1:
        print 'Error: input sequence has to be 1d: ndim =',xin.ndim
        return None
    
    xout = np.zeros(xin.size)

    # ensure L is odd integer so median requires no interpolation
    L = int(L)
    if L%2 == 0: # if even, make odd
        L += 1 
    else: # already odd
        pass 
    Lwing = (L-1)/2

    # body --------------------------------------------------------------------

    for i,xi in enumerate(xin):
  
        # left boundary (Lwing terms)
        if i < Lwing:
            xout[i] = np.median(xin[0:i+Lwing+1]) # (0 to i+Lwing)

        # right boundary (Lwing terms)
        elif i >= N - Lwing:
            xout[i] = np.median(xin[i-Lwing:N]) # (i-Lwing to N-1)
            
        # middle (N - 2*Lwing terms; input vector and filter window overlap completely)
        else:
            xout[i] = np.median(xin[i-Lwing:i+Lwing+1]) # (i-Lwing to i+Lwing)

    return xout

if __name__ == '__main__':

    # 100 pseudo-random integers ranging from 1 to 100, plus three large outliers for illustration.
    x = list(np.ceil(np.random.rand(25)*100)) + [1000] + \
        list(np.ceil(np.random.rand(25)*100)) + [2000] + \
        list(np.ceil(np.random.rand(25)*100)) + [3000] + \
        list(np.ceil(np.random.rand(25)*100))

    #---------------------------------------------------------------
    L = 2

    print 'L:',L
    print 'x:',x

    xout = medfilt1(x,L)

    if xout != None:
        print 'xout:',list(xout)
        
        try:
            import pylab as pl
            pl.subplot(2,1,1)
            pl.plot(x)
            pl.plot(xout)
            pl.grid(True)
            y1min = np.min(xout)*.5
            y1max = np.max(xout)*2
            pl.legend(['x (pseudo-random)','xout'])
            pl.title('median filter with window length ' + str(L) + ' (removes outliers, tracks remaining signal)')
        except:
            print 'pylab exception: not plotting results.'
    #---------------------------------------------------------------
    L = 103

    print 'L:',L
    print 'x:',x

    xout = medfilt1(x,L)

    if xout != None:
        print 'xout:',list(xout)
        
        try:
            pl.subplot(2,1,2)
            pl.plot(x)
            pl.plot(xout)
            pl.grid(True)
            y2min = np.min(xout)*.5
            y2max = np.max(xout)*2
            pl.legend(['same x (pseudo-random)','xout'])
            pl.title('median filter with window length ' + str(L) + ' (removes outliers and noise)')
        except:
            pass
    #---------------------------------------------------------------
    try:
        pl.subplot(2,1,1)
        pl.ylim([min(y1min,y2min),max(y1max,y2max)])
        pl.subplot(2,1,2)
        pl.ylim([min(y1min,y2min),max(y1max,y2max)])
        pl.show()
    except:
        pass