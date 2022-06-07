# Milestone Models

- **AD-SE-08-61, Coupled Multiphysics Driver Implementation** --- This milestone
  used the singlerod short/long problems. Generating the model was done with the
  script `tests/singlerod/make_openmc_model.py` from the ENRICO repository
  (there is a `--short` command line option to generate the short version)

- **AD-SE-08-66, Coupled Assembly Analysis** --- This milestone used the
  assembly short and long (v2) problems. Generating the model was done with
  `smr/build-assembly-long.py -a 100 --clone` on the ecp-benchmarks repository
  (git commit `631fefe`, after pull request #14). In these models, materials are
  fully differentiated across each fuel ring/axial segment.

- **AD-SE-08-73, Full core coupled-physics simulation** --- This milestone used
  the core-short and core-long (90 layer) models. Generating the models was done
  with `smr/build-core-short.py` and `smr/build-assembly-long.py -a 90` on the
  ecp-benchmarks repository (git commit `c7b89db`, after pull request #16). In
  these models, materials are not differentiated and no grid spacers are
  present. The lattice pitch is modified to be exactly 17 times the pin pitch
  (slightly different than NuScale specification).
