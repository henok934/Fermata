import React, { useEffect, useState } from 'react';
import './HomePage.css';

const HomePage = () => {
  const [buschangesCount, setBuschangesCount] = useState(0);
  const [cities, setCities] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:3000/api/buschanges'); // Adjust if needed
        const data = await response.json();
        setBuschangesCount(data.buschanges_count);
        setCities(data.cities);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="homepage">
      <header className="header">
        <div className="logo">Ticket Logo</div>
        <nav className="nav">
          <a href="#book">Book</a>
          <a href="#sign-in">Sign In</a>
          <a href="#home">Home</a>
        </nav>
      </header>
      <main className="main-content">
        <h1 className="title">We have the best routes</h1>
        <form className="search-form">
          <input type="text" placeholder="From" className="input-field" />
          <input type="text" placeholder="To" className="input-field" />
          <input type="date" className="input-field" />
          <button type="submit" className="search-button">Search</button>
        </form>
        
        <div className="results">
          <h2>Available Bus Changes</h2>
          <p>Total Bus Changes: {buschangesCount}</p>
          <h3>Cities:</h3>
          <ul>
            {cities.map((city, index) => (
              <li key={index}>{city}</li>
            ))}
          </ul>
        </div>
      </main>
    </div>
  );
};

export default HomePage;
