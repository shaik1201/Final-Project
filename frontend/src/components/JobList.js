import React, { useEffect, useState } from 'react';
import './JobList.css';
import JobCard from './JobCard';
import JobSearch from './JobSearch';
import UploadCV from './UploadCV';
import Features from './Features';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [cvFile, setCvFile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [message, setMessage] = useState(''); // State for managing messages
  const jobsPerPage = 9;

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = () => {
    setIsLoading(true);
    fetch(`${process.env.REACT_APP_BACKEND_URL}/jobs`)
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          setJobs(data);
        } else {
          console.error('Fetched data is not an array:', data);
        }
        setIsLoading(false);
      })
      .catch(error => {
        console.error('Error fetching jobs:', error);
        setIsLoading(false);
      });
  };

  const handleSearch = (searchParams) => {
    setIsLoading(true);
    setCurrentPage(1); // Reset to the first page on search
    fetch(`${process.env.REACT_APP_BACKEND_URL}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(searchParams),
    })
    .then(response => response.json())
    .then(data => {
      if (Array.isArray(data)) {
        setJobs(data);
      } else {
        console.error('Search results are not an array:', data);
      }
      setIsLoading(false);
    })
    .catch(error => {
      console.error('Error searching jobs:', error);
      setIsLoading(false);
    });
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
      setIsLoading(true);
      const formData = new FormData();
      formData.append('cv', cvFile);

      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/upload_cv`, {
          method: 'POST',
          body: formData,
        });

        const result = await response.json();

        if (response.status === 400) {
          setMessage(result.error);
        } else if (response.status === 401){
          setMessage(result.error);
        } else if (response.status === 402){
          setMessage(result.error);
        } else if (response.status === 500) {
          setMessage('An internal server error occurred while uploading your CV.');
        } else if (response.ok) {
          if (Array.isArray(result)) {
            setJobs(result);
            setMessage('CV uploaded successfully. Relevant jobs found!');
          } else {
            console.error('Uploaded CV response is not an array:', result);
          }
        }
      } catch (error) {
        console.error('Error uploading CV:', error);
        setMessage('An error occurred while uploading your CV. Please try again.');
      } finally {
        setIsLoading(false);
      }
    } else {
      setMessage('Please select a file to upload.');
    }
  };

  const indexOfLastJob = currentPage * jobsPerPage;
  const indexOfFirstJob = indexOfLastJob - jobsPerPage;
  const currentJobs = jobs.slice(indexOfFirstJob, indexOfLastJob);

  return (
    <div className="job-list">
      <Features />

      <div className="container">
        <h1 className="main-title">Discover Your Next Career Move</h1>
        <div className="search-upload-wrapper">
          <UploadCV onUpload={uploadCV} onFileChange={handleFileChange} message={message} />
          <div className="divider">
            <span>or</span>
          </div>
          <JobSearch onSearch={handleSearch} />
        </div>
        {isLoading ? (
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Finding perfect matches...</p>
          </div>
        ) : (
          <>
            <div className="job-cards-container">
              {currentJobs.map((job, index) => (
                <JobCard key={index} job={job} />
              ))}
            </div>
            <div className="pagination-container">
              <button
                className="button-navigation prev"
                onClick={handlePrevPage}
                disabled={currentPage === 1}
              >
                &larr; Previous
              </button>
              <span className="pagination-info">
                Page {currentPage} of {Math.ceil(jobs.length / jobsPerPage)}
              </span>
              <button
                className="button-navigation next"
                onClick={handleNextPage}
                disabled={currentPage === Math.ceil(jobs.length / jobsPerPage)}
              >
                Next &rarr;
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default JobList;
