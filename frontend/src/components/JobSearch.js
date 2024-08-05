import React, { useState, useEffect } from 'react';
import './JobSearch.css';
import FilterDropDowns from './FilterDropDowns';

const JobSearch = ({ onSearch }) => {
  const [title, setTitle] = useState('');
  const [filters, setFilters] = useState({
    company: [],
    location: [],
    datePosted: [],
    fieldOfExpertise: [],
    minExperience: [],
    softSkills: [],
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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    console.log(`Filter changed: ${name}`, value);
    setFilters(prevFilters => ({ ...prevFilters, [name]: value }));
  };

  const formatFiltersForBackend = (filters) => {
    const formattedFilters = {};
    for (const [key, value] of Object.entries(filters)) {
      if (value.length > 0) {
        // Join multiple values with commas or use the first value
        formattedFilters[key] = value.length > 1 ? value.join(',') : value[0];
      }
    }
    return formattedFilters;
  };

  const handleSearch = () => {
    const formattedFilters = formatFiltersForBackend(filters);
    console.log('Performing search with:', { title, filters: formattedFilters });
    onSearch({ title, filters: formattedFilters });
  };

  const handleClear = () => {
    console.log('Clearing all filters');
    setTitle('');
    setFilters({
      company: [],
      location: [],
      datePosted: [],
      fieldOfExpertise: [],
      minExperience: [],
      softSkills: [],
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