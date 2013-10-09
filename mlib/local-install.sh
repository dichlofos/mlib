#!/usr/bin/env bash

set -xe

DEST="/var/www/vhosts/mlib"
find . -name '*.pyc' | xargs rm -f
sudo rm -rf $DEST
sudo mkdir -p $DEST
sudo cp -r . "$DEST"
