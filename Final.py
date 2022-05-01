#Sylvia Le, Linh Nguyen, Uyen Tran
import libpyAI as ai
from Fuzzy import *

def AI_loop():
  # Release keys
  ai.thrust(0)
  ai.turnLeft(0)
  ai.turnRight(0)
  
  # find walls
  heading = int(ai.selfHeadingDeg())
  tracking = int(ai.selfTrackingDeg())

  frontWall = ai.wallFeeler(500,heading)
  left45Wall = ai.wallFeeler(500,heading+45)
  right45Wall = ai.wallFeeler(500,heading-45)
  left90Wall = ai.wallFeeler(500,heading+90)
  right90Wall = ai.wallFeeler(500,heading-90)
  left135Wall = ai.wallFeeler(500,heading+135)
  right135Wall = ai.wallFeeler(500,heading-135)
  leftBackWall = ai.wallFeeler(500, heading+210)  #add for faster turn at parallel angle
  rightBackWall = ai.wallFeeler(500, heading-210)
  backWall = ai.wallFeeler(500,heading-180) 
  trackWall = ai.wallFeeler(500,tracking)
  
  # attempts to fuzzy
  walls = [frontWall, left45Wall, right45Wall, left90Wall, right90Wall,
    left135Wall, right135Wall, leftBackWall, rightBackWall, backWall, trackWall]

  # inputs
  closest_wall = min(walls)
  speed = ai.selfSpeed()

  # create membership functions
  near = Membership(0, 150, True)
  far = Membership(100, 250)

  slow = Membership(0, 10, True)
  fast = Membership(5, 20)

  low = Membership(0, 50, True)
  high = Membership(15, 100)

  # fuzzify
  wall_near = near.calcY(closest_wall)
  wall_far = far.calcY(closest_wall)
  speed_slow = slow.calcY(speed)
  speed_fast = fast.calcY(speed)

  # rule evaluation
  near_slowX = min(wall_near, speed_slow)
  near_slow = high.clip(near_slowX, 1)

  near_fastX = min(wall_near, speed_fast)
  near_fast = high.clip(near_fastX, 1)

  far_slowX = min(wall_far, speed_slow)
  far_slow = low.clip(1, far_slowX)

  far_fastX = min(wall_far, speed_fast)
  far_fast = high.clip(far_fastX, 1)
  
  # print(near_slow, near_slowX)
  # print(near_fast, near_fastX)
  # print(far_slow, far_slowX)
  # print(far_fast, far_fastX)

  # defuzz
  risk_ranges = [near_slow, near_fast, far_slow, far_fast]
  risk_weights = [near_slowX, near_fastX, far_slowX, far_fastX]
  output = cog(risk_ranges, risk_weights)
  print(output)
  
  ######## PRODUCTION SYSTEMS ########
  if ai.selfSpeed() <= 5 and (frontWall >= 100) and (left45Wall >= 100) and (right45Wall >= 100) and (right90Wall >= 100) and (left90Wall >= 100) and (left135Wall >= 35) and (right135Wall >= 35) and (backWall >= 35):
    ai.thrust(1)
  elif trackWall < 100:
    ai.thrust(1)
  elif backWall <= 35 or left135Wall <= 35 or right135Wall <= 35 or leftBackWall <= 35 or rightBackWall <= 35:
    ai.thrust(1)
    
  # turn
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
  
  if bulletDist < 100 and bulletDist > 0:
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
