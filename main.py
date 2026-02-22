# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 13:25:57 2026

@author: imarv
"""
import numpy as np

def print_field(field):
    rows,cols = field.shape
    for x in range(0,rows):
        for y in range(0,cols):
            a = field[x][y]
            print(a," ", end="")
        print()
    
def next_generation(curr_field):
    next_field = np.array(curr_field.shape,dtype=int)
    
    return
    
def count_living_neighbours():
    return    

if __name__ == "__main__":
    field = np.eye(10,dtype=int)

    print(field)
    print_field(field)    