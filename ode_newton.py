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


def animate_solutions_with_particles(xs, t, title="", filename="trajectories.gif", fps=50):
    fig, (ax_plot, ax_drop) = plt.subplots(
        1, 2,
        figsize=(10, 5),
        gridspec_kw={"width_ratios": [3, 1]}
    )

    all_x = np.concatenate([x for x, _ in xs])
    span = all_x.max() - all_x.min()
    margin = 0.1 * span if span > 0 else 0.1

    y_min = all_x.min() - margin
    y_max = all_x.max() + margin

    # Left: x(t) plot
    ax_plot.set_xlim(t[0], t[-1])
    ax_plot.set_ylim(y_min, y_max)
    ax_plot.set_xlabel("Time [s]")
    ax_plot.set_ylabel("Height [m]")
    ax_plot.set_title(title)
    ax_plot.grid(alpha=0.3)

    # Right: falling particles
    particle_x_positions = np.arange(len(xs))
    ax_drop.set_xlim(-0.5, len(xs) - 0.5)
    ax_drop.set_ylim(y_min, y_max)
    ax_drop.set_xticks(particle_x_positions)
    ax_drop.set_xticklabels([])
    ax_drop.set_title("Particles")
    ax_drop.grid(alpha=0.2, axis="y")
    ax_drop.axhline(0, linewidth=1)

    lines = []
    points = []
    particles = []

    for i, (x, name) in enumerate(xs):
        line, = ax_plot.plot([], [], label=name)
        color = line.get_color()

        point, = ax_plot.plot([], [], "o", color=color)
        particle, = ax_drop.plot([particle_x_positions[i]], [x[0]], "o", color=color, markersize=12)

        lines.append(line)
        points.append(point)
        particles.append(particle)

    ax_plot.legend(loc="upper left")

    def update(frame):
        artists = []

        for i, ((x, _), line, point, particle) in enumerate(zip(xs, lines, points, particles)):
            line.set_data(t[:frame + 1], x[:frame + 1])
            point.set_data([t[frame]], [x[frame]])
            particle.set_data([particle_x_positions[i]], [x[frame]])

            artists.extend([line, point, particle])

        return artists

    animation = FuncAnimation(
        fig,
        update,
        frames=len(t),
        interval=1000 / fps,
        blit=True
    )

    animation.save(filename, writer=PillowWriter(fps=fps))
    plt.close(fig)


def main():

    # start at t=0, solve until t=1
    t_span = np.array([t0, t1])
    # times at which the solution should be evaluated
    t_eval = np.linspace(t0, t1, 500)

    solutions = []
    # construct a range of different initial velocities
    for v in [0., 1., 2., 3.]:
        solution = solve_ivp(uniform_constant_force, t_span, np.array([x0, v]), t_eval=t_eval, dense_output=True)
        solutions.append((solution.y[0, :], f"x0={x0}m, v0={v} $m/s²$"))
    #plot_solutions(solutions, solution.t, "x0=0, v0=0", "Particle position vs. time")
    animate_solutions_with_particles(
        solutions,
        solution.t,
        title="Particle position vs. time",
        filename="trajectories.gif"
    )

if __name__ == "__main__":
    main()