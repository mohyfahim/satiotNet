#!/bin/bash

OPT=$1
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
NS3_DIR=$SCRIPT_DIR/ns-3-dev

source $SCRIPT_DIR/venv/bin/activate

if [ -z $OPT ]; then
    $NS3_DIR/ns3 configure --enable-example \
        --enable-python-bindings --enable-tests --build-profile=debug \
        --out=$NS3_DIR/build/debug
else
    $NS3_DIR/ns3 configure --enable-python-bindings \
        --enable-tests --build-profile=optimized \
        --out=$NS3_DIR/build/optimized
fi


$NS3_DIR/ns3 build