import React, { useEffect, useState } from 'react';
import './JobList.css';
import JobCard from './JobCard';
import Navbar from './Navbar';
import JobSearch from './JobSearch';
import UploadCV from './UploadCV';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [cvFile, setCvFile] = useState(null);
  const jobsPerPage = 9;

  useEffect(() => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/jobs`)
      .then(response => response.json())
      .then(data => {
        console.log('Fetched jobs:', data); // Log the fetched data
        if (Array.isArray(data)) {
          setJobs(data);
        } else {
          console.error('Fetched data is not an array:', data);
        }
      })
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
        console.log('Search results:', data); // Log the search results
        if (Array.isArray(data)) {
          setJobs(data);
        } else {
          console.error('Search results are not an array:', data);
        }
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
        if (Array.isArray(result)) {
          setJobs(result);
        } else {
          console.error('Uploaded CV response is not an array:', result);
        }
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
        <UploadCV onUpload={uploadCV} onFileChange={handleFileChange}/>
        <div className='break-sent'>
          <h2>Or, search manually</h2>
        </div>

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
