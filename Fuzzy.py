

class Membership():
  def __init__(self, xmin, xmax, isnegative=False):
    self.isnegative = isnegative
    if isnegative:
      ymin = 1
      ymax = 0
      self.b = 1
      self.a = (ymax - ymin)/(xmax - xmin)
    else:
      ymin = 0
      ymax = 1
      self.a = (ymax - ymin)/(xmax - xmin)
      self.b = ymin - self.a*xmin

  def calcY(self, x):
    res = round(self.a*x + self.b, 3)
    if res <= 0:      # clipping values smaller than 0
      res = 0
    return res

  def calcX(self, y):
    return round((y - self.b)/self.a, 3)

  def clip(self, y1, y2):
    x1 = self.calcX(y1)
    x2 = self.calcX(y2)
    return x1, x2


def cog(ranges=[], weights=[]):
  weighted_sum = 0
  divisor = 0
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
  # create membership functions
  near = Membership(0, 35, True)
  far = Membership(20, 100)

  slow = Membership(0, 10, True)
  fast = Membership(5, 20)

  low = Membership(0, 50, True)
  high = Membership(15, 100)

  # inputs
  wall = 50
  speed = 7

  # fuzzify
  wall_near = near.calcY(wall)
  wall_far = far.calcY(wall)
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
  
  print(near_slow, near_slowX)
  print(near_fast, near_fastX)
  print(far_slow, far_slowX)
  print(far_fast, far_fastX)

  risk_ranges = [near_slow, near_fast, far_slow, far_fast]
  risk_weights = [near_slowX, near_fastX, far_slowX, far_fastX]
  # cog
  output = cog(risk_ranges, risk_weights)
  print(output)


if __name__ == "__main__":
  main()