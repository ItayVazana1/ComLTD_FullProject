import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { useUser } from '../context/UserContext'; // Access UserContext
import { searchCustomers } from '../services/api'; // Import the API function
import '../assets/styles/SearchCustomer.css';

/**
 * SearchCustomer Component:
 * Fetches and displays customer search results based on user input.
 */
function SearchCustomer({ username, onLogout }) {
  const { userData } = useUser(); // Access UserContext
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Make a call to the API function
      const response = await searchCustomers(searchQuery);
      setResults(response.customers || []);
    } catch (err) {
      console.error('Error fetching search results:', err);
      setError('Failed to fetch search results. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="search-customer-container">
      {/* Navbar */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

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
            <button type="submit" className="btn btn-dark" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>

          {/* Error Message */}
          {error && <div className="alert alert-danger">{error}</div>}

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
                <th>Gender</th>
              </tr>
            </thead>
            <tbody>
              {results.map((customer, index) => (
                <tr key={index}>
                  <td>{customer.first_name}</td>
                  <td>{customer.last_name}</td>
                  <td>{customer.phone_number}</td>
                  <td>{customer.email_address}</td>
                  <td>{customer.address}</td>
                  <td>{customer.package_id}</td>
                  <td>{customer.gender}</td>
                </tr>
              ))}
              {results.length === 0 && !loading && (
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
