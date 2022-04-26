#Evan Gray - May 2012
#Run: python3 Helper.py
import libpyAI as ai
frames=0
def AI_loop():
  global frames
  frames+=1
  if frames==20:
    ai.thrust(1)
    frames=0
  else:
    ai.thrust(0)
  ai.turnLeft(1)
  ai.fireShot()
ai.start(AI_loop,["-name","Pelper"])
