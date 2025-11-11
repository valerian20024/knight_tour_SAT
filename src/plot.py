import numpy as np
import matplotlib.pylab as pl
from matplotlib import colormaps as cm


def plot_solution(solution):
	solution_array = np.array(solution)
	M, N = solution_array.shape
	fig = pl.figure(figsize = (N * 5.0 / M, 5))
	ax = pl.gca()
	chessboard = ax.table(
		cellText = solution_array,
		cellColours = np.array(
			[['white' if (i + j) % 2 == 0 else 'orange' for j in range(N)] for i in range(M)]),
			loc=(0,0),
			cellLoc='center',
			fontsize = 15)
	ax.set_xticks([])
	ax.set_yticks([])
	for i in range(M):
		for j in range(N):
			cell = chessboard[i, j]
			cell.set_height(1.0 / M)
			cell.set_width(1.0 / N)
	pl.savefig(f"solution_plot.pdf")
	#pl.show()
	return

"""
This function plots a solution using a colormap that represents
in a clear way the progression of the knight on the chessboard.
It saves the illustration in a dedicated folder.

@param solution: list of list. The solution to display.
@param name: the name of the file to save. 
"""
def rainbow_plot(solution, name):
    solution_array = np.array(solution)
    M, N = solution_array.shape

    # Normalize step values for color mapping
    steps = solution_array.flatten()
    valid_steps = steps[steps >= 0]  # ignore -1 cells
    if len(valid_steps) > 0:
        vmin, vmax = valid_steps.min(), valid_steps.max()
    else:
        vmin, vmax = 0, 1  # fallback for no solution

    norm = pl.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm['turbo']

    # Building the color matrix
    cell_colors = []
    for i in range(M):
        row = []
        for j in range(N):
            step = solution[i][j]
            if step == -1:
                row.append('lightgray')  # no solution
            else:
                rgba = cmap(norm(step))
                row.append(rgba)  # RGBA tuple
        cell_colors.append(row)

    fig = pl.figure(figsize=(N * 5.0 / M, 5))
    ax = pl.gca()
    chessboard = ax.table(
        cellText=solution_array,
        cellColours=cell_colors,
        loc=(0,0),
        cellLoc='center',
        fontsize=15)
    ax.set_xticks([])
    ax.set_yticks([])
    for i in range(M):
        for j in range(N):
            cell = chessboard[i, j]
            cell.set_height(1.0 / M)
            cell.set_width(1.0 / N)
    pl.savefig(f"{name}.pdf")

"""
This function plots all solutions using a colormap.

@param solution: A list of solutions. The solutions to display.
@param name: the name of the file to save. 
"""
def rainbow_plot_all(solutions, name):
    index = 0
    for solution in solutions:
        rainbow_plot(solution, f"{name}_{index}")
        index += 1
