#!/bin/bash

# Run heuristic document-level filtering.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

RUN=$2
source "$PIPELINE_DIR/common_$RUN.sh"

# add customfilters to Python path
export PYTHONPATH=/home/jbarry/spinning-storage/jbarry/ga_BERT/Irish-BERT/filters/

count=$(find "$TOKENIZED_TEXT_DIR" -type f | wc -l | perl -pe 's/\s//g')

if [ $count -eq 0 ]; then
    error_exit "no files in $TOKENIZED_TEXT_DIR"
else
    echo "$SCRIPT: processing $count files in $TOKENIZED_TEXT_DIR"
fi

find "$TOKENIZED_TEXT_DIR" -type f | sort | while read f; do
    relpath=$(relative_path "$f" "$TOKENIZED_TEXT_DIR")
    reldir=$(dirname "$relpath")
    outdir="$DOC_FILTERED_DIR/$reldir"
    outbase=$(echo $(basename "$f") | perl -pe 's/\..*//')
    outpath=$(pwd_relative_path "$outdir/$outbase")
    mkdir -p "$outdir"
    if [ -s "$outpath" ]; then
	    echo "$SCRIPT: $outpath exists, skipping $f ." >&2
    else

        corpus=$(echo $outbase | awk -F "_" '{print $1}')
        echo "processing corpus: $corpus"
	    echo "$SCRIPT: filtering $f to $outpath ..." >&2

        # get the filtering type from the last string in the metadata
        FILTER_TYPE=$(echo $RUN | awk -F "_" '{print $NF}')

        # DOC filtering
        if [ "$FILTER_TYPE" == "document-heuristic" ]; then
            echo "$SCRIPT: running $DOC_FILTER" $DOC_FILTER_PARAMS >&2
            python3 "$DOC_FILTER" $DOC_FILTER_PARAMS "$f" > "$outpath"
        # OpusFilter
        else
            echo "$SCRIPT: running $OPUSFILTER_WRAPPER" $FILTER_TYPE $f >&2
            mkdir -p $OPUSFILTER_CONFIG_DIR
            python3 "$OPUSFILTER_WRAPPER" $FILTER_TYPE $f $OPUSFILTER_CONFIG_DIR $outpath
            sleep 10
        fi
    fi
done
