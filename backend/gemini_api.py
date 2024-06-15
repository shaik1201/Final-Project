import google.generativeai as genai
import json
import config

GOOGLE_API_KEY = config.GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_gemini_response(description):
    prompt = f"based on the following role description: {description} extract the years of experience required and the degree required. Example for an output: {{'years_of_experience': 2, 'degree_required': 'CS'}}."
    response = model.generate_content(prompt)
    model_output = response.text.strip()

    # print("Model Output:", model_output)
    # print(type(model_output))

    model_output_json = model_output.replace("'", '"').replace('None', 'null')

    try:
        model_output_dict = json.loads(model_output_json)
        
        years_of_experience = model_output_dict['years_of_experience']
        degree_required = model_output_dict['degree_required']
        
        # print(years_of_experience)
        # print(degree_required)

        return {
            'years_of_experience': years_of_experience,
            'degree_required': degree_required
        }
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None
    