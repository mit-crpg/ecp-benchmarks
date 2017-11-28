ECP Benchmarks
==============

This repository contains benchmarks for performance profiling of the OpenMC
and Shift Monte Carlo codes for ECP. Each directory contains a ``build-xml.py``
Python script which uses the OpenMC Python API to create XML input files for
OpenMC. The Python scripts and the XML files are included in this repository.
Each benchmark is derived from a subset (*e.g.*, fuel pins, assemblies) of the
full-core BEAVRS model with fresh UO2 fuel at HZP conditions. Each benchmark is
modeled in 2D with reflective boundary conditions along the axial dimension.

Model Descriptions
------------------

<dl>
    <dt>fuel-pin</dt>
    <dd>A single fuel pin with reflective boundary conditions (i.e., an infinitely repeating array of fuel pins). The default configuration is the BEAVRS fuel pin with fresh 1.6% enriched UO2 fuel, but the script can be toggled to 2.4% or 3.1% enriched fuel.</dd>
    <dt>assembly</dt>
    <dd>A single fuel assembly with reflective boundary conditions (i.e., an infinitely repeating lattice of fuel assemblies). The default configuration is the BEAVRS assembly with fresh 1.6% enriched UO2 fuel with 24 water-filled control rod guide tubes and a central air-filled instrument tube. However, the script can be toggled to use any of the 20+ fuel assemblies in the BEAVRS model.</dd>
    <dt>2x2-periodic</dt>
    <dd>A 2x2 fuel assembly colorset with periodic boundary conditions (i.e., an infinitely repeating lattice of the 2x2 assembly colorset). The default configuration includes the BEAVRS assembly with fresh 1.6% enriched UO2 fuel with 24 water-filled control rod guide tubes and a central air-filled instrument tube, along with a 3.1% enriched fuel assembly with 20 burnable poisons, four control rod guide tubes and a central instrument tube. However, the script may be toggled to use any pair of the 20+ fuel assemblies in the BEAVRS model.</dd>
    <dt>2x2-reflector</dt>
    <dd>A 2x2 fuel assembly colorset surrounded by a water reflector. Reflective boundary conditions are used on the top and left boundaries (adjacent to the assemblies) and vacuum boundary conditions are used on the bottom and right boundaries (adjacent to the reflector).  The default configuration includes the BEAVRS assembly with fresh 1.6% enriched UO2 fuel with 24 water-filled control rod guide tubes and a central air-filled instrument tube, along with a 3.1% enriched fuel assembly with 20 burnable poisons, four control rod guide tubes and a central instrument tube. However, the script may be toggled to use any pair of the 20+ fuel assemblies in the BEAVRS model.</dd>
    <dt>smr</dt>
    <dd>A 3D Small Modular Reactor (SMR) model that roughly mimics the design of the NuScale reactor. The reactor core has 37 fuel assemblies that alternate between 3.1% enriched and 2.4% enriched UO2 fuel. The center fuel assembly has 1.6% enriched UO2 fuel. Where possible, we have attempted to use the same parameters for the fuel assemblies and fuel rods as those specified in the NuScale <a href="https://www.nrc.gov/reactors/new-reactors/design-cert/nuscale.html">design submittal</a> to the Nuclear Regulatory Commission (NRC), for example: 264 fuel rods per assembly, 24 guide tubes per assembly, 1 instrument tube per assembly, five spacer grids per assembly, fuel rod pitch of 0.496 in, and an active fuel length of 200 cm. Many of the details of the actual NuScale fuel assembly design are redacted from the design submittal because they are export controlled/proprietary information. The purpose of our model is not to be an exact replica of the NuScale model; rather, it is intended to capture most of the physical complexities that are involved in modeling a full reactor core and to provide a suitable model for carrying out full core performance tests on the testbed architectures.</dd>
</dl>

Dependencies
------------

These scripts depend on the following Python packages:

* mit-crpg/openmc (develop branch)
* mit-crpg/PWR_benchmarks

Of particular note, The Python ``beavrs`` package must be installed from the
mit-crpg/PWR_benchmarks repository. This package may be installed with
``distutils`` as follows:

```bash
cd PWR_benchmarks/BEAVRS/openmc/inputs
python setup.py install
```
