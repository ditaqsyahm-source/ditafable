import React from "react";

export const SafeZoneOverlay: React.FC<{ visible?: boolean }> = ({ visible = false }) => {
  if (!visible) return null;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        zIndex: 999,
        border: "3px dashed rgba(239, 68, 68, 0.8)",
      }}
    >
      {/* Top Danger Zone (0 - 220px): Platform Navigation & Search */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 220,
          backgroundColor: "rgba(239, 68, 68, 0.25)",
          borderBottom: "2px solid #ef4444",
          color: "#fecaca",
          fontSize: 20,
          fontWeight: 700,
          padding: 12,
        }}
      >
        ⚠️ TOP DANGER ZONE (0 - 220px) — TikTok / Reels / Shorts UI Header
      </div>

      {/* Bottom Danger Zone (1550 - 1920px): Caption, Sound Ticker & Nav */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 370,
          backgroundColor: "rgba(239, 68, 68, 0.25)",
          borderTop: "2px solid #ef4444",
          color: "#fecaca",
          fontSize: 20,
          fontWeight: 700,
          padding: 12,
        }}
      >
        ⚠️ BOTTOM DANGER ZONE (1550 - 1920px) — Caption, Audio, Scrubber
      </div>

      {/* Right Danger Zone (940 - 1080px): Action Buttons */}
      <div
        style={{
          position: "absolute",
          top: 700,
          bottom: 400,
          right: 0,
          width: 140,
          backgroundColor: "rgba(239, 68, 68, 0.25)",
          borderLeft: "2px solid #ef4444",
          color: "#fecaca",
          fontSize: 16,
          fontWeight: 700,
          padding: 8,
          writingMode: "vertical-rl",
        }}
      >
        ⚠️ RIGHT BUTTONS (Like / Comment / Share)
      </div>

      {/* Safe Zone Center Highlight */}
      <div
        style={{
          position: "absolute",
          top: 240,
          bottom: 390,
          left: 70,
          right: 150,
          border: "2px solid #10b981",
          borderRadius: 16,
          pointerEvents: "none",
        }}
      >
        <span
          style={{
            position: "absolute",
            top: 10,
            left: 10,
            color: "#6ee7b7",
            fontSize: 18,
            fontWeight: 800,
          }}
        >
          ✓ SAFE ZONE AREA (Subtitles, Brand, Moral Card)
        </span>
      </div>
    </div>
  );
};
