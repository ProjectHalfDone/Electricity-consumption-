#@ Skipper Seabold
#
# http://jseabold.net/blog/2012/02/23/wavelet-regression-in-python/

import numpy as np

def coef_pyramid_plot(coefs, first=0, scale='uniform', ax=None):
    """
    Parameters
    ----------
    coefs : array-like wavelet coefficients. Expects an iterable in order Cdn, Cdn-1, ..., Cd1, Cd0

    first: int, optional
        The first level to plot. 0 is top level.

    scale: str (uniform, level), optional
        Scale the coefficients using the same scale or independently by level.

    ax: Axes, potional
        Matplotlib Axes instance

    Returns
    -------
    Figure: Matplotlib figure instance
        Either the parent figure of 'ax' or a new pyplot.Figure instance if 'ax' id None.
      
    """

    if ax is None:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111,facecolor='lightgrey')
    else:
        fig = ax.figure

    n_levels = len(coefs)
    n = 2**(n_levels-1) #assumes periodic

    if scale == 'uniform':
        biggest = [np.max(np.absolute(np.hstack(coefs)))] * n_levels
    else:
        #multiply by 2 so the biggest bars only take up .5
        biggest = [np.max(np.abs(i))* 2 for i in coefs]

    for i in range(first, n_levels):
        x = np.linspace(2**(n_levels - 2 - i), n - 2**(n_levels - 2 - i), 2**i)
        ymin = n_levels - i -1 + first
        yheight = coefs[i]/biggest[i]
        ymax = yheight + ymin
        #plots lines at y value
        ax.vlines(x, ymin, ymax, linewidth=1.1)

    ax.set_xlim(0,n)
    ax.set_ylim(first - 1, n_levels)
    ax.yaxis.set_ticks(np.arange(n_levels-1, first-1, -1))
    ax.yaxis.set_ticklabels(np.arange(first, n_levels))
    ax.tick_params(top=False, right=False, direction='out', pad=6)
    ax.set_ylabel("Levels", fontsize=14)
    ax.grid(True, alpha=.85, color="white", axis='y', linestyle='-')
    ax.set_title('Wavelet Detail Coefficients', fontsize=16, position=(.5,1.05))

    fig.subplots_adjust(top=.89)

    return fig
        
   
#Wavelet families
def doppler(x):
    """
    Parameters
    ----------
    x : array-like
        Domain of x is in (0,1]
 
    """
    if not np.all((x >= 0) & (x <= 1)):
        raise ValueError("Domain of doppler is x in (0,1]")
    return np.sqrt(x*(1-x))*np.sin((2.1*np.pi)/(x+.05))
 
def blocks(x):
    """
    Piecewise constant function with jumps at t.
 
    Constant scaler is not present in Donoho and Johnstone.
    """
    K = lambda x : (1 + np.sign(x))/2.
    t = np.array([[.1, .13, .15, .23, .25, .4, .44, .65, .76, .78, .81]]).T
    h = np.array([[4, -5, 3, -4, 5, -4.2, 2.1, 4.3, -3.1, 2.1, -4.2]]).T
    return 3.655606 * np.sum(h*K(x-t), axis=0)
 
def bumps(x):
    """
    A sum of bumps with locations t at the same places as jumps in blocks.
    The heights h and widths s vary and the individual bumps are of the
    form K(t) = 1/(1+|x|)**4
    """
    K = lambda x : (1. + np.abs(x)) ** -4.
    t = np.array([[.1, .13, .15, .23, .25, .4, .44, .65, .76, .78, .81]]).T
    h = np.array([[4, 5, 3, 4, 5, 4.2, 2.1, 4.3, 3.1, 2.1, 4.2]]).T
    w = np.array([[.005, .005, .006, .01, .01, .03, .01, .01, .005, .008, .005]]).T
    return np.sum(h*K((x-t)/w), axis=0)
 
def heavisine(x):
    """
    Sinusoid of period 1 with two jumps at t = .3 and .72
    """
    return 4 * np.sin(4*np.pi*x) - np.sign(x - .3) - np.sign(.72 - x)
