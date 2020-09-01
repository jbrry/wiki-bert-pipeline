import os
import sys

from shutil import copyfile

# directory names of corpora which have been downloaded
external_corpora = ['conll17', 'gdrive', 'oscar']

user = os.path.expanduser('~')
ga_data_dir = 'Irish-BERT/data/ga'
ga_full_path = os.path.join(user, ga_data_dir)
wiki_bert_path = os.path.join(user, "wiki-bert-pipeline")

# replace 'wikipedia-texts' dir with 'irish-texts' which is a combination of all texts
target_data_path = os.path.join(wiki_bert_path, 'data', 'ga', 'irish-texts')
if not os.path.exists(target_data_path):
    print(f"Creating target directory at: {target_data_path}")
    os.makedirs(target_data_path)


if os.path.exists(ga_full_path):
    print(f"Using Irish data directory at location: {ga_full_path}")
    for corpus in os.listdir(ga_full_path):
        if corpus in external_corpora:
            data_path = os.path.join(ga_full_path, corpus)

            for f in os.listdir(data_path):
                # if the file is a compressed file which has already been downloaded
                # copy it to the target directory
                if f.endswith(".bz2"):
                    original_file = os.path.join(data_path, f)
                    target_file = os.path.join(target_data_path, f)
                    copyfile(original_file, target_file)
else:
    print(f"Could not find Irish data directory, tried: {ga_full_path}")

