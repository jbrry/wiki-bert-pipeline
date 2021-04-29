#!/bin/bash

# Tokenize texts for given language.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

RUN=$2
source "$PIPELINE_DIR/common_$RUN.sh"

count=$(find "$EXTERNAL_CORPORA_DIR" -type f | wc -l | perl -pe 's/\s//g')

echo "pass"

if [ $count -eq 0 ]; then
    error_exit "no files in $EXTERNAL_CORPORA_DIR"
else
    echo "$SCRIPT: processing $count files in $EXTERNAL_CORPORA_DIR"
fi

find "$EXTERNAL_CORPORA_DIR" -type f | sort | while read f; do
    relpath=$(relative_path "$f" "$EXTERNAL_CORPORA_DIR")
    reldir=$(dirname "$relpath")
    outdir="$TOKENIZED_TEXT_DIR/$reldir"
    outbase=$(echo $(basename "$f") | perl -pe 's/\..*//')
    outpath=$(pwd_relative_path "$outdir/$outbase")
    mkdir -p "$outdir"
    if [ -s "$outpath" ]; then
    	echo "$SCRIPT: $outpath exists, skipping $f ." >&2
    else
	echo "$SCRIPT: tokenizing $f to $outpath ..." >&2
	python3 "$TOKENIZER" "$UDPIPE_MODEL_PATH" "$f" > "$outpath"
    fi
done
