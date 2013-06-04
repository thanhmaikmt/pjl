import pygame

pygame.init()
try:
     screen = pygame.display.set_mode((200, 200))
     # This should show a blank 200 by 200 window centered on the screen
     pygame.display.flip()
     while True:
         event = pygame.event.wait()
         if event.type == pygame.QUIT:
             break
finally:
     print "QUITING"
     pygame.quit()  # Keep this IDLE friendly 
     print " QUIT"