import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/AddCustomer.css';

/**
 * AddCustomer Component:
 * Displays a form for adding a new customer with validation.
 */
function AddCustomer({ username, onLogout }) {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    phone: '',
    email: '',
    address: '',
    package: '',
    creditCard: '',
  });

  const [error, setError] = useState('');

  const packages = ['Essential Plan', 'Streamer Lite', 'Unlimited Pro', 'Global Connect'];

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Basic validation
    const { firstName, lastName, phone, email, address, package: customerPackage, creditCard } =
      formData;

    if (
      !firstName ||
      !lastName ||
      !phone ||
      !email ||
      !address ||
      !customerPackage ||
      !creditCard
    ) {
      setError('Please fill out all fields.');
      return;
    }

    if (!/^\d{10}$/.test(phone)) {
      setError('Phone number must be 10 digits.');
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError('Invalid email format.');
      return;
    }

    if (!/^\d{16}$/.test(creditCard)) {
      setError('Credit card number must be 16 digits.');
      return;
    }

    setError('');
    alert('Customer added successfully!');
    setFormData({
      firstName: '',
      lastName: '',
      phone: '',
      email: '',
      address: '',
      package: '',
      creditCard: '',
    });
  };

  return (
    <div id="add-customer-container">
      {/* Navbar */}
      <Navbar username={username} onLogout={onLogout} />

      {/* Content */}
      <div id="add-customer-content" className="d-flex">
        <Sidebar />
        <main id="add-customer-main" className="col-md-9 col-lg-10 p-4">
          <h1 id="add_cust_title">Add New Customer</h1>
          <form id="add-customer-form" onSubmit={handleSubmit}>
            {/* Error Message */}
            {error && <div className="alert alert-danger">{error}</div>}

            {/* First Name */}
            <input
              id="firstName"
              type="text"
              placeholder="First Name"
              value={formData.firstName}
              onChange={handleChange}
              required
            />

            {/* Last Name */}
            <input
              id="lastName"
              type="text"
              placeholder="Last Name"
              value={formData.lastName}
              onChange={handleChange}
              required
            />

            {/* Phone */}
            <input
              id="phone"
              type="text"
              placeholder="Phone Number"
              value={formData.phone}
              onChange={handleChange}
              required
            />

            {/* Email */}
            <input
              id="email"
              type="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={handleChange}
              required
            />

            {/* Address */}
            <input
              id="address"
              type="text"
              placeholder="Address"
              value={formData.address}
              onChange={handleChange}
              required
            />

            {/* Package */}
            <select
              id="package"
              value={formData.package}
              onChange={handleChange}
              required
            >
              <option value="" disabled>
                Select Package
              </option>
              {packages.map((pkg, index) => (
                <option key={index} value={pkg}>
                  {pkg}
                </option>
              ))}
            </select>

            {/* Credit Card */}
            <input
              id="creditCard"
              type="text"
              placeholder="Credit Card Number"
              value={formData.creditCard}
              onChange={handleChange}
              required
            />

            {/* Submit Button */}
            <button type="submit">Add Customer</button>
          </form>
        </main>
      </div>
    </div>
  );
}

export default AddCustomer;
