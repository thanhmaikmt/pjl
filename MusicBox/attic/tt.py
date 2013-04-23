import sys, tty, termios
from select import select
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
try:
    tty.setraw(sys.stdin.fileno())
    [i, o, e] = select([sys.stdin.fileno()], [], [], 5)
    if i: ch=sys.stdin.read(1)
    else: ch=''     
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

print ch