import React, { useState, useEffect } from 'react';
import './JobSearch.css';
import FilterDropDowns from './FilterDropDowns.js';

const JobSearch = ({ onSearch }) => {
  const [title, setTitle] = useState('');
  const [filters, setFilters] = useState({
    company: [],
    location: [],
    datePosted: [],
    fieldOfExpertise: [],
    minExperience: [],
    techSkills: [],
    industry: [],
    scope: [],
    jobType: [],
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
  const [activeDropdown, setActiveDropdown] = useState(null); // Track active dropdown

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
      if (value.length > 0) { // Check if value is not empty
        formattedFilters[key] = value;
      }
    }
    return formattedFilters;
  };

  const handleSearch = () => {
    const formattedFilters = formatFiltersForBackend(filters);
    console.log('Performing search with:', { title, filters: formattedFilters });
    setCurrentPage(1); // Reset page to 1
    setActiveDropdown(null); // Close any open dropdowns
    onSearch({ title, filters: formattedFilters, page: 1 });
  };

  const handleClear = () => {
    setTitle('');
    setFilters({
      company: [],
      location: [],
      datePosted: [],
      fieldOfExpertise: [],
      minExperience: [],
      techSkills: [],
      industry: [],
      scope: [],
      jobType: [],
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
        <button onClick={handleSearch} className="search-button">
          <i className="fas fa-search"></i> Search
        </button>
        <button onClick={handleClear} className="clear-button">
          <i className="fas fa-times"></i> Clear
        </button>
      </div>
      <div className="filter-dropdowns">
        <FilterDropDowns
          filters={filters}
          filterOptions={filterOptions}
          handleInputChange={handleInputChange}
          activeDropdown={activeDropdown}
          setActiveDropdown={setActiveDropdown} // Pass to manage active dropdowns
        />
      </div>
    </div>
  );
};

export default JobSearch;
