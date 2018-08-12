#!/bin/sh

DPEA_REPO_ROOT=/home/pi/Documents/
PROCESS="main.py"

if test "$#" -ne 1; then
    echo "Usage: launcher.sh 'Project Name'"
    echo ""
    echo "example: . launch.sh InfinityMirrorPie"
    echo ""
    return
fi

if [ -z "$DPEA_REPO_ROOT" ]; then
    echo ""
    echo "You must set the 'DPEA_REPO_ROOT' env variable to the root of the project"
    echo ""
    echo "example: export DPEA_REPO_ROOT=/home/pi/Documents/"
    return
fi


RESULT=`ps -ef | grep -v sed | grep -v grep | sed -n /\${PROCESS}/p` 

pushd `pwd`
cd $DPEA_REPO_ROOT/$1

if [ "${RESULT:-null}" = null ]; then
    echo "Launching"
    python ${PROCESS}
else
    echo "running"
fi

popd
