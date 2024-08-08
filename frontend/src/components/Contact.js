import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Updated import
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  const [isSubmitted, setIsSubmitted] = useState(false);
  const navigate = useNavigate(); // Updated hook

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form data:', formData);
    // Implement the form submission logic here
    setIsSubmitted(true);
  };

  const handleHomeRedirect = () => {
    navigate('/'); // Updated function
  };

  return (
    <div className="contact-us-container">
      <h1>Contact Us</h1>
      {isSubmitted ? (
        <div className="thank-you-message">
          <p>Thank you for reaching out to us! Our team will get back to you as soon as possible.</p>
          <br></br>
          <p>In the meantime, feel free to explore our website</p>
          <button onClick={handleHomeRedirect} className="home-button">Go back to Job Search</button>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name" className="required">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email" className="required">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="message">Message:</label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
            />
          </div>
          <button type="submit" className="submit-button">Send</button>
        </form>
      )}
    </div>
  );
};

export default Contact;