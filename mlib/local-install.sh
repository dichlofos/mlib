#!/usr/bin/env bash

set -e

dest="/var/www/vhosts/mlib"

# clean cached files
find . -name '*.pyc' | xargs rm -f

sudo rm -rf "$dest"
sudo mkdir -p $dest
sudo cp -r . "$dest"

# prepare tmp storage
books="$dest/b"
sudo mkdir -p "$dest/b/storage"
sudo chmod -R 777 "$dest/b/storage"

echo "Installation to $dest completed"
