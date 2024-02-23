from openai import OpenAI
import os
import dotenv
import time
dotenv.load_dotenv()
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
client = OpenAI(
    api_key=OPENAI_API_KEY
)
completion = client.chat.completions.create(
# the format is just like model="ft:gpt-3.5-turbo-1106:mygpt::8xzcvv2C"
  model="YOUR-FINE-TUNED-MODEL-NAME",
  messages=[
    {"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."},
    {"role": "user", "content": "Hello!"}
  ]
)
print(completion.choices[0].message)

