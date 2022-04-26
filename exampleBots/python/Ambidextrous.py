#Evan Gray - May 2012
#Run: python3 Ambidextrous.py
import libpyAI as ai
frames=5
def lefty():
  global frames
  ai.turn(25)
  frames+=1
  if frames==10:
    frames=0
    ai.switchLoop(righty)
def righty():
  global frames
  ai.turn(-25)
  frames+=1
  if frames==10:
    frames=0
    ai.switchLoop(lefty)
ai.start(righty,["-name","Dexter"])
