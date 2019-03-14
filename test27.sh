#!/bin/bash -e

python2.7 -m nose -s -v --with-coverage --cover-package=pprp `pwd`/tests
