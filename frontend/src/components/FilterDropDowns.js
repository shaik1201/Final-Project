import React from 'react';
import './FilterDropDowns.css';

const CheckboxDropdown = ({ name, selectedValues, onChange, options, title, activeDropdown, setActiveDropdown }) => {
  const isOpen = activeDropdown === name;

  const handleCheckboxChange = (value) => {
    if (selectedValues.includes(value)) {
      onChange(name, selectedValues.filter(item => item !== value)); // Remove value
    } else {
      onChange(name, [...selectedValues, value]); // Add value
    }
  };

  const toggleDropdown = () => {
    if (isOpen) {
      setActiveDropdown(null); // Close if it's already open
    } else {
      setActiveDropdown(name); // Open the clicked dropdown and close others
    }
  };

  return (
    <div className="dropdown-container">
      <button className="dropdown-button" onClick={toggleDropdown}>
        {title}
      </button>
      {isOpen && (
        <div className="checkbox-dropdown scrollable-dropdown">
          {options.map(option => (
            <label key={option} className="checkbox-option">
              <input
                type="checkbox"
                checked={selectedValues.includes(option)}
                onChange={() => handleCheckboxChange(option)}
              />
              {option}
            </label>
          ))}
        </div>
      )}
    </div>
  );
};

const FilterDropdowns = ({ filters, filterOptions, handleInputChange, activeDropdown, setActiveDropdown }) => {
  const dropdownConfigs = [
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
    <>
      {dropdownConfigs.map(config => (
        <CheckboxDropdown
          key={config.name}
          name={config.name}
          selectedValues={filters[config.name]}
          onChange={handleInputChange}
          options={filterOptions[config.name]}
          title={config.title}
          activeDropdown={activeDropdown}
          setActiveDropdown={setActiveDropdown} // Manage active dropdowns
        />
      ))}
    </>
  );
};

export default FilterDropdowns;
