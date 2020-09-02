# Parameters passed to filterdocs.py. $LC is the two-character language
# code given as an argument to the top-level scripts.
# NOTE: this filtering was originally designed for wikipedia articles
# changed: 
# --max-sents from 1000 to 1000000000 
# --max toks from 10000 to 1000000000
DOC_FILTER_PARAMS="
--min-sents 3
--max-sents 1000000000
--avg-len 4
--upper-ratio 0.1
--no-word-ratio 0.2
--punct-ratio 0.075
--digit-ratio 0.075
--min-toks 20
--max-toks 10000000000
--min-words 30
--foreign-ratio 0.02
--word-chars $DOC_FILTER_WORD_CHARS
--language $LC
--langdetect $LC
"
