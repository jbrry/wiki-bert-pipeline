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

if os.path.exists(ga_data_dir):
    print(f"Found directory containing Irish files at {ga_data_dir}")
    for corpus in os.listdir(ga_data_dir):
        print(f"Found {corpus}")
        if corpus in external_corpora:

            if corpus == "gdrive":
                corpus += "/gathered"

            data_path = os.path.join(ga_data_dir, corpus)
            print(f"Copying Irish data from: {data_path}")
            
            for f in os.listdir(data_path):
                # if the file is a compressed file which has already been downloaded
                # copy it to the target directory
                if f.endswith(".bz2") or f.endswith(".gz"):
                    print(f"found file {f}")
                    original_file = os.path.join(data_path, f)
                    target_file = os.path.join(target_data_path, f)
                    copyfile(original_file, target_file)
else:
    print(f"Could not find Irish data directory, tried: {ga_data_dir}")
