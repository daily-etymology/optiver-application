#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
My solution to the Optiver questions.

I decided to use multiprocessing to utilise more of my computers resources and
obtain a better approximation in less time. This is possible because each 
iteration is independent.

Question 1: Solution = 4.5
Question 3: Solution = 14 (to the nearest integer)
"""
import numpy as np
import time
import multiprocessing
from boundary import surface_elipse, surface_square
import os

def make_move(start_pos, step_size = 1):
    """
    Make a random move in one of the 4 directions.
    
    Parameters
    ----------
    start_pos : 1D list with two elements
        A list with 2 points representing coordinate on the plane.
        E.g. [0,0] or [10,-2]
    step_size : integer, optional
        Size of one ant step. The default is 1.

    Returns
    -------
    list
        1D list with elements, representing new position after a random move.

    """
    if os.name == "posix":
        np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    step = np.random.choice([-step_size,step_size])
    if np.random.random() < 0.5:
        # Move X
        return [start_pos[0] + step, start_pos[1]]
    else:
        # Move Y
        return [start_pos[0], start_pos[1] + step]

def do_ant(surface, step_size = 1):
    """
    Surface agnostic solver. Travel along the surface until boundary is reached
    
    Parameters
    ----------
    surface : function reference
        Reference to a surface function. This is used to check whether ant hit
        the food boundary
    step_size : Integer, optional
        Size of one ant step. The default is 1.

    Returns
    -------
    counter : Integer
        Number of steps taken to reach the stopping criteria.

    """
    counter = 0
    current_location = [0,0]

    while 1:
        counter += 1
        current_location = make_move(current_location, step_size)
     
        if surface(current_location):
            return counter
        
        
def do_process(n_iterations, surface, step_size, send_end):
    """
    An independent worker of the distributed solver.

    Parameters
    ----------
    n_iterations : Integer
        Number of times to repeat the random walk.
    surface : Function reference
        Function reference which describes the surface.
    step_size : Integer
        Size of one ant step.
    send_end : Pipe
        Used for passing solution back to the parent process.

    Returns
    -------
    An implicit message through the pipe. Total sum used for the calculation of 
    the total average.

    """
    sol = 0
    for i in range(n_iterations):
        if i % 1000 == 0:
            print(f"\r{i} out of {n_iterations}\t{100*i/n_iterations:.2f}%",end="")
        sol += do_ant(surface, step_size = step_size) 
    send_end.send(sol)

def main():
    time_start = time.time()
    jobs = []
    pipe_list = []
    
    # Number of iterations per process
    n_iterations = 100000
    # Number of processes
    n_processes = 3
    
    question = 3 ## Either 1 or 3
    assert question in [1,3], "Invalid question number selected"
    if question == 1:
        surface = surface_square
        step_size = 1
    elif question == 3:
        surface = surface_elipse
        step_size = 10
    
    for i in range(n_processes):
        recv_end, send_end = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=do_process, 
                                    args=(n_iterations, surface, 
                                          step_size, send_end))
        jobs.append(p)
        pipe_list.append(recv_end)
        p.start()

    for proc in jobs:
        proc.join()
    result_list = [x.recv() for x in pipe_list]
    
    time_end = time.time()
    
    solution = sum(result_list)/(n_iterations*n_processes)
    
    final_string = f"""
Time elapsed:\t{time_end - time_start:.2f} seconds
processes:\t\t{n_processes}
iterations:\t\t{n_iterations}
total itrs:\t\t{n_processes*n_iterations}
Approx. sol:\t\t{solution:.3f}

Counters:\t\t{result_list}
    """
    print()
    print(final_string)

if __name__ == '__main__':
    main()