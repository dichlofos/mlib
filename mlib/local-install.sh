#!/usr/bin/env bash

set -e

dest="/var/www/vhosts/mlib"

# clean cached files
find . -name '*.pyc' | xargs rm -f

sudo rm -rf "$dest"
sudo mkdir -p $dest
sudo cp -r . "$dest"

sudo unlink "$dest/mlib/settings.py"
sudo cp ~mvel/work/settings/application-settings/mlib.local/$( hostname )/settings.py "$dest/mlib/"

# prepare tmp storage
books="$dest/b"
sudo mkdir -p "$dest/b/storage"
sudo chmod -R 777 "$dest/b/storage"

sudo mkdir -p $dest/admin
sudo ln -sf /usr/lib/python2.7/site-packages/django/contrib/admin/static "$dest/admin"

echo "Installation to $dest completed"
