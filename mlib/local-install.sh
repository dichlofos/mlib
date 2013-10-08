#!/usr/bin/env bash

DEST="/var/www/vhosts/mlib"
find . -name '*.pyc' | xargs rm
sudo cp -r . "$DEST"
