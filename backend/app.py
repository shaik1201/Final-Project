from flask import Flask, jsonify, request
from models import Job
from flask_cors import CORS
from jobs_scrapper import get_indeed_jobs
from pymongo import MongoClient
import config

# Example using Flask

app = Flask(__name__)
CORS(app)

# Database setup
client = MongoClient(config.MONGO_URI)
db = client.job_search_db


# @app.route('/jobs/scrape', methods=['POST'])
# def get_jobs_scrape():
#     indeed_jobs = get_indeed_jobs()
#     for job in indeed_jobs:
#         # print(get_gemini_response(job['description']))
#         try:
#             job['years_of_experience'] = get_gemini_response(job['description'])['years_of_experience']
#             job['degree_required'] = get_gemini_response(job['description'])['degree_required']
#         except:
#             job['years_of_experience'] = None
#             job['degree_required'] = None
#
#     print(indeed_jobs)
#
#     for job in indeed_jobs:
#         Job.create_job(job)
#     return jsonify({"message": "Jobs scraped successfully!"}), 201



@app.route('/jobs', methods=['GET'])
def get_jobs():
    job_list = Job.get_all_jobs()
    return jsonify(job_list)

@app.route('/search', methods=['POST'])
def search_jobs():
    job_list = Job.get_all_jobs()
    user_job_title = request.get_json()['user_job_title']
    relevant_jobs = [job for job in job_list if user_job_title.lower() in job['title'].lower()]
    return jsonify(relevant_jobs)

@app.route('/filters', methods=['GET'])
def get_filters():
    filters = get_unique_filter_values()
    return jsonify(filters)


# Function to get unique filter values from the database
def get_unique_filter_values():
    unique_filters = {
        "company": db.jobs.distinct("company"),
        "location": db.jobs.distinct("location"),
        "datePosted": ["Last 24 hours", "Last 7 days"],  # You might want to dynamically calculate these
        "fieldOfExpertise": db.jobs.distinct("field_of_expertise"),
        "minExperience": db.jobs.distinct("minimum_experience"),
        "softSkills": db.jobs.distinct("soft_skills"),
        "techSkills": db.jobs.distinct("technical_skills"),
        "industry": db.jobs.distinct("industry"),
        "scope": db.jobs.distinct("scope_of_position"),
        "jobType": db.jobs.distinct("job_type")
    }

    return unique_filters


if __name__ == '__main__':
    app.run(debug=True)



