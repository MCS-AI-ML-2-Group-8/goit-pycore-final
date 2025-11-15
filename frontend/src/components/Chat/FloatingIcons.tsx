import React, { useState } from "react";
import "./FloatingIcons.css";

const imageUrl = "/logo.png";

interface IconStyle {
  left: string;
  width: string;
  height: string;
  animationDelay: string;
  animationDuration: string;
  backgroundImage: string;
  rotateAnimation?: string;
}

const generateIcons = () => {
  const numIcons = 15;
  const horizontalPadding = 5; // 5% padding on each side
  const spawnWidth = 100 - horizontalPadding * 2; // Effective width for spawning icons
  const segmentWidth = spawnWidth / numIcons;

  return Array.from({ length: numIcons }).map((_, index) => {
    const size = Math.random() * 60 + 40; // 40px to 100px

    // Calculate position within the padded area to avoid edges
    const baseLeftPosition = horizontalPadding + index * segmentWidth;
    const randomOffset = (Math.random() - 0.5) * segmentWidth;
    const leftPosition = baseLeftPosition + randomOffset;

    return {
      left: `${leftPosition}%`,
      width: `${size}px`,
      height: `${size}px`,
      animationDelay: `${Math.random() * 15}s`,
      animationDuration: `${Math.random() * 10 + 15}s`, // 15s to 25s
      backgroundImage: `url(${imageUrl})`,
    };
  });
};

const FloatingIcons: React.FC = () => {
  const [icons] = useState<IconStyle[]>(generateIcons);

  return (
    <div className="floating-icons-container">
      {icons.map((style, index) => (
        <div key={index} className="icon" style={style} />
      ))}
    </div>
  );
};

export default FloatingIcons;
