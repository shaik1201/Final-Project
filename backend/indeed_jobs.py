import os
import csv
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_indeed_jobs():
    # Skills and Place of Work
    skill = 'Data Scientist'.strip()
    place = 'Israel'.strip()
    no_of_pages = 1

    # Creating the Main Directory
    main_dir = os.getcwd() + '\\'
    if not os.path.exists(main_dir):
        os.mkdir(main_dir)
        print('Base Directory Created Successfully.')

    # Name of the CSV File
    file_name = skill.title() + '_' + place.title() + '_Jobs.csv'
    # Path of the CSV File
    file_path = os.path.join(main_dir, file_name)

    # Initialize Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    print(f'\nScraping in progress...\n')
    job_data = []

    for page in range(no_of_pages):
        url = f'https://il.indeed.com/jobs?q={skill}&l={place}&start={page * 10}'
        driver.get(url)
        time.sleep(5)  # Wait for dynamic content to load

        # Use Selenium to find job cards
        job_listings = driver.find_elements(By.CSS_SELECTOR, 'div#mosaic-provider-jobcards ul > li')

        for job_listing in job_listings:
            try:
                # Extract the job title
                job_title_element = job_listing.find_element(By.CLASS_NAME, "jobTitle")
                job_title = job_title_element.text.strip() if job_title_element else "N/A"

                # Extract the company name
                company_element = job_listing.find_element(By.CSS_SELECTOR, 'span[data-testid="company-name"]')
                company = company_element.text.strip() if company_element else "N/A"

                # Extract the location
                location_element = job_listing.find_element(By.CSS_SELECTOR, 'div[data-testid="text-location"]')
                location = location_element.text.strip() if location_element else "N/A"

                # Extract the posted date
                posted_element = job_listing.find_element(By.CSS_SELECTOR, 'span[data-testid="myJobsStateDate"]')
                posted = posted_element.text.strip() if posted_element else "N/A"

                # Extract the job ID and construct the job link
                job_id = job_listing.find_element(By.CSS_SELECTOR, "a").get_attribute("id")
                job_id = job_id.replace('job_', '')
                job_link = f"https://il.indeed.com/viewjob?jk={job_id}" if job_id != "N/A" else "N/A"

                # Click the job element to get the description
                job_listing.click()

                # Help to load page so we can find and extract data
                time.sleep(random.randint(3, 5))

                try:
                    job_description = driver.find_element(By.ID, "jobDescriptionText").text
                except:
                    job_description = None

                job_data.append({
                    "title": job_title,
                    "job_id": job_id,
                    "company": company,
                    "location": location,
                    "date": posted,
                    "link": job_link,
                    "description": job_description
                })

            except Exception as e:
                print(f'Error processing job: {e}')
                
            # break

    # Close the browser
    driver.quit()
    return job_data

if __name__ == "__main__":
    jobs = get_indeed_jobs()
    print(jobs)
