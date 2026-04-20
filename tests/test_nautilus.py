"""
nautilus test
"""

import numpy as np
import pytest
import sys
import time

from orbitize import system, sampler
from orbitize.system import generate_synthetic_data


def test_nautilus_sampler():
    """
    basic
    """
    # generate synthetic data
    mtot = 1.2
    plx = 60.0
    orbit_frac = 95

    data_table, sma = generate_synthetic_data(
        orbit_frac,
        mtot,
        plx,
        num_obs=30,
    )

    # true ecc
    ecc_true = 0.5

    # initialize
    mySys = system.System(1, data_table, mtot, plx)
    lab = mySys.param_idx

    # fix all parameters except ecc
    mySys.sys_priors[lab["inc1"]] = np.pi / 4
    mySys.sys_priors[lab["sma1"]] = sma
    mySys.sys_priors[lab["aop1"]] = np.pi / 4
    mySys.sys_priors[lab["pan1"]] = np.pi / 4
    mySys.sys_priors[lab["tau1"]] = 0.8
    mySys.sys_priors[lab["plx"]] = plx
    mySys.sys_priors[lab["mtot"]] = mtot

    # initialize Nautilus sampler
    mysampler = sampler.NautilusSampler(mySys)

    # run 
    start = time.time()
    samples = mysampler.run_sampler(
        n_live=500,
        num_threads=4,
        verbose=False
    )
    end = time.time()

    print(f"Nautilus test runtime: {end - start:.3f} s")

    # get ecc posterior
    ecc_samples = mysampler.results.post[:, lab["ecc1"]]

    # check 
    assert np.median(ecc_samples) == pytest.approx(ecc_true, abs=0.1)


def test_nautilus_lnlike():
    """
    makes sure the stored lnlike matches calculated one
    """
    mtot = 1.2
    plx = 60.0
    orbit_frac = 95

    data_table, sma = generate_synthetic_data(
        orbit_frac,
        mtot,
        plx,
        num_obs=10,
    )

    mySys = system.System(1, data_table, mtot, plx)
    s = sampler.NautilusSampler(mySys)

    samples = s.run_sampler(n_live=200, num_threads=1)

    # compare lnlike
    returned_lnlike = s.results.lnlike[0]
    computed_lnlike = s._logl(samples[0])

    assert returned_lnlike == pytest.approx(computed_lnlike, abs=1e-2)


def test_nautilus_prior():
    """
    prior transform maps unit cube to valid param space
    """
    mtot = 1.2
    plx = 60.0

    data_table, _ = generate_synthetic_data(50, mtot, plx, num_obs=5)
    mySys = system.System(1, data_table, mtot, plx)

    s = sampler.NautilusSampler(mySys)

    u = np.random.rand(len(mySys.sys_priors))
    theta = s.ptform(u)

    assert len(theta) == len(u)
    assert np.all(np.isfinite(theta))


def test_nautilus_fixed():
    """
    fixed parameters
    """
    mtot = 1.2
    plx = 60.0

    data_table, sma = generate_synthetic_data(50, mtot, plx, num_obs=5)
    mySys = system.System(1, data_table, mtot, plx)
    lab = mySys.param_idx

    # fix sma
    mySys.sys_priors[lab["sma1"]] = sma

    s = sampler.NautilusSampler(mySys)

    start = time.time()
    samples = s.run_sampler(n_live=200)
    end = time.time()

    print(f"Nautilus fixed params runtime: {end - start:.3f} s")

    sma_samples = samples[:, lab["sma1"]]

    assert np.allclose(sma_samples, sma)


def test_nautilus_multithread():
    """
    multi threads 
    """
    mtot = 1.2
    plx = 60.0

    data_table, _ = generate_synthetic_data(50, mtot, plx, num_obs=10)
    mySys = system.System(1, data_table, mtot, plx)

    s = sampler.NautilusSampler(mySys)
    threadcount = [8, 4, 2, 1]
    result = {}
 
    for k in threadcount:
        start = time.time()
        samples = s.run_sampler(n_live=300, num_threads=k)
        end = time.time()
        print(f"runtime {k} threads: {end - start:.3f} s") 
        result[k] = samples 
        ecc_samples = samples[:, mySys.param_idx["ecc1"]]
        ecc_median = np.median(ecc_samples)
        ecc_true = 0.5
        assert ecc_median == pytest.approx(ecc_true, abs=0.1)


if __name__ == "__main__":
    test_nautilus_sampler()
    test_nautilus_lnlike()
    test_nautilus_prior()
    test_nautilus_fixed()
    test_nautilus_multithread()
    print("done")