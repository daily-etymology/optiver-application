#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def surface_square(position, width = 2):
    return np.max(np.abs(position)) >= width

def surface_elipse(position):
    x, y = position
    return ((x - 2.5) / 30)**2 + ((y - 2.5) / 40)**2 >= 1


if __name__ == "__main__":
    # Test square centre
    assert surface_square([0,0]) == False, "Wrong flag for centre"
    # Test square top
    assert surface_square([0,2]) == True, "Wrong flag for top"
    # Test square bottom
    assert surface_square([0,-2]) == True, "Wrong flag for bottom"
    # Test square right
    assert surface_square([2,0]) == True, "Wrong flag for right"
    # Test square left
    assert surface_square([-2,0]) == True, "Wrong flag for right"

    # Test square top left
    assert surface_square([-2,2]) == True, "Wrong flag for top left"
    # Test square top right
    assert surface_square([2,2]) == True, "Wrong flag for top right"
    # Test square bottom left
    assert surface_square([-2,-2]) == True, "Wrong flag for bottom left"
    # Test square bottom right
    assert surface_square([2,-2]) == True, "Wrong flag for bottom right"

    # Test square far outside
    assert surface_square([-200,-200]) == True, "Wrong flag for far outside"

    # Test width parameter
    assert surface_square([-10,-10], width = 20) == False, "Wrong flag for far outside"


    # Test ellipse centre
    assert surface_elipse((0,0)) == False, "Wrong flag for elipse centre"
    # Test ellipse top inner
    assert surface_elipse((0,42)) == False, "Wrong flag for elipse top inner"
    # Test ellipse top outer
    assert surface_elipse((0,43)) == True, "Wrong flag for elipse top outer"
    # Test ellipse right inner
    assert surface_elipse((32,0)) == False, "Wrong flag for elipse right inner"
    # Test ellipse right outer
    assert surface_elipse((33,0)) == True, "Wrong flag for elipse right outer"
    # Test ellipse left inner
    assert surface_elipse((-27,0)) == False, "Wrong flag for elipse left inner"
    # Test ellipse left outer
    assert surface_elipse((-28,0)) == True, "Wrong flag for elipse left outer"
    # Test ellipse bottom inner
    assert surface_elipse((0,-37)) == False, "Wrong flag for bottom left inner"
    # Test ellipse bottom outer
    assert surface_elipse((0,-38)) == True, "Wrong flag for bottom left outer"
