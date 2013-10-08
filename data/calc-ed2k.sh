#!/usr/bin/env bash

for d in ./Lib/201[123]*; do
    echo "Dir $d";
    if ! [ -e $d/*.* ] ; then
        echo "No files"
        continue
    fi
    for f in $d/*.* ; do
        ehash=$( ed2k_hash $f | perl -p -e 's/.*([0-9a-f]{32}).*/\1/' )
        echo "  $f"
        echo "$f $ehash" >> list.ed2k
    done
done
