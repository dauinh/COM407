# Testing method: fuzzy system in main() => FuzzySystem() in main() => FuzzySystem() in xpilot
# Note: 
#   - change rule evaluaion for bullet dodging and enemy shooting
#   - create parameter for FuzzySystem
"""Membership
"""
class Membership():
  def __init__(self, xmin, xmax, isnegative=False):
    self.xmin = xmin
    self.xmax = xmax
    self.isnegative = isnegative
    if isnegative:
      self.b = 1
      self.a = -self.b/xmax
    else:
      self.a = 1/(xmax - xmin)
      self.b = - self.a*xmin

  def calcY(self, x):
    res = round(self.a*x + self.b, 3)
    # input smaller than fuzzy range
    if x <= self.xmin:
      if self.isnegative: res = 1
      else: res = 0
    # input larger than fuzzy range
    elif x >= self.xmax:
      if self.isnegative: res = 0
      else: res = 1
    return res

  def calcX(self, y):
    return round((y - self.b)/self.a, 3)

  def clip(self, y1, y2):
    x1 = self.calcX(y1)
    x2 = self.calcX(y2)
    return x1, x2

"""FuzzySystem
"""
class FuzzySystem():

  def __init__(self, wall: list, speed: list, angle: list, risk: list):
    """
      create membership functions
    """
    # distance to walls
    self.near = Membership(wall[0][0], wall[0][1], True)
    self.far = Membership(wall[1][0], wall[1][1])

    # speed
    self.slow = Membership(speed[0][0], speed[0][1], True)
    self.fast = Membership(speed[1][0], speed[1][1])

    # angle
    self.small = Membership(angle[0][0], angle[0][1], True)
    self.large = Membership(angle[1][0], angle[1][1])

    # risk
    self.low = Membership(risk[0][0], risk[0][1], True)
    self.high = Membership(risk[1][0], risk[1][1])

  def wall_risk(self, wall, speed):
    """
      calculate crashing into walls risk
    """
    wall_near = self.near.calcY(wall)
    wall_far = self.far.calcY(wall)
    speed_slow = self.slow.calcY(speed)
    speed_fast = self.fast.calcY(speed)

    near_slowX = min(wall_near, speed_slow)
    near_slow = self.high.clip(near_slowX, 1)

    near_fastX = min(wall_near, speed_fast)
    near_fast = self.high.clip(near_fastX, 1)

    far_slowX = min(wall_far, speed_slow)
    far_slow = self.low.clip(1, far_slowX)

    far_fastX = min(wall_far, speed_fast)
    far_fast = self.high.clip(far_fastX, 1)

    risk_ranges = [near_slow, near_fast, far_slow, far_fast]
    risk_weights = [near_slowX, near_fastX, far_slowX, far_fastX]

    return self.cog(risk_ranges, risk_weights)

  def bullet_risk(self, distance, angle):
    """
      calculate being hit by risk
    """
    distance_near = self.near.calcY(distance)
    distance_far = self.far.calcY(distance)
    angle_small = self.small.calcY(angle)
    angle_large = self.large.calcY(angle)

    near_smallX = min(distance_near, angle_small)
    near_small = self.high.clip(near_smallX, 1)

    near_largeX = min(distance_near, angle_large)
    near_large = self.low.clip(1, near_largeX)

    far_smallX = min(distance_far, angle_small)
    far_small = self.low.clip(1, far_smallX)

    far_largeX = min(distance_far, angle_large)
    far_large = self.low.clip(1, far_largeX)

    risk_ranges = [near_small, near_large, far_small, far_large]
    risk_weights = [near_smallX, near_largeX, far_smallX, far_largeX]

    return self.cog(risk_ranges, risk_weights)

  def enemy_risk(self, distance, angle):
    """
      calculate risk to shoot enemy
    """
    distance_near = self.near.calcY(distance)
    distance_far = self.far.calcY(distance)
    angle_small = self.small.calcY(angle)
    angle_large = self.large.calcY(angle)

    near_smallX = min(distance_near, angle_small)
    near_small = self.high.clip(near_smallX, 1)

    near_largeX = min(distance_near, angle_large)
    near_large = self.low.clip(1, near_largeX)

    far_smallX = min(distance_far, angle_small)
    far_small = self.high.clip(far_smallX, 1)

    far_largeX = min(distance_far, angle_large)
    far_large = self.low.clip(1, far_largeX)

    risk_ranges = [near_small, near_large, far_small, far_large]
    risk_weights = [near_smallX, near_largeX, far_smallX, far_largeX]

    return self.cog(risk_ranges, risk_weights)

  def cog(self, ranges=[], weights=[]):
    weighted_sum = 0
    divisor = 1
    for i in range(4):
      n = int((ranges[i][1] - ranges[i][0]) // 10 )    # buggy
      divisor += weights[i] * n

      start = (ranges[i][0] // 10 + 1 ) * 10
      val = 0
      for j in range(n):
        val += start + 10*j
      
      weighted_sum += val * weights[i]
    
    return round(weighted_sum / divisor, 2)

# Helper function to test in main
def cog(ranges=[], weights=[]):
  weighted_sum = 0
  divisor = 1
  for i in range(4):
    n = int((ranges[i][1] - ranges[i][0]) // 10 )    # buggy
    divisor += weights[i] * n

    start = (ranges[i][0] // 10 + 1 ) * 10
    val = 0
    for j in range(n):
      val += start + 10*j
    
    weighted_sum += val * weights[i]
  
  return round(weighted_sum / divisor, 2)


def main():
  wall_range = [[100, 200], [120, 250]]
  speed_range = [[0, 10], [5, 20]]
  angle_range = [[0, 90], [70, 180]]
  risk_range = [[0, 50], [30, 100]]
  system = FuzzySystem(wall_range, speed_range, angle_range, risk_range)
  risk = system.bullet_risk(50, 7)
  print(risk)

  # create membership functions
  near = Membership(100, 200, True)
  far = Membership(120, 250)

  slow = Membership(0, 10, True)
  fast = Membership(5, 20)

  low = Membership(0, 50, True)
  high = Membership(30, 100)

  # inputs
  wall = 50
  speed = 7

  # fuzzify
  wall_near = near.calcY(wall)
  wall_far = far.calcY(wall)
  speed_slow = slow.calcY(speed)
  speed_fast = fast.calcY(speed)
  # print(wall_near, wall_far, speed_slow, speed_fast)

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

  risk_ranges = [near_slow, near_fast, far_slow, far_fast]
  risk_weights = [near_slowX, near_fastX, far_slowX, far_fastX]
  # cog
  output = cog(risk_ranges, risk_weights)
  print(output)


if __name__ == "__main__":
  main()
