import config
import google.generativeai as genai
import json

def get_gemini_response(text):
    GOOGLE_API_KEY = config.GOOGLE_API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    model_output = model.generate_content(f'''
    based on the following CV text: {text} extract the user years of experience,
    soft skills, technical skills, field of expertise and if the user is a student or not.
    make the output in a json format so when i will do json.load(output) it will work. Example for an output: {'{'}
    'years_of_experience': 2,
    'soft_skills': ['communication', 'teamwork'],
    'technical_skills': ['Python', 'JavaScript'],
    'field_of_expertise': 'Data Science',
    'is_student': False
    {'}'}
''').text.strip()

    # print("Model Output:", model_output)
    # print(type(model_output))

    model_output_json = model_output.replace("'", '"')
    
    print(model_output_json)

    model_output_dict = json.loads(model_output_json)
    
    print(model_output_dict)