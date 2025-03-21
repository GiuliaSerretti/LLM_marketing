import llm_marketing.prompts as llm_prompts
from huggingface_hub import InferenceClient
import random
import os
import pandas as pd
import json

class InferenceEngine:
    def __init__(self, args):
        self.args = args
    
        # Check if API key is set via command line
        if args.api_key is not None:
            api_key = args.api_key
        elif "HF_API_KEY" in os.environ:
            api_key = os.environ["HF_API_KEY"]
        else:
            raise ValueError("API key not found. Please set it via command line or environment variable HF_API_KEY.")
    
        # Create HF InferenceClient
        self.client = InferenceClient(api_key=api_key, headers={"X-use-cache": "false"})

        # Load original dataset
        self.df = pd.read_csv(args.dataset)
        self.cols = self.df.columns
        self.df = self.df[self.cols[1:5]]
        # Rename columns
        self.df.columns = ["GENDER", "AGE", "EMPLOYMENT", "INCOME"]

        # Check if model supports system context
        if "gemma" in args.model:
            self.system = False
        else:
            self.system = True

    def bootstrap_profiles(self, n=None):
        if n is None:
            n = len(self.df)
        return self.df.sample(n, replace=True)
    
    def generate_prompt(self, profile):
        # Get profile values
        GENDER = profile["GENDER"]
        AGE = profile["AGE"]
        EMPLOYMENT = profile["EMPLOYMENT"]
        INCOME = profile["INCOME"]

        # Generate prompt
        prompt = llm_prompts.prompt
        prompt = prompt.replace("[AGE]", str(AGE))
        prompt = prompt.replace("[GENDER]", str(GENDER))
        prompt = prompt.replace("[EMPLOYMENT]", str(EMPLOYMENT))
        prompt = prompt.replace("[INCOME]", str(INCOME))

        if self.system:
            messages = [
                    {"role": "system", "content": llm_prompts.context},
                    {"role": "user", "content": prompt},
                ]
        else:
            messages = [
                {"role": "user", "content": "\n".join([llm_prompts.context, prompt])}
            ]
            
        return messages
        
    def parse_json(self, json_data):
        print(json_data)
        try:
            # Remove markdown formatting
            json_data = json_data.replace("```json\n", "")
            json_data = json_data.replace("```json", "")
            json_data = json_data.replace("```", "")
            data = json.loads(json_data)
            return data
        except:
            return None
        
    def generate_answer(self, messages):
        completion = self.client.chat.completions.create(
            model="google/gemma-2-27b-it", 
            messages=messages, 
            max_tokens=512,
            # temperature=1.0,       # Increase randomness
            # top_p=0.9,              # Enable more token diversity
            seed = random.randint(0, int(1e9)),
        )
        # Print number of tokens
        return self.parse_json(completion.choices[0].message.content)

    def run(self):
        profile = self.bootstrap_profiles(n=1).iloc[0]
        messages = self.generate_prompt(profile)
        answer = self.generate_answer(messages)
        
        if answer is None:
            print("Invalid JSON format. Please try again.")
        print(answer)
        # Create df with answers using self.cols as columns
        df = pd.DataFrame([answer])
        df.columns = self.cols[1:]

        # Save to CSV
        df.to_csv("output.csv", index=False)
        print("Saved to output.csv")
            
