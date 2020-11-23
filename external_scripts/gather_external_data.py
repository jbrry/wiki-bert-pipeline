import os
import sys
from shutil import copyfile
import subprocess
from argparse import ArgumentParser
import fileinput


def argparser():
    parser = ArgumentParser(
        description='.'
    )
    parser.add_argument(
        '--datasets',
        type=str,
        help='Specify the datasets to copy.',
        choices={
            'conll17',
            'gdrive',
            'NCI',
            'NCI_old',
            'oscar',
        },
        nargs='+',
    )
    parser.add_argument('--filter-type', type=str,
        choices={
            'none',
            'basic',
            'basic_0.5',
            'basic_0.8',
            })
    parser.add_argument('--input-type', type=str,
        choices={
            'raw',
            'processed',
            'filtered',
            })

    return parser

def main(argv):
    args = argparser().parse_args(argv[1:])
    corpora_string = "_".join(args.datasets)
    run_string = f'{corpora_string}_filtering_{args.filter_type}'
    print(f"copying data for run: {run_string}")

    ga_data_dir = os.path.join('..', 'Irish-BERT/data/ga')

    target_data_path =  os.path.join('data', run_string, 'ga', 'external-texts')
    if not os.path.exists(target_data_path):
        print(f"Creating directory at: {target_data_path}")
        os.makedirs(target_data_path)

    
    data_path = f'DATA_DIR=$(pwd_relative_path "$BASE_DIR/data/{corpora_string}_filtering_{args.filter_type}")'
    external_path = f'EXTERNAL_CORPORA_DIR="$DATA_DIR/ga/external-texts"'

    # take the default config file and alter it based on the specific data/filtering type.
    # this is necessary because it means environment paths won't change if the pipeline is being run for multiple configurations simultaneously.
    DEFAULT_CONFIG="pipeline/default.sh"
    SPECIFIC_CONFIG=f"pipeline/common_{run_string}.sh"
    print(f"creating config: {SPECIFIC_CONFIG}")
    copyfile(DEFAULT_CONFIG, SPECIFIC_CONFIG)

    for line in fileinput.input(SPECIFIC_CONFIG, inplace=1):
        new_line_symbol = line.rfind('\n')
        line = line[:new_line_symbol]
        # replace placeholder data dir with specific data dir
        if line == 'DATA_DIR=$(pwd_relative_path "$BASE_DIR/data")':
            line = line.replace(line, data_path)
            print(line)
        # set external corpora dir based on new data dir
        elif line == 'EXTERNAL_CORPORA_DIR=""':
            line = line.replace(line, external_path)
            print(line)
        # keep line unchanged
        else:
            print(line)

    found_files = 0
    copied_files = 0

    if os.path.exists(ga_data_dir):
        print(f"Found directory containing Irish files at {ga_data_dir}")
        for corpus in os.listdir(ga_data_dir):
            if corpus in args.datasets:
                print(f"Found {corpus}")
                file_path = os.path.join(corpus, args.input_type)
                data_path = os.path.join(ga_data_dir, file_path)
                print(f"Copying Irish data from: {data_path}")
                
                for f in os.listdir(data_path):
                    found_files += 1
                    # copy file to the target directory
                    if f.endswith(".bz2") or f.endswith(".gz"):
                        print(f"found file {f}")
                        original_file = os.path.join(data_path, f)
                        target_file = os.path.join(target_data_path, f)
                        copyfile(original_file, target_file)
                        copied_files += 1

                print(f"copied {(copied_files / found_files) * 100}% of files for {corpus}")
    else:
        print(f"Could not find Irish data directory, tried: {ga_data_dir}")

if __name__ == '__main__':
    sys.exit(main(sys.argv))
