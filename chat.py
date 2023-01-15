"""
This is the program which uses Cohere AI API.
You can place your query and it will respond with the answser
"""
import os
import cohere

from dotenv import load_dotenv


load_dotenv()

co = cohere.Client(
    os.environ.get("COHEREKEY")
)  # setup your key as COHEREKEY = "your-key" in .env file

# or you can simply give the apikey as string as
# co = cohere.Client("your-key")

prompt = """
This is conversation between intelligent AI and Human

Human: How can you help me?
AI: You can ask me any question you want I will reply with curated answer?

--
Human: What is AI?
AI: Artificial Intelligence is a subfield of computer science.
It enables computers to perform tasks that are characteristic of human intelligence.

--
"""

txt = input("Enter your query : ")

prompt += "Human: {}".format(txt)

response = co.generate(
    model="xlarge",
    prompt=prompt,
    max_tokens=100,
    temperature=0.6,
    stop_sequences=["--"],
)

response = response.generations[0].text
print(response)
