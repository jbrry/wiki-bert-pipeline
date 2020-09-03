#!/bin/bash

# wraps pipeline driver script but first gathers external corpora

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 LC" >&2
    echo "    where LC is a two-character language code (e.g. \"en\")" >&2
    exit 1
fi

LC="$1"
LC_TEXT_DIR=data/$LC/$LC-texts

# first populate corpora dir with external corpora you have already collected
if [ -d "$LC_TEXT_DIR" ]; then
    echo "$LC_TEXT_DIR exists, skipping the copying of external files ..." >&2
else
    echo "Copying external files to $LC_TEXT_DIR"
    python external_scripts/gather_external_data.py 
fi

# launch wiki-bert pipeline
./RUN.sh $LC

