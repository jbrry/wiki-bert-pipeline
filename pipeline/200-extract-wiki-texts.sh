#!/bin/bash

# Extract texts from Wikipedia dump data for given language.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
RUN=$2
source "$PIPELINE_DIR/common_$RUN.sh"

IGNORED_TAGS="abbr,b,big,blockquote,br,center,cite,em,font,h1,h2,h3,h4,hiero,hr,i,kbd,nowiki,p,plaintext,poem,ref,s,span,strike,strong,sub,sup,tt,u,var"

if [ ! -s "$WIKI_DUMP_PATH" ]; then
    error_exit "missing $WIKI_DUMP_PATH"
fi

if [ ! -s "$WIKIEXTRACTOR" ]; then
    error_exit "missing $WIKIEXTRACTOR
    (try \`git submodule update --init\`?)"
fi

mkdir -p "$WIKI_TEXT_DIR"

# also make a corpus-agnostic directory for the language
mkdir -p "$EXTERNAL_CORPORA_DIR"

count=$(find "$WIKI_TEXT_DIR" -type f | wc -l | perl -pe 's/\s//g')

if [ $count -gt 0 ]; then
    echo "$SCRIPT: $WIKI_TEXT_DIR contains $count files, skipping extraction." \
	 >&2
    exit 0
else
    echo "$SCRIPT: extracting $WIKI_DUMP_PATH to $WIKI_TEXT_DIR" >&2
    python3 "$WIKIEXTRACTOR" \
	    --filter_disambig_pages \
	    --ignored_tags "$IGNORED_TAGS" \
	    --output "$WIKI_TEXT_DIR" \
	    --compress \
	    "$WIKI_DUMP_PATH"

    # copy all of the wikipedia files to a general corpora directory
    echo "copying output Wikipedia files from $WIKI_TEXT_DIR to $EXTERNAL_CORPORA_DIR..." 
    find $WIKI_TEXT_DIR -maxdepth 2 -type f | xargs -I {} cp -v {} $EXTERNAL_CORPORA_DIR;
fi
