from pymongo import MongoClient
from datetime import datetime, timedelta
import config
import math

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
            "technical_skills": job_data['Technical Skills'],
            "industry": job_data['Industry'],
            "scope_of_position": job_data['Scope of Position'],
            "job_type": job_data['Job Type']
        }
        db.jobs.insert_one(job)


    @staticmethod
    def get_all_jobs():
        jobs = db.jobs.find().sort([("date", -1), ("title", 1)])  # Sort by date (descending) and then by title (ascending)
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

    @staticmethod
    def print_all_jobs():
        jobs = db.jobs.find()
        for job in jobs:
            print(job)

    import math

    @staticmethod
    def clean_and_delete_jobs():
        jobs = db.jobs.find()

        for job in jobs:
            job_id = job["_id"]
            title = job.get("title")
            link = job.get("link")
            company = job.get("company")

            # Check if 'title', 'link', or 'company' are NaN or None
            if (title is None or (isinstance(title, float) and math.isnan(title))) or \
                    (link is None or (isinstance(link, float) and math.isnan(link))) or \
                    (company is None or (isinstance(company, float) and math.isnan(company))):
                print(f"Deleting job with ID: {job_id} due to NaN in title, link, or company")
                db.jobs.delete_one({"_id": job_id})
            else:
                # Check other fields and replace NaN or None with "Other"
                fields_to_check = [
                    "description", "location", "date", "education",
                    "field_of_expertise", "minimum_experience",
                    "technical_skills", "industry", "scope_of_position", "job_type"
                ]

                update_fields = {}
                for field in fields_to_check:
                    value = job.get(field)
                    if value is None or (isinstance(value, float) and math.isnan(value)):
                        update_fields[field] = "No Specified"

                # Update the job if there are fields to update
                if update_fields:
                    print(f"Updating job with ID: {job_id} with fields: {update_fields}")
                    db.jobs.update_one({"_id": job_id}, {"$set": update_fields})


    @staticmethod
    def delete_old_jobs():
        # Calculate the date one month ago from today
        one_month_ago = datetime.now() - timedelta(days=30)

        # Find and delete jobs that were posted more than a month ago
        deleted_count = 0
        for job in db.jobs.find():
            job_date_str = job.get("date")
            if job_date_str:
                try:
                    # Assuming the date is stored as a string in 'YYYY-MM-DD' format
                    job_date = datetime.strptime(job_date_str, '%Y-%m-%d')

                    if job_date < one_month_ago:
                        print(
                            f"Deleting job with ID: {job['_id']}, Title: {job.get('title', 'No title')}, Date: {job_date_str}")
                        db.jobs.delete_one({"_id": job["_id"]})
                        deleted_count += 1
                except ValueError:
                    print(f"Skipping job with ID: {job['_id']} due to invalid date format: {job_date_str}")

        print(f"Total jobs deleted: {deleted_count}")

    @staticmethod
    def delete_duplicate_jobs():
        # Use an aggregation pipeline to find duplicates based on date, title, company, and location
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "date": "$date",
                        "title": "$title",
                        "company": "$company",
                        "location": "$location"
                    },
                    "count": {"$sum": 1},
                    "ids": {"$push": "$_id"}
                }
            },
            {"$match": {"count": {"$gt": 1}}}
        ]

        duplicates = list(db.jobs.aggregate(pipeline))
        deleted_count = 0

        for duplicate in duplicates:
            job_identifiers = duplicate["_id"]
            job_ids = duplicate["ids"]

            # Keep the first job, delete the rest
            job_ids_to_delete = job_ids[1:]  # Keep the first one, delete the rest

            for _id in job_ids_to_delete:
                db.jobs.delete_one({"_id": _id})
                deleted_count += 1
                print(f"Deleted duplicate job with date: {job_identifiers['date']}, title: {job_identifiers['title']}, "
                      f"company: {job_identifiers['company']}, location: {job_identifiers['location']}, _id: {_id}")

        print(f"Total duplicate jobs deleted: {deleted_count}")

    # delete jobs not from israel
    @staticmethod
    def delete_jobs_by_location(locations):
        # Build the query to match jobs with locations in the specified list
        query = {"location": {"$in": locations}}

        # Delete the matching jobs
        result = db.jobs.delete_many(query)

        print(f"Deleted {result.deleted_count} jobs with specified locations.")


    @staticmethod
    def delete_jobs_by_title(titles):
        # Ensure titles is a list
        if isinstance(titles, str):
            titles = [titles]

        # Build the query to match jobs with titles in the specified list
        query = {"title": {"$in": titles}}

        # Delete the matching jobs
        result = db.jobs.delete_many(query)

        print(f"Deleted {result.deleted_count} jobs with specified titles.")






