ECP Benchmarks
==============

This repository contains benchmarks for performance profiling of the OpenMC
and Shift Monte Carlo codes for ECP. Each directory contains a ``build-xml.py''
Python script which uses the OpenMC Python API to create XML input files for
OpenMC. The Python scripts as well as the XML files are included in this repository.
Each benchmark is derived from a subset (*e.g.*, fuel pins, assemblies) of the
full-core BEAVRS model with fresh UO2 fuel at HZP conditions. Each model is modeled
in 2D by using reflective boundary conditions along the axial dimension.

Model Descriptions
------------------

**fuel-pin**  
A single fuel pin with reflective boundary conditions (*i.e.*, an infinitely repeating
array of fuel pins). The default configuration is the BEAVRS fuel pin with fresh 1.6\%
enriched UO2 fuel, but the script can be toggled to 2.4\% or 3.1\% enriched fuel.

**assembly**  
A single fuel assembly with reflective boundary conditions (*i.e.*, an infinitely
repeating lattice of fuel assemblies). The default configuration is the BEAVRS assembly
with fresh 1.6\% enriched UO2 fuel with 24 water-filled control rod guide tubes and a
central air-filled instrument tube. However, the script can be toggled to use any of
the 20+ fuel assemblies in the BEAVRS model.

**2x2-periodic**  
A 2x2 fuel assembly colorset with periodic boundary conditions (*i.e.*, an infinitely
repeating lattice of the 2x2 assembly colorset). The default configuration includes the
BEAVRS assembly with fresh 1.6\% enriched UO2 fuel with 24 water-filled control rod guide
tubes and a central air-filled instrument tube, along with a 3.1\% enriched fuel assembly
with 20 burnable poisons, four control rod guide tubes and a central instrument tube.
However, the script may be toggled to use any pair of the 20+ fuel assemblies in the
BEAVRS model.

**2x2-reflector**  
A 2x2 fuel assembly colorset surrounded by a water reflector. Reflective boundary
conditions are used on the top and left boundaries (adjacent to the assemblies) and
vacuum boundary conditions are used on the bottom and right boundaries (adjacent to the
reflector).  The default configuration includes the BEAVRS assembly with fresh 1.6\%
enriched UO2 fuel with 24 water-filled control rod guide tubes and a central air-filled
instrument tube, along with a 3.1\% enriched fuel assembly with 20 burnable poisons, four
control rod guide tubes and a central instrument tube. However, the script may be toggled
to use any pair of the 20+ fuel assemblies in the BEAVRS model.

Dependencies
------------

These scripts depend on the following Python packages:

* mit-crpg/openmc (develop branch)
* mit-crpg/OpenCG
* mit-crpg/PWR_benchmarks

Of particular note, The Python ``beavrs`` package must be installed from the
mit-crpg/PWR_benchmarks repository. This package may be installed with
``distutils`` as follows:

```bash
cd PWR_benchmarks/BEAVRS/openmc/inputs
python setup.py install
```
