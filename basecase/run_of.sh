#!/bin/bash
 
blockMesh	> blockMesh.log
surfaceFeatures > surfaceFeatures.log
decomposePar -noFields	> decomposePar1.log
mpirun -np 32 snappyHexMesh -overwrite -parallel > snappyHexMesh.log
reconstructParMesh -constant	> reconstructParMesh.log
rm -r processor*
renumberMesh -overwrite	> renumberMesh.log
checkMesh		> checkMesh.log
decomposePar		> decomposePar2.log
>&2 echo "   |--> Start stimulation"
mpirun -np 32 simpleFoam -parallel	> simpleFoam.log
reconstructPar -latestTime		> reconstructPar.log
rm -r processor*
python KStest.py

