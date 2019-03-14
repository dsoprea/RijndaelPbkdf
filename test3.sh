#!/bin/bash -e

python3 -m nose -s -v --with-coverage --cover-package=pprp `pwd`/tests
