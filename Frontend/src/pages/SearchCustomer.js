import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/SearchCustomer.css';

/**
 * SearchCustomer Component:
 * Displays a search form and a table for displaying customer search results.
 */
function SearchCustomer({ username, onLogout }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]); // Placeholder for customer search results

  // Mock data for results (to be replaced with database queries later)
  const mockData = [
    {
      firstName: 'John',
      lastName: 'Doe',
      phone: '1234567890',
      email: 'john.doe@example.com',
      address: '123 Main St',
      package: 'Unlimited Pro',
      creditCard: '1234567812345678',
    },
    {
      firstName: 'Jane',
      lastName: 'Smith',
      phone: '9876543210',
      email: 'jane.smith@example.com',
      address: '456 Elm St',
      package: 'Streamer Lite',
      creditCard: '8765432187654321',
    },
    // Add more mock customers here
  ];

  const handleSearch = (e) => {
    e.preventDefault();

    // Filter mock data based on search query
    const filteredResults = mockData.filter(
      (customer) =>
        customer.firstName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        customer.lastName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        customer.email.toLowerCase().includes(searchQuery.toLowerCase())
    );

    setResults(filteredResults);
  };

  return (
    <div id="search-customer-container">
      {/* Navbar */}
      <Navbar username={username} onLogout={onLogout} />

      {/* Content */}
      <div id="search-customer-content" className="d-flex">
        <Sidebar />
        <main id="search-customer-main" className="col-md-9 col-lg-10 p-4">
          <h1 className="mb-4">Search Customers</h1>
          <form id="search-customer-form" className="d-flex mb-4 gap-2" onSubmit={handleSearch}>
            <input
              type="text"
              className="form-control"
              placeholder="Search by name, email, or phone"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="btn btn-dark">
              Search
            </button>
          </form>

          {/* Results Table */}
          <table id="results-table" className="table table-striped table-bordered">
            <thead className="table-dark">
              <tr>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Address</th>
                <th>Package</th>
                <th>Credit Card</th>
              </tr>
            </thead>
            <tbody>
              {results.slice(0, 15).map((customer, index) => (
                <tr key={index}>
                  <td>{customer.firstName}</td>
                  <td>{customer.lastName}</td>
                  <td>{customer.phone}</td>
                  <td>{customer.email}</td>
                  <td>{customer.address}</td>
                  <td>{customer.package}</td>
                  <td>{customer.creditCard}</td>
                </tr>
              ))}
              {results.length === 0 && (
                <tr>
                  <td colSpan="7" className="text-center text-muted">
                    No results found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </main>
      </div>
    </div>
  );
}

export default SearchCustomer;
