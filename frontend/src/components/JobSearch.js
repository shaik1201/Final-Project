import React, { useState, useEffect } from 'react';
import './JobSearch.css';
import FilterDropDowns from './FilterDropDowns.js';

const JobSearch = ({ onSearch }) => {
  const [title, setTitle] = useState('');
  const [filters, setFilters] = useState({
    company: '',
    location: '',
    datePosted: '',
    fieldOfExpertise: '',
    minExperience: '',
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
    techSkills: [],
    industry: [],
    scope: [],
    jobType: []
  });

  const [isCleared, setIsCleared] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/filters`)
      .then(response => response.json())
      .then(data => {
        console.log('Fetched filter options:', data);
        setFilterOptions(data);
      })
      .catch(error => console.error('Error fetching filter options:', error));
  }, []);

  useEffect(() => {
    if (isCleared) {
      console.log('Filters cleared, performing search');
      handleSearch();
      setIsCleared(false);
    }
  }, [isCleared]);

  const handleInputChange = (name, value) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [name]: value
    }));
  };

  const formatFiltersForBackend = (filters) => {
    const formattedFilters = {};
    for (const [key, value] of Object.entries(filters)) {
      if (value) { // Check if value is not empty
        formattedFilters[key] = value;
      }
    }
    return formattedFilters;
  };

  const handleSearch = () => {
    const formattedFilters = formatFiltersForBackend(filters);
    console.log('Performing search with:', { title, filters: formattedFilters });
    setCurrentPage(1); // Reset page to 1
    onSearch({ title, filters: formattedFilters, page: 1 });
  };

  const handleClear = () => {
    setTitle('');
    setFilters({
      company: '',
      location: '',
      datePosted: '',
      fieldOfExpertise: '',
      minExperience: '',
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
          aria-label="Search by job title"
        />
        <button onClick={handleSearch} className="search-button" aria-label="Search jobs">
          <i className="fas fa-search"></i> Search
        </button>
        <button onClick={handleClear} className="clear-button" aria-label="Clear search">
          <i className="fas fa-times"></i> Clear
        </button>
      </div>
      <div className="filter-dropdowns">
        <FilterDropDowns
          filters={filters}
          filterOptions={filterOptions}
          handleInputChange={handleInputChange}
        />
      </div>
    </div>
  );
};


export default JobSearch;
