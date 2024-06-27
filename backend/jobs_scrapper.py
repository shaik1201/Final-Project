import random
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from deep_translator import GoogleTranslator
from langdetect import detect

import re
from datetime import datetime, timedelta


def close_popup(driver):
    try:
        # Using the class name from the provided screenshot to locate the close button
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'css-yi9ndv'))
        )
        close_button.click()
    except Exception as e:
        print(f"No pop-up to close or unable to close pop-up: {e}")


def get_indeed_jobs(skill, num_jobs, sort):
    place = 'Israel'.strip()
    total_jobs_scraped = 0

    # Initialize Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    print(f'\nScraping in progress...\n')
    job_data = []

    page = 0
    while total_jobs_scraped < num_jobs:
        if sort == 'date':
            url = f'https://il.indeed.com/jobs?q={skill}&l={place}&sort=date&start={page}'
        else:
            url = f'https://il.indeed.com/jobs?q={skill}&l={place}&start={page}'
        driver.get(url)
        time.sleep(5)  # Wait for dynamic content to load

        # Close any pop-ups if they appear
        close_popup(driver)

        # Use Selenium to find job cards
        job_listings = driver.find_elements(By.CSS_SELECTOR, 'div#mosaic-provider-jobcards ul > li')
        add_the_job = True
        for job_listing in job_listings:
            if total_jobs_scraped >= num_jobs:
                break
            try:
                time.sleep(1)  # Wait for dynamic content to load

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
                posted = convert_relative_date(posted)

                # Extract the job ID and construct the job link
                job_link_element = job_listing.find_element(By.CSS_SELECTOR, "a")
                job_id = job_link_element.get_attribute("id").replace('job_', '') if job_link_element else "N/A"
                job_link = f"https://il.indeed.com/viewjob?jk={job_id}" if job_id != "N/A" else "N/A"

                # Click the job element to get the description
                job_listing.click()

                # Help to load page so we can find and extract data
                time.sleep(random.randint(3, 5))

                # Extract the job description
                job_description = driver.find_element(By.ID, "jobDescriptionText").text if driver.find_element(By.ID, "jobDescriptionText") else "N/A"

                # Translate the features to English
                # job_title_language = detect(job_title)
                # if job_title_language not in ['en']:
                #     job_title = GoogleTranslator(source='iw', target='en').translate(job_title)


                location, add_the_job = process_location(location, add_the_job)

                # location_language = detect(location)
                # if location_language in ['iw', 'he']:
                #     location = GoogleTranslator(source='iw', target='en').translate(location)
                #
                # # Split the location string and filter out 'Israel', then join the parts back into a single string
                # location = ', '.join(part.strip() for part in location.split(',') if 'israel' not in part.lower())
                # location = location.split(',')
                #
                # # Fix the location for when only Tel Aviv District is provided
                # if len(location) == 1 and location[0].lower() == 'tel aviv district':
                #     location = ['Tel Aviv-Yafo', 'Tel Aviv District']
                #
                # # Fix the location for when only Tel Aviv District is provided
                # if len(location) == 1 and location[0].lower() == 'central district':
                #     add_the_job = False
                #
                # for i, part in enumerate(location):
                #     if part.lower() == 'central district':
                #         location[i] = 'Center District'
                #
                # for i, part in enumerate(location):
                #     if part.lower() == 'Tel Aviv - Jaffa':
                #         location[i] = 'Tel Aviv-Yafo'
                #
                # location = ', '.join(location)

                # posted_language = detect(posted)
                # if posted_language in ['en']:
                #     posted = GoogleTranslator(source='iw', target='en').translate(posted)

                job_description_language = detect(job_description)
                if job_description_language in ['iw', 'he']:
                    job_description = GoogleTranslator(source='iw', target='en').translate(job_description)

                if add_the_job:
                    job_data.append({
                        "title": job_title,
                        "job_id": job_id,
                        "company": company,
                        "location": location,
                        "date": posted,
                        "link": job_link,
                        "description": job_description
                    })

                    total_jobs_scraped += 1
                    print(f'Job {total_jobs_scraped} scraped successfully!')

                add_the_job = True

            except Exception as e:
                print(f'Error processing job: {e}')

        page += 1

    # Close the browser
    driver.quit()
    return job_data


