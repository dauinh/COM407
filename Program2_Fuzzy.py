#Sylvia Le, Linh Nguyen, Uyen (Holly) Tran
#2/13/2022
#Supporting functions for the main program
import math

def dist_to_wall(angle, tracking_dist):

	dist_to_wall = 0
	
	if(angle >= 0 and angle <= 90):
		comp_angle = 90 - angle
		dist_to_wall = round(tracking_dist * math.sin(comp_angle),4)
		
	elif(angle >= 90 and angle <= 180):
		comp_angle = 180 - angle
		dist_to_wall = round(tracking_dist * math.sin(comp_angle) * (-1),4)
		
	elif(angle >= 180 and angle <= 270):
		dist_to_wall = round(tracking_dist * math.sin(-angle) * (-1),4)

	else:
		dist_to_wall = round(tracking_dist * math.sin(-angle),4)
		
	return dist_to_wall

# Calculate membership of distance to wall
def fuzzy(distance_to_wall):	
	
	# risk
	close, med, far = 0, 0, 0
	
	if distance_to_wall <= 150:
		close = -0.04 * distance_to_wall + 7
	
	elif distance_to_wall >= 150 and distance_to_wall <= 175:
		close = -0.04 * distance_to_wall + 7
		med = 0.01 * distance_to_wall - 1.5
	
	elif distance_to_wall >= 175 and  distance_to_wall <= 250:
		med = 0.01 * distance_to_wall - 1.5
		
	elif distance_to_wall >= 250 and distance_to_wall <= 350:
		med = 0.01 * distance_to_wall - 1.5
		
	elif distance_to_wall >= 350 and distance_to_wall <= 375:
		med = 0.01 * distance_to_wall - 1.5
		far = 0.02 * distance_to_wall - 7
	
	else:
		far = 0.02 * distance_to_wall - 7

	return close, med, far
	
def defuzz(d1, d2, d3):
	
	# weights of risks
	low = 20
	med = 50
	high = 80
	total = (low * d1 + med * d2 + high * d3) / (d1 + d2 + d3)
	
	return total

	
