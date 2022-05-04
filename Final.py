#Sylvia Le, Linh Nguyen, Uyen Tran
import libpyAI as ai
import math
from Fuzzy import FuzzySystem

# attempts to fuzzy
wall_range = [[0, 150], [100, 250]]
speed_range = [[0, 10], [5, 20]]
angle_range = [[0, 90], [70, 180]]
risk_range = [[0, 35], [15, 100]]

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
  
  walls = [frontWall, left45Wall, right45Wall, left90Wall, right90Wall,
    left135Wall, right135Wall, leftBackWall, rightBackWall, backWall, trackWall]

  # inputs
  closest_wall = min(walls)
  speed = ai.selfSpeed()

  system = FuzzySystem(wall_range, speed_range, angle_range, risk_range)
  wall_risk = system.wall_risk(closest_wall, speed)
  print(wall_risk)
  
  ######## PRODUCTION SY STEMS ########
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
  bullet_dist = ai.shotDist(0)
  bullet_angle = abs(ai.shotVelDir(0) - heading)    # test this
  # if bullet_angle == 90:
  #   thrust
  if bullet_dist < 100 and bullet_dist > 0:
    
    turn = (bullet_angle + 90) % 360
    ai.turnToDeg(turn)
    if ai.selfSpeed() <= 20:
      ai.thrust(1)
    ai.emergencyThrust()
    # print(turn)
    
  # aim
  turn_speed = ai.getTurnSpeed()
  enemy_dist = ai.enemyDistance(0)
  enemy_vel = ai.enemySpeed(0)
  alpha = abs(heading - ai.enemyTrackingDeg(0)) 
  
  if enemy_dist <= 1000:
    x = (enemy_dist*math.sin(alpha)+enemy_vel*(alpha/turn_speed)) / (enemy_dist*math.cos(alpha))
    turn_angle = (math.degrees(math.atan(x)) + heading) % 360
    ai.turnToDeg(round(turn_angle)) 
    
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
