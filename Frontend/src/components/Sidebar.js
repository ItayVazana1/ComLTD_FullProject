import React from 'react';
import { useLocation } from 'react-router-dom';
import '../assets/styles/Global.css';
import '../assets/styles/sidebar.css';
import logo from '../assets/images/logo.png';

const menuItems = [
  { title: 'Home', href: '/' },
  { title: 'About', href: '/about' },
  { title: 'Data Plans', href: '/data-plans' },
  {
    title: 'Customers',
    subMenu: [
      { title: 'New Customer', href: '/customers/new' },
      { title: 'Search', href: '/customers/search' },
    ],
  },
  {
    title: 'Account',
    subMenu: [
      { title: 'My Profile', href: '/account/profile' },
      { title: 'Change My Password', href: '/account/change-password' },
    ],
  },
  { title: 'Contact Us', href: '/contact' },
];

function Sidebar() {
  const location = useLocation(); // Get the current location

  /**
   * Check if the current path matches any of the submenu items.
   * @param {Array} subMenu - The submenu items to check.
   * @returns {boolean} - True if the current path matches a submenu item.
   */
  const isSubMenuActive = (subMenu) =>
    subMenu.some((subItem) => location.pathname.startsWith(subItem.href));

  /**
   * Renders a submenu under a parent menu item.
   * @param {Array} subMenu - Array of submenu items.
   * @param {Number} parentIndex - Index of the parent menu item.
   */
  const renderSubMenu = (subMenu, parentIndex) => {
    return (
      <ul
        id={`submenu-${parentIndex}`}
        className={`submenu collapse nav flex-column ms-3 ${
          isSubMenuActive(subMenu) ? 'show' : '' // Ensure the submenu is visible if active
        }`}
      >
        {subMenu.map((subItem, subIndex) => (
          <li id={`submenu-item-${parentIndex}-${subIndex}`} className="nav-item" key={subIndex}>
            <a
              href={subItem.href}
              className={`nav-link text-white ${
                location.pathname === subItem.href ? 'active-link' : ''
              }`} // Highlight active link
            >
              {subItem.title}
            </a>
          </li>
        ))}
      </ul>
    );
  };

  return (
    <nav id="sidebar" className="col-md-3 col-lg-2 sidebar text-white d-flex flex-column vh-100">
      {/* Company Logo */}
      <img
        id="sidebar-logo"
        src={logo}
        alt="Company logo"
        className="logo img-fluid p-3 mt-4"
        style={{ maxHeight: '200px' }}
      />

      {/* Company Name */}
      <h5 id="sidebar-company-name" className="h5 text-center">Communication LTD</h5>
      <h6 id="sidebar-divider" className="h6 text-center">_______________________________</h6>

      {/* Navigation Menu */}
      <ul id="sidebar-menu" className="nav flex-column p-3">
        {menuItems.map((item, index) => (
          <li id={`menu-item-${index}`} className="nav-item mt-2" key={index}>
            {item.subMenu ? (
              <>
                <a
                  id={`menu-link-${index}`}
                  href={`#submenu-${index}`}
                  className="nav-link text-white"
                  data-bs-toggle="collapse"
                  role="button"
                  aria-expanded={isSubMenuActive(item.subMenu)} // Keep submenu expanded if active
                  aria-controls={`submenu-${index}`}
                >
                  {item.title}
                </a>
                {renderSubMenu(item.subMenu, index)}
              </>
            ) : (
              <a
                id={`menu-link-${index}`}
                href={item.href}
                className={`nav-link text-white ${
                  location.pathname === item.href ? 'active-link' : ''
                }`} // Highlight active link
              >
                {item.title}
              </a>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default Sidebar;
