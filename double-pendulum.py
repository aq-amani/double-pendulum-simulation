from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from collections import deque

import matplotlib.colors as mplcolors

import argparse

dt = 0.01
time_points = []
G = 9.8
history_len = 200 # Number of trajectory points to display

class Pendulum:

    def derivs(self, state, t):

        M1 = self.M1
        M2 = self.M2
        L1 = self.L1
        L2 = self.L2
        dydx = np.zeros_like(state)
        dydx[0] = state[1]

        delta = state[2] - state[0]
        den1 = (M1+M2) * L1 - M2 * L1 * cos(delta) * cos(delta)
        dydx[1] = ((M2 * L1 * state[1] * state[1] * sin(delta) * cos(delta)
                    + M2 * G * sin(state[2]) * cos(delta)
                    + M2 * L2 * state[3] * state[3] * sin(delta)
                    - (M1+M2) * G * sin(state[0]))
                   / den1)

        dydx[2] = state[3]

        den2 = (L2/L1) * den1
        dydx[3] = ((- M2 * L2 * state[3] * state[3] * sin(delta) * cos(delta)
                    + (M1+M2) * G * sin(state[0]) * cos(delta)
                    - (M1+M2) * L1 * state[1] * state[1] * sin(delta)
                    - (M1+M2) * G * sin(state[2]))
                   / den2)

        return dydx

    def __init__(self, M1, M2, L1, L2, th1, w1, th2, w2):
        self.state = np.radians([th1, w1, th2, w2])
        self.L1 = L1
        self.L2 = L2
        self.L = L1+L2 # maximal length of the combined pendulum
        self.M1 = M1
        self.M2 = M2

        # integrate ODE using scipy.integrate.
        self.y = integrate.odeint(self.derivs, self.state, time_points)

        self.x1 = L1*sin(self.y[:, 0])
        self.y1 = -L1*cos(self.y[:, 0])
        self.x2 = L2*sin(self.y[:, 2]) + self.x1
        self.y2 = -L2*cos(self.y[:, 2]) +self.y1
        self.history_x, self.history_y = deque(maxlen=history_len), deque(maxlen=history_len)

    def update(self, i):
        thisx = [0, self.x1[i], self.x2[i]]
        thisy = [0, self.y1[i], self.y2[i]]

        if i == 0:
            self.history_x.clear()
            self.history_y.clear()

        self.history_x.appendleft(thisx[2])
        self.history_y.appendleft(thisy[2])
        return thisx, thisy, self.history_x, self.history_y

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value





P = []
lines = []
traces = []

def init_data(pendulum_count, initial_condition_delta, simulation_stop_time):
    global fig
    global ax
    global time_points
    global m
    global lines
    global traces
    global time_text

    time_points = np.arange(0, simulation_stop_time, dt)
    for i in range(pendulum_count):
        # th1 and th2 are the initial angles (degrees CCW from the perpendicular)
        # w1 and w2 are the initial angular velocities (degrees per second)
        p = Pendulum(M1=1.0, M2=1.0, L1=2, L2=2, th1=120.0-i*initial_condition_delta , w1=0.0, th2=-10.0, w2=0.0)
        P.append(p)
    L = P[0].L
    axis_limit = L + 1

    fig = plt.figure(dpi=300)
    fig.patch.set_facecolor('black')
    fig.tight_layout()

    ax = fig.add_subplot(autoscale_on=False, xlim=(-axis_limit, axis_limit), ylim=(-axis_limit, np.ceil(axis_limit/2)))
    ax.set_aspect('equal')
    ax.grid(False)
    ax.set_facecolor('black')

    norm = mplcolors.Normalize(0, pendulum_count - 1)
    m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
    count = 0
    for p in P:
        #Pendulums
        line, = ax.plot([], [], 'o-', lw=2, color=m.to_rgba(count))
        lines.append(line)
        #Traces
        trace, = ax.plot([], [], '-', lw=0.5, ms=2, color=m.to_rgba(count))
        traces.append(trace)
        count += 1

    time_text = plt.figtext(0.02, 0.85, '', c = 'white', fontsize=7) if save_video else ax.text(0.05, 0.85, '', transform=ax.transAxes, color='white', va = 'bottom', fontsize=5)

def animate(i):

    count = 0
    for p in P:
        thisx, thisy, history_x, history_y = p.update(i)
        #Pendulums
        lines[count].set_data(thisx, thisy)
        #Traces
        traces[count].set_data(history_x, history_y)
        count += 1

    time_text.set_text(f'Time = {round((i*dt), 2)}s\nPendulum count = {pendulum_count}\nInitial condition delta = {initial_condition_delta}' )
    return tuple(lines) + tuple(traces) + (time_text,)

def main():
    global save_video
    global initial_condition_delta
    global pendulum_count
    parser = argparse.ArgumentParser(description='Double pendulum simulator')


    parser.add_argument('-n','--count', help='Pendulum count', default = 5, type = int, metavar = '')
    parser.add_argument('-d','--delta', help='Initial condition delta', default = 0.005, type = float, metavar = '')
    parser.add_argument('-v','--video', help='Create a video file of the animation', action ='store_true')
    parser.add_argument('-t','--time', help='Number of seconds to simulate', default = 30, type = float, metavar = '')

    args = vars(parser.parse_args())
    pendulum_count = args['count']
    initial_condition_delta = args['delta']
    save_video = args['video']
    simulation_stop_time = args['time']

    init_data(pendulum_count, initial_condition_delta, simulation_stop_time)
    ani = animation.FuncAnimation(fig, animate, len(P[0].y), interval=dt*1000, blit=(not save_video), repeat = False)
    if save_video:
        import time
        filename = f'{time.strftime("%Y%m%d%H%M%S")}_n{pendulum_count}_d{initial_condition_delta}_t{simulation_stop_time}.mp4'
        ani.save(filename, writer="ffmpeg", dpi=300, fps=100)
    else:
        plt.show()


if __name__ == "__main__":
    main()

