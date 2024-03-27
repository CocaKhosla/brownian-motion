import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib import style
import math
import random

class Brownian():
    def __init__(self, v, theta, ohmega, x_border, y_border, time_step, threshold, error, iter):
        self.v = v
        self.theta = theta
        self.ohmega = ohmega
        self.x = 0
        self.y = 0
        self.x_border = x_border
        self.y_border = y_border
        self.time_step = time_step
        self.traj = [(self.x, self.y, 'moving')]
        self.threshold = threshold
        self.error = error
        self.iter = iter

    def rotate(self, time, total_time):

        new_angle = 0
        temp_x = self.x + self.v * math.cos(self.theta) * self.time_step * 50
        temp_y = self.y + self.v * math.sin(self.theta) * self.time_step * 50
        
        if temp_x <= -1 * self.x_border:
            new_angle = random.uniform(-math.pi / 2, math.pi/2)
        
        elif temp_x >= self.x_border:
            new_angle = random.uniform(math.pi/2, 3*math.pi/2)

        elif temp_y <= -1 * self.y_border:
            new_angle = random.uniform(0, math.pi)
        
        else:
            new_angle = random.uniform(-math.pi, 0)
        
        while (abs(new_angle - self.theta) > self.error and time < total_time):
            # print(time)
            if new_angle > self.theta:
                self.theta += self.ohmega * self.time_step
            else:
                self.theta -= self.ohmega * self.time_step
            time += time_step
            self.traj.append((self.x, self.y, 'rotating'))
        return time

    def move(self, total_time):
        time = 0
        rotated = False
        # last = -1
        while (time < total_time):

            # print(f'{self.x}, {self.y}, {self.theta}')
            time += time_step
            dist_x = self.v * math.cos(self.theta) * self.time_step
            dist_y = self.v * math.sin(self.theta) * self.time_step
            if (abs(self.x + dist_x) >= self.x_border or abs(self.y + dist_y) >= self.y_border) and rotated:
                rotated = False
                time = self.rotate(time, total_time)
            else:
                self.x += dist_x
                self.y += dist_y
                if abs(self.x) < self.x_border and abs(self.y) < self.y_border:
                    rotated = True
                    self.traj.append((self.x, self.y, 'moving'))
                else:
                    self.traj.append((self.x, self.y, 'rotating'))
            
        # print('time')
        # print(time)
    def plot(self):
        style.use('fivethirtyeight')

        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        def animate(i):
            ax1.clear()
            ax1.set_xlim(left=-1*self.x_border, right=self.x_border)
            ax1.set_ylim(bottom=-1*self.y_border, top=self.y_border)
            ax1.set_title(self.traj[i][2])
            ax1.set_facecolor("#e1ddbf")

            ax1.spines['top'].set_visible(True)
            ax1.plot(self.traj[i][0], self.traj[i][1], marker="o")
        ani = animation.FuncAnimation(fig, animate, frames=len(self.traj), interval=50)
        ani.save(filename=f"brownian_motion{self.iter}.gif", writer="pillow")

if __name__=='__main__':
    v = 1
    theta = random.uniform(0, 2 * math.pi)
    ohmega = 1
    x_border = 1
    y_border = 1
    total_time = 30
    time_step = 0.05
    threshold = 0.5
    error = 0.05
    number_of_iter = 4
    for i in range(number_of_iter):
        print(f'{i+1}th stage')
        ego_vehicle = Brownian(v, theta, ohmega, x_border, y_border, time_step, threshold, error, i)
        ego_vehicle.move(total_time)
        ego_vehicle.plot()