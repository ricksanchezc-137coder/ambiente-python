import os 
from dotenv import load_dotenv

print("Antes do load_dotenv:", os.getenv("API_KEY"))

load_dotenv()

print("Depois do load_dotenv:", os.getenv("API_KEY"))
print("DEBUG:", os.getenv("DEBUG"))

