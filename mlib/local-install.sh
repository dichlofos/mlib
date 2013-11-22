#!/usr/bin/env bash

set -xe

dest="/var/www/vhosts/mlib"
find . -name '*.pyc' | xargs rm -f
sudo rm -rf "$dest"
sudo mkdir -p $dest
sudo cp -r . "$dest"
books="$dest/b"
sudo mkdir -p "$dest/b/storage"
sudo chmod -R 777 "$dest/b/storage"
#sudo bash -xe <<EOF
#unlink "$books" 2>/dev/null || true
#EOF
#sudo ln -sf /storage/whiterose/libraries/lib.mexmat.ru/Lib $books
