import React, { useState } from 'react';
import './UploadCV.css';

const UploadCV = ({ onUpload, onFileChange }) => {
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
        <h2>Upload your CV to get recommended jobs for you</h2><br/>
      <label htmlFor="file-upload" className="custom-file-upload">
        Choose File
      </label>
      <input id="file-upload" type="file" accept="application/pdf" onChange={handleFileChange} />
      {fileName && <span className="file-name">{fileName}</span>}
      <button onClick={onUpload}>Upload CV</button>
    </div>
  );
}

export default UploadCV;
