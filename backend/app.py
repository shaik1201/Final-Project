from flask import Flask, jsonify, request
from models import Job
from flask_cors import CORS
# from jobs_scrapper import get_indeed_jobs
from pymongo import MongoClient
import config
import re
# from deep_translator import GoogleTranslator
import os
from read_pdf import extract_text
from gemini_for_CV import get_gemini_response
import json

app = Flask(__name__)
CORS(app)

try:
    client = MongoClient(config.MONGO_URI)
    db = client.job_search_db
    print("Connection to MongoDB successful")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

# UPLOAD_FOLDER = 'uploads'  # Directory to save the uploaded files
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

@app.route('/upload_cv', methods=['POST'])
def upload_cv():
    if 'cv' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['cv']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        text = extract_text(file)
        if text:
            # print(text)
            features = json.loads(get_gemini_response(text))
            print(features)
            years_of_experience = features['years_of_experience']
            soft_skills = features['soft_skills']
            technical_skills = features['technical_skills']
            field_of_expertise = features['field_of_expertise']
            is_student = features['is_student']
            job_list = Job.get_all_jobs()
            relevant_jobs = []
            for job in job_list:
                if years_of_experience and int(years_of_experience) < int(job['minimum_experience'][0]):
                    continue
                # if soft_skills and not any(skill in job['soft_skills'] for skill in soft_skills):
                #     continue
                # if technical_skills and not any(skill in job['technical_skills'] for skill in technical_skills):
                #     continue
                # if field_of_expertise and field_of_expertise not in job['field_of_expertise']:
                #     continue
                if (is_student == False and job['scope_of_position'] == 'Part-time')\
                    or (is_student == True and job['scope_of_position'] == 'Full-time'):
                    continue
                relevant_jobs.append(job)
            return jsonify(relevant_jobs)
            
            
        return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"error": "File upload failed"}), 500


@app.route('/jobs', methods=['GET'])
def get_jobs():
    job_list = Job.get_all_jobs()
    return jsonify(job_list)


@app.route('/search', methods=['POST'])
def search_jobs():
    filters = request.get_json()
    user_job_title = filters.get('title', '').lower()
    user_city = filters.get('city', '').lower()

    # Collect filter values
    user_company = filters['filters'].get('company', '')
    user_location = filters['filters'].get('location', '')
    user_date_posted = filters['filters'].get('datePosted', '')
    user_field_of_expertise = filters['filters'].get('fieldOfExpertise', '')
    user_min_experience = filters['filters'].get('minExperience', '')
    user_soft_skills = filters['filters'].get('softSkills', '')
    user_tech_skills = filters['filters'].get('techSkills', '')
    user_industry = filters['filters'].get('industry', '')
    user_scope = filters['filters'].get('scope', '')
    user_job_type = filters['filters'].get('jobType', '')

    job_list = Job.get_all_jobs()
    print(user_job_type)

    relevant_jobs = []
    for job in job_list:
        if user_job_title and user_job_title not in job['title'].lower():
            continue
        if user_city and user_city not in job['location'].lower():
            continue
        if user_company and user_company not in job['company']:
            continue
        if user_location and user_location not in job['location']:
            continue
        if user_date_posted and user_date_posted not in job['date']:
            continue
        if user_field_of_expertise and user_field_of_expertise not in job['field_of_expertise']:
            continue
        if user_min_experience and user_min_experience not in job['minimum_experience']:
            continue
        if user_soft_skills and user_soft_skills not in job['soft_skills']:
            continue
        if user_tech_skills and user_tech_skills not in job['technical_skills']:
            continue
        if user_industry and user_industry not in job['industry']:
            continue
        if user_scope and user_scope not in job['scope_of_position']:
            continue
        if user_job_type and user_job_type not in job['job_type']:
            continue

        relevant_jobs.append(job)

    return jsonify(relevant_jobs)


@app.route('/filters', methods=['GET'])
def get_filters():
    filters = get_unique_filter_values()
    return jsonify(filters)



def get_unique_filter_values():
    def add_to_set(name, distinct_values, result_set):
        exclude_set = {"etc.", "None", "Other", "none", "other", "nan"}  # Add any other values you want to exclude here
        for value in distinct_values:
            if value:
                if name == "company" or name == 'location':
                    # Use a simpler split for companies
                    parts = re.split(r'or | and | / | \(|\)', value)
                else:
                    # Use the original, more complex split for other attributes
                    parts = re.split(r', | or | and | / | \(|\)', value)

                for part in parts:
                    clean_part = part.strip()
                    if clean_part and clean_part not in exclude_set and "מחוז" not in clean_part:
                        result_set.add(clean_part)

    # Usage of add_to_set with the name parameter
    companies = set()
    add_to_set("company", db.jobs.distinct("company"), companies)

    locations = set()
    add_to_set("location", db.jobs.distinct("location"), locations)

    dates_posted = set()
    add_to_set("date", db.jobs.distinct("date"), dates_posted)

    fields_of_expertise = set()
    add_to_set("field_of_expertise", db.jobs.distinct("field_of_expertise"), fields_of_expertise)

    min_experience = set()
    add_to_set("minimum_experience", db.jobs.distinct("minimum_experience"), min_experience)

    soft_skills = set()
    add_to_set("soft_skills", db.jobs.distinct("soft_skills"), soft_skills)

    tech_skills = set()
    add_to_set("technical_skills", db.jobs.distinct("technical_skills"), tech_skills)

    industries = set()
    add_to_set("industry", db.jobs.distinct("industry"), industries)

    scopes = set()
    add_to_set("scope_of_position", db.jobs.distinct("scope_of_position"), scopes)

    job_types = set()
    add_to_set("job_type", db.jobs.distinct("job_type"), job_types)

    # Translate locations
    # translated_locations = set()
    # for location in locations:
    #     translated_location = GoogleTranslator(source='iw', target='en').translate(location)
    #     translated_locations.add(translated_location)

    unique_filters = {
        "company": sorted(list(companies)),
        "location": sorted(list(locations)),
        "datePosted": sorted(list(dates_posted)),  # You might want to dynamically calculate these
        "fieldOfExpertise": sorted(list(fields_of_expertise)),
        "minExperience": sorted(list(min_experience)),
        "softSkills": sorted(list(soft_skills)),
        "techSkills": sorted(list(tech_skills)),
        "industry": sorted(list(industries)),
        "scope": sorted(list(scopes)),
        "jobType": sorted(list(job_types))
    }

    return unique_filters



if __name__ == '__main__':
    app.run(debug=True)



