import random
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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

            except Exception as e:
                print(f'Error processing job: {e}')

        page += 1

    # Close the browser
    driver.quit()
    return job_data


def get_linkedin_jobs(skill, num_jobs):
    # Skills and Place of Work
    place = 'Israel'.strip()
    total_jobs_scraped = 0

    # Initialize Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    print('\nScraping in progress...\n')
    job_data = []

    # URL for LinkedIn's job search with appropriate encoding for spaces
    url = f'https://www.linkedin.com/jobs/search?keywords={skill.replace(" ", "%20")}&location={place.replace(" ", "%20")}'
    driver.get(url)
    time.sleep(5)  # Wait for initial content to load

    while total_jobs_scraped < num_jobs:
        # Adjusted selectors for LinkedIn
        job_listings = driver.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list > li')

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

                try:
                    job_description = driver.find_element(By.CSS_SELECTOR, 'div.show-more-less-html__markup').text
                except:
                    job_description = "N/A"

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

            except Exception as e:
                print(f'Error processing job: {e}')

        # Scroll down to load more jobs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Wait for additional content to load

    # Close the browser
    driver.quit()
    return job_data



if __name__ == "__main__":
    skill = 'Data Analyst'.strip()
    num_jobs = 20

    jobs_indeed = get_indeed_jobs(skill, num_jobs)
    # jobs_linkedin = get_linkedin_jobs(skill, num_jobs)

    print(f'\nScraping completed successfully!\n')

    df_indeed = pd.DataFrame(jobs_indeed)
    # df_linkedin = pd.DataFrame(jobs_linkedin)

    df_indeed.to_csv('Jobs_Indeed.csv', index=False)
    # df_linkedin.to_csv('Jobs_LinkedIn.csv', index=False)

