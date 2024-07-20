import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'
import { NavLink } from 'react-router-dom';
import About from './About.js'; // Import About component
import Contact from './Contact.js'; // Import Contact component
// Comment

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
      <h1>LLM For Job Searching</h1>

        <ul className="nav-menu">
          <li className="nav-item">
            <NavLink exact to="/" className="nav-links" activeClassName="active-link">
              Home
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/about" className="nav-links" activeClassName="active-link">
              About
             </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/contact" className="nav-links" activeClassName="active-link">
              Contact
            </NavLink>
          </li>
          {/* Add more <li> elements for additional navigation items */}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
