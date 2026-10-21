import React from "react";

export const StorybookVignette: React.FC = () => {
  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        zIndex: 20,
      }}
    >
      {/* 1. Deep Fairytale Twilight Vignette */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(180deg, rgba(3, 7, 12, 0.78) 0%, rgba(3, 7, 12, 0.18) 25%, rgba(3, 7, 12, 0.22) 70%, rgba(3, 7, 12, 0.88) 100%)",
        }}
      />

      {/* 2. Horizontal Soft Edge Darkening */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(90deg, rgba(3, 7, 12, 0.45) 0%, transparent 18%, transparent 82%, rgba(3, 7, 12, 0.45) 100%)",
        }}
      />

      {/* 3. Golden Corner Filigree Accents (SVG) */}
      {/* Top Left */}
      <svg
        style={{ position: "absolute", top: 30, left: 30, width: 80, height: 80, opacity: 0.75 }}
        viewBox="0 0 100 100"
      >
        <path
          d="M10,90 Q10,10 90,10 M20,90 Q20,20 90,20 M10,10 L35,10 M10,10 L10,35"
          stroke="#d4af37"
          strokeWidth="3.5"
          fill="none"
          strokeLinecap="round"
        />
        <circle cx="15" cy="15" r="4" fill="#fef08a" />
      </svg>

      {/* Top Right */}
      <svg
        style={{
          position: "absolute",
          top: 30,
          right: 30,
          width: 80,
          height: 80,
          transform: "scaleX(-1)",
          opacity: 0.75,
        }}
        viewBox="0 0 100 100"
      >
        <path
          d="M10,90 Q10,10 90,10 M20,90 Q20,20 90,20 M10,10 L35,10 M10,10 L10,35"
          stroke="#d4af37"
          strokeWidth="3.5"
          fill="none"
          strokeLinecap="round"
        />
        <circle cx="15" cy="15" r="4" fill="#fef08a" />
      </svg>

      {/* Bottom Left */}
      <svg
        style={{
          position: "absolute",
          bottom: 30,
          left: 30,
          width: 80,
          height: 80,
          transform: "scaleY(-1)",
          opacity: 0.75,
        }}
        viewBox="0 0 100 100"
      >
        <path
          d="M10,90 Q10,10 90,10 M20,90 Q20,20 90,20 M10,10 L35,10 M10,10 L10,35"
          stroke="#d4af37"
          strokeWidth="3.5"
          fill="none"
          strokeLinecap="round"
        />
        <circle cx="15" cy="15" r="4" fill="#fef08a" />
      </svg>

      {/* Bottom Right */}
      <svg
        style={{
          position: "absolute",
          bottom: 30,
          right: 30,
          width: 80,
          height: 80,
          transform: "scale(-1, -1)",
          opacity: 0.75,
        }}
        viewBox="0 0 100 100"
      >
        <path
          d="M10,90 Q10,10 90,10 M20,90 Q20,20 90,20 M10,10 L35,10 M10,10 L10,35"
          stroke="#d4af37"
          strokeWidth="3.5"
          fill="none"
          strokeLinecap="round"
        />
        <circle cx="15" cy="15" r="4" fill="#fef08a" />
      </svg>
    </div>
  );
};
