import React, { useState } from 'react';
import './JobCard.css';

const JobCard = ({ job }) => {
  const [showMore, setShowMore] = useState(false);

  const handleShowMore = () => {
    setShowMore(!showMore);
  };

  const getTimeAgo = (dateString) => {
    const jobDate = new Date(dateString);
    const today = new Date();

    const timeDiff = today - jobDate;
    const daysDiff = Math.floor(timeDiff / (1000 * 60 * 60 * 24));

  if (daysDiff === 0) {
      return 'today';
    } else if (daysDiff === 1) {
      return '1 day ago';
    } else {
      return `${daysDiff} days ago`;
    }
  };

  return (
    <div className="job-card">
      <div className="job-card-header">
        <h2 className="job-title">{job.title}</h2>
        <span className="job-company">{job.company}</span>
      </div>
      <div className={`job-card-body ${showMore ? 'expanded' : 'collapsed'}`}>
        <p className="job-location"><i className="fas fa-map-marker-alt"></i> {job.location}</p>
        <p className="job-date"><i className="far fa-calendar-alt"></i> Posted: {getTimeAgo(job.date)}</p>
        <div className="job-details">
          <p className="job-field_of_expertise"><span className="title">Field of expertise:</span> {job.field_of_expertise}</p>
          <p className="job-minimum_experience"><span className="title">Minimum experience:</span> {job.minimum_experience}</p>
          <p className="job-technical_skills"><span className="title">Technical skills:</span> {job.technical_skills}</p>
          <p className="job-industry"><span className="title">Industry:</span> {job.industry}</p>
          <p className="job-scope_of_position"><span className="title">Scope of position:</span> {job.scope_of_position}</p>
          <p className="job-job_type"><span className="title">Job type:</span> {job.job_type}</p>
        </div>
      </div>
      <div className="job-card-footer">
        <button className="button show-more" onClick={handleShowMore}>
          {showMore ? 'Show Less' : 'Show More'}
        </button>
        <a href={job.link} target="_blank" rel="noopener noreferrer" className="job-link">
          View Job <i className="fas fa-external-link-alt"></i>
        </a>
      </div>
    </div>
  );
};

export default JobCard;
