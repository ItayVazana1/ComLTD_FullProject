import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { useUser } from '../context/UserContext'; // Access UserContext for global user data
import { searchCustomers } from '../services/api'; // API function to search for customers
import '../assets/styles/SearchCustomer.css'; // Import CSS for component styling

/**
 * SearchCustomer Component:
 * Allows users to search for customers in the database and view results in a table.
 * @param {string} username - The username to display in the Navbar
 * @param {Function} onLogout - Function to handle user logout
 */
function SearchCustomer({ username, onLogout }) {
  const { userData } = useUser(); // Access user data from context
  const [searchQuery, setSearchQuery] = useState(''); // State to store the search input
  const [results, setResults] = useState([]); // State to store the search results
  const [loading, setLoading] = useState(false); // State to manage loading spinner
  const [error, setError] = useState(''); // State to handle error messages

  /**
   * Handle the search form submission
   * @param {Event} e - Form submission event
   */
  const handleSearch = async (e) => {
    e.preventDefault(); // Prevent form submission from reloading the page
    setLoading(true); // Show loading spinner
    setError(''); // Clear any previous errors

    try {
      // Call the API to search for customers
      const response = await searchCustomers(searchQuery);
      setResults(response.customers || []); // Update results state
    } catch (err) {
      console.error('Error fetching search results:', err); // Log the error
      setError('Failed to fetch search results. Please try again.'); // Show user-friendly error message
    } finally {
      setLoading(false); // Hide loading spinner
    }
  };

  return (
    <div id="search-customer-container">
      {/* Navbar */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Content Section */}
      <div id="search-customer-content" className="d-flex">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content Area */}
        <main id="search-customer-main" className="col-md-9 col-lg-10 p-4">
          <h1 className="mb-4">Search Customers</h1>

          {/* Search Form */}
          <form id="search-customer-form" className="d-flex mb-4 gap-2" onSubmit={handleSearch}>
            <input
              type="text"
              className="form-control"
              placeholder="Search by name, email, or phone"
              value={searchQuery} // Controlled input value
              onChange={(e) => setSearchQuery(e.target.value)} // Update search query state
            />
            <button type="submit" className="btn btn-dark" disabled={loading}>
              {loading ? 'Searching...' : 'Search'} {/* Show spinner or button text */}
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
                    No results found. {/* Message when no results are found */}
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
