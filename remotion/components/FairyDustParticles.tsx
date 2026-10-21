import React, { useMemo } from "react";
import { useCurrentFrame } from "remotion";

interface Particle {
  id: number;
  x: number;
  y: number;
  radius: number;
  baseAlpha: number;
  speedY: number;
  speedX: number;
  pulseSpeed: number;
  pulseOffset: number;
  color: string;
}

export const FairyDustParticles: React.FC<{
  count?: number;
  width?: number;
  height?: number;
}> = ({ count = 48, width = 1080, height = 1920 }) => {
  const frame = useCurrentFrame();

  const particles: Particle[] = useMemo(() => {
    const list: Particle[] = [];
    for (let i = 0; i < count; i++) {
      // Deterministic pseudorandom seed
      const pseudo = Math.sin(i * 997.3) * 10000;
      const r1 = pseudo - Math.floor(pseudo);
      const pseudo2 = Math.sin((i + 1) * 331.7) * 10000;
      const r2 = pseudo2 - Math.floor(pseudo2);

      list.push({
        id: i,
        x: r1 * width,
        y: r2 * height,
        radius: 4 + (i % 6) * 2.5,
        baseAlpha: 0.55 + (i % 4) * 0.15,
        speedY: -(0.8 + (i % 3) * 0.5),
        speedX: ((i % 5) - 2) * 0.35,
        pulseSpeed: 0.06 + (i % 3) * 0.03,
        pulseOffset: i * 0.65,
        color:
          i % 4 === 0
            ? "#fef08a" // Bright gold
            : i % 4 === 1
            ? "#f59e0b" // Warm amber
            : i % 4 === 2
            ? "#86efac" // Emerald fairy
            : "#ffffff", // Pure starlight
      });
    }
    return list;
  }, [count, width, height]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        zIndex: 35, // High z-index over background and vignette
        overflow: "hidden",
        mixBlendMode: "screen",
      }}
    >
      {particles.map((p) => {
        // Calculate dynamic position based on frame
        const currentY = (p.y + p.speedY * frame * 1.4) % height;
        const normY = currentY < 0 ? currentY + height : currentY;
        const currentX =
          p.x +
          p.speedX * frame +
          Math.sin(frame * 0.035 + p.pulseOffset) * 25;
        const currentAlpha =
          p.baseAlpha * (0.65 + 0.35 * Math.sin(frame * p.pulseSpeed + p.pulseOffset));

        return (
          <div
            key={p.id}
            style={{
              position: "absolute",
              left: currentX,
              top: normY,
              width: p.radius * 2,
              height: p.radius * 2,
              borderRadius: "50%",
              backgroundColor: p.color,
              opacity: Math.max(0.2, Math.min(1.0, currentAlpha)),
              boxShadow: `0 0 ${p.radius * 3}px ${p.color}, 0 0 ${p.radius * 6}px ${p.color}`,
              filter: `drop-shadow(0 0 8px ${p.color})`,
              transform: `scale(${0.9 + 0.35 * Math.sin(frame * p.pulseSpeed + p.pulseOffset)})`,
            }}
          />
        );
      })}
    </div>
  );
};
