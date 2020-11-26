#!/bin/bash

# wraps pipeline driver script but first gathers external corpora which have already been collected

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 LC RUN" >&2
    echo "    where LC is a two-character language code (e.g. \"en\") and RUN is the name of the run" >&2
    exit 1
fi

LC="$1"
RUN="$2" # data/conll17_gdrive_NCI_oscar_filtering_basic/ga/external-texts

RUN_TEXT_DIR=data/$RUN/$LC/$LC-texts

# first populate the RUN corpora dir with external corpora you have already collected
# this should already be created if you ran external_scripts/gather_external_data.py
if [ -d "$RUN_TEXT_DIR" ]; then
    echo "$RUN_TEXT_DIR exists, skipping the copying of external files ..." >&2
else
    echo "Copying external files to $LC_TEXT_DIR"
    python external_scripts/gather_external_data.py 
fi

# launch wiki-bert pipeline (paths should already have been set)
./RUN.sh $LC

