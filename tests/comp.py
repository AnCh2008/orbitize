import orbitize
import numpy as np
from orbitize import system
from orbitize.system import generate_synthetic_data
import orbitize.driver
from orbitize import sampler 
import orbitize.results
import h5py
import orbitize.results
o = orbitize.results.Results()
n = orbitize.results.Results()
o.load_results('{}/GJ504_OFTI_1.hdf5'.format(orbitize.DATADIR))
n.load_results('{}/GJ504_results_6.hdf5'.format(orbitize.DATADIR))

corner_figure0 = o.plot_corner(downsample=100000,param_list=['sma1', 'ecc1', 'inc1', 'aop1', 'pan1','tau1'])
corner_figure1 = n.plot_corner(param_list=['sma1', 'ecc1', 'inc1', 'aop1', 'pan1','tau1'])
corner_figure = n.plot_corner(downsample=100000,param_list=['sma1', 'ecc1', 'inc1', 'aop1', 'pan1','tau1'], compresults=o)
#plt.show() 