
import React, { useState } from 'react';
import './FilterDropDowns.css';

const FilterDropDowns = ({ filters, filterOptions, handleInputChange }) => {
  const dropdownConfigs = [
    { name: "company", title: "Company" },
    { name: "location", title: "Location" },
    { name: "datePosted", title: "Date posted" },
    { name: "fieldOfExpertise", title: "Field of expertise" },
    { name: "minExperience", title: "Minimum experience" },
    { name: "softSkills", title: "Soft skills" },
    { name: "techSkills", title: "Technical skills" },
    { name: "industry", title: "Industry" },
    { name: "scope", title: "Scope of position" },
    { name: "jobType", title: "Job type" }
  ];

  return (
    <div className="dropdown-container">
      {dropdownConfigs.map(config => (
        <Dropdown
          key={config.name}
          name={config.name}
          title={config.title}
          options={filterOptions[config.name]}
          selectedValues={filters[config.name]}
          handleInputChange={handleInputChange}
        />
      ))}
    </div>
  );
};

const Dropdown = ({ name, title, options, selectedValues, handleInputChange }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleCheckboxChange = (option) => {
    handleInputChange(name, option);
  };

  const handleSelectAll = () => {
    if (selectedValues.length === options.length) {
      // If all options are selected, unselect all
      options.forEach(option => handleInputChange(name, option));
    } else {
      // Otherwise, select all options
      options.forEach(option => {
        if (!selectedValues.includes(option)) {
          handleInputChange(name, option);
        }
      });
    }
  };

  return (
    <div className="dropdown">
      <button className="dropdown-button" onClick={() => setIsOpen(!isOpen)}>
        {title}
      </button>
      {isOpen && (
        <div className="dropdown-content">
          <div className="checkbox-item">
            <input
              type="checkbox"
              id={`${name}-all`}
              checked={selectedValues.length === options.length}
              onChange={handleSelectAll}
            />
            <label htmlFor={`${name}-all`}>All</label>
          </div>
          {options.map(option => (
            <div key={option} className="checkbox-item">
              <input
                type="checkbox"
                id={`${name}-${option}`}
                value={option}
                checked={selectedValues.includes(option)}
                onChange={() => handleCheckboxChange(option)}
              />
              <label htmlFor={`${name}-${option}`}>{option}</label>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FilterDropDowns;



