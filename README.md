ExaSMR Benchmarks
=================

This repository contains benchmarks for performance profiling of the OpenMC and
Shift Monte Carlo codes for the ECP ExaSMR project. Each directory contains a
Python script which uses the OpenMC Python API to create XML input files for
OpenMC.

Model Descriptions
------------------

<dl>
    <dt>smr</dt>
    <dd>A 3D Small Modular Reactor (SMR) model that roughly mimics the design of
    the NuScale reactor. The reactor core has 37 fuel assemblies that alternate
    between 3.1% enriched and 2.4% enriched UO2 fuel. The center fuel assembly
    has 1.6% enriched UO2 fuel. Where possible, we have attempted to use the
    same parameters for the fuel assemblies and fuel rods as those specified in
    the NuScale <a
    href="https://www.nrc.gov/reactors/new-reactors/design-cert/nuscale.html">design
    submittal</a> to the Nuclear Regulatory Commission (NRC), for example: 264
    fuel rods per assembly, 24 guide tubes per assembly, 1 instrument tube per
    assembly, five spacer grids per assembly, fuel rod pitch of 0.496 in, and an
    active fuel length of 200 cm. Many of the details of the actual NuScale fuel
    assembly design are redacted from the design submittal because they are
    export controlled/proprietary information. The purpose of our model is not
    to be an exact replica of the NuScale model; rather, it is intended to
    capture most of the physical complexities that are involved in modeling a
    full reactor core and to provide a suitable model for carrying out full core
    performance tests on the testbed architectures.</dd>
</dl>

Dependencies
------------

To generate models using the scripts in this package, you must use a recent
version of OpenMC's Python API.
