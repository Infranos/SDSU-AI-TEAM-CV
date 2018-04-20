#!/bin/bash

rm `ls *png | grep -v offline`

if [ -d __pycache__ ]; then
	rm -rf __pycache__
fi
