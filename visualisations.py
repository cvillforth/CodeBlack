import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive, widgets
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

## Here, we are defining some parameters
G = 6.67e-11 #units are m^3 kg^-1 s^-2
M_sun = 1.99e30 #units is kg
au = 1.5e11 # the distance of the earth to the sun in m
ly = 9.46e15 # lightyear in m
c = 2.998e8 # speed of light in m/s 

def kepler_velocity(a, M):
    """
    This function calculated the velocity given a semi-major axis a and mass of the central object M.
    a: semi-major axis in meters
    M: central mass in kg
    returns: velocity in m/s
    """
    v = np.sqrt(G*M/a)
    return v

def schwarzschild(Mbh):
    """
    This function calculated the Schwarzschild radius of a black hole
    MBh: black hole mass in kg
    returns: Schwarzschild radius in m
    """
    rs = 2*G*Mbh/(c**2)
    return rs

def bh_interactive(manual=True):
    #setting the scale over which we will look at the rotation velocity.
    #min_r = 0.01
    max_r = 100

    ##We will not be looking at distances in meters, instead, lets use astronimcal units
    scale_by = au
    scale_by_name = 'Astronomical Units'

    def f(r_blr, bhmass):
        #creating the figure
        plt.figure(2)
        ##Calculate the schwarzschild radius
        r_s = schwarzschild(10**(bhmass)*M_sun)/scale_by
        ##creates an array of distances
        x = np.linspace(r_s, max_r, num=1000)
        ## calculates keplerian velocity
        v_ar = kepler_velocity(x*scale_by, 10**(bhmass)*M_sun)/1000
        ##plots the Keplerian rotation curve
        plt.plot(x, v_ar, c='grey')
        ##calculates and markes the current radius and velocity
        plt.axvline(r_blr, c='r', ls='--')
        if r_blr >= r_s:
            v = kepler_velocity(r_blr*scale_by, 10**(bhmass)*M_sun)/1000
        else:
            v = kepler_velocity(r_s*scale_by, 10**(bhmass)*M_sun)/1000
        plt.axhline(v, c='r', ls='--')
        plt.plot([r_blr], [v], marker='*', c='r', ms=20)
        ##Calculate the schwarzschild radius
        r_s = schwarzschild(10**(bhmass)*M_sun)/scale_by
        plt.text(1.1*r_s, 0.9*max(v_ar), "Schwarzschild Radius", rotation=90, ha='left', va='top', c='m', weight='bold')
        plt.axvline(r_s, c='m')
        plt.axvline(0, c='m')
        plt.gca().add_patch(Rectangle((0,0),r_s,1.2*max(v_ar),fill=True, color='m', alpha=0.5, zorder=100))
        if r_blr > r_s:
            plt.text(0.25*max_r, 0.8*max(v_ar),
                     "You are at %.2f %s \n from a %.2f Million Solar mass black hole \n and are rotating at %.2f km/s"
                     %(r_blr, scale_by_name, 10**(bhmass)/1e6, v), weight='bold')
        else:
            plt.text(0.25*max_r, 0.8*max(v_ar),"You have fallen into the black hole!", weight='bold', c='r')
        plt.xlim(0,max_r)
        plt.xlabel("Distance from BH (in %s)" % scale_by_name)
        plt.ylabel("Velocity or objects orbiting (in km/s)")
        plt.show()
    
    blr_slider = widgets.FloatSlider(
        value=max_r,
        min=0,
        max=max_r,
        step=0.1,
        description='distance from BH',
        disabled=False,
        continuous_update=True,
        orientation='horizontal',
        readout=True,
        readout_format='.1f')

    bhmass_slider = widgets.FloatSlider(
        value=7,
        min=6,
        max=9,
        step=0.1,
        description='BH mass (log)',
        disabled=False,
        continuous_update=True,
        orientation='horizontal',
        readout=True,
        readout_format='.1f')

    interactive_plot = interactive(f, {'manual': manual}, r_blr=blr_slider, bhmass=bhmass_slider)
    return(interactive_plot)