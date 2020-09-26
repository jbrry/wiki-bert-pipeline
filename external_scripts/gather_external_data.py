import os
import sys
from shutil import copyfile

# directory names of corpora which have been downloaded
external_corpora = ['conll17', 'gdrive', 'oscar', 'opus']

ga_data_dir = os.path.join('..', 'Irish-BERT/data/ga')

# replace 'wikipedia-texts' dir with 'ga-texts' which is a combination of all ga texts
target_data_path = os.path.join('data', 'ga', 'ga-texts')
if not os.path.exists(target_data_path):
    print(f"Creating directory at: {target_data_path}")
    os.makedirs(target_data_path)


found_files = 0
copied_files = 0

if os.path.exists(ga_data_dir):
    print(f"Found directory containing Irish files at {ga_data_dir}")
    for corpus in os.listdir(ga_data_dir):
        if corpus in external_corpora:
            print(f"Found {corpus}")
            file_path = corpus + "/processed"

            data_path = os.path.join(ga_data_dir, file_path)
            print(f"Copying Irish data from: {data_path}")
            
            for f in os.listdir(data_path):
                found_files += 1
                # if the file is a compressed file which has already been downloaded
                # copy it to the target directory
                if f.endswith(".bz2") or f.endswith(".gz"):
                    print(f"found file {f}")
                    original_file = os.path.join(data_path, f)
                    target_file = os.path.join(target_data_path, f)
                    copyfile(original_file, target_file)
                    copied_files += 1

        print(f"copied {(copied_files / found_files) * 100}% of files")
else:
    print(f"Could not find Irish data directory, tried: {ga_data_dir}")

