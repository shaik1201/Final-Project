from pymongo import MongoClient
import config

try:
    client = MongoClient(config.MONGO_URI)
    db = client.job_search_db
    print("Connection to MongoDB successful")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

class Job:
    def __init__(self, title, description, job_id, company, location, date, link, Education, Field_of_Expertise, Minimum_Experience, Technical_Skills, Industry, Scope_of_Position, Job_Type):
        self.title = title
        self.description = description
        self.job_id = job_id
        self.company = company
        self.location = location
        self.date = date
        self.link = link
        self.education = Education
        self.field_of_expertise = Field_of_Expertise
        self.minimum_experience = Minimum_Experience
        # self.soft_skills = Soft_Skills
        self.technical_skills = Technical_Skills
        self.industry = Industry
        self.scope_of_position = Scope_of_Position
        self.job_type = Job_Type

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
            "education": job_data['Education'],
            "field_of_expertise": job_data['Field of Expertise'],
            "minimum_experience": job_data['Minimum Experience'],
            # "soft_skills": job_data['Soft Skills'],
            "technical_skills": job_data['Technical Skills'],
            "industry": job_data['Industry'],
            "scope_of_position": job_data['Scope of Position'],
            "job_type": job_data['Job Type']
        }
        db.jobs.insert_one(job)


    @staticmethod
    def get_all_jobs():
        jobs = db.jobs.find()
        job_list = [{"title": job["title"], "description": job["description"],
                    "job_id": job['job_id'], "company": job['company'],
                    "location": job['location'], "date": job['date'],
                    "link": job['link'], "education": job['education'],
                    "field_of_expertise": job['field_of_expertise'],
                    "minimum_experience": job['minimum_experience'],
                    "technical_skills": job['technical_skills'],
                    "industry": job['industry'], "scope_of_position": job['scope_of_position'],
                    "job_type": job['job_type']
                    } for job in jobs]
        return job_list

    @staticmethod
    def get_job_by_id(job_id):
        job = db.jobs.find_one({"_id": job_id})
        if job:
            return {"title": job["title"], "description": job["description"],
                    "job_id": job['job_id'], "company": job['company'],
                    "location": job['location'], "date": job['date'],
                    "link": job['link'], "education": job['education'],
                    "field_of_expertise": job['field_of_expertise'],
                    "minimum_experience": job['minimum_experience'],
                    "technical_skills": job['technical_skills'],
                    "industry": job['industry'], "scope_of_position": job['scope_of_position'],
                    "job_type": job['job_type']
                    }
        return None

    @staticmethod
    def update_job(job_id, job):
        db.jobs.update_one(
            {"_id": job_id},
            {"$set": {"title": job["title"], "description": job["description"],
                    "job_id": job['job_id'], "company": job['company'],
                    "location": job['location'], "date": job['date'],
                    "link": job['link'], "education": job['education'],
                    "field_of_expertise": job['field_of_expertise'],
                    "minimum_experience": job['minimum_experience'],
                    "technical_skills": job['technical_skills'],
                    "industry": job['industry'], "scope_of_position": job['scope_of_position'],
                    "job_type": job['job_type']
                    }
             }
        )

    @staticmethod
    def delete_job(job_id):
        db.jobs.delete_one({"_id": job_id})

