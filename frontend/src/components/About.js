import React from 'react';
import './About.css';
import content from './AboutUsContent'; // Import the content

const About = () => {
const formatTextWithNewLines = (text) => {
  return text.split('\n').map((line, index) => (
    <React.Fragment key={index}>
      {line.trim()}
      {index !== text.split('\n').length - 1 && <br />}
    </React.Fragment>
  ));
};

 let tovtech_text = content.tovtech.text.split('\n').map((sentence, index, arr) => (
    <React.Fragment key={index}>
      {sentence.trim()}
      {index === arr.length - 1 ? (
        <>
          {' '}
          <a href="https://tovtech.org/" target="_blank" rel="noopener noreferrer">
           TovTech
          </a>
          .
        </>
      ) : (
        <>
          .<br />
        </>
      )}
    </React.Fragment>
  ));

  return (
    <div className='about-container'>
      {/* About Us Section */}
      <section className='section about-us'>
        <h1>{content.aboutUs.title}</h1>
        <p>{formatTextWithNewLines(content.aboutUs.text)}</p>
      </section>

      {/* TovTECH Section */}
      <section className='section tovtech-section'>
        <h2>{content.tovtech.title}</h2>
        <p>{tovtech_text}
        </p>
      </section>

      {/* Project Overview Section */}
      <section className='section project-overview'>
        <h2>{content.projectOverview.title}</h2>
        <p>{formatTextWithNewLines(content.projectOverview.text)}</p>
      </section>

      {/* Website Purpose Section */}
      <section className='section website-purpose'>
        <h2>{content.websitePurpose.title}</h2>
        <p>{formatTextWithNewLines(content.websitePurpose.text)}</p>
      </section>

      {/* Logos Section */}
      <section className='section logos-section'>
        <h2>{content.logos.title}</h2>
        <div className='logos'>
        <a href="https://tovtech.org/" target="_blank" rel="noopener noreferrer">
         <img src='/images/TovTech_logo.png' alt='TovTECH Logo' className='logo' />
         </a>
         <a href="https://www.technion.ac.il/" target="_blank" rel="noopener noreferrer">
          <img src='/images/technion_logo.jpg' alt='Technion Logo' className='logo' />
          </a>
          <a href="https://dds.technion.ac.il/he/" target="_blank" rel="noopener noreferrer">
          <img src='/images/dds_logo.jpg' alt='Data Decision Science Faculty Logo' className='logo' />
          </a>
        </div>
      </section>
    </div>
  );
};

export default About;