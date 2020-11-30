from scipy import *
from numpy import sin, cos
import numpy as np
import pygame
import sys

pygame.init()       # Initialize the Pygame Library for Animation

# Some parameter to initialize the simulation for Simple Pendulum
# Simple pendulum follows the simple harmonic motion which is represnted by the folowing equation:
#
#           theta.. = - (g/l) * sin(theta)
#
ts = .01 		    # Time step size in seconds (delta t)
td = 5 * 60 		# Trial duration in minutes (How long should simulation run?)
te = int(td/ts) 	# No. of timesteps in trial duration (integer)

mu = 0.001 		    # Friction factor
m = 1 			    # Mass of the bob
g = 9.81 		    # Gravitational acceleration


th = [pi/2]		    # Initial angle in radians
om = [1] 		    # Initial angular velocity i.e. First Derivative of Theta(th)
u = 0 			    # Initial Torque

# Some parameters to draw animation of simple pendulum
SCREEN_SIZE = 500
BOB_SIZE = 16

# To open a window of size 640,480, use the statement below.
# Create a blank screen of defined size
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
# To set caption on screen
pygame.display.set_caption('Simple Pendulum Simulation')

# Pivot point to hang the bob
PIVOT = (SCREEN_SIZE/2, SCREEN_SIZE/9)
# Length of the string
l = PIVOT[1] * 4

# Color codes to be used in animation
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

clock = pygame.time.Clock()
# For timer on pygame simultaion
font = pygame.font.SysFont('Arial', 25)


class RealTime():

    def __init__(self, ts, td, te, mu, m, g, l, th, om, u):
        self._ts = ts
        self._td = td
        self._te = te
        self._mu = mu
        self._m = m
        self._g = g
        self._l = l
        self._th = th
        self._om = om
        self._u = u

    # Fourth order Runge Kutta (RK4) to differentiate the simple pendulum equation motion
    def run(self):
        for j in range(self._te):
            # Euler approximation
            self._th.append(self._th[j] + self._ts * self._om[j])
            f1 = (-self._mu * self._om[j] + self._m * self._g *
                  self._l * sin(self._th[j]) + self._u)/(self._m*(self._l ^ 2))
            self._om.append(self._om[j] + self._ts * f1)

            # Approximation 1 at mid-interval
            th2 = self._th[j+1] + (self._ts/2) * self._om[j+1]
            f2 = (-self._mu * self._om[j+1] + self._m * self._g *
                  self._l * sin(self._th[j+1]) + self._u)/(self._m*(self._l ^ 2))
            om2 = self._om[j+1] + (self._ts/2) * f2

            # Approximation 2 at mid-interval
            th3 = th2 + (self._ts/2) * om2
            f3 = (-self._mu * om2 + self._m * self._g * self._l *
                  sin(th2) + self._u)/(self._m * (self._l ^ 2))
            om3 = om2 + (self._ts/2) * f3

            # Approximation at next time step
            th4 = th3 + (self._ts) * om3
            f4 = (-self._mu * om3 + self._m * self._g * self._l *
                  sin(th3) + self._u)/(self._m * (self._l ^ 2))
            om4 = om3 + (self._ts) * f4

            dth = (self._om[j] + 2 * self._om[j+1] + 2 * om2 + om3)/6
            dom = (f1 + 2 * f2 + 2 * f3 + f4)/6
            self._th[j+1] = self._th[j] + self._ts * dth
            self._om[j+1] = self._om[j] + self._ts * dom
            yield self._th[j]

    # Calculate the position of bob from the given angle theta using the equation: x = x_ini + l * sin(theta)  & y = y_ini - l * cos(theta)
    def getPosition(self, theta):
        x = PIVOT[0] + self._l * np.sin(theta)   # x is in positive direction
        y = PIVOT[1] - self._l * np.cos(theta)   # y is in negative direction
        return [int(x), int(y)]

    # Function to animate the motion of pendulum (visualization)

    def Animate(self, theta):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            # RK4 acts as a generator and using next() subsequent angles can be obtained
            pos = self.getPosition(theta.next())
            screen.fill(black)
            # Converting milliseconds to seconds
            time_clock = pygame.time.get_ticks()/1000
            format_time = '{0:02d}'.format(time_clock)
            screen.blit(font.render('Time (s): ' +
                                    format_time, True, green), (400, 20))
            pygame.draw.lines(screen, white, False, [
                              (0, PIVOT[1]), (SCREEN_SIZE, PIVOT[1])], 2)
            pygame.draw.circle(screen, red, PIVOT, 3, 3)
            pygame.draw.lines(screen, red, False, [PIVOT, (pos[0], pos[1])], 2)
            pygame.draw.circle(
                screen, green, (pos[0], pos[1]), BOB_SIZE, BOB_SIZE)
            pygame.display.flip()

        clock.tick(120)


# Instantiate the simGen class to create an instance of simulation
RealTime = RealTime(ts, td, te, mu, m, g, l, th, om, u)
theta = RealTime.run()

if __name__ == '__main__':
    RealTime.Animate(theta)
