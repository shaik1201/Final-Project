import React, { useState } from 'react';
import './UploadCV.css';

const UploadCV = ({ onUpload, onFileChange, message }) => {
  const [fileName, setFileName] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      onFileChange(e);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload your CV and let us do the rest 🏖️</h2>
      <label htmlFor="file-upload" className="custom-file-upload">
        <i className="fas fa-upload"></i> Choose File
      </label>
      <input id="file-upload" type="file" accept="application/pdf" onChange={handleFileChange} />
      {fileName && <span className="file-name">{fileName}</span>}
      <button onClick={onUpload} className="upload-button">
        <i className="fas fa-cloud-upload-alt"></i> Upload CV
      </button>
      {/* Display the message below the button */}
      {message && <p className="upload-message">{message}</p>}
    </div>
  );
};

export default UploadCV;
