import llm_marketing.prompts as llm_prompts
from openai import OpenAI
import random
import os
import pandas as pd
import json
from PandaSQLite import PandaSQLiteDB
import time

class InferenceEngine:
    def __init__(self, args):
        self.args = args
        self.model = args.model
    
        # Check if API key is set via command line
        if args.api_key is not None:
            api_key = args.api_key
        elif "NOVITA_API_KEY" in os.environ:
            api_key = os.environ["NOVITA_API_KEY"]
        else:
            raise ValueError("API key not found. Please set it via command line or environment variable HF_API_KEY.")
    
        print(f"Using model: {args.model}")
        # Create HF InferenceClient
        self.client = OpenAI(
            base_url="https://api.novita.ai/v3/openai",
            api_key=api_key
        )

        self.db = PandaSQLiteDB(args.output)
        self.create_schema()

    def create_schema(self):
        self.tname = self.model.replace("/", "_").replace("-","_").replace(".","_") + "_answers"
        print(f"Creating table {self.tname}")
        # Create schema
        self.db.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.tname} (
            profile_id INTEGER,
            answer_id INTEGER,
            gender TEXT,
            age TEXT,
            employment TEXT,
            income TEXT,
            Q1 INTEGER,
            Q2 INTEGER,
            Q3 INTEGER,
            Q4 INTEGER,
            Q5 INTEGER,
            Q6 INTEGER,
            Q7 INTEGER,
            Q8 INTEGER,
            Q9 INTEGER,
            Q10 TEXT,
            Q11 INTEGER,
            Q12 INTEGER,
            Q13 INTEGER,
            Q14 INTEGER,
            Q15 INTEGER,
            Q16 INTEGER,
            Q17 INTEGER,
            Q18 INTEGER,
            Q19 TEXT,
            Q20 INTEGER
        )
        """)
            
    
    def generate_prompt(self, profile):
        # Get profile values
        GENDER = profile["GENDER"]
        AGE = profile["AGE"]
        EMPLOYMENT = profile["EMPLOYMENT"]
        INCOME = profile["INCOME"]

        # Generate prompt
        context = llm_prompts.context
        context = context.replace("[AGE]", str(AGE).lower().replace(".", ""))
        context = context.replace("[GENDER]", str(GENDER).lower().replace(".", ""))
        context = context.replace("[EMPLOYMENT]", str(EMPLOYMENT).lower().replace(".", ""))
        context = context.replace("[INCOME]", str(INCOME).lower().replace(".", ""))

        messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": llm_prompts.prompt},
            ]

        return messages
        
    def parse_json(self, json_data):
        try:
            # Remove markdown formatting
            json_data = json_data.replace("```json\n", "")
            json_data = json_data.replace("```json", "")
            json_data = json_data.replace("```", "")
            # print(f"Parsing JSON: {json_data}")
            data = json.loads(json_data)
            return data
        except:
            return None
    
    def save_to_db(self, profile_id, answer_id, profile, data):
        def wrap(val):
            if isinstance(val, str):
                escaped = val.replace("'", "''")  # escape single quotes
                return f"'{escaped}'"
            elif isinstance(val, list):
                # Convert list to comma-separated string and escape it
                joined = ",".join(map(str, val))
                escaped = joined.replace("'", "''")
                return f"'{escaped}'"
            else:
                return str(val)

        # Merge all values in the correct order
        values = [
            profile_id,
            answer_id,
            profile["GENDER"],
            profile["AGE"],
            profile["EMPLOYMENT"],
            profile["INCOME"],
            data["Q1"], data["Q2"], data["Q3"], data["Q4"], data["Q5"],
            data["Q6"], data["Q7"], data["Q8"], data["Q9"], data["Q10"],
            data["Q11"], data["Q12"], data["Q13"], data["Q14"], data["Q15"],
            data["Q16"], data["Q17"], data["Q18"], data["Q19"], data["Q20"],
        ]

        wrapped_values = ", ".join(wrap(v) for v in values)

        self.db.execute(f"""
            INSERT INTO {self.tname} (
                profile_id, answer_id,
                gender, age, employment, income,
                Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10,
                Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20
            ) VALUES ({wrapped_values})
        """)


    def generate_answer(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
            max_tokens=self.args.max_tokens,
            temperature=self.args.temperature,
            seed=random.randint(0, 10000),
            top_p=self.args.top_p,
        )

        return self.parse_json(completion.choices[0].message.content)
    
    def generate_answer(self, messages):
        for attempt in range(3):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=False,
                    max_tokens=self.args.max_tokens,
                    temperature=self.args.temperature,
                    seed=random.randint(0, 10000),
                    top_p=self.args.top_p,
                )
                return self.parse_json(completion.choices[0].message.content)        
            except Exception as e:
                print(f"[Warning] APIStatusError (attempt {attempt+1}/3): {e}")
                time.sleep(15 * (attempt + 1))  # Exponential backoff
        # if we get here, all retries failed:
        raise RuntimeError("LLM call failed after 3 retries")

    def run(self, df, chunk_id):
        self.df = df
        # Iterate over all profiles in the dataset
        w = 0
        n_answers = self.args.num_samples_per_profile * len(self.df)
        for idx in range(len(self.df)):
            if w % 5 == 0:
                print(f"Chunk {chunk_id} - Profile {idx} - {w}/{n_answers} answers generated")
                
            # Get profile
            profile = self.df.iloc[idx]
            messages = self.generate_prompt(profile)

            answer_id = 0
            while answer_id < self.args.num_samples_per_profile:
                # Generate answer
                answer = self.generate_answer(messages)
            
                if answer is None:
                    print(f"Chunk {chunk_id} - Invalid JSON format. Retrying...")
                    continue
                
                # Save to database
                try:
                    self.save_to_db(profile["ID"], answer_id, profile, answer)
                    self.db.commit()
                except:
                    print(f"Chunk {chunk_id} - Error saving to database. Retrying...")
                    continue
                answer_id += 1
                w += 1