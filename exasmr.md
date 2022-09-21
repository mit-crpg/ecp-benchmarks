---
author: Steven Hamilton
title: ExaSMR Project KPP-1 Verification
---

# Science Challenge Problem Description

The ExaSMR challenge problem is the simulation of a representative NuScale SMR
core by coupling continuous-energy Monte Carlo neutronics with CFD. Features
of the problem include the following:

* representative model of the complete in-vessel coolant loop,
* hybrid LES/RANS turbulence model or RANS plus an LES-informed momentum
  source for treatment of mixing vanes, and
* pin-resolved spatial fission power and reaction rate tallies.

Details on the challenge problem specification are given in the table.

The simulation objective is to calculate reactor start-up conditions that
demonstrate the initiation of natural coolant flow circulation through the
reactor core and primary heat exchanger. The driver application, ENRICO,
performs inline coupling of the Nek5000 CFD module with Monte Carlo through a
common API that supports two Monte Carlo modules: Shift, which targets the
Frontier architecture at ORNL, and OpenMC, which targets the Aurora system at
ANL.

Minimum neutronics requirements for the coupled simulation are as
follows:

* full-core representative SMR model containing 37 assemblies with $17\times
  17$ pins per assembly and 264 fuel pins per assembly item,
* depleted fuel compositions containing $O(150)$ nuclides per material,
* $10^{10}$ neutrons per eigenvalue iteration,
* pin-resolved reaction rate with a single radial tally region and 20 axial
  levels, and
* six macroscopic nuclide-independent reaction rate tallies.


Minimum CFD requirements for the coupled simulation are as follows:

* assembly bundle mesh models with momentum sources from a resolved CFD
  calculation on a representative spacer grid and
* full-core mesh $200\times 10^6$ elements and $70\times 10^9$ DOF.

Table: Challenge problem details

