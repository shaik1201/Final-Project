from flask import Flask, jsonify, request
from models import Job
from flask_cors import CORS
from datetime import datetime, timedelta

from pymongo import MongoClient
import config
import re
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


@app.route('/upload_cv', methods=['POST'])
def upload_cv():
    if 'cv' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['cv']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 401

    if file:
        text = extract_text(file)
        if text:
            features = get_gemini_response(text)
            if 'error' in features:
                return jsonify({"error": features['error']}), 402

            field_of_expertise = features['field_of_expertise']
            years_of_experience = features['years_of_experience']
            technical_skills = features['technical_skills']
            is_student = features['is_student']

            job_list = Job.get_all_jobs()
            relevant_jobs = []
            for job in job_list:
                if field_of_expertise:
                    field_of_expertise_lower = [f.lower() for f in field_of_expertise]
                    job_field_of_expertise_lower = [item.strip().lower() for item in job['field_of_expertise'].split(',')]
                    if not any(f in field_of_expertise_lower for f in job_field_of_expertise_lower):
                        continue
                if years_of_experience and int(years_of_experience) < int(job['minimum_experience'][0]):
                    continue
                if technical_skills:
                    tech_skills_lower = [t.lower() for t in technical_skills]
                    job_tech_skills_lower = [item.strip().lower() for item in job['technical_skills'].split(',')]
                    if not any(t in tech_skills_lower for t in job_tech_skills_lower):
                        continue
                if is_student is True and job['scope_of_position'] == 'Full-time':
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
    user_company = filters['filters'].get('company', '')
    user_location = filters['filters'].get('location', '')
    user_date_posted = filters['filters'].get('datePosted', [])  # Expecting a list
    user_field_of_expertise = filters['filters'].get('fieldOfExpertise', '')
    user_min_experience = filters['filters'].get('minExperience', '')
    user_tech_skills = filters['filters'].get('techSkills', '')
    user_industry = filters['filters'].get('industry', '')
    user_scope = filters['filters'].get('scope', '')
    user_job_type = filters['filters'].get('jobType', '')

    # Get the current time
    now = datetime.now()

    # Create a list to store all date thresholds based on user selection
    date_thresholds = []

    # Convert each date filter into a date threshold and store it in the list
    for date_filter in user_date_posted:
        if date_filter == "Past 3 Days":
            date_thresholds.append(now - timedelta(days=3))
        elif date_filter == "Past 7 Days":
            date_thresholds.append(now - timedelta(days=7))
        elif date_filter == "Past 14 Days":
            date_thresholds.append(now - timedelta(days=14))
        elif date_filter == "Past 1 Month":
            date_thresholds.append(now - timedelta(days=30))

    job_list = Job.get_all_jobs()

    relevant_jobs = []
    for job in job_list:
        # if user_job_title and not any(title in job['title'].lower() for title in user_job_title):
        #     continue
        if user_job_title and user_job_title not in job['title'].lower():
            continue

        if user_company and not any(company in job['company'] for company in user_company):
            continue

        if user_location and not any(location in job['location'] for location in user_location):
            continue

        if user_field_of_expertise and not any(
                expertise in job['field_of_expertise'] for expertise in user_field_of_expertise):
            continue

        if user_min_experience and not any(
                experience in job['minimum_experience'] for experience in user_min_experience):
            continue

        if user_tech_skills and not any(tech_skill in job['technical_skills'] for tech_skill in user_tech_skills):
            continue

        if user_industry and not any(industry in job['industry'] for industry in user_industry):
            continue

        if user_scope and not any(scope in job['scope_of_position'] for scope in user_scope):
            continue

        if user_job_type and not any(job_type in job['job_type'] for job_type in user_job_type):
            continue

        # Filter by date if date thresholds are set
        if date_thresholds:
            job_date = datetime.strptime(job['date'], '%Y-%m-%d')
            # Check if the job date is within any of the date ranges
            if not any(job_date >= threshold for threshold in date_thresholds):
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
                    # Use a simpler split for companies and locations
                    parts = re.split(r'or | and | / | \(|\)', value)
                else:
                    # Use the original, more complex split for other attributes
                    parts = re.split(r', | or | and | / | \(|\)', value)

                for part in parts:
                    clean_part = part.strip()

                    # Handle the singular form of "year"
                    if name == "minimum_experience" and clean_part == "1 years":
                        clean_part = "1 year"

                    if clean_part and clean_part not in exclude_set and "מחוז" not in clean_part:
                        result_set.add(clean_part)

    companies = set()
    add_to_set("company", db.jobs.distinct("company"), companies)

    locations = set()
    add_to_set("location", db.jobs.distinct("location"), locations)

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

    # Predefined date options in the correct order with new labels
    dates_posted = ["Past 3 Days", "Past 7 Days", "Past 14 Days", "Past 1 Month"]

    unique_filters = {
        "company": sorted(list(companies)),
        "location": sorted(list(locations)),
        "datePosted": dates_posted,  # Explicit order with new labels
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
