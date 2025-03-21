
#!/usr/bin/env python3
import os
import sys
import argparse

if __name__ == '__main__':

    # Find script's location and its prefix
    bin = os.path.realpath(os.path.expanduser(__file__))
    prefix = os.path.dirname(os.path.dirname(bin))

    # Allow src to be imported
    src = os.path.join(prefix, "src")
    sys.path.insert(0, src)

    # Import AGI modules
    from llm_marketing.engine import InferenceEngine

    # Parse arguments
    # Main parser
    parser = argparse.ArgumentParser(description='Run inference using the Huggingface API in order to generate model answers to survey questions.')
    parser.add_argument('--model', type=str, help='Model name', choices=['google/gemma-2-27b-it'], required=True)
    parser.add_argument('--api_key', type=str, help='Huggingface API key', default=None)
    parser.add_argument('--dataset', type=str, help='Path to the original dataset', default=os.path.join(prefix, "dataset", "survey.csv"))

    # Required arguments
    args = parser.parse_args()
    
    # Convert to dictionary
    engine = InferenceEngine(args)
    engine.run()
   