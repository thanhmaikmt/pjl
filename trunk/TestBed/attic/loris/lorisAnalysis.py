

import loris, os, time


name='flute'

  
a = loris.Analyzer( 270 )       # reconfigure Analyzer
a.setFreqDrift( 30 )

file=loris.AiffFile( name+'.aiff' )
v = file.samples()
samplerate=file.sampleRate()

parts = a.analyze( v, samplerate )
    

# loris.channelize( flut, loris.createFreqReference( flut, 291*.8, 291*1.2, 50 ), 1 )

refenv = a.fundamentalEnv()
loris.channelize( parts, refenv, 1 )
loris.distill( parts )
 
     

for part in parts:
    print "*****************************************"
    it=part.iterator()
    while not it.atEnd():
        bp=it.next()
        print "t:",bp.time(), " a:",bp.amplitude()," bw:",bp.bandwidth()," f:",bp.frequency()," p:",bp.phase()
    
loris.exportSpc(name+".spc",parts,60)
print "Done"

    
#path = os.getcwd()
#file = os.path.join(path, 'clarinet.aiff')    
#clar,size,samplerate=analysis(file,390,30,-80,415)

#fund=390

#clar = loris.importSdif( 'clarinet.pytest.sdif' )