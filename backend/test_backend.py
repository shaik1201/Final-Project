import requests
# Replace with your server URL
url = "http://127.0.0.1:5000/search"
# Job title to search for
job_title = "Data Scientist"
# Prepare the JSON data
data = {"user_job_title": job_title}
# Send the POST request with JSON data
response = requests.post(url, json=data)
# Check for successful response
if response.status_code == 200:
  # Get the response data (list of relevant jobs)
  relevant_jobs = response.json()
  print(relevant_jobs)
else:
  print("Error: Failed to search for jobs")