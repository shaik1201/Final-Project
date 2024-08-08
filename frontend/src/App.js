import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import JobList from './components/JobList';
import About from './components/About';
import Contact from './components/Contact';
import HeadOfPage from './components/HeadOfPage';
import Features from './components/Features';

const App = () => {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <HeadOfPage />
        <Routes>
          <Route path="/" element={<JobList />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

