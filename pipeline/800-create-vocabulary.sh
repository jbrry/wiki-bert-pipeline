#!/bin/bash

# Create sentencepiece model for given language.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
RUN=$2
source "$PIPELINE_DIR/common_$RUN.sh"

if [ ! -s "$SAMPLED_TEXT_PATH" ]; then
    error_exit "$TOKENIZED_SAMPLE_PATH does not exist"
fi

mkdir -p "$HUGGINGFACE_TOKENIZER_MODEL_DIR"

if [ -s "$HUGGINGFACE_TOKENIZER_MODEL_PATH/vocab.txt" ]; then
    echo "$SCRIPT: $HUGGINGFACE_TOKENIZER_MODEL_PATH.vocab exists, not recreating." >&2
    exit 0
else
    params="
    $SAMPLED_TEXT_PATH
    --outdir=$HUGGINGFACE_TOKENIZER_MODEL_PATH
    --number_unused=100"
    echo "$SCRIPT: running $HUGGINGFACE_TOKENIZER" $params >&2
    python3 "$HUGGINGFACE_TOKENIZER" $params
fi

