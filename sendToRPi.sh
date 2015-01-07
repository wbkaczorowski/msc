#!/bin/bash

rsync -av $1 --exclude=".*/" led@rpi:~/$1
