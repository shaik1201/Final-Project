import config
import google.generativeai as genai
import json

GOOGLE_API_KEY = config.GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("based on the following role description: for this data analyst position you need a bachelor's degree in CS/IS/IE and 2 years of experience. extract the years of experience required and the degree required. Example for an output: {'years_of_experience': 2, 'degree_required': 'CS'}.")
model_output = response.text.strip()

print("Model Output:", model_output)
print(type(model_output))

model_output_json = model_output.replace("'", '"')

model_output_dict = json.loads(model_output_json)

print(model_output_dict['years_of_experience'])
print(model_output_dict['degree_required'])
