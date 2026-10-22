import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";

async function main() {
  const args = process.argv.slice(2);
  let packetPath = "curriculum/content_packet_day_001.json";
  let outputPath = "output/dita_fable_day_001_master.mp4";
  let compId = "FableStorybookShorts"; // Default 1080x1920
  let extractFrames = true;
  let frameRange: [number, number] | undefined = undefined;
  let useImages = false;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--packet" && args[i + 1]) packetPath = args[i + 1];
    if (args[i] === "--out" && args[i + 1]) outputPath = args[i + 1];
    if (args[i] === "--comp" && args[i + 1]) compId = args[i + 1];
    if (args[i] === "--no-frames") extractFrames = false;
    if (args[i] === "--use-images") useImages = true;
    if (args[i] === "--frames" && args[i + 1]) {
      const parts = args[i + 1].split("-").map((p) => parseInt(p, 10));
      if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
        frameRange = [parts[0], parts[1]];
      }
    }
  }

  const baseDir = path.resolve(".");
  const resolvedPacket = path.resolve(packetPath);
  if (!fs.existsSync(resolvedPacket)) {
    console.error(`[Remotion Engine] Error: Packet file not found: ${resolvedPacket}`);
    process.exit(1);
  }

  const packet = JSON.parse(fs.readFileSync(resolvedPacket, "utf-8"));
  const audioMetaPath = path.resolve("public/audio_meta.json");
  const brollManifestPath = path.resolve("public/broll_manifest.json");

  let durationInFrames = 1346; // ~56.1s @ 24fps
  let timedSubtitles = [];

  if (fs.existsSync(audioMetaPath)) {
    try {
      const audioMeta = JSON.parse(fs.readFileSync(audioMetaPath, "utf-8"));
      if (audioMeta.duration_frames) {
        durationInFrames = audioMeta.duration_frames + 6; // +0.25s tail buffer
      }
      if (audioMeta.timed_subtitles) {
        timedSubtitles = audioMeta.timed_subtitles;
      }
    } catch (e) {
      console.warn("[Remotion Engine] Warning reading audio_meta.json:", e);
    }
  }

  let scenes = [];
  if (fs.existsSync(brollManifestPath)) {
    try {
      scenes = JSON.parse(fs.readFileSync(brollManifestPath, "utf-8"));
      if (useImages) {
        // Force imageSrc to render 3D Pixar storybook plates
        scenes = scenes.map((s: any) => ({ ...s, videoSrc: undefined }));
        console.log(`[Remotion Engine] Forced 3D Pixar image plates mode for high speed render`);
      }
      console.log(`[Remotion Engine] Loaded ${scenes.length} storybook scenes from manifest`);
    } catch (e) {
      console.warn("[Remotion Engine] Warning reading broll_manifest.json:", e);
    }
  }

  fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true });

  const inputProps = {
    channelName: packet.metadata?.channel_name || "Dita Dongeng & Fabel",
    channelHandle: packet.metadata?.handle || "@ditafable",
    title:
      packet.social_fleet_distribution_metadata?.title ||
      "Kancil Ciko & Apel Emas yang Terbelah",
    script:
      packet.verbatim_script_master?.full_spoken_text_id ||
      packet.script_text ||
      "",
    timedSubtitles,
    audioFile: "voiceover_day_001.mp3",
    bgmFile: "bgm/bgm_bedtime_lullaby.mp3",
    sfxSparkleFile: "sfx/magic_sparkle.mp3",
    scenes,
    showSafeZoneGuide: false,
  };

  console.log(`[Remotion Engine] Bundling Remotion composition from remotion/index.ts...`);
  const bundleLocation = await bundle({
    entryPoint: path.resolve("remotion/index.ts"),
    webpackOverride: (config) => config,
  });

  console.log(`[Remotion Engine] Selecting composition '${compId}'...`);
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: compId,
    inputProps,
  });

  const is1080p = compId.includes("1080") || composition.width === 1080;
  const width = is1080p ? 1080 : 720;
  const height = is1080p ? 1920 : 1280;

  // Detect Google Chrome or Microsoft Edge on Windows/Linux
  const possibleBrowsers = [
    process.env.REMOTION_BROWSER_EXECUTABLE,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
  ];

  let chromeExecutable: string | undefined = undefined;
  for (const b of possibleBrowsers) {
    if (b && fs.existsSync(b)) {
      chromeExecutable = b;
      break;
    }
  }

  const renderFramesCount = frameRange
    ? frameRange[1] - frameRange[0] + 1
    : durationInFrames;

  console.log(
    `[Remotion Engine] Rendering ${renderFramesCount} frames (${(
      renderFramesCount / 24
    ).toFixed(1)}s) at ${width}x${height} @24fps to ${outputPath}...`
  );
  if (frameRange) {
    console.log(`[Remotion Engine] Frame range: [${frameRange[0]} ... ${frameRange[1]}]`);
  }
  if (chromeExecutable) {
    console.log(`[Remotion Engine] Using browser: ${chromeExecutable}`);
  }

  const startTime = Date.now();
  await renderMedia({
    composition: {
      ...composition,
      durationInFrames,
      fps: 24,
      width,
      height,
    },
    serveUrl: bundleLocation,
    codec: "h264",
    imageFormat: "jpeg",
    jpegQuality: 75,
    crf: is1080p ? 22 : 24,
    frameRange,
    outputLocation: path.resolve(outputPath),
    inputProps,
    browserExecutable: chromeExecutable,
    chromiumOptions: (process.platform === "linux"
      ? {
          gl: "swiftshader",
          args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
        }
      : {
          gl: "angle",
          args: [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--use-gl=angle",
            "--use-angle=d3d11",
          ],
        }) as any,
    concurrency: 4,
    onProgress: ({ progress }) => {
      process.stdout.write(
        `\r[Remotion Engine] Render Progress: ${(progress * 100).toFixed(0)}%`
      );
    },
  });

  const elapsedSec = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\n[Remotion Engine] Render finished in ${elapsedSec}s -> ${outputPath}`);

  const stat = fs.statSync(outputPath);
  console.log(
    `[Remotion Engine] Final Output Size: ${(stat.size / (1024 * 1024)).toFixed(2)} MB`
  );

  // Extract Preview Thumbnail Frames
  if (extractFrames && fs.existsSync(outputPath)) {
    const framesDir = path.resolve("output/preview_frames");
    fs.mkdirSync(framesDir, { recursive: true });

    const keyMoments = [
      { name: "frame_01_ciko_hutan_apel.jpg", time: "00:00:05.000" },
      { name: "frame_02_apel_terbelah.jpg", time: "00:00:18.000" },
      { name: "frame_03_jalan_setapak_kabut.jpg", time: "00:00:38.000" },
      { name: "frame_04_pintu_pengakuan_jujur.jpg", time: "00:01:00.000" },
      { name: "frame_05_kakek_beruang_memeluk.jpg", time: "00:01:20.000" },
      { name: "frame_06_malam_tidur_bintang.jpg", time: "00:01:38.000" },
    ];

    console.log(`[Remotion Engine] Extracting ${keyMoments.length} preview frames...`);
    for (const km of keyMoments) {
      const outFrame = path.join(framesDir, km.name);
      try {
        execSync(
          `ffmpeg -y -ss ${km.time} -i "${path.resolve(outputPath)}" -vframes 1 -q:v 2 "${outFrame}"`,
          { stdio: "ignore" }
        );
        console.log(`  ✓ Saved: ${km.name}`);
      } catch (e) {
        console.warn(`  ✗ Failed extracting frame ${km.name}:`, e);
      }
    }
  }
}

main().catch((err) => {
  console.error("[Remotion Engine] Render failed with exception:", err);
  process.exit(1);
});
