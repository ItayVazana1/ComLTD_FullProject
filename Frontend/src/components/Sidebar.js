import React from 'react';
import '../assets/styles/sidebar.css'
import logo from '../assets/images/logo.png'

const menuItems = [
  { title: 'Home', href: '/', style: { fontWeight: 'bold', backgroundColor: 'var(--color-dark-forest)' } },
  { title: 'About', href: '/about' },
  { title: 'Data Plans', href: '/data-plans' },
  {
    title: 'Customers',
    subMenu: [
      { title: 'New Customer', href: '#' },
      { title: 'Search', href: '#' },
    ],
  },
  {
    title: 'Account',
    subMenu: [
      { title: 'My Profile', href: '#' },
      { title: 'Change My Password', href: '#' },
    ],
  },
  { title: 'Contact Us', href: '/contact' },
];

function Sidebar() {
  const renderSubMenu = (subMenu, parentIndex) => {
    return (
      <ul className="collapse nav flex-column ms-3" id={`submenu-${parentIndex}`}>
        {subMenu.map((subItem, subIndex) => (
          <li className="nav-item" key={subIndex}>
            <a href={subItem.href} className="nav-link text-white">
              {subItem.title}
            </a>
          </li>
        ))}
      </ul>
    );
  };

  return (
    <nav id="sidebar" className="col-md-3 col-lg-2 text-white d-flex flex-column vh-100">
      <img
        src={logo}
        alt="Company logo"
        className="logo img-fluid p-3 mt-4"
        style={{ maxHeight: '250px' }}
      />
      <h6 className="h6 text-center">Communication LTD</h6>
      <h6 className="h6 text-center">_______________________________</h6>
      <ul className="nav flex-column p-3">
        {menuItems.map((item, index) => (
          <li className="nav-item mt-2" key={index}>
            {item.subMenu ? (
              <>
                <a
                  href={`#submenu-${index}`}
                  className="nav-link text-white"
                  data-bs-toggle="collapse"
                  role="button"
                  aria-expanded="false"
                  aria-controls={`submenu-${index}`}
                >
                  {item.title}
                </a>
                {renderSubMenu(item.subMenu, index)}
              </>
            ) : (
              <a href={item.href} className="nav-link text-white" style={item.style || {}}>
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
