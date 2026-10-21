import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Video,
} from "remotion";
import { FairyDustParticles } from "./FairyDustParticles";
import { StorybookVignette } from "./StorybookVignette";
import { SafeZoneOverlay } from "./SafeZoneOverlay";

export interface FableSceneItem {
  scene_id?: string;
  timeStart: number;
  timeEnd: number;
  videoSrc?: string;
  imageSrc?: string;
  query?: string;
  description?: string;
}

export interface TimedSubtitleChunk {
  start: number;
  end: number;
  text: string;
}

export interface FableStorybookShortsProps {
  channelName?: string;
  channelHandle?: string;
  title?: string;
  script?: string;
  timedSubtitles?: TimedSubtitleChunk[];
  audioFile?: string;
  bgmFile?: string;
  sfxSparkleFile?: string;
  scenes?: FableSceneItem[];
  showSafeZoneGuide?: boolean;
}

const HIGHLIGHT_WORDS = [
  "kancil",
  "ciko",
  "apel",
  "emas",
  "kletuk",
  "aduh",
  "terbelah",
  "terkejut",
  "cemas",
  "deg-deg-deg",
  "berdebar",
  "sembunyi",
  "pesan",
  "ibu",
  "hebat",
  "berani",
  "jujur",
  "pondok",
  "tok",
  "terbuka",
  "senyum",
  "teduh",
  "maafkan",
  "memecahkan",
  "berlutut",
  "memeluk",
  "sayang",
  "berharga",
  "lega",
  "damai",
  "nyenyak",
  "selimutmu",
  "tidur",
  "mimpi",
  "indah",
];

