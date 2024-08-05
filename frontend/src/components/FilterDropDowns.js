import React from 'react';
import MultiSelectDropdown from './MultiSelectDropdown';
import './FilterDropDowns.css'

const FilterDropDowns = ({ filters, filterOptions, handleInputChange }) => {
  const dropdownConfigs = [
    { name: "company", placeholder: "Company", title: "Company" },
    { name: "location", placeholder: "Location", title: "Location" },
    { name: "datePosted", placeholder: "Date posted", title: "Date posted" },
    { name: "fieldOfExpertise", placeholder: "Field of expertise", title: "Field of expertise" },
    { name: "minExperience", placeholder: "Minimum experience", title: "Minimum experience" },
    { name: "softSkills", placeholder: "Soft skills", title: "Soft skills" },
    { name: "techSkills", placeholder: "Technical skills", title: "Technical skills" },
    { name: "industry", placeholder: "Industry", title: "Industry" },
    { name: "scope", placeholder: "Scope of position", title: "Scope of position" },
    { name: "jobType", placeholder: "Job type", title: "Job type" }
  ];

  const handleMultiSelectChange = (name, selectedValues) => {
    console.log(`selectedValues under handleMultiSelectChange inside FilterDropDowns:`, selectedValues)
    handleInputChange({ target: { name, value: selectedValues } });
  };

const selectedValues = {};
Object.keys(filterOptions).forEach(key => {
    selectedValues[key] = [];
});

console.log(`filterOptions under FilterDropDowns:`, filterOptions);
console.log(`~~~~ filters under FilterDropDowns:`, filters);

return (
  <div className="dropdown-container">
    {dropdownConfigs.map(config => {
      console.log(`filterOptions of ${config.name} under FilterDropDowns:`, filterOptions[config.name]);
      console.log(`filters of ${config.name} under FilterDropDowns:`, filters[config.name]);

      return (
        <MultiSelectDropdown
          key={config.name}
          name={config.name}
          selectedValues={filters[config.name] || []}
          onChange={handleMultiSelectChange}
          options={filterOptions[config.name]}
          placeholder="All"
          title={config.title}
        />
      );
    })}
  </div>
);
};

export default FilterDropDowns;