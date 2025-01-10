import React from 'react';
import '../assets/styles/Global.css';
import '../assets/styles/About.css';

/**
 * OurStory Component:
 * Displays the story of the company with a title and a detailed paragraph.
 * - Highlights the company's vision and journey.
 */
function OurStory() {
  return (
    <section id="our-story-section" className="our-story">
      {/* Section Title */}
      <h1 id="our-story-title">Our Story</h1>

      {/* Story Paragraph */}
      <p id="our-story-text">
        Founded in 2010, <b>Communication LTD</b> was born from a simple yet ambitious vision:<br />
        to make staying connected easier for everyone, no matter where life takes them.
        <br />
        Our journey began when our founder, a seasoned traveler,<br />experienced the challenges
        of finding affordable and reliable internet while abroad.
        <br />
        Inspired by this gap, they assembled a team of tech enthusiasts and telecommunications<br />
        experts to create a company that bridges the connectivity divide for people at home and on the go.
        <br />
        Since our inception, we’ve grown into a trusted provider of internet solutions,<br />offering tailored
        data packages for both local and international use.
        <br />
        At <b>Communication LTD</b>, we believe in connecting people, ideas, and opportunities<br />because in today’s
        world, staying connected means staying empowered.
      </p>
    </section>
  );
}

export default OurStory;
