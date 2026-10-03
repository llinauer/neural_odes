"""
Newton's second law: A simple ODE
"""

import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

m = 1.0
F = -9.81
x0 = 1.
v0 = 0.
t0 = 0.
t1 = 0.3

def uniform_constant_force(t, state):
    _, v = state
    return np.array([v, F/m])


def plot_solutions(xs, t, name="", title=""):
    fig = go.Figure()

    for x, name in xs:
        fig.add_trace(go.Scatter(y=x, x=t, mode='lines+markers', name=name))
    fig.update_layout(title=dict(text=title), yaxis_zeroline=False, xaxis_zeroline=False)
    fig.show()


def animate_solutions(xs, t, title="", filename="trajectories.gif"):
    fig, ax = plt.subplots(figsize=(8, 5))

    all_x = np.concatenate([x for x, _ in xs])
    margin = 0.1 * (all_x.max() - all_x.min())

    ax.set_xlim(t[0], t[-1])
    ax.set_ylim(all_x.min() - margin, all_x.max() + margin)

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Height [m]")
    ax.set_title(title)
    ax.grid(alpha=0.3)

    lines = []
    points = []

    for x, name in xs:
        line, = ax.plot([], [], label=name)
        point, = ax.plot([], [], "o")

        lines.append(line)
        points.append(point)

    ax.legend()

    def update(frame):
        for (x, _), line, point in zip(xs, lines, points):
            line.set_data(t[:frame + 1], x[:frame + 1])
            point.set_data([t[frame]], [x[frame]])

        return lines + points

    animation = FuncAnimation(
        fig,
        update,
        frames=len(t),
        interval=50,
        blit=True
    )

    animation.save(
        filename,
        writer=PillowWriter(fps=20)
    )

    plt.close(fig)


def main():

    # start at t=0, solve until t=1
    t_span = np.array([t0, t1])
    # times at which the solution should be evaluated
    t_eval = np.linspace(t0, t1, 200)

    solutions = []
    # construct a range of different initial velocities
    for v in [0., 1., 2., 3.]:
        solution = solve_ivp(uniform_constant_force, t_span, np.array([x0, v]), t_eval=t_eval, dense_output=True)
        solutions.append((solution.y[0, :], f"x0={x0}, v0={v}"))
    #plot_solutions(solutions, solution.t, "x0=0, v0=0", "Particle position vs. time")
    animate_solutions(
        solutions,
        solution.t,
        title="Particle position vs. time",
        filename="trajectories.gif"
    )

if __name__ == "__main__":
    main()