def get_linkedin_jobs(skill, num_jobs, sort):
    # Skills and Place of Work
    place = 'Israel'.strip()
    total_jobs_scraped = 0

    # Initialize Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    print('\nScraping in progress...\n')
    job_data = []

    # Sort by date (one week ago)
    if sort == 'date':
        url = f'https://www.linkedin.com/jobs/search?f_TPR=r604800&keywords={skill.replace(" ", "%20")}&location={place.replace(" ", "%20")}'
    # Sort by recommended
    else:
        url = f'https://www.linkedin.com/jobs/search?keywords={skill.replace(" ", "%20")}&location={place.replace(" ", "%20")}'
    driver.get(url)
    time.sleep(5)  # Wait for initial content to load

    # Check if redirected to the main page
    if driver.current_url == 'https://www.linkedin.com/':
        jobs_link = driver.find_element(By.XPATH, '//a[contains(@href, "jobs/search")]')
        jobs_link.click()
        time.sleep(5)  # Wait for the jobs page to load

    while total_jobs_scraped < num_jobs:
        # Adjusted selectors for LinkedIn
        job_listings = driver.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list > li')
        add_the_job = True
        for job_listing in job_listings[total_jobs_scraped:]:
            if total_jobs_scraped >= num_jobs:
                break
            try:
                # Extract the job title
                job_title_element = job_listing.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title')
                job_title = job_title_element.text.strip() if job_title_element else "N/A"

                # Extract the company name
                company_element = job_listing.find_element(By.CSS_SELECTOR, 'h4.base-search-card__subtitle')
                company = company_element.text.strip() if company_element else "N/A"

                # Extract the location
                location_element = job_listing.find_element(By.CSS_SELECTOR, 'span.job-search-card__location')
                location = location_element.text.strip() if location_element else "N/A"

                # Extract the posted date
                posted_element = job_listing.find_element(By.CSS_SELECTOR, 'time')
                posted = posted_element.get_attribute('datetime') if posted_element else "N/A"

                # Extract the job ID and construct the job link
                job_link_element = job_listing.find_element(By.CSS_SELECTOR, 'a.base-card__full-link')
                job_link = job_link_element.get_attribute('href') if job_link_element else "N/A"
                title_and_job_id = job_link.split('/')[-1].split('?')[0] if job_link != "N/A" else "N/A"
                job_id = title_and_job_id.split('-')[-1] if title_and_job_id != "N/A" else "N/A"

                # Click the job element to get the description
                job_link_element.click()
                time.sleep(random.randint(3, 5))  # Help to load page so we can find and extract data

                show_more_button = driver.find_element(By.CSS_SELECTOR, 'button.show-more-less-html__button')
                show_more_button.click()

                time.sleep(2)  # Wait for the content to expand
                job_description_element = driver.find_element(By.CSS_SELECTOR, 'div.show-more-less-html__markup')
                job_description = job_description_element.text if job_description_element else "N/A"


                location, add_the_job = process_location(location, add_the_job)

                # posted_language = detect(posted)
                # if posted_language not in ['en']:
                #     posted = GoogleTranslator(source='iw', target='en').translate(posted)

                job_description_language = detect(job_description)
                if job_description_language in ['iw', 'he']:
                    job_description = GoogleTranslator(source='iw', target='en').translate(job_description)

                if add_the_job:
                    job_data.append({
                        "title": job_title,
                        "job_id": job_id,
                        "company": company,
                        "location": location,
                        "date": posted,
                        "link": job_link,
                        "description": job_description
                    })

                    total_jobs_scraped += 1
                    print(f'Job {total_jobs_scraped} scraped successfully!')

                add_the_job = True

            except Exception as e:
                print(f'Error processing job: {e}')

        # Scroll down to load more jobs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Wait for additional content to load

    # Close the browser
    driver.quit()
    return job_data


def process_location(location, add_the_job):
    location_language = detect(location)
    if location_language in ['iw', 'he']:
        location = GoogleTranslator(source='iw', target='en').translate(location)

    # Split the location string and filter out 'Israel', then join the parts back into a single string
    location_parts = [part.strip() for part in location.split(',') if 'israel' not in part.lower()]

    # Fix the location for when only Tel Aviv District or Central District is provided
    if len(location_parts) == 1:
        if location_parts[0].lower() == 'tel aviv district':
            location_parts = ['Tel Aviv-Yafo', 'Tel Aviv District']
        elif location_parts[0].lower() == 'central district':
            add_the_job = False
            return location_parts, add_the_job

    # Normalize location names
    for i, part in enumerate(location_parts):
        if part.lower() == 'central district':
            location_parts[i] = 'Center District'
        elif part.lower() == 'tel aviv - jaffa':
            location_parts[i] = 'Tel Aviv-Yafo'
        elif part.lower() == "ra'anana":
            location_parts[i] = "Raanana"

    location = ', '.join(location_parts)
    location = location.title()

    add_the_job = True
    return location, add_the_job

def convert_relative_date(relative_date):
    today = datetime.now()

    if 'just posted' in relative_date.lower():
        return today.strftime('%Y-%m-%d')

    match = re.search(r'(\d+)', relative_date)
    if match:
        days_ago = int(match.group(1))
        published_date = today - timedelta(days=days_ago)
        return published_date.strftime('%Y-%m-%d')

    return None



if __name__ == "__main__":
    skill = 'Data Analyst'.strip()
    num_jobs = 20
    sort = 'date'

    jobs_indeed = get_indeed_jobs(skill, num_jobs)
    jobs_linkedin = get_linkedin_jobs(skill, num_jobs, sort)

    print(f'\nScraping completed successfully!\n')

    df_indeed = pd.DataFrame(jobs_indeed)
    df_linkedin = pd.DataFrame(jobs_linkedin)

    df_indeed.to_csv('Jobs_Indeed.csv', index=False)
    df_linkedin.to_csv('Jobs_LinkedIn.csv', index=False)

