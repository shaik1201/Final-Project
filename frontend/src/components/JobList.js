import React, { useEffect, useState } from 'react';
import './JobList.css';
import JobCard from './JobCard';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [user_job_title, set_user_job_title] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const jobsPerPage = 10;

  const indexOfLastJob = currentPage * jobsPerPage;
  const indexOfFirstJob = indexOfLastJob - jobsPerPage;
  const currentJobs = jobs.slice(indexOfFirstJob, indexOfLastJob);

  const handleNextPage = () => {
    setCurrentPage((prevPage) => prevPage + 1);
  };
  
  const handlePreviousPage = () => {
    setCurrentPage((prevPage) => (prevPage > 1 ? prevPage - 1 : 1));
  };

//   useEffect(() => {
//     fetch(`${process.env.REACT_APP_BACKEND_URL}/jobs`)
//       .then(response => response.json())
//       .then(data => setJobs(data))
//       .catch(error => console.error('Error fetching jobs:', error));
//   }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    const user_job_title_json = { user_job_title };

    fetch(`${process.env.REACT_APP_BACKEND_URL}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user_job_title_json),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        setJobs(data);
    })
    .catch(error => console.error('Error adding job:', error));
  };

  const handleScrape = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/jobs/scrape`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error(`Error scraping jobs: ${response.statusText}`);
      }
      const scrapedJobs = await response.json();
      setJobs([...jobs, ...scrapedJobs]);
    } catch (error) {
      console.error('Error scraping jobs:', error);
    }
  };

  return (
    <div className="container">
      <h1>LLM For Job Searching</h1>
      <div className="button-container">
        <button className="button" onClick={handleScrape}>Scrape Jobs</button>
      </div>
      <form>
        <div className="job-form-container">
          <input
            type="text"
            placeholder="Title"
            value={user_job_title}
            onChange={(e) => set_user_job_title(e.target.value)}
            className="job-input"
          />
          <button className="button" type="submit" onClick={handleSubmit}>Search</button>
        </div>
      </form>
      <div className="job-cards-container">
        {currentJobs.map((job, index) => (
          <JobCard key={index} job={job} />
        ))}
      </div>
      <div className="pagination-container">
        {currentPage > 1 && (
          <button className="button" onClick={handlePreviousPage}>Previous</button>
        )}
        {indexOfLastJob < jobs.length && (
          <button className="button" onClick={handleNextPage}>Next</button>
        )}
      </div>
    </div>
  );
};

export default JobList;
