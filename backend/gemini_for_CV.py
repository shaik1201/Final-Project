import config
import time
import google.generativeai as genai
import json


def get_gemini_response(text, max_retries=5, delay=2):
    for attempt in range(max_retries):
        GOOGLE_API_KEY = config.GOOGLE_API_KEY
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f'''
            Based on the following CV text: {text}, extract the user's years of experience,
            soft skills, technical skills, field of expertise, and whether the user is a student or not.
            Make the output in a valid JSON format. Example output:
            {{
                "years_of_experience": 2,
                "soft_skills": ["communication", "teamwork"],
                "technical_skills": ["Python", "JavaScript"],
                "field_of_expertise": "Data Science",
                "is_student": false
            }}
        '''
        model_output = model.generate_content(prompt).text
        model_output_json = model_output.replace("'", '"')

        if is_valid_json(model_output_json):
            return model_output_json
        else:
            print(f"Retry {attempt + 1}/{max_retries}: Failed to parse JSON. Retrying in {delay} seconds...")
            time.sleep(delay)

    raise ValueError("Failed to get valid JSON response from the model after several retries.")


def is_valid_json(data):
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False