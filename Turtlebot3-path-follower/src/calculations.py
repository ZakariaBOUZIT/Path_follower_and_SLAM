#!/usr/bin/env python3

import sympy
from sympy import symbols, Function, sqrt
import math

def calculate_velocity(T_val, H_val, W_val):
    W, H, T, t = symbols(r'W, H, T, t') 

    v = Function(r'v')(t)
    x = Function(r'x')(t)
    y = Function(r'y')(t)
    theta = Function(r'theta')(t)

    #x = (W/2)*sympy.sin(2*math.pi*t/T) # a function for the component x(t) of the figure-eight trajectory
    #y = (H/2)*sympy.sin(4*math.pi*t/T) # a function for the component y(t) of the figure-eight trajectory

    #Circle
    x = sympy.cos(t)
    y = sympy.sin(t)

    # taking a derivative
    xdot = x.diff(t)
    ydot = y.diff(t)

    xddot = xdot.diff(t)
    yddot = ydot.diff(t)


    # from the kinematic equations  xdot = v*cos(theta)
    #                               ydot = v*sin(theta) we get:
    v = sqrt(xdot**2 + ydot**2)
    theta = sympy.atan2(ydot, xdot)

    thetadot = theta.diff(t)        # derivative d/dt of theta(t) 
    omega = thetadot                # defining omega
    
    v = sympy.simplify(v.subs([(W, W_val), (H, H_val), (T, T_val)]))
    omega = sympy.simplify(omega.subs([(W, W_val), (H, H_val), (T, T_val)]))
    x = sympy.simplify(x.subs([(W, W_val), (H, H_val), (T, T_val)]))
    xdot = sympy.simplify(xdot.subs([(W, W_val), (H, H_val), (T, T_val)]))
    xddot = sympy.simplify(xddot.subs([(W, W_val), (H, H_val), (T, T_val)]))
    y = sympy.simplify(y.subs([(W, W_val), (H, H_val), (T, T_val)]))
    ydot = sympy.simplify(ydot.subs([(W, W_val), (H, H_val), (T, T_val)]))
    yddot = sympy.simplify(yddot.subs([(W, W_val), (H, H_val), (T, T_val)]))

    """
    This gives us functions of time
    """

    return x, y, xdot, ydot, xddot, yddot, v, omega


class FigureEight():
    def __init__(self, T_val, H_val, W_val):
        self._x, self._y, self._xdot, self._ydot, self._xddot, self._yddot, self._v, self._omega = calculate_velocity(T_val, H_val, W_val)
        self._t = symbols(r't')

    def get_velocity(self, time_step):

        x = self._x.subs(self._t, time_step)
        y = self._y.subs(self._t, time_step)
        v = self._v.subs(self._t, time_step)
        omega = self._omega.subs(self._t, time_step)
        return x, y, v, omega
