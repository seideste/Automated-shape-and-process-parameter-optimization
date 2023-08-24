import pyvista as vtki
import numpy as np
import pandas as pd
import sys
from scipy.optimize import curve_fit
from scipy import stats
import scipy
import math
import copy
import sys
import vtk
import time
from vtk.util.numpy_support import vtk_to_numpy

def fit_function(x, mu, sigma):
    return (1/(np.sqrt(2*np.pi)*x*sigma)*np.exp(-((np.log(x)-mu)**2)/(2*sigma**2)))

if __name__ == '__main__':
    path = './'
    reader = vtki.OpenFOAMReader(path)
    times =len(reader.time_values)
    time = reader.time_values
    y = np.logspace(-2, -6, num=5000,base=10,endpoint=True)
    z = np.zeros(len(y))
    reader = vtki.OpenFOAMReader(path)
    reader.set_active_time_value(float(reader.time_values[-1]))
    mesh = reader.read()
    internal_mesh = mesh["internalMesh"]
    water = internal_mesh.compute_cell_sizes()
    water.cell_data['epsilon'] = water.cell_data['k']*water.cell_data['omega']*0.09
    water.cell_data['l']  = np.power(np.power((0.8953*10**(-6)),3)/water.cell_data['epsilon'],1/4)
    total_volume=water.volume
    frequencies, bin_edges = np.histogram(water.cell_data['l'],bins=20000,weights=water.cell_data['Volume'],density=True)
    binscenters = np.array([0.5 * (bin_edges[i] + bin_edges[i+1]) for i in range(len(bin_edges)-1)])
    popt, pcov = curve_fit(fit_function, xdata=binscenters, ydata=frequencies, p0=[0.01, 5])
    d1 = np.random.lognormal(popt[0], popt[1], 1000)
    frozen_lognorm = stats.lognorm(s=popt[1], scale=math.exp(popt[0]))

    for j in range(len(y)):
        z[j] = frozen_lognorm.pdf(y[j])

    bin1 = bin_edges[1:]
    f1 = frequencies

    with open('basecase.npy', 'rb') as f:
        d2 = np.load(f)

    res = stats.ks_2samp(d1,d2,alternative='two-sided')

    with open('results.npy', 'wb') as f:
        np.save(f, res)
    with open('dist_y.npy', 'wb') as f:
        np.save(f, z)
    with open('dist_x.npy', 'wb') as f:
        np.save(f, y)
    with open('bin1.npy', 'wb') as f:
        np.save(f, bin1)
    with open('f1.npy', 'wb') as f:
        np.save(f, f1)
    with open('temp.txt', 'w') as f:
        f.write(str(res.statistic))
