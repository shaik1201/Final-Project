import React from 'react';
import './FilterDropDowns.css';

const Dropdown = ({ name, value, onChange, options, placeholder, title }) => (
  <div className="dropdown-container">
    <label htmlFor={name}>{title}</label>
    <select
      id={name}
      name={name}
      value={value}
      onChange={e => onChange(name, e.target.value)} // Extract name and value before passing
      className="filter-dropdown"
    >
      <option value="" disabled>{placeholder}</option>
      {options.map(option => (
        <option key={option} value={option}>{option}</option>
      ))}
    </select>
  </div>
);

const FilterDropdowns = ({ filters, filterOptions, handleInputChange }) => {
  const dropdownConfigs = [
    { name: "company", placeholder: "Company", title: "Company" },
    { name: "location", placeholder: "Location", title: "Location" },
    { name: "datePosted", placeholder: "Date posted", title: "Date posted" },
    { name: "fieldOfExpertise", placeholder: "Field of expertise", title: "Field of expertise" },
    { name: "minExperience", placeholder: "Minimum experience", title: "Minimum experience" },
    { name: "techSkills", placeholder: "Technical skills", title: "Technical skills" },
    { name: "industry", placeholder: "Industry", title: "Industry" },
    { name: "scope", placeholder: "Scope of position", title: "Scope of position" },
    { name: "jobType", placeholder: "Job type", title: "Job type" }
  ];

  return (
    <>
      {dropdownConfigs.map(config => (
        <Dropdown
          key={config.name}
          name={config.name}
          value={filters[config.name]}
          onChange={handleInputChange} // handleInputChange will receive name and value
          options={filterOptions[config.name]}
          placeholder={"All"}
          title={config.title}
        />
      ))}
    </>
  );
};

export default FilterDropdowns;
