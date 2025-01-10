import React, { useEffect, useState } from 'react';

/**
 * TypingEffect Component:
 * Simulates a typing effect for an array of text lines.
 * - Displays each line character by character with a delay.
 * - Allows customizable typing speed and delay between lines.
 */
function TypingEffect({ sentences, typingSpeed, delayBetweenLines }) {
  const [currentText, setCurrentText] = useState(''); // Text currently displayed
  const [lineIndex, setLineIndex] = useState(0); // Index of the current line
  const [charIndex, setCharIndex] = useState(0); // Index of the current character

  useEffect(() => {
    if (lineIndex >= sentences.length) return; // Exit if all lines are displayed

    const currentLine = sentences[lineIndex];

    if (charIndex < currentLine.length) {
      // Typing each character
      const timeout = setTimeout(() => {
        setCurrentText((prev) => prev + currentLine[charIndex]);
        setCharIndex((prev) => prev + 1);
      }, typingSpeed);

      return () => clearTimeout(timeout);
    } else {
      // Move to the next line after delay
      const timeout = setTimeout(() => {
        setCurrentText((prev) => prev + '<br>'); // Add a line break
        setCharIndex(0);
        setLineIndex((prev) => prev + 1);
      }, delayBetweenLines);

      return () => clearTimeout(timeout);
    }
  }, [charIndex, lineIndex, sentences, typingSpeed, delayBetweenLines]);

  return (
    <div
      id="typing-text"
      dangerouslySetInnerHTML={{ __html: currentText }} // Render text with HTML
    />
  );
}

export default TypingEffect;
