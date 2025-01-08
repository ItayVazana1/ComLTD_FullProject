import React, { useEffect, useState } from 'react';

function TypingEffect({ userName, typingSpeed = 5000, delayBetweenLines = 200 }) {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const textArray = [
    `Hello, ${userName} !`,
    'It\'s great to see you again!']


  const [currentText, setCurrentText] = useState(''); // הטקסט שמוצג
  const [lineIndex, setLineIndex] = useState(0); // אינדקס השורה
  const [charIndex, setCharIndex] = useState(0); // אינדקס התו

  useEffect(() => {
    if (lineIndex >= textArray.length) return;

    const currentLine = textArray[lineIndex];

    if (charIndex < currentLine.length) {

      const timeout = setTimeout(() => {
        setCurrentText((prev) => prev + currentLine[charIndex]);
        setCharIndex((prev) => prev + 1);
      }, typingSpeed);
      return () => clearTimeout(timeout);
    } else {

      const timeout = setTimeout(() => {
        setCurrentText((prev) => prev + '<br>'); 
        setCharIndex(0);
        setLineIndex((prev) => prev + 1);
      }, delayBetweenLines);
      return () => clearTimeout(timeout);
    }
  }, [charIndex, lineIndex, textArray, typingSpeed, delayBetweenLines]);

  return (
    <div
      id="typing-text"
      dangerouslySetInnerHTML={{ __html: currentText }}
    />
  );
}

export default TypingEffect;
