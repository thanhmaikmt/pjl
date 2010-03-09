a:     DAT          'H'
       DAT          'e'
       DAT          'l'
       DAT          'l'
       DAT          'o'
       DAT           0
ptr:   DAT           a
loop:  JMZ     end  @ptr
       OUT     @ptr
       ADD    #1    ptr
       JMP    loop
end:   HLT

