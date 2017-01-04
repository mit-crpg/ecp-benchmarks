"""A parametric study over MPI procs and OMP threads for a benchmark."""

import os
import glob
import numpy as np
import openmc

# Query user for benchmark to profile (i.e., '2x2-periodic')
benchmark = input('Benchmark: ')
os.chdir(benchmark)

# Query user for hardware platform to consider
platform = os.environ['HOSTNAME']

# Default MPI+OMP runtime parameters for Phi/Haswell
if 'thing' in platform:
    platform = 'haswell'
    mpi_procs = [1, 2, 4, 8, 36, 72]
    omp_threads = [72, 36, 18, 9, 2, 1]
else:
    platform = 'phi'
    mpi_procs = [4, 4, 4, 64, 64, 64]
    omp_threads = [16, 32, 64, 1, 2, 4]

# Allocate arrays for timing data for inactive and active cycles
times = np.zeros((len(mpi_procs),2), dtype=np.int)

# Instantiate a Summary object to retrieve the geometry
su = openmc.Summary('summary.h5')

for i, xs in enumerate(['ace', 'multipole']):

    # Construct uniform initial source distribution over fissionable zones
    lower_left = su.opencg_geometry.bounds[:2] + [-10.]
    upper_right = su.opencg_geometry.bounds[3:5] + [10.]
    source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
    source.space.only_fissionable = True

    settings_file = openmc.Settings()
    settings_file.batches = 10
    settings_file.inactive = 5
    settings_file.particles = 10000
    settings_file.ptables = True
    settings_file.output = {'tallies': False}
    settings_file.source = source
    settings_file.sourcepoint_write = False

    if xs == 'multipole':
        settings_file.temperature = {'multipole': True, 'tolerance': 1000}

    settings_file.export_to_xml()

    for j, (procs, threads) in enumerate(zip(mpi_procs, omp_threads)):

        # Run OpenMC - works for both flat and cache memory modes
        #openmc.run(threads=threads, mpi_procs=procs,
        #           mpi_exec='HYDRA_TOPO_DEBUG=1 mpiexec -bind-to numa')

        # Run OpenMC - works for both flat mode with MCDRAM only
        #openmc.run(threads=threads, mpi_procs=procs,
        #           mpi_exec='HYDRA_TOPO_DEBUG=1 mpiexec -bind-to core:16 numactl --preferred 4,5,6,7')

        # Run OpenMC - works for both flat and cache memory modes
        openmc.run(threads=threads, mpi_procs=procs,
                   mpi_exec='HYDRA_TOPO_DEBUG=1 mpiexec -bind-to core:16')

        # Glob the names of all statepoints in the directory
        sp_filenames = glob.glob('statepoint.*.h5')

        # Load the final statepoint
        sp = openmc.StatePoint(sp_filenames[0])

        # Extract cumulative time spent in (in)active cycles in seconds
        inactive = sp.runtime['inactive batches']
        active = sp.runtime['active batches']

        # Convert times to neutrons / second
        times[j,0] = int((sp.n_inactive * sp.n_particles) / inactive)
        times[j,1] = int((sp.n_realizations * sp.n_particles) / active)

        print('inactive time (n / sec): {}'.format(times[j,0]))
        print('active time (n / sec): {}'.format(times[j,1]))

    # Save timing data to CSV files
    np.savetxt('{}-{}.csv'.format(platform, xs), times, delimiter=',', fmt='%d')
