#!/usr/bin/env python3

import sys
from sentencepiece import SentencePieceProcessor


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-o', '--output-format', default="piece",
                    help='Whether to output pieces or ids (use `id` to output ids)')
    ap.add_argument('model', help='SentencePiece model')
    ap.add_argument('file', nargs='+')

    return ap


def load_model(model_path):
    sp_model = SentencePieceProcessor()
    model_path += ".model"
    sp_model.load(model_path)
    return sp_model


def sentencepiece_encode(sp_model, fn, output_format):
    with open(fn, 'r') as f:
        for l in f:
            if output_format == "piece":
                print(" ".join(str(x) for x in sp_model.encode_as_pieces(l)))
            elif output_format == "id":
                print(" ".join(str(x) for x in sp_model.encode_as_ids(l)))


def main(argv):
    args = argparser().parse_args(argv[1:])
    sp_model = load_model(args.model)
    
    for fn in args.file:
        sentencepiece_encode(sp_model, fn, args.output_format)
    
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))