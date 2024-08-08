import React from 'react';
import './FilterCheckboxes.css';

const FilterCheckboxes = ({ filters, filterOptions, handleInputChange }) => {
  const checkboxConfigs = [
    { name: "company", title: "Company" },
    { name: "location", title: "Location" },
    { name: "datePosted", title: "Date posted" },
    { name: "fieldOfExpertise", title: "Field of expertise" },
    { name: "minExperience", title: "Minimum experience" },
    { name: "techSkills", title: "Technical skills" },
    { name: "industry", title: "Industry" },
    { name: "scope", title: "Scope of position" },
    { name: "jobType", title: "Job type" }
  ];

  return (
    <div className="checkbox-container">
      {checkboxConfigs.map(config => (
        <div key={config.name} className="checkbox-group">
          <label>{config.title}</label>
          {filterOptions[config.name].map(option => (
            <div key={option} className="checkbox-item">
              <input
                type="checkbox"
                id={`${config.name}-${option}`}
                name={config.name}
                value={option}
                checked={filters[config.name].includes(option)}
                onChange={() => handleInputChange(config.name, option)}
              />
              <label htmlFor={`${config.name}-${option}`}>{option}</label>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default FilterCheckboxes;