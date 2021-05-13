#!/bin/bash

# Create ELECTRA TFRecords with given vocabulary and sequence length.

# NOTE: replace instances of "DOC_FILTERED" with "TOKENIZED_TEXT" in this
# script to generate records for all texts (instead of filtered).

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
RUN=$2
source "$PIPELINE_DIR/common_$RUN.sh"

count=$(find "$DOC_FILTERED_DIR" -type f | wc -l | perl -pe 's/\s//g')

if [ $count -eq 0 ]; then
    error_exit "no files in $DOC_FILTERED_DIR"
else
    echo "$SCRIPT: processing $count files in $DOC_FILTERED_DIR"
fi

for seq_len in 128 512; do
    # ELECTRA operates on a directory of texts as opposed to individul files
	if [ $seq_len -eq 128 ]; then
	    outdir="$ELECTRA_TFRECORD_DIR_128"
	elif [ $seq_len -eq 512 ]; then
	    outdir="$ELECTRA_TFRECORD_DIR_512"
	else
	    error_exit "unexpected seq_len $seq_len"
	fi

	mkdir -p "$outdir"
	
    if [ -s "$outdir" ]; then
	    echo "$SCRIPT: $outdir exists, skipping." >&2
	else
	    echo "$SCRIPT: creating ELECTRA TFRecord from $DOC_FILTERED_DIR to $outdir ..." >&2
	    echo "$SCRIPT: running $CREATE_ELECTRA_TFRECORD" >&2

		echo $params
		python3 "$CREATE_ELECTRA_TFRECORD" --corpus-dir "$DOC_FILTERED_DIR" \
			--vocab-file $WORDPIECE_VOCAB_PATH \
			--output-dir $outdir --max-seq-length $seq_len \
			--num-processes 50 --no-lower-case
	fi
done