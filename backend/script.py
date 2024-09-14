from jobs_scrapper import get_indeed_jobs, get_linkedin_jobs
from gemini_prompts import edit_data, prompts_dict
from models import Job


if __name__ == '__main__':

    # Define the skills to scrape jobs for
    roles = ["Software Engineer", "Data Scientist", "Data Engineer",
              "Data Analyst", "Business Intelligence (BI) Developer",
              "DevOps Engineer", "Cloud Engineer", "AI/ML Engineer",
              "Cybersecurity Engineer", "Product Manager"]

    # Define the number of jobs to scrape per skill
    num_jobs_per_role = 10

    # Define the sort order of the jobs
    sort = 'date'

    # Initialize empty lists to store job data
    indeed_jobs = []
    linkedin_jobs = []

    # Scrape jobs from Indeed
    for role in roles:  # First five skills
        scrapped_indeed_jobs_dict = get_indeed_jobs(role, num_jobs_per_role, sort)
        # Edit the scraped data and add new features
        indeed_jobs.extend(scrapped_indeed_jobs_dict)
    # Scrape jobs from LinkedIn for the last five skills
    for role in roles:  # Last five skills
        scrapped_linkedin_jobs_dict = get_linkedin_jobs(role, num_jobs_per_role, sort)
        # Edit the scraped data and add new features
        linkedin_jobs.extend(scrapped_linkedin_jobs_dict)
    print("Jobs scraped successfully!")

    indeed_jobs_new = edit_data(indeed_jobs, prompts_dict)
    linkedin_jobs_new = edit_data(linkedin_jobs, prompts_dict)
    print("New features added successfully!")

    for job in indeed_jobs_new:
        Job.create_job(job)

    for job in linkedin_jobs_new:
        Job.create_job(job)

    # Delete all jobs that 'title', 'link', or 'company' are NaN or None
    Job.clean_and_delete_jobs()
    print("Jobs cleaned successfully!")

    # Delete jobs that were posted more than a month ago
    Job.delete_old_jobs()
    print("Old jobs deleted successfully!")

    # Delete duplicate jobs
    Job.delete_duplicate_jobs()
    print("Duplicate jobs deleted successfully!")

    print("All Jobs in the Database:")
    Job.print_all_jobs()