const SceneVisual: React.FC<{
  scene: FableSceneItem;
  durationInFrames: number;
  isFirst: boolean;
}> = ({ scene, durationInFrames, isFirst }) => {
  const relFrame = useCurrentFrame();

  // Smooth Ken Burns slow zoom (1.02 -> 1.14)
  const scale = interpolate(relFrame, [0, durationInFrames], [1.02, 1.14], {
    extrapolateRight: "clamp",
  });

  // Slow horizontal drift (-10px -> +10px)
  const panX = interpolate(
    relFrame,
    [0, durationInFrames],
    [isFirst ? 0 : -12, 12],
    { extrapolateRight: "clamp" }
  );

  // Crossfade opacity
  const fade = 14;
  const opacity = interpolate(
    relFrame,
    [0, fade, durationInFrames - fade, durationInFrames],
    [isFirst ? 0.3 : 0.4, 1.0, 1.0, 0.4],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          transform: `scale(${scale}) translate(${panX}px, 0px)`,
          opacity,
        }}
      >
        {scene.videoSrc ? (
          <Video
            src={staticFile(scene.videoSrc)}
            muted
            loop
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        ) : scene.imageSrc ? (
          <Img
            src={staticFile(scene.imageSrc)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        ) : (
          <div
            style={{
              width: "100%",
              height: "100%",
              background:
                "radial-gradient(circle at 50% 35%, #182e21 0%, #0c1710 60%, #060b08 100%)",
            }}
          />
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const FableStorybookShorts: React.FC<FableStorybookShortsProps> = ({
  channelName = "Dita Dongeng & Fabel",
  channelHandle = "@ditafable",
  title = "Kancil Ciko & Apel Emas yang Terbelah",
  script = "",
  timedSubtitles = [],
  audioFile = "voiceover_day_001.mp3",
  bgmFile = "bgm/bgm_bedtime_lullaby.mp3",
  sfxSparkleFile = "sfx/magic_sparkle.mp3",
  scenes = [],
  showSafeZoneGuide = false,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const currentTimeSec = frame / fps;

  // Global Progress for top bar
  const totalProgress = frame / durationInFrames;

  // Top Hook Headline Banner: Visible during first 4.0 seconds, then fades out smoothly
  const hookBannerOpacity = interpolate(
    frame,
    [0, fps * 3.2, fps * 4.2],
    [1, 1, 0],
    { extrapolateRight: "clamp" }
  );

  // Hook Banner Scale Spring
  const hookScale = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  // Moral Plaque Spotlight (Visible around 74s to 88s - during Grandfather Bear's advice)
  const moralPlaqueOpacity = interpolate(
    currentTimeSec,
    [73.5, 75.0, 87.0, 88.5],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Outro Bedtime Card (Last 8.0 seconds)
  const outroStartTimeSec = (durationInFrames / fps) - 8.0;
  const outroOpacity = interpolate(
    currentTimeSec,
    [outroStartTimeSec, outroStartTimeSec + 1.2],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Find active timed subtitle chunk
  let currentSubtitle = "";
  let subRelFrame = 0;

  if (timedSubtitles && timedSubtitles.length > 0) {
    const active = timedSubtitles.find(
      (s) => currentTimeSec >= s.start && currentTimeSec <= s.end + 0.12
    );
    if (active) {
      currentSubtitle = active.text;
      const subStartFrame = Math.round(active.start * fps);
      subRelFrame = Math.max(0, frame - subStartFrame);
    }
  } else if (script) {
    // Fallback: chunk script text evenly
    const words = script.split(/\s+/).filter(Boolean);
    const chunkSize = 4;
    const chunks: string[] = [];
    for (let i = 0; i < words.length; i += chunkSize) {
      chunks.push(words.slice(i, i + chunkSize).join(" "));
    }
    const chunkDurFrames = Math.max(
      1,
      Math.floor(durationInFrames / Math.max(chunks.length, 1))
    );
    const chunkIdx = Math.min(
      chunks.length - 1,
      Math.floor(frame / chunkDurFrames)
    );
    currentSubtitle = chunks[chunkIdx] || "";
    subRelFrame = frame % chunkDurFrames;
  }

  // Kinetic spring scale for active subtitle chunk
  const subScale = spring({
    frame: subRelFrame,
    fps,
    config: { damping: 13, stiffness: 150 },
  });

  // Render text with highlighted keywords
  const renderHighlightedWords = (text: string) => {
    const tokens = text.split(/(\s+)/);
    return tokens.map((token, idx) => {
      const clean = token.toLowerCase().replace(/[^a-z0-9]/g, "");
      const isMatch = HIGHLIGHT_WORDS.some((kw) => clean === kw || clean.startsWith(kw));

      if (isMatch) {
        return (
          <span
            key={idx}
            style={{
              color: "#fcd34d",
              fontWeight: 900,
              textShadow: "0 0 18px rgba(252, 211, 77, 0.85)",
            }}
          >
            {token}
          </span>
        );
      }
      return <span key={idx}>{token}</span>;
    });
  };

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#03060a",
        color: "#ffffff",
        fontFamily: "'Georgia', 'Palatino Linotype', 'Cinzel', serif",
        overflow: "hidden",
      }}
    >
      {/* 1. Voiceover Audio */}
      {audioFile && <Audio src={staticFile(audioFile)} />}

      {/* 2. Soft Bedtime Lullaby BGM (ducked so voice is crystal clear) */}
      {bgmFile && <Audio src={staticFile(bgmFile)} volume={0.12} />}

      {/* 3. Magic Sparkle Chimes SFX (Intro and Outro) */}
      {sfxSparkleFile && (
        <>
          <Sequence from={0} durationInFrames={Math.round(fps * 3.5)}>
            <Audio src={staticFile(sfxSparkleFile)} volume={0.25} />
          </Sequence>
          <Sequence
            from={Math.max(0, durationInFrames - Math.round(fps * 4.5))}
            durationInFrames={Math.round(fps * 4.0)}
          >
            <Audio src={staticFile(sfxSparkleFile)} volume={0.22} />
          </Sequence>
        </>
      )}

      {/* 4. Visual Layer (3D Pixar Woodland / B-Roll / Plates with Ken Burns) */}
      <AbsoluteFill>
        {scenes && scenes.length > 0 ? (
          scenes.map((sc, idx) => {
            const startFrame = Math.round((sc.timeStart || 0) * fps);
            const endFrame = Math.round(
              (sc.timeEnd || durationInFrames / fps) * fps
            );
            const duration = Math.max(1, endFrame - startFrame);

            return (
              <Sequence
                key={sc.scene_id || idx}
                from={startFrame}
                durationInFrames={duration}
              >
                <SceneVisual
                  scene={sc}
                  durationInFrames={duration}
                  isFirst={idx === 0}
                />
              </Sequence>
            );
          })
        ) : (
          <div
            style={{
              width: "100%",
              height: "100%",
              background:
                "radial-gradient(circle at 50% 30%, #13241b 0%, #081119 55%, #03060a 100%)",
            }}
          />
        )}
      </AbsoluteFill>

      {/* 5. Fairy Dust Floating Particles (Luminous Magic Sparkles) */}
      <FairyDustParticles count={48} width={1080} height={1920} />

      {/* 6. Storybook Vignette & Gold Corner Filigree */}
      <StorybookVignette />

      {/* 7. Top Progress Indicator (Subtle Fairytale Gold to Amber) */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: `${totalProgress * 100}%`,
          height: 8,
          background: "linear-gradient(90deg, #f59e0b, #fef08a, #10b981)",
          zIndex: 80,
          boxShadow: "0 0 14px rgba(245, 158, 11, 0.7)",
        }}
      />

      {/* 8. Top Channel Branding Badge (Safe Zone Y: 155px) */}
      <div
        style={{
          position: "absolute",
          top: 155,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 50,
        }}
      >
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 12,
            background: "rgba(10, 20, 15, 0.88)",
            border: "2px solid rgba(212, 175, 55, 0.65)",
            borderRadius: 9999,
            padding: "10px 28px",
            boxShadow:
              "0 8px 32px rgba(0, 0, 0, 0.6), 0 0 20px rgba(245, 158, 11, 0.2)",
            backdropFilter: "blur(12px)",
          }}
        >
          <span style={{ fontSize: 24, filter: "drop-shadow(0 0 6px #f59e0b)" }}>
            🌙
          </span>
          <span
            style={{
              fontSize: 18,
              fontWeight: 800,
              letterSpacing: 2.2,
              textTransform: "uppercase",
              color: "#fef08a",
            }}
          >
            {channelName}
          </span>
          <span
            style={{
              fontSize: 16,
              color: "rgba(255, 255, 255, 0.75)",
              fontWeight: 600,
            }}
          >
            {channelHandle}
          </span>
        </div>
      </div>

      {/* 9. Opening Hook Headline Card (First 4.0s - Compact, Elegant & High Safe Zone) */}
      {hookBannerOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            top: 215,
            left: 50,
            right: 50,
            textAlign: "center",
            opacity: hookBannerOpacity,
            transform: `scale(${hookScale})`,
            zIndex: 60,
          }}
        >
          <div
            style={{
              display: "inline-block",
              padding: "7px 22px",
              backgroundColor: "rgba(180, 83, 9, 0.95)",
              border: "2px solid #fef08a",
              color: "#ffffff",
              fontSize: 18,
              fontWeight: 800,
              borderRadius: 10,
              textTransform: "uppercase",
              letterSpacing: 2.0,
              boxShadow: "0 6px 20px rgba(0, 0, 0, 0.6)",
              marginBottom: 10,
            }}
          >
            🍎 KISAH PENGANTAR TIDUR
          </div>
          <div
            style={{
              fontSize: 36,
              fontWeight: 800,
              lineHeight: 1.25,
              color: "#ffffff",
              textShadow: "0 4px 18px rgba(0, 0, 0, 0.95)",
              padding: "0 20px",
              maxWidth: 780,
              margin: "0 auto",
            }}
          >
            {title.includes("(") ? title.split("(")[0].trim() : title}
          </div>
        </div>
      )}

      {/* 10. Moral Plaque Feature (Highlight in Scene 4 - detik 36 - 49) */}
      {moralPlaqueOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            top: 360,
            left: 60,
            right: 60,
            opacity: moralPlaqueOpacity,
            zIndex: 65,
            display: "flex",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              background:
                "linear-gradient(135deg, rgba(254, 243, 199, 0.95) 0%, rgba(253, 230, 138, 0.88) 100%)",
              border: "3px solid #b45309",
              borderRadius: 22,
              padding: "24px 34px",
              boxShadow:
                "0 18px 45px rgba(0, 0, 0, 0.75), 0 0 28px rgba(245, 158, 11, 0.4)",
              textAlign: "center",
              maxWidth: 880,
            }}
          >
            <div
              style={{
                fontSize: 26,
                fontStyle: "italic",
                fontWeight: 800,
                color: "#451a03",
                lineHeight: 1.4,
                marginBottom: 10,
              }}
            >
              "Kejujuran Ciko jauh lebih berharga daripada sepuluh apel emas."
            </div>
            <div
              style={{
                fontSize: 18,
                fontWeight: 900,
                letterSpacing: 2.0,
                textTransform: "uppercase",
                color: "#92400e",
              }}
            >
              — Kakek Beruang yang Baik Hati 🍯❤️
            </div>
          </div>
        </div>
      )}

      {/* 11. Kinetic Subtitle Container (Strict Safe Zone Y: 1380px - 1560px) */}
      {currentSubtitle && (
        <div
          style={{
            position: "absolute",
            bottom: 250,
            left: 50,
            right: 50,
            minHeight: 140,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 70,
          }}
        >
          <div
            style={{
              padding: "20px 38px",
              backgroundColor: "rgba(8, 22, 14, 0.94)",
              borderRadius: 24,
              border: "3px solid #d4af37",
              boxShadow:
                "0 16px 45px rgba(0, 0, 0, 0.85), 0 0 28px rgba(212, 175, 55, 0.45)",
              backdropFilter: "blur(14px)",
              transform: `scale(${subScale})`,
              textAlign: "center",
              maxWidth: "88%",
            }}
          >
            <span
              style={{
                fontFamily: "'Georgia', 'Palatino Linotype', serif",
                fontSize: 38,
                fontWeight: 800,
                lineHeight: 1.35,
                color: "#ffffff",
                textShadow: "0 3px 12px rgba(0, 0, 0, 0.95)",
              }}
            >
              {renderHighlightedWords(currentSubtitle)}
            </span>
          </div>
        </div>
      )}

      {/* 12. Outro Bedtime Card & Seamless Loop Bridge (Last 5.0 seconds) */}
      {outroOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            bottom: 120,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            opacity: outroOpacity,
            zIndex: 75,
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 12,
              background: "rgba(254, 240, 138, 0.15)",
              border: "2px solid rgba(254, 240, 138, 0.45)",
              borderRadius: 9999,
              padding: "12px 32px",
              boxShadow: "0 6px 25px rgba(0, 0, 0, 0.6)",
              backdropFilter: "blur(10px)",
              color: "#fef08a",
              fontSize: 20,
              fontWeight: 800,
              letterSpacing: 1.0,
            }}
          >
            <span>✨ Tarik Selimutmu & Selamat Tidur Nyenyak • Simpan Cerita Ini ✨</span>
          </div>
        </div>
      )}

      {/* 13. Optional Safe Zone Overlay for QA */}
      <SafeZoneOverlay visible={showSafeZoneGuide} />
    </AbsoluteFill>
  );
};
