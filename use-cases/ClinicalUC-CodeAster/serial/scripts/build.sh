#!/bin/bash

IMGBASENAME=code_aster_clinical

echo "Build ${IMGBASENAME} container with Singularity"

cd def
if test -n "$USE_SB"; then
    echo "Build Sandbox image"
    singularity build --sandbox --fakeroot --force ../${IMGBASENAME}.imgdir ${IMGBASENAME}.def
else
    echo "Build SIF image"
    sudo singularity build --force ../${IMGBASENAME}.sif ${IMGBASENAME}.def
fi
cd ..

