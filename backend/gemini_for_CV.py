import config
import google.generativeai as genai
import json

def get_gemini_response(text):
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

    # model_output_dict = json.loads(model_output_json)
    
    # print(model_output_dict)
    
    return model_output_json