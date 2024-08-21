from copy import deepcopy
import pandas as pd
import google.generativeai as genai
import google.api_core.exceptions
import json
import re
import time
import google.api_core.exceptions
import config
import os
from jobs_scrapper import get_linkedin_jobs, get_indeed_jobs
from models import Job


genai.configure(api_key=config.GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

prompt_template = """
Given the following job description, please analyze and divide the content into distinct, relevant features and present the analysis in a structured format suitable for database entry. The expected format for each feature is a key-value pair, where the key is the feature name and the value is the detailed information extracted from the job description. Use the following keys for the feature:

'{feature_key}': {feature_description}

The output must be directly usable as JSON, meaning it should be a single JSON object with no additional characters or formatting outside of this object. Please ensure the response is precisely in the JSON format, without markdown or other syntactical adornments, to facilitate direct parsing into a database. Ensure that you extract the information from the job description accurately and only use the default value if you are absolutely certain the information is not present in the description.
Moreover, ensure you're using triple quotes around the string that spans multiple lines.
Your response should follow this structure:

{{
  "{feature_key}": "{example_output}"
}}

Please ensure the analysis is concise, well-organized, and captures the essence of each section based on the job description provided. The output must be correctly formatted as JSON for easy parsing.
IMPORTANT: Your response should always be in English, even if the job description is in another language.

Job Description:
"""

prompts_dict = {
    "educationPrompt": prompt_template.format(
        feature_key="Education",
        feature_description="Specify the type of education required for the job. Your answer should be one or more of the following items: BSc, BA, MSc, MBA, PhD, Diploma, Certificate. If the job description uses phrases like 'Bachelor's degree', 'Bachelor in', 'Master in', etc., translate them to BSc, MSc, etc. If the job description does not specify the required education but does mention a domain, default to 'Other'. Ensure the response is concise and directly lists the relevant education types without additional commentary.",
        example_output="BSc, MSc"
    ),
    "fieldPrompt": prompt_template.format(
        feature_key="Field of Expertise",
        feature_description="List the required fields of expertise or domains relevant to the job. If the job description does not specify the required fields of expertise, default to 'Other'. Ensure the response is concise and directly lists the relevant fields without additional commentary.",
        example_output="Data Science, Machine Learning"
    ),
    "experiencePrompt": prompt_template.format(
        feature_key="Minimum Experience",
        feature_description="Specify the required years of experience for the job in the format '{x years}'. If the job description states a range of experience (e.g., 'between x-y years'), use the minimum value in the range. If no specific years of experience are mentioned, please state '0 years'. Ensure the response is concise and directly lists the relevant experience without additional commentary.",
        example_output="3 years"
    ),
    # "softSkillsPrompt": prompt_template.format(
    #     feature_key="Soft Skills",
    #     feature_description="Specify the required personality traits and soft skills for the job. If the job description does not mention any specific traits, please state 'None'. Ensure the response is concise and directly lists the relevant traits without additional commentary.",
    #     example_output="Communication, Teamwork"
    # ),
    "technicalSkillsPrompt": prompt_template.format(
        feature_key="Technical Skills",
        feature_description="Specify the required programming languages, tools, platforms, and other technical skills relevant to the job. If no specific technical skills are mentioned in the job description, please state 'None'. Ensure the response is concise and directly lists the relevant skills without additional commentary.",
        example_output="Python, TensorFlow, Keras"
    ),
    "industryPrompt": prompt_template.format(
        feature_key="Industry",
        feature_description="Specify the principal industry or sector in which the company operates. Your answer should be one or more of the following items: technology, finance, healthcare, education, manufacturing, retail, energy, construction, real estate, transportation, logistics, media, entertainment, government, public sector, hospitality, tourism, agriculture, legal, professional services, travel, other. If the job description does not specify an industry or sector, please state 'other'. Ensure the response is concise and directly lists the relevant industry or sector without additional commentary.",
        example_output="Technology, Finance"
    ),
    "scopePositionPrompt": prompt_template.format(
        feature_key="Scope of Position",
        feature_description="Specify the most suitable scope of position from the following: full-time, part-time, contract, temporary, freelance, internship, casual. If the job description does not specify a scope of position, please state 'full-time'. Ensure the response is concise and directly lists the relevant scope of position without additional commentary.",
        example_output="Full-time, Part-time"
    ),
    "jobTypePrompt": prompt_template.format(
        feature_key="Job Type",
        feature_description="Specify the most suitable job type from the following: in-office, hybrid, remote. If the job description does not specify a job type, please state 'in-office'. Ensure the response is concise and directly lists the relevant job type without additional commentary.",
        example_output="Remote, Hybrid"
    )
}

def retry_with_exponential_backoff(func, max_attempts=10, initial_delay=16, backoff_factor=2):
    delay = initial_delay
    for attempt in range(max_attempts):
        try:
            return func()
        except google.api_core.exceptions.ResourceExhausted as e:
            if attempt == max_attempts - 1:
                raise
            print(f"Resource exhausted, retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= backoff_factor


# def edit_data(job_data, prompts_dict):
#     # iterate over each job description and send it with the prompt to the model for creating new features
#     for idx, job in enumerate(job_data):
#         print(f"Processing job {idx + 1} / {len(job_data)}...")
#         job_dict = {}
#         for key, prompt in prompts_dict.items():
#             while True:
#                 def generate_content():
#                     return model.generate_content(prompt + job['description'])
#
#                 response = retry_with_exponential_backoff(generate_content)
#                 output_str = response.text
#
#                 # Use regular expressions to remove the markdown code block syntax in a case-insensitive manner
#                 clean_output = re.sub(r'^```json\n', '', output_str, flags=re.IGNORECASE)
#                 clean_output = re.sub(r'```$', '', clean_output, flags=re.IGNORECASE).strip()
#
#                 print(f"Clean Output: {clean_output}")
#
#                 # # Assuming the model's response is directly in JSON format in the response.text
#                 output_dict = json.loads(clean_output)
#                 if not output_dict:
#                     break
#
#                 feature = list(output_dict.keys())[0]
#                 value = output_dict[feature]
#
#                 if type(value) != str:
#                     continue
#
#                 if key == "educationPrompt":
#                     return_value = isValidEducation(value)
#                     if return_value:
#                         output_dict[feature] = return_value
#                         break
#
#                 elif key == "fieldPrompt":
#                     break
#
#                 elif key == "experiencePrompt" and isValidExperience(value):
#                     break
#
#                 # elif key == "softSkillsPrompt":
#                 #     break
#
#                 elif key == "technicalSkillsPrompt":
#                     break
#
#                 elif key == "industryPrompt":
#                     return_value = isValidIndustry(value)
#                     if return_value:
#                         output_dict[feature] = return_value
#                         break
#
#                 elif key == "scopePositionPrompt":
#                     return_value = isValidScopePosition(value)
#                     if return_value:
#                         output_dict[feature] = return_value
#                         break
#
#                 elif key == "jobTypePrompt":
#                     return_value = isValidJobType(value)
#                     if return_value:
#                         output_dict[feature] = return_value
#                         break
#
#             job_dict.update(output_dict)
#
#         # Update the job dictionary with the new keys and values
#         job.update(job_dict)
#
#     return job_data

# def edit_data(job_data, prompts_dict):
#     for idx, job in enumerate(job_data):
#         print(f"Processing job {idx + 1} / {len(job_data)}...")
#         job_dict = {}
#         for key, prompt in prompts_dict.items():
#             while True:
#                 def generate_content():
#                     return model.generate_content(prompt + job['description'])
#
#                 response = retry_with_exponential_backoff(generate_content)
#                 output_str = response.text
#
#                 # Use regular expressions to remove the markdown code block syntax in a case-insensitive manner
#                 clean_output = re.sub(r'^```json\n', '', output_str, flags=re.IGNORECASE)
#                 clean_output = re.sub(r'```$', '', clean_output, flags=re.IGNORECASE).strip()
#
#                 print(f"Clean Output: {clean_output}")
#
#                 try:
#                     # Assuming the model's response is directly in JSON format in the response.text
#                     output_dict = json.loads(clean_output)
#                 except json.JSONDecodeError as e:
#                     print(f"Error decoding JSON: {e}")
#                     continue
#
#                 if not output_dict:
#                     break
#
#                 feature = list(output_dict.keys())[0]
#                 value = output_dict[feature]
#
#                 if type(value) != str:
#                     continue
#
#                 # Validate and decide to break the loop based on the feature key
#                 # if key == "educationPrompt":
#                 #     return_value = isValidEducation(value)
#                 #     if return_value:
#                 #         output_dict[feature] = return_value
#                 #         break
#
#                 if key == "educationPrompt":
#                     return_value = isValidEducation(value)
#                     output_dict[feature] = return_value
#                     break
#
#                 elif key == "fieldPrompt":
#                     break
#
#                 elif key == "experiencePrompt" and isValidExperience(value):
#                     break
#
#                 elif key == "technicalSkillsPrompt":
#                     break
#
#                 elif key == "industryPrompt":
#                     return_value = isValidIndustry(value)
#                     output_dict[feature] = return_value
#                     break
#
#                 elif key == "scopePositionPrompt":
#                     return_value = isValidScopePosition(value)
#                     output_dict[feature] = return_value
#                     break
#
#                 elif key == "jobTypePrompt":
#                     return_value = isValidJobType(value)
#                     output_dict[feature] = return_value
#                     break
#
#             job_dict.update(output_dict)
#
#         # Update the job dictionary with the new keys and values
#         job.update(job_dict)
#
#     return job_data

def edit_data(job_data, prompts_dict):
    for idx, job in enumerate(job_data):
        print(f"Processing job {idx + 1} / {len(job_data)}...")
        job_dict = {}
        skip_job = False  # Flag to skip the rest of the prompts for the current job

        for key, prompt in prompts_dict.items():
            while True:
                def generate_content():
                    return model.generate_content(prompt + job['description'])

                try:
                    response = retry_with_exponential_backoff(generate_content)
                    output_str = response.text
                except ValueError as e:
                    print(f"Error for job {idx + 1} with prompt {key}: {e}")
                    print("Skipping this job and continuing with the next one...")
                    skip_job = True  # Set the flag to skip the rest of the prompts
                    break  # Break the while loop

                # Use regular expressions to remove the markdown code block syntax in a case-insensitive manner
                clean_output = re.sub(r'^```json\n', '', output_str, flags=re.IGNORECASE)
                clean_output = re.sub(r'```$', '', clean_output, flags=re.IGNORECASE).strip()

                print(f"Clean Output: {clean_output}")

                try:
                    # Assuming the model's response is directly in JSON format in the response.text
                    output_dict = json.loads(clean_output)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    continue

                if not output_dict:
                    break

                feature = list(output_dict.keys())[0]
                value = output_dict[feature]

                if type(value) != str:
                    continue

                # Validate and decide to break the loop based on the feature key
                if key == "educationPrompt":
                    return_value = isValidEducation(value)
                    output_dict[feature] = return_value
                    break

                elif key == "fieldPrompt":
                    break

                elif key == "experiencePrompt" and isValidExperience(value):
                    break

                elif key == "technicalSkillsPrompt":
                    break

                elif key == "industryPrompt":
                    return_value = isValidIndustry(value)
                    output_dict[feature] = return_value
                    break

                elif key == "scopePositionPrompt":
                    return_value = isValidScopePosition(value)
                    output_dict[feature] = return_value
                    break

                elif key == "jobTypePrompt":
                    return_value = isValidJobType(value)
                    output_dict[feature] = return_value
                    break

            if skip_job:
                break  # Break the for loop if an error occurred

            job_dict.update(output_dict)

        if skip_job:
            continue  # Skip to the next job if an error occurred

        # Update the job dictionary with the new keys and values
        job.update(job_dict)

    return job_data


def isValidEducation(value):
    normalization_dict = {
        "B.A.": "BA",
        "B.A": "BA",
        "BA.": "BA",
        "B.Sc.": "BSc",
        "B.Sc": "BSc",
        "BSc.": "BSc",
        "M.Sc.": "MSc",
        "M.Sc": "MSc",
        "MSc.": "MSc",
        "M.B.A.": "MBA",
        "M.B.A": "MBA",
        "MBA.": "MBA"
    }

    # List of valid education types
    valid_education_types = ["BSc", "BA", "MSc", "MBA", "PhD", "Diploma", "Certificate", "High School", "High school diploma", "Other"]

    # Normalize the input by replacing variations with standard forms
    for key, standard in normalization_dict.items():
        value = value.replace(key, standard)

    # Handle cases with multiple values separated by '/'
    value = value.replace('/', ', ')

    # Split the value by commas and strip any leading/trailing whitespace from each item
    education_fields = [item.strip() for item in value.split(",")]

    # Check if all items in the split list are valid education types
    for field in education_fields:
        if field not in valid_education_types:
            return 'Other'

    # Join the normalized fields back into a comma-separated string
    return ", ".join(education_fields)



def isValidExperience(value):
    # Define the regular expression pattern
    pattern = r'^(1 year|\d+ years)$'

    # Use re.match to check if the answer matches the pattern
    if re.match(pattern, value):
        return True
    return False


def isValidIndustry(value):
    valid_industry_types = [
        "technology",
        "finance",
        "healthcare",
        "education",
        "manufacturing",
        "retail",
        "energy",
        "construction",
        "real estate",
        "transportation",
        "logistics",
        "media",
        "entertainment",
        "government",
        "public sector",
        "hospitality",
        "tourism",
        "agriculture",
        "legal",
        "professional services",
        "travel",
        "other",
        'food service'
    ]

    value = value.lower()

    # Handle cases with multiple values separated by '/'
    value = value.replace('/', ', ')

    # Split the value by commas and strip any leading/trailing whitespace from each item
    industry_fields = [item.strip() for item in value.split(",")]

    # Check if all items in the split list are valid education types
    for field in industry_fields:
        if field not in valid_industry_types:
            return 'Other'

    # Join the normalized fields back into a comma-separated string
    industry_fields = ", ".join(industry_fields)
    return industry_fields.title()


def isValidScopePosition(value):
    value = value.lower()
    if value in ["full-time", "part-time", "contract", "temporary", "freelance", "internship", "casual"]:
        return value.title()
    return 'Full-Time'


def isValidJobType(value):
    value = value.lower()
    if value in ["in-office", "hybrid", "remote"]:
        return value.title()
    return 'In-Office'



if __name__ == '__main__':
    skills_indeed = ["Software Engineer", "Data Scientist", "Data Engineer", "Data Analyst", "Business Intelligence (BI) Developer"]
    skills_linkedin = ["DevOps Engineer", "Cloud Engineer", "AI/ML Engineer", "Cybersecurity Engineer", "Product Manager"]

    num_jobs_per_skill = 10
    sort = 'date'

    # # Create the 'jobs' folder if it doesn't exist
    # os.makedirs('jobs', exist_ok=True)
    #
    # # Initialize empty lists to store job data
    # indeed_jobs = []
    # linkedin_jobs = []
    #
    # # Scrape jobs from Indeed for the first five skills
    # for skill in skills_indeed:  # First five skills
    #     scrapped_indeed_jobs_dict = get_indeed_jobs(skill, num_jobs_per_skill, sort)
    #     # Edit the scraped data and add new features
    #     indeed_jobs.extend(scrapped_indeed_jobs_dict)
    #
    # # Scrape jobs from LinkedIn for the last five skills
    # for skill in skills_linkedin:  # Last five skills
    #     scrapped_linkedin_jobs_dict = get_linkedin_jobs(skill, num_jobs_per_skill, sort)
    #     # Edit the scraped data and add new features
    #     linkedin_jobs.extend(scrapped_linkedin_jobs_dict)
    #
    # # indeed_jobs.extend(edit_data(indeed_jobs, prompts_dict))
    # # linkedin_jobs.extend(edit_data(linkedin_jobs, prompts_dict))
    #
    # # Convert the updated job data to DataFrames
    # df_indeed_update = pd.DataFrame(indeed_jobs)
    # df_linkedin_update = pd.DataFrame(linkedin_jobs)
    #
    # # Save the updated DataFrames to CSV files in the 'jobs' folder
    # df_indeed_update.to_csv('jobs/Jobs_Indeed_1.csv', index=False)
    # df_linkedin_update.to_csv('jobs/Jobs_LinkedIn_1.csv', index=False)

    # Read the CSV files back into dictionaries
    # scrapped_indeed_jobs_dict = pd.read_csv('jobs/Jobs_Indeed_1.csv').to_dict('records')
    # scrapped_linkedin_jobs_dict = pd.read_csv('jobs/Jobs_LinkedIn_1.csv').to_dict('records')

    # Edit the scrapped jobs data and add the new features
    # indeed_jobs = edit_data(scrapped_indeed_jobs_dict, prompts_dict)
    # df_indeed_update = pd.DataFrame(indeed_jobs)
    # df_indeed_update.to_csv('jobs/Jobs_Indeed_update_1.csv', index=False)
    # Store the jobs into the database MongoDB
    # for job in indeed_jobs:
    #     Job.create_job(job)

    # linkedin_jobs = edit_data(scrapped_linkedin_jobs_dict, prompts_dict)
    # df_linkedin_update = pd.DataFrame(linkedin_jobs)
    # df_linkedin_update.to_csv('jobs/Jobs_LinkedIn_update_1.csv', index=False)

    # read Jobs_LinkedIn_update_1.csv
    # df = pd.read_csv('jobs/Jobs_LinkedIn_update_1.csv')
    # linkedin_jobs = df.to_dict('records')
    # for job in linkedin_jobs:
    #     Job.create_job(job)

    # Job.clean_and_delete_jobs()
    # print("Jobs scraped successfully!")

    # delete old jobs
    Job.delete_old_jobs()


