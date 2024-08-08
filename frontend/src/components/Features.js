import React from 'react';
import './Features.css';

const featuresData = [
  {
    title: 'Search for Jobs 🔍',
    description: 'Search for jobs that match your skills and interests.',
  },
  {
    title: 'Upload Your CV 📄',
    description: 'Get recommendations based on your CV.',
  },
  {
    title: 'Apply for Jobs 📝',
    description: 'Follow the links to apply for jobs.',
  }
];

const Features = () => {
  return (
    <section className="features">
      {featuresData.map((feature, index) => (
        <div className="feature-card" key={index}>
          <h3 className="feature-title">{feature.title}</h3>
          <p className="feature-description">{feature.description}</p>
        </div>
      ))}
    </section>
  );
};

export default Features;
