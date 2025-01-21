import React from 'react';
import '../assets/styles/Global.css'; // Global styles
import '../assets/styles/About.css'; // Styles specific to the About page

/**
 * OurStory Component:
 * Renders a section that tells the company's story, including its vision, mission, and journey.
 * Highlights the purpose and achievements of the company in an engaging manner.
 */
function OurStory() {
  return (
    <section id="our-story-section" className="our-story">
      {/* Section Title */}
      <h1 id="our-story-title">Our Story</h1>

      {/* Story Paragraph */}
      <p id="our-story-text">
        {/* Introduction to the company */}
        Founded in 2010, <b>Communication LTD</b> was born from a simple yet ambitious vision:<br />
        to make staying connected easier for everyone, no matter where life takes them.
        <br />
        {/* The origin of the idea */}
        Our journey began when our founder, a seasoned traveler,<br />experienced the challenges
        of finding affordable and reliable internet while abroad.
        <br />
        {/* Bridging the connectivity gap */}
        Inspired by this gap, they assembled a team of tech enthusiasts and telecommunications<br />
        experts to create a company that bridges the connectivity divide for people at home and on the go.
        <br />
        {/* Growth and current status */}
        Since our inception, we’ve grown into a trusted provider of internet solutions,<br />offering tailored
        data packages for both local and international use.
        <br />
        {/* Vision and mission */}
        At <b>Communication LTD</b>, we believe in connecting people, ideas, and opportunities<br />because in today’s
        world, staying connected means staying empowered.
      </p>
    </section>
  );
}

export default OurStory;
