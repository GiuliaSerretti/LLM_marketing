#!/usr/bin/env python3
import os
import sys
import argparse
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

# ensure your src/ is on PYTHONPATH
bin = os.path.realpath(__file__)
prefix = os.path.dirname(os.path.dirname(bin))
sys.path.insert(0, os.path.join(prefix, "src"))

from llm_marketing.engine import InferenceEngine

def worker(chunk_id: int, df_slice: pd.DataFrame, args):
    """
    Run inference on one slice, all writing to the same SQLite file.
    """
    engine = InferenceEngine(args)
    engine.run(df_slice, chunk_id)
    return chunk_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run inference in parallel by splitting dataset into chunks."
    )
    parser.add_argument("--model",   required=True, help="Model name")
    parser.add_argument("--api_key", default=None,  help="API key")
    parser.add_argument("--dataset", default=os.path.join(prefix, "dataset", "survey.csv"))
    parser.add_argument("--output",  default=os.path.join(prefix, "experiments", "answers.sql"))
    parser.add_argument("-k", "--num_samples_per_profile", type=int, default=5, choices=range(1,10))
    parser.add_argument("-T", "--temperature", type=float, default=1.0)
    parser.add_argument("-p", "--top_p",      type=float, default=0.9)
    parser.add_argument("-m", "--max_tokens", type=int, default=512)
    parser.add_argument("-n", "--num_processes", type=int, default=1,
                        help="How many parallel processes to launch")
    args = parser.parse_args()

    # load & trim
    df = pd.read_csv(args.dataset)
    df = df.iloc[:, 1:5]
    df.columns = ["GENDER","AGE","EMPLOYMENT","INCOME"]
    df["ID"] = df.index

    # split into N roughly equal sub-DataFrames
    slices = np.array_split(df, args.num_processes)

    with ProcessPoolExecutor(max_workers=args.num_processes) as exe:
        futures = {
            exe.submit(worker, idx, slice_df, args): idx
            for idx, slice_df in enumerate(slices)
        }
        for fut in as_completed(futures):
            chunk_id = fut.result()
            print(f"✔ Chunk #{chunk_id} done")
