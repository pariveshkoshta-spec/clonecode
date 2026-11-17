import os
import re
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def query_llm(prompt: str, model_name: str) -> int:
    retries = 3
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a rigid classification bot. You evaluate code pairs. Your output must be exactly a single digit: '1' or '0'. No text, no explanation."},
                    {"role": "user", "content": prompt}
                ],
                model=model_name,
                temperature=0.0,
                max_tokens=20,
            )
            answer = response.choices[0].message.content.strip()
            
            matches = re.findall(r'[01]', answer)
            if matches:
                return int(matches[0])
            else:
                return 0
        except Exception as e:
            if "429" in str(e) or "Rate limit" in str(e):
                if attempt < retries - 1:
                    time.sleep(3) # Wait before retry
                    continue
            print(f"Error querying {model_name}: {e}")
            return 0
    return 0