------------------------------------------------------------------------------------
Functional requirement     Minimum criteria
-------------------------  ---------------------------------------------------------
Physical phenomena and     Eigenvalue form of the linear
associated models          Boltzmann transport equation with quasistatic
                           nuclide neutronics coupled to hybrid RANS/LES
                           (or equivalent accuracy incompressible CFD with
                           Boussinesq approximation, or low-Mach
                           incompressible CFD with nonzero thermal divergence.

Numerical approach,        The neutronics solver is an MC particle transport;
and associated models      the CFD solver is a spectral finite element on
                           unstructured grids. Physics are coupled by using a
                           quasistatic approximation.

Simulation details         The neutronics model has a minimum of 200,000 tally
                           bins and 10 billion particle histories per
                           eigenvalue iteration. The CFD model has a minimum
                           of 200 million elements and 70 billion DOF.

Demonstration calculation  Run 30 eigenvalue cycles (10 inactive and 20 active)
requirements               to estimate the MC particle tracking rate and
                           1000 time steps toward steady-state
                           convergence in the CFD solve. Only one nonlinear
                           (Picard) iteration is required. To facilitate
                           comparison with the baseline measurement, the
                           neutronics portion of this calculation requires six
                           macroscopic reaction rates and one radial region
                           per pin.
------------------------------------------------------------------------------------

# Demonstration Calculation

## Facility Requirements

All workflow and runtime requirements use standard ECP and facility-supported
libraries (e.g., Trilinos, HDF5).

## Input description and Execution

### Problem Inputs

To run ExaSMR coupled problems through the ENRICO driver, the following inputs
are required:

* Monte Carlo driver input (XML)
* Monte Carlo geometry input file (XML or HDF5)
* Monte Carlo material compositions file (HDF5)
* CFD parameter file (text)
* CFD mesh file (binary)
* CFD C++ user-defined functions (text)
* CFD OCCA user-defined kernels (text)
* CFD restart file (binary, optional)
* ENRICO driver input (XML)
* Batch submission script (text)

For the KPP-1 measurement case, the following inputs are used:

-------------------------------------------------------------------------
Component     Filename                         Description
------------  -------------------------------  --------------------------
Monte Carlo   singlerod_short.inp.xml          Driver input

              singlerod_short.rtk.xml          Geometry input

              singlerod_short_compositions.h5  Material definitions

CFD           rod_short.udf                    User-defined C++ functions

              rod_short.oudf                   User-defined OCCA kernels

              rod_short.re2                    Mesh file

              rod_short.par                    Solver parmeters

Driver        enrico.xml                       Coupled driver settings

Submission    submit.lsf                       Batch submission script
-------------------------------------------------------------------------

### Resource Requirements

Estimated compute requirements for KPP-1 verification are two hours using the
full Frontier or Aurora machines.

## Problem Artifacts

Standard artifacts for coupled simulations include:

* Screen output of submitted jobs
* HDF5 output from Monte Carlo solver
* NekRS state field output files (native binary format)

The NekRS files will be made available upon request; however, it is anticipated
that these files will be very large (>1 TB). It is therefore not likely that
the NekRS files will be useful for verification and we suggest that the other
artifacts be used as the primary confirmation of execution.
Because the run to be used for the FOM measurement will not be able to 
fully converge a coupled simulation, we cannot check the accuracy of computed 
results, but we can assess whether the simulation meets several sanity checks
related to consistency of the numerical models and that computed quantities
obey certain physical characteristics. These checks, all of which are printed
to the screen output, include:

1. Verify consistency of the problem geometries. The ENRICO driver displays
diagnostics related to volumetric mapping from the CFD mesh to the MC geometry,
ensuring that the sum of the volume of the thermal/fluids elements matches the
volume of the corresponding MC cell containing those elements.
Exact agreement is not expected, but we anticipate the average volumetric error
to be less than 1% and the maximum error for any element to be under 10% (some 
small regions may be slightly off due to modeling differences related to the 
gap between the fuel and clad in fuel pins). This check ensures that the physics
models are geometrically equivalent and correctly aligned in space.
2. The fuel temperature should be nonuniform, i.e., the minimum and maximum 
temperatures should be different. The minimum temperature should be greater than
the coolant inlet temperature of 531.15K and the maximum temperature should be
above this value. In a converged simulation, the fuel temperature is expected
to reach a maximum of between 1000K and 1200K. For the FOM measurement, the 
actual temperature rise is expected to be much smaller, but the temperature
should not exceed 1300K.
3. The coolant/fluid temperature should be nonuniform, i.e., the minimum and
maximum temperatures should be different. The minimum temperature should be
approximately equal to the coolant inlet temperature of 531.15K and the maximum
temperature should be above this value. In a converged simulation, the coolant 
temperature is expected to reach a maximum of around 590-610K. For the FOM
measurement, the actual temperature rise is expected to be much smaller,
but the coolant temperature should not exceed 620K.
4. The eigenvalue (k-eff) computed by the MC solver should be approximately
equal to 1. The actual value will depend on the temperature and coolant 
density distribution, but it is expected that it will likely be between 0.95
and 1.05.

In addition, we will provide visualization artifacts in the form of 1D lineout
and 2D slices of the temperature and heat generation rate at several locations 
in the problem. These artifacts can be examined to confirm that the simulations 
are behaving as expected. Because the KPP-1 verification simulation will not be
fully converged, certain aspects of these visualizations will not necessarily
satisfy all physical characteristics of a converged solution. For example, 
the small number of time steps executed in the CFD calculation may result in
the fluid temperature not being monotonically increasing with respect to the
axial height in the problem. Therefore, to aid in the evaluation of these
visualization artifacts, we will provide a series of equivalent plots showing
the progression towards convergence on a similar (but smaller) example problem.
These plots are intended to provide a basis for evaluating whether the results 
of the KPP-1 verification simulation are showing the expected progress towards 
a converged solution, even though the results themselves will not be converged.

KPP-1 FOM measurement data can be obtained by running provided `python` script
to extract performance data from above artifacts:
```
>>> python process_fom.py case_name
```
This script will extract timing data for each of the physics solvers and evaluate
the ExaSMR FOM metric. The MC transport FOM uses the follow information:

* the number of particle histories per eigenvalue cycle,
* the number of active cycles (the MC FOM is only taken over active cycles),
* the total time spent in the active cycles.

All of these quantities are contained in the HDF5 output file.
The FOM calculation for the CFD solver uses the following information:

* the number of degrees of freedom in the problem,
* the number of time steps,
* the time spent in the CFD solve.

This information is contained in the ENRICO screen output and will be parsed by
the provided python script.

## Verification of KPP-1 Threshold

*Give evidence that*

1. *The FOM measurement met threshold ($>50$)*
2. *The executed problem met challenge problem minimum criteria*

