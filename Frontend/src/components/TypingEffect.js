import React, { useEffect, useState } from "react";

/**
 * TypingEffect Component:
 * Simulates a typing animation for an array of sentences.
 * Supports HTML rendering and executes any embedded <script> tags in the text.
 * 
 * @param {Array} sentences - An array of strings to display as a typing effect.
 * @param {number} typingSpeed - Speed of typing each character (in ms).
 * @param {number} delayBetweenLines - Delay between typing consecutive sentences (in ms).
 */
function TypingEffect({ sentences, typingSpeed, delayBetweenLines }) {
  const [currentText, setCurrentText] = useState(""); // Text currently being displayed
  const [lineIndex, setLineIndex] = useState(0); // Index of the current sentence being typed
  const [charIndex, setCharIndex] = useState(0); // Index of the current character being typed
  const [scriptExecuted, setScriptExecuted] = useState(false); // Track if embedded scripts have been executed

  /**
   * Effect to execute embedded <script> tags in the currentText.
   */
  useEffect(() => {
    const executeScriptTags = (htmlContent) => {
      if (scriptExecuted) return; // Prevent duplicate script execution

      // Parse HTML content for <script> tags
      const div = document.createElement("div");
      div.innerHTML = htmlContent;

      const scripts = div.querySelectorAll("script");
      scripts.forEach((script) => {
        const newScript = document.createElement("script");
        newScript.innerHTML = script.innerHTML;
        document.body.appendChild(newScript); // Append and execute script in the document
      });

      setScriptExecuted(true); // Mark scripts as executed
    };

    executeScriptTags(currentText); // Execute scripts in the current text
  }, [currentText, scriptExecuted]);

  /**
   * Effect to handle the typing animation logic.
   */
  useEffect(() => {
    if (lineIndex >= sentences.length) return; // Stop if all sentences have been displayed

    const currentLine = sentences[lineIndex]; // Current sentence being typed

    if (charIndex < currentLine.length) {
      // Type the next character
      const timeout = setTimeout(() => {
        setCurrentText((prev) => prev + currentLine[charIndex]); // Append the character
        setCharIndex((prev) => prev + 1); // Move to the next character
      }, typingSpeed);

      return () => clearTimeout(timeout); // Cleanup timeout
    } else {
      // Move to the next sentence after a delay
      const timeout = setTimeout(() => {
        setCurrentText((prev) => prev + "<br>"); // Add a line break
        setCharIndex(0); // Reset character index for the next sentence
        setLineIndex((prev) => prev + 1); // Move to the next sentence
      }, delayBetweenLines);

      return () => clearTimeout(timeout); // Cleanup timeout
    }
  }, [charIndex, lineIndex, sentences, typingSpeed, delayBetweenLines]);

  return (
    <div
      id="typing-text"
      dangerouslySetInnerHTML={{ __html: currentText }} // Render the current text with HTML content
    />
  );
}

export default TypingEffect;
