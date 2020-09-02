#!/bin/bash

# wraps pipeline driver script but first gathers external corpora

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 LC" >&2
    echo "    where LC is a two-character language code (e.g. \"en\")" >&2
    exit 1
fi

LC="$1"

# first populate corpora dir with external corpora
python external_scripts/gather_external_data.py

# launch wiki-bert pipeline
./RUN.sh $LC

