from time import time
import os
import numpy as np
import solution_template as st
import matplotlib.pylab as pl
from matplotlib import colormaps as cm
from knight_tour import *

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

"""
This script generates many solutions and compares timing between the efficient 
and naive solutions.
"""
def timing_test_script():

    def test(m, n, i0, j0, mode):
        dir_path = f"figs/test/{mode}/{m}x{n}/"
        filename = f"{i0}_{j0}"
        path = dir_path + filename
        os.makedirs(dir_path, exist_ok=True)

        start = time()
        solver, var = build_knight_tour(m, n, i0, j0, mode)
        solution, res = extract_solution(solver, m, n, m * n, var)
        end = time()

        if res: 
            rainbow_plot(solution, path)

        return start, end, res

    M = [0, 3, 4, 5, 6, 7]
    N = M

    for m in M:
        for n in N:
            if m <= n:  # avoid to repeat 3x7 and 7x3 solutions
                for i0 in range(m):
                    for j0 in range(n):
                        start_n, end_n, res_n = test(m, n, i0, j0, 'n')
                        start_sc, end_sc, res_sc = test(m, n, i0, j0, 'sc')
                        
                        time_sc = end_sc - start_sc
                        time_n = end_n - start_n
                        
                        print(f"Test {m}x{n}@({i0},{j0})")
                        print(f"  sc: {time_sc}, {res_sc}")
                        print(f"  n : {time_n}, {res_n}")
                        print(f"  BETTER" if time_n > time_sc and res_n and res_sc else "  Meh")
                        
                        

if __name__ == '__main__':

    # Question 1
    #rainbow_plot(st.question1(3, 4, 0, 0)[0], "figs/test/test_rainbow_plot") # custom made
    #rainbow_plot_all(st.question1(3, 4, 0, 0)[0], "figs/test/testrainbowplotall") # plotting all solutions

    #timing_test_script()

    rainbow_plot(st.question1(3, 3, 1, 1)[0], "figs/manual/test_3x3@(1, 1)")

    #plot_solution(st.question1(5, 5, 0, 0)[0]) # there should be a solution
    #plot_solution(st.question1(3, 7, 0, 0)[0]) # there should be a solution
    #plot_solution(st.question1(7, 5, 3, 1)[0]) # there should be a solution
    #plot_solution(st.question1(4, 4, 0, 0)[0]) # there should not be a solution

    # Question 2
    #plot_solution(st.question1(8, 8, 0, 0)[0])

    # Question 3
    #print("Number of solutions for a 3x4 chessboard: " + str(st.question3()))

    # Question 4
    #print("Number of solutions for a 3x4 chessboard, up to symmetry: " + str(st.question4()))

    # Question 5
    #print(st.question5(4, 4, 0, 0)) # should be the empty list
    #print(st.question5(3, 4, 1, 3))
    #print(st.question5(3, 4, 1, 3)) # should not systematically give the same result as the previous call
