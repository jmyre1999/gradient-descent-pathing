from vpython import *
from time import sleep
import numpy as np

cyl_pts = [
	[4.83235, -14.8836],
	[-6.3787, -19.9093],
	[-12.7574, -4.83235],
	[13.144, -4.63905],
	[9.85799, 9.27811],
	[-11.0177, 13.5306],
	[0.5578, 19.1361]
]

ball_pts = [
	[0, -30],
	[0, 30],
	[15, -30],
	[-15, -30],
	[15, 30],
	[-15, 30],
]

colors = [
	color.yellow,
	color.blue,
	color.purple,
	color.cyan,
	color.orange,
	color.black,
]

def gradient_descent(scene):
	if scene.goal and scene.goal.visible:
		while scene.is_pathing:
			g = np.array([
						[scene.goal.pos.x],
                        [scene.goal.pos.y]
						])
			num_ball = 0
			for ball in scene.balls:
				if ball.is_pathing == True:
					v = np.array([
	                        [ball.pos.x],
	                        [ball.pos.y]
	                        ])
					step = grad(v, g, scene.obstacles, scene.balls)
					ball.pos.x = v.item(0) - (0.25)*step.item(0)
					ball.pos.y = v.item(1) - (0.25)*step.item(1)
					if np.linalg.norm( v - g ) <= 4:
						ball.is_pathing = False
				status = []
				for ball in scene.balls:
					status.append(ball.is_pathing)
				if not True in status:
					scene.caption = 'Reached goal'
					scene.goal.visible = False
					scene.is_pathing = False
			sleep(.001)
	return

def grad(p, g, obstacles, balls):
	y1 = np.add(p, np.array([
					[0],
                    [1]
					]))
	y2 = np.add(p, np.array([
					[0],
                    [-1]
					]))

	x1 = np.add(p, np.array([
					[1],
                    [0]
					]))
	x2 = np.add(p, np.array([
					[-1],
                    [0]
					]))

	cx = pathplan(x1, g, obstacles, balls) - pathplan(x2, g, obstacles, balls)
	cy = pathplan(y1, g, obstacles, balls) - pathplan(y2, g, obstacles, balls) 

	r = np.array([[cx], [cy]])

	return np.divide(r, np.linalg.norm(r)) 

def pathplan(p, g, obstacles, balls):

	# Goal cost (Euclidean distance squared)
	distance = np.linalg.norm(p - g) 
	c1 = distance*distance

	# Collision cost
	c2 = 0
	for obstacle in obstacles:
		o = np.array([
				     [obstacle.pos.x],
				     [obstacle.pos.y]
				     ])
		distance = np.linalg.norm(p - o)
		if distance <= obstacle.radius+2:
			c2 = c2 + log((obstacle.radius+2) / distance)

	# Ball cost
	c3 = 0
	for ball in balls:
		b = np.array([
				     [ball.pos.x],
				     [ball.pos.y]
				     ])
		if not np.array_equal(p, b):
			distance = np.linalg.norm(p - b)
			if distance <= ball.radius+1:
				c3 = c3 + log((ball.radius+1) / distance)

	return c1 + 800*c2 + 400*c3

def print_pos(e):
	print(e.pos)
	place_cylinder(e.pos.x, e.pos.y)
	return


# Sets the current goal position and begins pathing if stationary
def set_goal(e):
	if(e.pos.x <= 25 and e.pos.x >= -25 and e.pos.y <= 35 and e.pos.y >= -35):
		e.canvas.caption = "Pathing..."
		for ball in e.canvas.balls:
			ball.is_pathing = True
		if e.canvas.goal:
			e.canvas.goal.pos.x = e.pos.x
			e.canvas.goal.pos.y = e.pos.y
			e.canvas.goal.visible = True
		else:
			e.canvas.goal = box(pos=vector(e.pos.x,e.pos.y,0.25), height=1, width=0.25, length=1, color=color.green)
		if e.canvas.is_pathing == False:
			e.canvas.is_pathing = True
			gradient_descent(e.canvas)
	else:
		e.canvas.is_pathing = False
		if e.canvas.goal:
			e.canvas.goal.visible = False
		e.canvas.caption = 'Error: Location out of bounds'
	return

# Places a cylinder obstacle at position x,y in the current scene
def place_cylinder(x, y):
	cyl = cylinder(pos=vector(x, y, 0), radius=3, length=5, color=color.red, axis=vector(0,0,1))
	return cyl

def place_ball(x, y, c):
	ball = sphere(pos=vector(x, y, 1.25), radius=1, color=c, make_trail=True)
	return ball

def main():
	# Initialize scene
	scene = canvas()
	# Set goal attribute
	scene.goal = None
	scene.is_pathing = False
	box(pos=vector(0,0,0), height=70, width=0.5, length=50)
	scene.obstacles = []
	for pt in cyl_pts:
		cyl = place_cylinder(pt[0], pt[1])
		scene.obstacles.append(cyl)
	scene.balls = []
	count = 0
	for pt in ball_pts:
		ball = place_ball(pt[0], pt[1], colors[count])
		scene.balls.append(ball)
		count = count + 1
	scene.bind('mousedown', set_goal)
	return

main()