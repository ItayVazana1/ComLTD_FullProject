import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import PlanCard from '../components/PlanCard';
import '../assets/styles/colors.css'
import '../assets/styles/main.css'
import '../assets/styles/DataPlans.css';
import p1 from '../assets/images/plan_1.png'
import p2 from '../assets/images/plan_2.png'
import p3 from '../assets/images/plan_3.png'
import p4 from '../assets/images/plan_4.png'



const plansData = [
  {
    title: 'Essential Plan',
    description:'',
    image: p1,
    details: [
      { label: 'Data Limit', value: '5GB' },
      { label: 'Price', value: '$10/month' },
      { label: 'Speed', value: 'Up to 20Mbps' },
    ],
    borderColor: '#533946',
  },
  {
    title: 'Streamer Lite',
    description:'',
    image: p2,
    details: [
      { label: 'Data Limit', value: '20GB' },
      { label: 'Price', value: '$25/month' },
      { label: 'Speed', value: 'Up to 50Mbps' },
    ],
    borderColor: '#2E9CA0',
  },
  {
    title: 'Unlimited Pro',
    description:'',
    image: p3,
    details: [
      { label: 'Data Limit', value: 'Unlimited (Fair Use: 100GB)' },
      { label: 'Price', value: '$40/month' },
      { label: 'Speed', value: 'Up to 100Mbps' },
    ],
    borderColor: '#0F2C33',
  },
  {
    title: 'Global Connect',
    description:'',
    image: p4,
    details: [
      { label: 'Data Limit', value: '300GB' },
      { label: 'Price', value: '$70/month' },
      { label: 'Speed', value: 'High-speed 5G' },
    ],
    borderColor: '#21616A',
  },
];

function DataPlans({ onLogout }) {
  return (
    <div className="data-plans-container">
      <Navbar onLogout={onLogout} />
      <div className="content d-flex">
        <Sidebar />
        <main className="col-md-9 col-lg-10 p-4">
          <h1>Our Data Plans</h1>
          <div className="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4">
            {plansData.map((plan, index) => (
              <div className="col" key={index}>
                <PlanCard {...plan} />
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}

export default DataPlans;
