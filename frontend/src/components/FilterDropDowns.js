import React from 'react';
import './FilterDropDowns.css';

// Utility function to truncate text with ellipsis
const truncateText = (text, maxLength) => {
  if (text.length > maxLength) {
    return text.slice(0, maxLength) + '...';
  }
  return text;
};

const CheckboxDropdown = ({ name, selectedValues, onChange, options, activeDropdown, setActiveDropdown, title }) => {
  const isOpen = activeDropdown === name;

  // Check if all options are selected
  const areAllSelected = options.length > 0 && selectedValues.length === options.length;

  const selectedText = areAllSelected
    ? `${title}: Select All`
    : truncateText(selectedValues.join(', '), 20); // Adjust maxLength as needed

  const handleCheckboxChange = (value) => {
    if (selectedValues.includes(value)) {
      onChange(name, selectedValues.filter(item => item !== value)); // Remove value
    } else {
      onChange(name, [...selectedValues, value]); // Add value
    }
  };

  const handleSelectAll = () => {
    if (areAllSelected) {
      // If all options are selected, deselect all
      onChange(name, []);
    } else {
      // Otherwise, select all options
      onChange(name, [...options]);
    }
  };

  const toggleDropdown = () => {
    setActiveDropdown(isOpen ? null : name); // Toggle dropdown
  };

  return (
    <div className="dropdown-container">
      <button className="dropdown-button" onClick={toggleDropdown}>
        {selectedValues.length > 0 ? selectedText : title} {/* Show "Select All" or selected values */}
      </button>
      {isOpen && (
        <div className="checkbox-dropdown scrollable-dropdown">
          <label className="checkbox-option">
            <input
              type="checkbox"
              checked={areAllSelected}
              onChange={handleSelectAll}
            />
            Select All
          </label>
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
    { name: 'company', title: 'Company' },
    { name: 'location', title: 'Location' },
    { name: 'datePosted', title: 'Date posted' },
    { name: 'fieldOfExpertise', title: 'Field of expertise' },
    { name: 'minExperience', title: 'Minimum experience' },
    { name: 'techSkills', title: 'Technical skills' },
    { name: 'industry', title: 'Industry' },
    { name: 'scope', title: 'Scope of position' },
    { name: 'jobType', title: 'Job type' },
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
          setActiveDropdown={setActiveDropdown}
        />
      ))}
    </>
  );
};

export default FilterDropdowns;
