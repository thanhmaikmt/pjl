from pool import *


class X:

    def __init__(self,vec):
        self.vec=vec


goals=[None,None,None]
brainPlug=None

pool=Pool_Mino(20,brainPlug,goals)


vecs=[X([1,0,1]),X([3,3,4]),X([4,4,3]),X([3,6,1]),X([5,3,1]),X([2,2,2]),X([3,2,1]),X([2,4,5]),X([5,0,0])]


for v in vecs:
    pool.add(v)
    pool.debug("X")