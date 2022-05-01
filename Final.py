#Sylvia Le, Linh Nguyen, Uyen Tran
import libpyAI as ai
from Program2_Fuzzy import *

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
  
  
  ########PRODUCTION SYSTEMS
  far = 100
  near = 35
  #if frontWall <= near:
  #  ai.fasterTurnrate()
  #  ai.turnLeft(1)
  #  ai.thrust(1)
  if ai.selfSpeed() <= 5 and (frontWall >= far) and (left45Wall >= far) and (right45Wall >= far) and (right90Wall >= far) and (left90Wall >= far) and (left135Wall >= near) and (right135Wall >= near) and (backWall >= near):
    ai.thrust(1)
  elif trackWall < far:
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
    
  # dodge
  bulletDist = ai.shotDist(0)
  
  if bulletDist < far and bulletDist > 0:
    bulletAngle = ai.shotVelDir(0)
    turn = (bulletAngle + 90) %360
    ai.turnToDeg(turn)
    if ai.selfSpeed() <= 20:
      ai.thrust(1)
    ai.emergencyThrust()
    # print(turn)
    
  # aim
  arr = []
  val = 0
  # distance between agent and closet enemy
  closest = ai.enemyDistance(0)
  if closest <= 1000:
    ai.turnToDeg(ai.aimdir(0))
  ai.fireShot()
  #for i in range(4):
  #  if ai.enemyDistance(i) > 9999:
  #    ai.turnRight(1)
  #  else:
  #    arr.append(enemyDistance(i))
  #    val += 1
  #print(arr)
  #print(val)

ai.start(AI_loop,["-name","Final","-join","localhost"])
