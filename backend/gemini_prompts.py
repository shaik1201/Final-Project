from copy import deepcopy
import pandas as pd
import google.generativeai as genai
import json
import re
import time
import google.api_core.exceptions
import config
from jobs_scrapper import get_linkedin_jobs, get_indeed_jobs
from models import Job
from translator import translateLocation


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
    "softSkillsPrompt": prompt_template.format(
        feature_key="Soft Skills",
        feature_description="Specify the required personality traits and soft skills for the job. If the job description does not mention any specific traits, please state 'None'. Ensure the response is concise and directly lists the relevant traits without additional commentary.",
        example_output="Communication, Teamwork"
    ),
    "technicalSkillsPrompt": prompt_template.format(
        feature_key="Technical Skills",
        feature_description="Specify the required programming languages, tools, platforms, and other technical skills relevant to the job. If no specific technical skills are mentioned in the job description, please state 'None'. Ensure the response is concise and directly lists the relevant skills without additional commentary.",
        example_output="Python, TensorFlow, Keras"
    ),
    "industryPrompt": prompt_template.format(
        feature_key="Industry",
        feature_description="Specify the principal industry or sector in which the company operates. Your answer should be one or more of the following items: technology, finance, healthcare, education, manufacturing, retail, energy, construction and real estate, transportation and logistics, media and entertainment, government and public sector, hospitality and tourism, agriculture, legal, professional services, other. If the job description does not specify an industry or sector, please state 'other'. Ensure the response is concise and directly lists the relevant industry or sector without additional commentary.",
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

def retry_with_exponential_backoff(func, max_attempts=10, initial_delay=8, backoff_factor=2):
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


def edit_data(job_data, prompts_dict, prompt_template):
    # iterate over each job description and send it with the prompt to the model for creating new features
    for idx, job in enumerate(job_data):
        print(f"Processing job {idx + 1} / {len(job_data)}...")
        job_dict = {}
        for key, prompt in prompts_dict.items():
            while True:
                def generate_content():
                    return model.generate_content(prompt + job['description'])

                response = retry_with_exponential_backoff(generate_content)
                output_str = response.text

                # Use regular expressions to remove the markdown code block syntax in a case-insensitive manner
                clean_output = re.sub(r'^```json\n', '', output_str, flags=re.IGNORECASE)
                clean_output = re.sub(r'```$', '', clean_output, flags=re.IGNORECASE).strip()

                print(f"Clean Output: {clean_output}")

                # Assuming the model's response is directly in JSON format in the response.text
                try:
                    output_dict = json.loads(clean_output)
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
                    print(f"Failed to decode JSON: {clean_output}")
                    break

                # # Assuming the model's response is directly in JSON format in the response.text
                # output_dict = json.loads(clean_output)
                if not output_dict:
                    break
                feature = list(output_dict.keys())[0]
                value = output_dict[feature]

                if type(value) != str:
                    continue

                if key == "educationPrompt":
                    return_value = isValidEducation(value)
                    if return_value:
                        output_dict[feature] = return_value
                        break

                elif key == "fieldPrompt":
                    break

                elif key == "experiencePrompt" and isValidExperience(value):
                    break

                elif key == "softSkillsPrompt":
                    break

                elif key == "technicalSkillsPrompt":
                    break

                elif key == "industryPrompt":
                    return_value = isValidIndustry(value)
                    if return_value:
                        output_dict[feature] = return_value
                        break

                elif key == "scopePositionPrompt" and isValidScopePosition(value):
                    break

                elif key == "jobTypePrompt" and isValidJobType(value):
                    break

            job_dict.update(output_dict)

        # Update the job dictionary with the new keys and values
        job.update(job_dict)

    return job_data


def output_start_swith_json(input_str):
    return input_str.startswith("```json") or input_str.startswith("```JSON")


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
    valid_education_types = ["BSc", "BA", "MSc", "MBA", "PhD", "Diploma", "Certificate", "Other"]

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
            return False

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
        "construction and real estate",
        "transportation and logistics",
        "media and entertainment",
        "government and public sector",
        "hospitality and tourism",
        "agriculture",
        "legal",
        "professional services",
        "other"
    ]

    value = value.lower()

    # Handle cases with multiple values separated by '/'
    value = value.replace('/', ', ')

    # Split the value by commas and strip any leading/trailing whitespace from each item
    industry_fields = [item.strip() for item in value.split(",")]

    # Check if all items in the split list are valid education types
    for field in industry_fields:
        if field not in valid_industry_types:
            return False

    # Join the normalized fields back into a comma-separated string
    return ", ".join(industry_fields)


def isValidScopePosition(value):
    value = value.lower()
    if value in ["full-time", "part-time", "contract", "temporary", "freelance", "internship", "casual"]:
        return True
    return False


def isValidJobType(value):
    value = value.lower()
    if value in ["in-office", "hybrid", "remote"]:
        return True
    return False



if __name__ == '__main__':
    skill = 'Data Analyst'.strip()
    num_jobs = 15
    sort = 'date'
    # Scrape the jobs from Indeed
    scrapped_jobs_dict = get_indeed_jobs(skill, num_jobs, sort)

    # Edit the scrapped jobs data and add the new features
    indeed_jobs = edit_data(scrapped_jobs_dict, prompts_dict, prompt_template)
    indeed_jobs_english_locations = translateLocation(indeed_jobs)

    df_indeed = pd.DataFrame(indeed_jobs)
    # df_linkedin = pd.DataFrame(jobs_linkedin)

    df_indeed.to_csv('Jobs_Indeed.csv', index=False)
    # df_linkedin.to_csv('Jobs_LinkedIn.csv', index=False)

    # # Store the jobs into the database MongoDB
    # for job in indeed_jobs_english_locations:
    #     Job.create_job(job)
    # print("Jobs scraped successfully!")

