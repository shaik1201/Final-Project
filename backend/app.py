from flask import Flask, jsonify, request
from models import Job
from flask_cors import CORS
from indeed_jobs import get_indeed_jobs
from gemini_api import get_gemini_response

app = Flask(__name__)
CORS(app)

@app.route('/jobs/scrape', methods=['POST'])
def get_jobs_scrape():
    indeed_jobs = get_indeed_jobs()
    for job in indeed_jobs:
        # print(get_gemini_response(job['description']))
        try:
            job['years_of_experience'] = get_gemini_response(job['description'])['years_of_experience']
            job['degree_required'] = get_gemini_response(job['description'])['degree_required']
        except:
            job['years_of_experience'] = None
            job['degree_required'] = None
    
    print(indeed_jobs)
    
    for job in indeed_jobs:
        Job.create_job(job)
    return jsonify({"message": "Jobs scraped successfully!"}), 201

@app.route('/jobs', methods=['GET'])
def get_jobs():
    job_list = Job.get_all_jobs()
    return jsonify(job_list)

@app.route('/search', methods=['POST'])
def search_jobs():
    job_list = Job.get_all_jobs()
    # print(job_list)
    
    user_job_title = request.get_json()['user_job_title']
    print(user_job_title)
    relevant_jobs = []
    for job in job_list:
        if user_job_title.lower() in job['title'].lower():
            relevant_jobs.append(job)
    print(relevant_jobs)
    return jsonify(relevant_jobs)

# @app.route('/jobs', methods=['POST'])
# def add_job():
#     job_data = request.json
#     print(job_data)
#     Job.create_job(job_data)
#     return jsonify({"message": "Job added successfully!"}), 201

@app.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.get_job_by_id(job_id)
    if job:
        return jsonify(job)
    return jsonify({"message": "Job not found"}), 404

@app.route('/jobs/<job_id>', methods=['PUT'])
def update_job(job_id):
    job_data = request.json
    Job.update_job(job_id, job_data)
    return jsonify({"message": "Job updated successfully!"})

@app.route('/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    Job.delete_job(job_id)
    return jsonify({"message": "Job deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
