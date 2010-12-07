'''
Created on 6 Dec 2010

@author: pjl
'''

#!/usr/bin/env python
import sys,os

def decodeSpeech(hmmd,lmdir,dictp,wavfile):
    """
    Decodes a speech file
    """
    try:
        import pocketsphinx as ps
        import sphinxbase
    except:
        print """Pocket sphinx and sphixbase is not installed
        in your system. Please install it with package manager.
        """
    
    speechRec = ps.Decoder(hmm = hmmd, lm = lmdir, dict = dictp)
    wavFile = file(wavfile,'rb')
    wavFile.seek(44)
    speechRec.decode_raw(wavFile)
    result = speechRec.get_hyp()

    return result[0]


if __name__ == "__main__":
    hmdir = "../hmm/wsj1"
    lmd = "../wsj/wlist5o.3e-7.vp.tg.lm.DMP"
    dictd = "../wsj/wlist5o.dic"
    wavfile = "sa1.wav"
    recognised = decodeSpeech(hmdir,lmd,dictd,wavfile)
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print recognised
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"