from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
db = client.job_search_db

class Job:
    def __init__(self, title, description, job_id, company, location, date, link, years_of_experience, degree_required):
        self.title = title
        self.description = description
        self.job_id = job_id
        self.company = company
        self.location = location
        self.date = date
        self.link = link
        self.years_of_experience = years_of_experience
        self.degree_required = degree_required


    @staticmethod
    def create_job(job_data):
        job = {
            "title": job_data['title'],
            "description": job_data['description'],
            "job_id": job_data['job_id'],
            "company": job_data['company'],
            "location": job_data['location'],
            "date": job_data['date'],
            "link": job_data['link'],
            "years_of_experience": job_data['years_of_experience'],
            "degree_required": job_data['degree_required']
        }
        db.jobs_shai.insert_one(job)

    @staticmethod
    def get_all_jobs():
        jobs = db.jobs_shai.find()
        job_list = [{"title": job["title"], "description": job["description"],
                    "job_id": job['job_id'], "company": job['company'],
                    "location": job['location'], "date": job['date'], 
                    "link": job['link'],
                    "years_of_experience": job['years_of_experience'],
                    "degree_required": job['degree_required']} for job in jobs]
        return job_list

    @staticmethod
    def get_job_by_id(job_id):
        job = db.jobs_shai.find_one({"_id": job_id})
        if job:
            return {"title": job["title"], "description": job["description"],
                    "job_id": job['job_id'], "company": job['company'],
                    "location": job['location'], "date": job['date'], 
                    "link": job['link'],
                    "years_of_experience": job['years_of_experience'],
                    "degree_required": job['degree_required']}
        return None

    @staticmethod
    def update_job(job_id, job):
        db.jobs_shai.update_one(
            {"_id": job_id},
            {"$set": {"title": job["title"], "description": job["description"],
                    "job_id": job['job_id'], "company": job['company'],
                    "location": job['location'], "date": job['date'], 
                    "link": job['link'],
                    "years_of_experience": job['years_of_experience'],
                    "degree_required": job['degree_required']}}
        )

    @staticmethod
    def delete_job(job_id):
        db.jobs_shai.delete_one({"_id": job_id})
