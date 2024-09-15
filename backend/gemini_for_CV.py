import config
import time
import google.generativeai as genai
import json
import re

def get_gemini_response(text, max_retries=5, delay=2):
    for attempt in range(max_retries):
        GOOGLE_API_KEY = config.GOOGLE_API_KEY
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt = f'''
        Based on the following CV text: {text}, extract the user's field of expertise,
        years of experience, technical skills, and whether the user is a student or not.
        Provide the output in valid JSON format. Example output:
        {{
            "field_of_expertise": ["Data Science", "Data Engineering"],
            "years_of_experience": 2,
            "technical_skills": ["Python", "JavaScript"],
            "is_student": false
        }}

        If you cannot extract **any** of the fields (due to lack of information or unrecognizable content), return the following error message:
        {{
            "error": "The uploaded file is not a CV or lacks the required information."
        }}
        '''

        # check for education, years_of_experience
        model_output = model.generate_content(prompt).text
        # Use regular expressions to remove the markdown code block syntax in a case-insensitive manner
        clean_output = re.sub(r'^```json\n', '', model_output, flags=re.IGNORECASE)
        model_output_json = re.sub(r'```$', '', clean_output, flags=re.IGNORECASE).strip()
        if is_valid_json(model_output_json):
            output_dict = json.loads(model_output_json)
            if 'error' in output_dict:
                return output_dict
            is_student = output_dict['is_student']
            if isValidStudent(is_student):
                return output_dict
            else:
                print(f"Retry {attempt + 1}/{max_retries}: Failed to parse JSON. Retrying in {delay} seconds...")
                time.sleep(delay)
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

def isValidStudent(value):
    # Check if the value is "yes" or "no"
    if value in [False, True]:
        return True
    return False