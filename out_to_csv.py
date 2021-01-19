import pandas as pd
import glob
import json
import plac


@plac.annotations(dir_in=("Directory with JSON output files", "positional", None, str),
                  path_out=("Path to output CSV file", "positional", None, str))
def main(dir_in: str, path_out: str):
    files = glob.glob(dir_in + '/*.json')  # get all json files
    # iterate over files and append to dataframe:
    df = pd.DataFrame()
    for file in files:
        out = json.load(open(file, 'r'))
        df = df.append(pd.json_normalize(out['response']))
    # write output
    df.to_csv(path_out, index=False)


if __name__ == '__main__':
    plac.call(main)
