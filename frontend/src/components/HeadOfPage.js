import React from 'react';
import './HeadOfPage.css';

const HeadOfPage = () => {
  return (
    <div 
      className="head-of-page"
      style={{
        backgroundImage: `
          linear-gradient(135deg, rgba(52, 152, 219, 0.8) 0%, rgba(44, 62, 80, 0.8) 100%),
          url(${process.env.PUBLIC_URL + '/images/depositphotos_70174505-stock-photo-creativity-team-working-together.jpg'})
        `,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      <h1 className="title">Let's Find Your Dream Job!</h1>
      <p className="description">
        Here you can find the latest job listings, learn more about us, and get in touch. 
        We are dedicated to helping you find your dream job.
      </p>
    </div>
  );
};

export default HeadOfPage;
