#!/bin/bash

# Use sentencepiece model to encode raw text

# NOTE: replace instances of "DOC_FILTERED" with "TOKENIZED_TEXT" in this
# script to generate SentencePiece encodings for all texts (instead of filtered).

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
RUN=$2
source "$PIPELINE_DIR/common_$RUN.sh"

count=$(find "$DOC_FILTERED_DIR" -type f | wc -l | perl -pe 's/\s//g')

if [ $count -eq 0 ]; then
    error_exit "no files in $DOC_FILTERED_DIR"
else
    echo "$SCRIPT: processing $count files in $DOC_FILTERED_DIR"
fi


mkdir -p "$SENTENCEPIECE_TEXT_DIR"


find "$DOC_FILTERED_DIR" -type f | sort | while read f; do
    relpath=$(relative_path "$f" "$DOC_FILTERED_DIR")
    reldir=$(dirname "$relpath")
    outdir="$SENTENCEPIECE_TEXT_DIR/$reldir"
    outbase=$(echo $(basename "$f") | perl -pe 's/\..*//')
    outpath=$(pwd_relative_path "$outdir/$outbase.bpe")
    mkdir -p "$outdir"
    if [ -s "$outpath" ]; then
	    echo "$SCRIPT: $outpath exists, skipping $f ." >&2
    else
	echo "$SCRIPT: encoding $f to $outpath with SentencePiece model "$SENTENCEPIECE_MODEL_PATH" ..." >&2
	python3 "$SENTENCEPIECE_ENCODER" "$SENTENCEPIECE_MODEL_PATH" "$f" \
		> "$outpath"
    fi
done