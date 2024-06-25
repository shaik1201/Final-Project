// src/JobSearch.js
import React, { useState, useEffect } from 'react';
import './JobSearch.css';
import FilterDropDowns from './FilterDropDowns.js'

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

  const [isCleared, setIsCleared] = useState(false);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/filters`)
      .then(response => response.json())
      .then(data => setFilterOptions(data))
      .catch(error => console.error('Error fetching filter options:', error));
  }, []);

  useEffect(() => {
    if (isCleared) {
      onSearch({ title, city, filters });
      setIsCleared(false); // Reset the cleared state after performing the search
    }
  }, [isCleared, title, city, filters, onSearch]);


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
    setIsCleared(true);
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
          <FilterDropDowns filters={filters} filterOptions={filterOptions} handleInputChange={handleInputChange} />

      </div>
    </div>
  );
};

export default JobSearch;
