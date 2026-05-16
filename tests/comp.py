import orbitize
import numpy as np
from orbitize import system
from orbitize.system import generate_synthetic_data
import orbitize.driver
from orbitize import sampler 
import orbitize.results
import h5py
import orbitize.results

#myDriver = orbitize.driver.Driver('{}/GJ504.csv'.format(orbitize.DATADIR), # path to data file
#                                  'OFTI', # name of algorithm for orbit-fitting
#                                  1, # number of secondary bodies in system
#                                  1.22, # total mass [M_sun]
#                                  56.95, # total parallax of system [mas]
#                                  mass_err=0.08, # mass error [M_sun]
#                                  plx_err=0.26) # parallax error [mas]

#s = myDriver.sampler
#orbits = s.run_sampler(1000)

#myResults = s.results


#sma = [x[s.system.param_idx['sma1']] for x in orbits]
#import matplotlib.pyplot as plt
#plt.hist(sma, bins=30)
#plt.xlabel('orbital semi-major axis [AU]')
#plt.ylabel('occurrence')
#plt.title("")
#corner_figure = myResults.plot_corner(param_list=['sma1', 'ecc1', 'inc1', 'aop1', 'pan1','tau1']) 
#plt.show()

#o = orbitize.results.Results()
#n = orbitize.results.Results()
#o.load_results('{}/GJ504_OFTI_1.hdf5'.format(orbitize.DATADIR))
#n.load_results('{}/GJ504_results_6.hdf5'.format(orbitize.DATADIR))

# corner_figure0 = o.plot_corner(downsample=100000,param_list=['sma1', 'ecc1', 'inc1', 'aop1', 'pan1','tau1'])
#corner_figure1 = n.plot_corner(param_list=['sma1', 'ecc1', 'inc1', 'aop1', 'pan1','tau1'])
#corner_figure = n.plot_corner(downsample=100000,param_list=['sma1', 'ecc1', 'inc1', 'aop1', 'pan1','tau1'], compresults=o)
#plt.show() 