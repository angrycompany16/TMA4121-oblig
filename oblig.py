import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as anim

def initial_condition_2d(x):
    return np.sin(x[0]) * np.sin(x[1])

X_END = np.pi
Y_END = np.pi
T_END = 1

X_STEPS = 11
Y_STEPS = 10
T_STEPS = 100

h = X_END / X_STEPS
k = Y_END / Y_STEPS
p = T_END / T_STEPS

g = p / np.power(h, 2)
v = p / np.power(k, 2)

x_values = np.linspace(0, X_END, X_STEPS)
y_values = np.linspace(0, Y_END, Y_STEPS)
t_values = np.linspace(0, T_END, T_STEPS)

x_values, y_values = np.meshgrid(x_values, y_values)

u_values = np.array([np.zeros((Y_STEPS, X_STEPS)) for _ in range(T_STEPS)])
u_values[0] = initial_condition_2d((x_values, y_values))

for n in range(1, T_STEPS):
    u_values[n, 0] = np.zeros(X_STEPS)
    u_values[n, -1] = np.zeros(X_STEPS)
    u_values[n, :, 0] = np.zeros(Y_STEPS)
    u_values[n, :, -1] = np.zeros(Y_STEPS)
    
    for i in range(1, Y_STEPS - 1):
        for j in range(1, X_STEPS - 1):            
            u_values[n, i, j] = (
                u_values[n - 1, i, j] + 
                v * (
                    u_values[n - 1, i + 1, j]
                  - 2 * u_values[n - 1, i, j]
                  + u_values[n - 1, i - 1, j]
                ) + 
                g * (
                    u_values[n - 1, i, j + 1]
                  - 2 * u_values[n - 1, i, j]
                  + u_values[n - 1, i, j - 1]
                )
            )

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(y_values, x_values, u_values[0], vmin=u_values[0].min() * 2, cmap=cm.Blues)

def update_anim(framenumber):
    ax.clear()
    ax.set_zlim(None, 1)   
    plot = ax.plot_surface(y_values, x_values, u_values[framenumber], vmin=u_values[0].min() * 2, cmap=cm.Blues)
    return plot

animation = anim.FuncAnimation(fig, func=update_anim, frames=100, interval=30, blit=False)
plt.show()