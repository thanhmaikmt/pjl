from backpropbrain import *



def checkItWorks(brain):
    #  This is what I used to train the brain
    TD = [[[0., 0. , 0.],[0.,1.0]],   \
      [[0.0, 0.0 ,1.0],[1.,0.0]], \
      [[0.0 , 1.0, 0.0 ],[1.,0.0]], \
      [[0.0 , 1.0, 1.0],[0.,1.0]],  \
      [[1., 0. , 0.],[1.,0.0]],   \
      [[1.0, 0.0 ,1.0],[0.,1.0]], \
      [[1.0 , 1.0, 0.0 ],[0.,1.0]], \
      [[1.0 , 1.0, 1.0],[1.,.0]]]


    print "--- checking output for training set . . . "

    print "    input         target           actual     "
    for td in TD:
        o=brain.ffwd(td[0])
        print td[0],td[1],o


file=open("greystuff","r")
brain=loadBrain(file)


# I'll just check it works

checkItWorks(brain)



