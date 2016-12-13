"""A parametric study over MPI procs and OMP threads for a benchmark."""

import os
import glob
import numpy as np
import openmc

# Query user for benchmark to profile (i.e., '2x2-periodic')
benchmark = input('Benchmark: ')
os.chdir(benchmark)

# Query user for hardware platform to consider
platform = input('Hardware platform (Haswell / Phi): ')

# Default MPI+OMP runtime parameters for HASWELL/Phi
if platform.lower() == 'haswell':
    mpi_procs = [1, 2, 4, 8, 36, 72]
    omp_threads = [72, 36, 18, 9, 2, 1]
elif platform.lower() == 'phi':
    mpi_procs = [4, 64, 64, 64]
    omp_threads = [64, 1, 2, 4]
else:
    exit('Unknown hardware platform {}'.format(platform))

# Allocate NumPy arrays for timing data
inactive_times = np.zeros(len(mpi_procs), dtype=np.int)
active_times = np.zeros(len(mpi_procs), dtype=np.int)

for i, (procs, threads) in enumerate(zip(mpi_procs, omp_threads)):

    # Run OpenMC
    openmc.run(threads=threads, mpi_procs=procs)

    # Glob the names of all statepoints in the directory
    sp_filenames = glob.glob('statepoint.*.h5')

    # Load the final statepoint
    sp = openmc.StatePoint(sp_filenames[0])

    # Extract cumulative time spent in (in)active cycles in seconds
    inactive_time = sp.runtime['inactive batches']
    active_time = sp.runtime['active batches']

    # Convert times to neutrons / second
    inactive_times[i] = int((sp.n_inactive * sp.n_particles) / inactive_time)
    active_times[i] = int((sp.n_realizations * sp.n_particles) / active_time)

    print('inactive time (n / sec): {}'.format(inactive_times[i]))
    print('active time (n / sec): {}'.format(active_times[i]))

# Save timing data to CSV files
np.savetxt('{}-{}-inactive.csv'.format(benchmark, platform),
           inactive_times, delimiter=',')
np.savetxt('{}-{}-active.csv'.format(benchmark, platform),
           active_times, delimiter=',')
