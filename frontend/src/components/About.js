import React from 'react';
import './About.css';
import content from './AboutUsContent'; // Import the content

const About = () => {
  return (
    <div className='about-container'>
      {/* About Us Section */}
      <section className='section about-us'>
        <h1>{content.aboutUs.title}</h1>
        <p>{content.aboutUs.text}</p>
      </section>

      {/* TovTECH Section */}
      <section className='section tovtech-section'>
        <h2>{content.tovtech.title}</h2>
        <p>{content.tovtech.text}</p>
      </section>

      {/* Project Overview Section */}
      <section className='section project-overview'>
        <h2>{content.projectOverview.title}</h2>
        <p>{content.projectOverview.text}</p>
      </section>

      {/* Website Purpose Section */}
      <section className='section website-purpose'>
        <h2>{content.websitePurpose.title}</h2>
        <p>{content.websitePurpose.text}</p>
      </section>

      {/* Logos Section */}
      <section className='section logos-section'>
        <h2>{content.logos.title}</h2>
        <div className='logos'>
         <img src='/images/TovTech_logo.png' alt='TovTECH Logo' className='logo' />
          <img src='/images/technion_logo.jpg' alt='Technion Logo' className='logo' />
          <img src='/images/dds_logo.jpg' alt='Data Decision Science Faculty Logo' className='logo' />
        </div>
      </section>
    </div>
  );
};

export default About;
