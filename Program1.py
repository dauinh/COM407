#Sylvia Le, Linh Nguyen, Uyen Tran
import libpyAI as ai
def AI_loop():
  #Release keys
  ai.thrust(0)
  ai.turnLeft(0)
  ai.turnRight(0)
  
  
  #find walls
  heading = int(ai.selfHeadingDeg())
  tracking = int(ai.selfTrackingDeg())
  frontWall = ai.wallFeeler(500,heading)
  
  left45Wall = ai.wallFeeler(500,heading+45)
  right45Wall = ai.wallFeeler(500,heading-45)
  left90Wall = ai.wallFeeler(500,heading+90)
  right90Wall = ai.wallFeeler(500,heading-90)
  left135Wall = ai.wallFeeler(500,heading+135)
  leftBackWall = ai.wallFeeler(500, heading+210)  #add for faster turn at parallel angle
  right135Wall = ai.wallFeeler(500,heading-135)
  rightBackWall = ai.wallFeeler(500, heading-210)
  backWall = ai.wallFeeler(500,heading-180) 
  trackWall = ai.wallFeeler(500,tracking)
  
  
  #find enemy stats
  enemyDist = ai.selfLockDist()
  enemyDir = ai.lockHeadingDeg()
  
  
  ########PRODUCTION SYSTEMS
  #thrust and heading != tracking
  if ai.selfSpeed() <= 5 and (frontWall >= 200) and (left45Wall >= 200) and (right45Wall >= 200) and (right90Wall >= 200) and (left90Wall >= 200) and (left135Wall >= 50) and (right135Wall >= 50) and (backWall >= 50):
    ai.thrust(1)
  elif trackWall < 100:
    ai.thrust(1)
  elif backWall <= 50 or left135Wall <= 50 or right135Wall <= 50 or leftBackWall <= 50 or rightBackWall <= 50:
    ai.thrust(1)
    
  #turn
  elif frontWall <= 300 and (left45Wall < right45Wall): 
    ai.turnRight(1)
  elif left90Wall <= 200:
    ai.turnRight(1) 
  elif frontWall <= 300 and (left45Wall > right45Wall):
    ai.turnLeft(1)
  elif right90Wall <= 200:
    ai.turnLeft(1)
    
  #shot 
  if enemyDir > heading and enemyDist <= 50:
  	ai.turnLeft(1)
  	ai.fireShot()
  elif enemyDir < heading and enemyDist <= 50:
  	ai.turnRight(1)
  	ai.fireShot()
  
  #even if no enemy present, still shot
  ai.fireShot()

ai.start(AI_loop,["-name","One","-join","localhost"])
