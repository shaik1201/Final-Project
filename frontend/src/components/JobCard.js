import React, { useState } from 'react';
import './JobCard.css';

const JobCard = ({ job }) => {
  const [showMore, setShowMore] = useState(false);

  const handleShowMore = () => {
    setShowMore(!showMore);
  };

  return (
    <div className="job-card">
      <h2 className="job-title">{job.title}</h2>
      <p className="job-company"><span className="title">Company:</span> {job.company}</p>
      <p className="job-location"><span className="title">Location:</span> {job.location}</p>
      <p className="job-date"><span className="title">Date posted:</span> {job.date.slice(6)}</p>


      {showMore && (
        <div className="job-details">
          <p className="job-field_of_expertise"><span className="title">Field of expertise:</span> {job.field_of_expertise}</p>
          <p className="job-minimum_experience"><span className="title">Minimum experience:</span> {job.minimum_experience}</p>
          <p className="job-soft_skills"><span className="title">Soft skills:</span> {job.soft_skills}</p>
          <p className="job-technical_skills"><span className="title">Technical skills:</span> {job.technical_skills}</p>
          <p className="job-industry"><span className="title">Industry:</span> {job.industry}</p>
          <p className="job-scope_of_position"><span className="title">Scope of position:</span> {job.scope_of_position}</p>
          <p className="job-job_type"><span className="title">Job type:</span> {job.job_type}</p>
          <a href={job.link} target="_blank" rel="noopener noreferrer" className="job-link">
              View Job
          </a>
        </div>
      )}

      <button className="button show-more" onClick={handleShowMore}>
        {showMore ? 'Show Less' : 'Show More'}
      </button>
    </div>
  );
};

export default JobCard;
