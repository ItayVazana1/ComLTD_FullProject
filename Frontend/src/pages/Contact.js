import React, { useState } from 'react';
import '../assets/styles/Contact.css'
import '../assets/styles/colors.css'
import '../assets/styles/main.css'
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';


function Contact({ onLogout }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Your message has been sent successfully!');
    setFormData({ name: '', email: '', message: '' });
  };

  return (
    <div className="contact-container">
      <Navbar onLogout={onLogout} />
      <div className="content d-flex">
        <Sidebar />
        <main className="col-md-9 col-lg-10 p-4">
  <section className="text-center mb-5">
    <h1 className="display-4 text-dark">We'd Love to Hear From You 😊</h1>
    <p className="lead text-muted">
      Got a question, suggestion, or need help?<br></br> Drop us a message, and we'll get back to you as soon as possible.
    </p>
  </section>
  <div className="row justify-content-center">
    <div className="col-md-10 col-lg-8">
      <form className="shadow-lg p-4 rounded bg-light" onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="form-label text-primary fw-bold">
            Full Name
          </label>
          <input
            id="name"
            type="text"
            className="form-control"
            placeholder="Your Full Name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="email" className="form-label text-primary fw-bold">
            Email Address
          </label>
          <input
            id="email"
            type="email"
            className="form-control"
            placeholder="Your Email Address"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="message" className="form-label text-primary fw-bold">
            Your Message
          </label>
          <textarea
            id="message"
            className="form-control"
            rows="5"
            placeholder="Write your message here..."
            value={formData.message}
            onChange={handleChange}
            required
          ></textarea>
        </div>
        <div className="text-center">
          <button className="btn btn-success btn-lg w-100" type="submit">
            Send Message
          </button>
        </div>
      </form>
    </div>
  </div>
</main>
      </div>
    </div>
  );
}

export default Contact;
