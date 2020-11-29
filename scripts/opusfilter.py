import fileinput
import subprocess
from shutil import copyfile
import sys
import os

"""Wraps opusfilter to take in a default configuration, edit some of the parameters and run the filter."""

# Default OpusFilter configs with placeholder values.
# The basic config does not contain any character script or language filters.
OPUSFILTER_CONFIGS = {
                        "basic": "config/opusfilter_basic.yaml",
                        "basic_char_lang": "config/opusfilter_basic_char_lang.yaml",
                        }


def replace_default_config(specific_config,
                            input_directory,
                            file_name,
                            char_filter_threshold=None,
                            lang_filter_threshold=None):

    """
    Takes a default configuration file and uses `fileinput` to replace lines based on the current configuration.
    
    Args:
    specific_config:
        the specific config file we are writing to.
    input_directory:
        the 'tokenized-texts' directory where the texts we are filtering are located.
        Note: OpusFilter requires the input and output directory to be the same, so we also use this as the output_directory
        but copy the filtered file afterwards.
    file_name:
        the basename of the input file, which is usually in the format <corpus>_<chunk>
    char_filter_threshold:
        the threshold to be applied for the character script filter.
    lang_filter_threshold:
        the threshold to be applied for the language id filters.
    """

    char_block = False
    lang_block = False

    for line in fileinput.input(specific_config, inplace=1):
        new_line_symbol = line.rfind('\n')
        line = line[:new_line_symbol]

        if "LanguageIDFilter" in line:
            lang_block = True
        elif "CharacterScoreFilter" in line:
            char_block = True

        # replace output_directory NOTE: opusfilter requires input/output file to be in the same output directory so here we use the input_directory
        if "output_directory" in line:
            string = f"  output_directory: {input_directory}"
            line = line.replace(line, string)
            print(line)        
        # replace inputs
        elif "inputs" in line:
            string = f"      inputs: [{file_name}]"
            line = line.replace(line, string)
            print(line)
        # replace outputs
        elif "outputs" in line:
            string = f"      outputs: [{file_name}-filtered]"
            line = line.replace(line, string)
            print(line)
        # replace thresholds
        elif "thresholds" in line:
            if char_block:
                string = f"            thresholds: [{char_filter_threshold}]"
                char_block = False
            elif lang_block:
                string = f"            thresholds: [{lang_filter_threshold}]"
                lang_block = False
            line = line.replace(line, string)
            print(line)
        # keep line unchanged
        else:
            print(line)


# get appropriate values from inputs
run, file_in, config_path, out_path = sys.argv[1:]

# find the appropriate template configuration
parts = run.split("+")
print(parts)

use_char = False
use_lang = False
use_basic = False
skip_filtering = False

for part in parts:
    if "char" in part:
        char_filter_threshold = part.split("-")[1]
        print(f"using threshold of {char_filter_threshold} for character script.")
        use_char = True
    elif "lang" in part:
        lang_filter_threshold = part.split("-")[1]
        print(f"using threshold of {lang_filter_threshold} for language ID.")
        use_lang = True
    elif "basic" in part:
        print("using basic filtering.")
        use_basic = True

if use_basic and use_char and use_lang:
    default_config = OPUSFILTER_CONFIGS["basic_char_lang"]
elif not use_char and not use_lang and use_basic:
    default_config = OPUSFILTER_CONFIGS["basic"]
elif not use_basic and not use_char and not use_lang:
    skip_filtering = True

input_directory = os.path.dirname(file_in)
file_name = os.path.basename(file_in)
output_directory = os.path.dirname(out_path)

if not skip_filtering:
    specific_config=f"{config_path}/opusfilter_{run}.yaml"
    print(f"creating config: {specific_config}")
    copyfile(default_config, specific_config)

    # write out the specifig config.
    cfg_out = replace_default_config(specific_config, input_directory, file_name, char_filter_threshold, lang_filter_threshold)

    print("\n", "----------")
    print(f"filtering {file_in} with the following configuration:")
    cmd=f"cat {specific_config}"
    rcmd = subprocess.call(cmd, shell=True)

    # run OpusFilter with the file-specific configuration (this needs to be installed on your system)
    cmd=f"opusfilter {specific_config}"
    rcmd = subprocess.call(cmd, shell=True)

    # move the file to filtered-texts directory (as OpusFilter writes output to the same directory as the input file)
    cmd = f"mv {input_directory}/{file_name}-filtered {output_directory}/{file_name}"
    rcmd = subprocess.call(cmd, shell=True)
else:
    print("Skipping filtering step.")
    # move the file to filtered-texts directory (as OpusFilter writes output to the same directory as the input file)
    cmd = f"mv {input_directory}/{file_name} {output_directory}/{file_name}"
    rcmd = subprocess.call(cmd, shell=True)
