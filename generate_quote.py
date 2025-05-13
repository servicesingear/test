from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time  # Optional: To add a delay between iterations

load_dotenv(override=True)  # Load environment variables from .env file
api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key)

# File to store generated prompts
PROMPT_FILE = "generated_quotes.txt"

# Function to read existing prompts from the file
def get_existing_prompts(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as file:
        return file.read().splitlines()

# Run the generation process 30 times
for _ in range(1):
    existing_prompts = get_existing_prompts(PROMPT_FILE)
    existing_prompts_text = "\n".join(existing_prompts)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            f"give me a short quotation , but dont repeat the following\n{existing_prompts_text}"
        ],
        config=types.GenerateContentConfig(
            max_output_tokens=500,
            temperature=0.2
        )
    )
    generated_prompt = response.text.strip()
    if generated_prompt not in existing_prompts:
        with open(PROMPT_FILE, "a", encoding="utf-8") as file:  # Specify UTF-8 encoding
            file.write(generated_prompt + "\n")
        print(generated_prompt)

    # Optional: Add a delay to avoid overwhelming the API
    time.sleep(1)
