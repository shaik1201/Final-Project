// import React, { useEffect, useState } from 'react';
// import './JobList.css';
//
// const JobList = () => {
//   const [jobs, setJobs] = useState([]);
//   const [user_job_title, set_user_job_title] = useState('');
//
// //   useEffect(() => {
// //     fetch(`${process.env.REACT_APP_BACKEND_URL}/jobs`)
// //       .then(response => response.json())
// //       .then(data => setJobs(data))
// //       .catch(error => console.error('Error fetching jobs:', error));
// //   }, []);
//
//   const handleSubmit = (e) => {
//     e.preventDefault();
//     const user_job_title_json = { user_job_title };
//
//     fetch(`${process.env.REACT_APP_BACKEND_URL}/search`, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(user_job_title_json),
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data);
//         setJobs(data);
//     })
//     .catch(error => console.error('Error adding job:', error));
//   };
//
//   const handleScrape = async () => {
//     try {
//       const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/jobs/scrape`, {
//         method: 'POST',
//       });
//       if (!response.ok) {
//         throw new Error(`Error scraping jobs: ${response.statusText}`);
//       }
//       const scrapedJobs = await response.json();
//       setJobs([...jobs, ...scrapedJobs]);
//     } catch (error) {
//       console.error('Error scraping jobs:', error);
//     }
//   };
//
//   return (
//     <div>
//       <h1>Job List</h1>
//       <button className="button" onClick={handleScrape}>Scrape Jobs</button>
//       <form>
//       <div className="job-form-container">
//         <input
//           type="text"
//           placeholder="Title"
//           value={user_job_title}
//           onChange={(e) => set_user_job_title(e.target.value)}
//           className="job-input"
//         />
//         <button className="button" type="submit" onClick={handleSubmit}>Search</button>
//       </div>
//       </form>
//
//
//       <table className="job-table">
//         <thead>
//         <tr>
//           <th>Title</th>
//           <th>Company</th>
//           <th>Location</th>
//           <th>Date</th>
//           <th>Link</th>
//           <th>Education</th>
//           <th>Field of Expertise</th>
//           <th>Minimum Experience</th>
//           <th>Soft Skills</th>
//           <th>Technical Skills</th>
//           <th>Industry</th>
//           <th>Scope of Position</th>
//           <th>Job Type</th>
//           {/* <th>Description</th> */}
//
//         </tr>
//         </thead>
//         <tbody>
//           {jobs.map((job, index) => (
//             <tr key={index}>
//               <td>{job.title}</td>
//               <td>{job.company}</td>
//               <td>{job.location}</td>
//                 <td>{job.date}</td>
//                 <td>
//                   <a href={job.link} target="_blank" rel="noopener noreferrer">{job.link}</a>
//                 </td>
//                 <td>{job.education}</td>
//                 <td>{job.field_of_expertise}</td>
//                 <td>{job.minimum_experience}</td>
//                 <td>{job.soft_skills}</td>
//                 <td>{job.technical_skills}</td>
//                 <td>{job.industry}</td>
//                 <td>{job.scope_of_position}</td>
//                 <td>{job.job_type}</td>
//                 {/* <td>{job.description}</td> */}
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// };
//
// export default JobList;

  // const handleScrape = async () => {
  //   try {
  //     const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/jobs/scrape`, {
  //       method: 'POST',
  //     });
  //     if (!response.ok) {
  //       throw new Error(`Error scraping jobs: ${response.statusText}`);
  //     }
  //     const scrapedJobs = await response.json();
  //     setJobs([...jobs, ...scrapedJobs]);
  //   } catch (error) {
  //     console.error('Error scraping jobs:', error);
  //   }
  // };


// ---------------------------------------------------

// import React, { useEffect, useState } from 'react';
// import './JobList.css';
// import JobCard from './JobCard';
// import Navbar from './Navbar';
//
// const JobList = () => {
//   const [jobs, setJobs] = useState([]);
//   const [user_job_title, set_user_job_title] = useState('');
//   const [currentPage, setCurrentPage] = useState(1);
//   const jobsPerPage = 10;
//
//   useEffect(() => {
//     fetch(`${process.env.REACT_APP_BACKEND_URL}/jobs`)
//       .then(response => response.json())
//       .then(data => setJobs(data))
//       .catch(error => console.error('Error fetching jobs:', error));
//   }, []);
//
//   const handleSubmit = (e) => {
//     e.preventDefault();
//     const user_job_title_json = { user_job_title };
//
//     fetch(`${process.env.REACT_APP_BACKEND_URL}/search`, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(user_job_title_json),
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data);
//         setJobs(data);
//     })
//     .catch(error => console.error('Error adding job:', error));
//   };
//
//   return (
//     <div>
//       <Navbar />
//       <div className="container">
//         <h1>LLM For Job Searching</h1>
//         {/* <div className="button-container"> */}
//         {/*   <button className="button" onClick={handleScrape}>Scrape Jobs</button> */}
//         {/* </div> */}
//         <form>
//           <div className="job-form-container">
//             <input
//               type="text"
//               placeholder="Title"
//               value={user_job_title}
//               onChange={(e) => set_user_job_title(e.target.value)}
//               className="job-input"
//             />
//             <button className="button" type="submit" onClick={handleSubmit}>Search</button>
//           </div>
//         </form>
//         <div className="job-cards-container">
//           {jobs.map((job, index) => (
//             <JobCard key={index} job={job} />
//           ))}
//         </div>
//         <div className="pagination-container">
//           {/* Pagination controls if needed */}
//         </div>
//       </div>
//     </div>
//   );
// };
//
// export default JobList;
//

// src/JobList.js
import React, { useEffect, useState } from 'react';
import './JobList.css';
import JobCard from './JobCard';
import JobSearch from './JobSearch';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
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

  const indexOfLastJob = currentPage * jobsPerPage;
  const indexOfFirstJob = indexOfLastJob - jobsPerPage;
  const currentJobs = jobs.slice(indexOfFirstJob, indexOfLastJob);

  return (
    <div>
      <div className="">
        <h1>LLM For Job Searching</h1>
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

