#Sylvia Le, Linh Nguyen, Uyen Tran
import libpyAI as ai
import math
from Fuzzy import FuzzySystem

# attempts to fuzzy
wall_range = [[100, 300], [200, 500]]
speed_range = [[0, 10], [5, 20]]
angle_range = [[20, 30], [20, 40]]
risk_range = [[0, 30], [25, 100]]

def AI_loop():
  # Release keys
  ai.thrust(0)
  ai.turnLeft(0)
  ai.turnRight(0)
  ai.setTurnSpeed(35)
  ai.setPower(40)
  
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
  bullet_dist = ai.shotDist(0)
  bullet_angle = abs(ai.shotVelDir(0) - heading)    # test this
  #enemy_dist = ai.enemyDistance(0)
  #alpha = abs(heading - ai.enemyTrackingDeg(0)) 
  ai.lockClose()
  enemy_dist = ai.selfLockDist()
  enemy_angle = ai.lockHeadingDeg()

  system = FuzzySystem(wall_range, speed_range, angle_range, risk_range)
  wall_risk = system.wall_risk(closest_wall, speed)
  bullet_risk = system.bullet_risk(ai.shotDist(0), bullet_angle)
  enemy_risk = system.enemy_risk(enemy_dist, enemy_angle)
  
  print('wall risk: ', wall_risk)
  print('bullet risk: ', bullet_risk)
  print('enemy risk: ', enemy_risk)
  print()
  
  risks = {'wall': wall_risk, 'bullet': bullet_risk, 'enemy': enemy_risk}
  highest = max(risks.values())
  
  # WALL BEHAVIOR
  if risks['wall'] == highest:
    print('wall behavior')
    if speed <= 5 and (frontWall >= 200) and (left45Wall >= 200) and (right45Wall >= 200) and (right90Wall >= 200) and (left90Wall >= 200) and (left135Wall >= 50) and (right135Wall >= 35) and (backWall >= 35):
      ai.thrust(1)
    elif speed <= 5 and trackWall < 100:
      ai.thrust(1)
    elif speed <= 5 and (backWall <= 50 or left135Wall <= 50 or right135Wall <= 50 or leftBackWall <= 50 or rightBackWall <= 50):
      ai.thrust(1)
    
		# turn
    if frontWall <= 300 and (left45Wall < right45Wall): 
      ai.turnRight(1)
    elif left90Wall <= 200: 
      ai.turnRight(1) 
    elif frontWall <= 300 and (left45Wall > right45Wall):
      ai.turnLeft(1)
    elif right90Wall <= 200:
      ai.turnLeft(1)

  # BULLET BEHAVIOR
  elif risks['bullet'] == highest:
    print('bullet behavior')
    if bullet_angle <= 110 and bullet_angle >= 70:
      ai.thrust(1)
    if bullet_dist < 100 and bullet_dist > 0:
      turn = (bullet_angle + 90) % 360
      ai.turnToDeg(turn)
      if ai.selfSpeed() <= 10:
        ai.setPower(30)
        ai.thrust(1)
        #ai.emergencyThrust()
      
  # ENEMY BEHAVIOR
  elif risks['enemy'] == highest:
    print('enemy behavior')
    #~ turn_speed = ai.getTurnSpeed()
    #~ enemy_vel = ai.enemySpeed(0)
    #~ gamma = ai.enemyTrackingDeg(0) % 90
    
    #~ enemy_velX = enemy_vel * math.cos(gamma)
    #~ enemy_velY = enemy_vel * math.sin(gamma)
    
    #~ rel_enemy_velX =  enemy_velX - ai.selfVelX()
    #~ rel_enemy_velY = enemy_velY - ai.selfVelY()
    
    #~ rel_enemy_vel = math.sqrt((rel_enemy_velX)**2+(rel_enemy_velY)**2)
    #~ if enemy_dist <= 1000:
      #~ x = (enemy_dist*math.sin(alpha)+rel_enemy_vel*(alpha/turn_speed)) / (enemy_dist*math.cos(alpha))
      #~ turn_angle = (math.degrees(math.atan(x)) + heading) % 360
      #~ ai.turnToDeg(round(turn_angle))
    
    if enemy_dist <= 1000:
      ai.setTurnSpeed(60)
      ai.turnToDeg(int(enemy_angle))
    ai.fireShot()
  print('----------------')

ai.start(AI_loop,["-name","Final","-join","localhost"])
