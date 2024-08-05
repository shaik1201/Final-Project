import React from 'react';
import Select from 'react-select';

const MultiSelectDropdown = ({ name, selectedValues, onChange, options, placeholder, title }) => {
  const handleChange = (selectedOptions) => {
    console.log(`selectedOptions under handleChange inside MultiSelectDropdown:`, selectedOptions);
    onChange(name, selectedOptions ? selectedOptions.map(option => option.value) : []);
  };

  console.log(`Raw options for ${name}:`, options);

  const selectOptions = Array.isArray(options)
    ? options.map(option => ({ value: option, label: option }))
    : [];

  console.log(`Processed selectOptions for ${name}:`, selectOptions);

  const value = Array.isArray(selectedValues)
    ? selectedValues.map(value => ({ value, label: value }))
    : [];

  console.log(`Raw selectedValues for ${name}:`, selectedValues);
  console.log(`Processed value for ${name}:`, value);

  return (
    <div className="dropdown-container">
      <label htmlFor={name}>{title}</label>
      <Select
        isMulti
        name={name}
        options={selectOptions}
        className="filter-dropdown"
        classNamePrefix="select"
        onChange={handleChange}
        value={value}
        placeholder={placeholder}
      />
    </div>
  );
};

export default MultiSelectDropdown;