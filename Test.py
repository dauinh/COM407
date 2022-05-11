#Sylvia Le, Linh Nguyen, Uyen Tran
import libpyAI as ai
from Program2_Fuzzy import * 

def AI_loop():
  #Release keys
  ai.thrust(0)
  ai.turnLeft(0)
  ai.turnRight(0)
  
  mess = ai.scanGameMsg(0)
  if 'Final left' in mess:
    ai.quitAI()
  
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
  

  risk_list = []
  for i in range(8):
    degree = 45*i
    distance = ai.wallFeeler(10000,tracking+(45*i))
    result = dist_to_wall(degree, distance)
    # print("From angle", degree, "at ", result)
    close, med, far = fuzzy(result)
    risk = defuzz(far, med, close)
    risk_list.append(risk)
  
  # find most risky wall
  max_risk = max(risk_list)
  track_risk = (tracking + (risk_list.index(max_risk)*45) % 360)
  min_risk = min(risk_list)
  
  # print("max risk", max_risk)
  # print("track risk", track_risk)
  
  near = 50
  ########PRODUCTION SYSTEMS
  if ai.selfSpeed() <= 5 and (frontWall >= 200) and (left45Wall >= 200) and (right45Wall >= 200) and (right90Wall >= 200) and (left90Wall >= 200) and (left135Wall >= 50) and (right135Wall >= 50) and (backWall >= 50):
    ai.thrust(1)
  elif trackWall < 100:
    ai.thrust(1)
  elif backWall <= near or left135Wall <= near or right135Wall <= near or leftBackWall <= near or rightBackWall <= near:
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
  ai.lockClose()
  #find enemy stats
  enemyDist = ai.selfLockDist()
  enemyDir = ai.lockHeadingDeg()
  #print(enemyDist, enemyDir)
  if enemyDist <= 500:
  	ai.turnToDeg(int(enemyDir))
  
  #even if no enemy present, still shot
  ai.fireShot()

ai.start(AI_loop,["-name","Test","-join","localhost"])
