// src/JobSearch.js
import React, { useState, useEffect } from 'react';
import './JobSearch.css';

const JobSearch = ({ onSearch }) => {
  const [title, setTitle] = useState('');
  const [city, setCity] = useState('');
  const [filters, setFilters] = useState({
    company: '',
    location: '',
    datePosted: '',
    fieldOfExpertise: '',
    minExperience: '',
    softSkills: '',
    techSkills: '',
    industry: '',
    scope: '',
    jobType: '',
  });

  const [filterOptions, setFilterOptions] = useState({
    company: [],
    location: [],
    datePosted: [],
    fieldOfExpertise: [],
    minExperience: [],
    softSkills: [],
    techSkills: [],
    industry: [],
    scope: [],
    jobType: []
  });

  useEffect(() => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/filters`)
      .then(response => response.json())
      .then(data => setFilterOptions(data))
      .catch(error => console.error('Error fetching filter options:', error));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
  };

  const handleSearch = () => {
    onSearch({ title, city, filters });
  };

  const handleClear = () => {
    setTitle('');
    setCity('');
    setFilters({
      company: '',
      location: '',
      datePosted: '',
      fieldOfExpertise: '',
      minExperience: '',
      softSkills: '',
      techSkills: '',
      industry: '',
      scope: '',
      jobType: '',
    });
  };

  return (
    <div className="search-container">
      <div className="search-inputs">
        <input
          type="text"
          placeholder="Search by title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="search-input"
        />
        {/* <input
          type="text"
          placeholder="Search by city"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="search-input"
        /> */}
        <button onClick={handleSearch} className="search-button">Search</button>
        <button onClick={handleClear} className="clear-button">Clear</button>
      </div>
      <div className="filter-dropdowns">
        <select name="company" value={filters.company} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Company</option>
          {filterOptions.company.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        <select name="location" value={filters.location} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Location</option>
          {filterOptions.location.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        <select name="datePosted" value={filters.datePosted} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Date posted</option>
          {filterOptions.datePosted.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        <select name="fieldOfExpertise" value={filters.fieldOfExpertise} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Field of expertise</option>
          {filterOptions.fieldOfExpertise.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        <select name="minExperience" value={filters.minExperience} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Minimum experience</option>
          {filterOptions.minExperience.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        <select name="softSkills" value={filters.softSkills} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Soft skills</option>
          {filterOptions.softSkills.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        <select name="techSkills" value={filters.techSkills} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Technical skills</option>
          {filterOptions.techSkills.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        <select name="industry" value={filters.industry} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Industry</option>
          {filterOptions.industry.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        <select name="scope" value={filters.scope} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Scope of position</option>
          {filterOptions.scope.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
        <select name="jobType" value={filters.jobType} onChange={handleInputChange} className="filter-dropdown">
          <option value="" disabled>Job type</option>
          {filterOptions.jobType.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default JobSearch;
