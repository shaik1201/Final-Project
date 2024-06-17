import React from "react";

const JobCard = ({ job }) => {
  return (
    <div className="job-card">
      <h2 className="job-title">{job.title}</h2>
      <p className="job-company"><span className="title">Company:</span> {job.company}</p>
      <p className="job-location"><span className="title">Location:</span> {job.location}</p>
      <p className="job-date"><span className="title">Date posted:</span> {job.date}</p>
      <p className="job-experience"><span className="title">Years of experience:</span> {job.years_of_experience}</p>
      <p className="job-degree"><span className="title">Degree required:</span> {job.degree_required}</p>
      <a href={job.link} target="_blank" rel="noopener noreferrer" className="job-link">
        View Job
      </a>
    </div>
  );
};

export default JobCard;
