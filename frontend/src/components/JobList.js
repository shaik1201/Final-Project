import React, { useEffect, useState } from 'react';
import './JobList.css';
import JobCard from './JobCard';
import Navbar from './Navbar';
import JobSearch from './JobSearch';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [cvFile, setCvFile] = useState(null);
  const jobsPerPage = 9;

  useEffect(() => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/jobs`)
      .then(response => response.json())
      .then(data => setJobs(data))
      .catch(error => console.error('Error fetching jobs:', error));
  }, []);

  const handleSearch = (searchParams) => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(searchParams),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        setJobs(data);
    })
    .catch(error => console.error('Error searching jobs:', error));
  };

  const handleNextPage = () => {
    if (currentPage < Math.ceil(jobs.length / jobsPerPage)) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleFileChange = (e) => {
    setCvFile(e.target.files[0]);
  };

  const uploadCV = async () => {
    if (cvFile) {
      const formData = new FormData();
      formData.append('cv', cvFile);

      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/upload_cv`, {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`Error uploading CV: ${response.statusText}`);
        }

        const result = await response.json();
        console.log('CV uploaded successfully:', result);
      } catch (error) {
        console.error('Error uploading CV:', error);
      }
    } else {
      alert('Please select a file to upload.');
    }
  };

  const indexOfLastJob = currentPage * jobsPerPage;
  const indexOfFirstJob = indexOfLastJob - jobsPerPage;
  const currentJobs = jobs.slice(indexOfFirstJob, indexOfLastJob);

  return (
    <div>
      <div className="container">
        <h1>LLM For Job Searching</h1>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button onClick={uploadCV}>Upload CV</button>

        <JobSearch onSearch={handleSearch} />
        <div className="job-cards-container">
          {currentJobs.map((job, index) => (
            <JobCard key={index} job={job} />
          ))}
        </div>
        <div className="pagination-container">
          <button 
            className="button-navigation" 
            onClick={handlePrevPage} 
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span>Page {currentPage} of {Math.ceil(jobs.length / jobsPerPage)}</span>
          <button 
            className="button-navigation" 
            onClick={handleNextPage} 
            disabled={currentPage === Math.ceil(jobs.length / jobsPerPage)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default JobList;
