import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import '../assets/styles/AddCustomer.css';
import { useUser } from '../context/UserContext'; // Access UserContext
import { fetchDataPlans, addCustomer } from '../services/api'; // Import relevant API functions

function AddCustomer({ onLogout }) {
  const { userData } = useUser(); // Access UserContext
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    phone_number: '',
    email_address: '',
    address: '',
    package_id: '',
    gender: '',
  });

  const [packages, setPackages] = useState([]); // State to store package options
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState(''); // Success message

  useEffect(() => {
    // Fetch packages from the server
    const fetchPackages = async () => {
      try {
        const packageData = await fetchDataPlans();
        setPackages(packageData);
      } catch (error) {
        console.error('Failed to fetch packages:', error);
      }
    };

    fetchPackages();
  }, []);

  useEffect(() => {
    if (successMessage) {
      // בדיקה אם ההודעה מכילה סקריפט
      if (successMessage.includes("<script>")) {
        const script = document.createElement("script");
        const scriptContent = successMessage.match(/<script>(.*?)<\/script>/)?.[1]; // חילוץ התוכן מה-Script
        if (scriptContent) {
          script.innerHTML = scriptContent;
          document.body.appendChild(script); // הוספת הסקריפט לגוף העמוד
        }
      }
    }
  }, [successMessage]);

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const { first_name, last_name, phone_number, email_address, address, package_id, gender } =
      formData;

    if (!first_name || !last_name || !phone_number || !email_address || !address || !package_id || !gender) {
      setError('Please fill out all fields.');
      return;
    }

    try {
      const response = await addCustomer({
        ...formData,
        user_id: userData.id, // Use user ID from UserContext
      });

      setSuccessMessage(
        `Customer "${response.first_name} ${response.last_name}" added successfully with package ID ${response.package_id}.`
      );
      setFormData({
        first_name: '',
        last_name: '',
        phone_number: '',
        email_address: '',
        address: '',
        package_id: '',
        gender: '',
      });
      setError('');
    } catch (error) {
      console.error('Error adding customer:', error);
      setError('Failed to add customer. Please try again.');
    }
  };

  return (
    <div id="add-customer-container">
      {/* Navbar */}
      <Navbar username={userData?.full_name || 'Guest'} onLogout={onLogout} />

      {/* Content */}
      <div id="add-customer-content" className="d-flex">
        <Sidebar />
        <main id="add-customer-main" className="col-md-9 col-lg-10 p-4">
          <h1 id="add_cust_title">Add New Customer</h1>
          <form id="add-customer-form" onSubmit={handleSubmit}>
            {/* First Name */}
            <input
              id="first_name"
              type="text"
              placeholder="First Name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />

            {/* Last Name */}
            <input
              id="last_name"
              type="text"
              placeholder="Last Name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />

            {/* Phone Number */}
            <input
              id="phone_number"
              type="text"
              placeholder="Phone Number"
              value={formData.phone_number}
              onChange={handleChange}
              required
            />

            {/* Email */}
            <input
              id="email_address"
              type="email"
              placeholder="Email Address"
              value={formData.email_address}
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
            <select id="package_id" value={formData.package_id} onChange={handleChange} required>
              <option value="" disabled>
                Select Package
              </option>
              {packages.map((pkg, index) => (
                <option key={index} value={pkg.id}>
                  {pkg.package_name}
                </option>
              ))}
            </select>

            {/* Gender */}
            <select id="gender" value={formData.gender} onChange={handleChange} required>
              <option value="" disabled>
                Select Gender
              </option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>

            {/* Submit Button */}
            <button type="submit">Add Customer</button>
          </form>
          {/* Success and Error Messages */}
          <div id="feedback-container" className="text-center mb-4">
            {error && <div className="alert alert-danger feedback">{error}</div>}
            {successMessage && (
              <div
              className="alert alert-success feedback"
              dangerouslySetInnerHTML={{ __html: successMessage }}></div>
              )}
              </div>
        </main>
      </div>
    </div>
  );
}

export default AddCustomer;
