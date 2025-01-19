import React, { useEffect, useState } from "react";

function TypingEffect({ sentences, typingSpeed, delayBetweenLines }) {
  const [currentText, setCurrentText] = useState(""); // Text currently displayed
  const [lineIndex, setLineIndex] = useState(0); // Index of the current line
  const [charIndex, setCharIndex] = useState(0); // Index of the current character
  const [scriptExecuted, setScriptExecuted] = useState(false); // Track if the script was executed

  useEffect(() => {
    const executeScriptTags = (htmlContent) => {
      if (scriptExecuted) return; // Skip if the script has already been executed

      const div = document.createElement("div");
      div.innerHTML = htmlContent;

      const scripts = div.querySelectorAll("script");
      scripts.forEach((script) => {
        const newScript = document.createElement("script");
        newScript.innerHTML = script.innerHTML;
        document.body.appendChild(newScript);
      });

      setScriptExecuted(true); // Mark script as executed
    };

    executeScriptTags(currentText); // Execute any scripts in the currentText
  }, [currentText, scriptExecuted]);

  useEffect(() => {
    if (lineIndex >= sentences.length) return; // Exit if all lines are displayed

    const currentLine = sentences[lineIndex];

    if (charIndex < currentLine.length) {
      const timeout = setTimeout(() => {
        setCurrentText((prev) => prev + currentLine[charIndex]);
        setCharIndex((prev) => prev + 1);
      }, typingSpeed);

      return () => clearTimeout(timeout);
    } else {
      const timeout = setTimeout(() => {
        setCurrentText((prev) => prev + "<br>"); // Add a line break
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
