import fs from "fs";
import path from "path";
import { execSync } from "child_process";

async function runDailyPipeline() {
  const args = process.argv.slice(2);
  const rootDir = process.cwd();
  const stateDir = path.join(rootDir, "state");
  fs.mkdirSync(stateDir, { recursive: true });
  const statePath = path.join(stateDir, "campaign_state.json");

  let dayNum: number = 1;
  let explicitDay = false;
  let forceRender = false;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--day" && args[i + 1]) {
      dayNum = parseInt(args[i + 1], 10);
      explicitDay = true;
    }
    if (args[i] === "--force") {
      forceRender = true;
    }
  }

  // 1. Resolve Target Day from Campaign State if not provided via CLI
  let campaignState: any = {};
  if (fs.existsSync(statePath)) {
    try {
      campaignState = JSON.parse(fs.readFileSync(statePath, "utf-8"));
    } catch (e) {
      campaignState = {};
    }
  }

  if (!explicitDay) {
    const totalPub = campaignState.total_published || 0;
    const isDay1Pub = campaignState.pipeline_status?.day_001 === "PUBLISHED";
    if (totalPub === 0 || !isDay1Pub) {
      dayNum = 1;
    } else {
      dayNum = campaignState.next_day || (campaignState.active_day ? campaignState.active_day + 1 : 2);
    }
  }

  // Resolve cycle day (1 to 182) for perpetual multi-month / multi-year execution
  const cycleDay = ((dayNum - 1) % 182) + 1;
  const cycleDayStr = String(cycleDay).padStart(3, "0");
  const dayStr = String(dayNum).padStart(3, "0");
  const packetPath = `curriculum/content_packet_day_${cycleDayStr}.json`;
  const outputVideo = `output/dita_fable_day_${dayStr}_master.mp4`;
  const compressedVideo = `output/dita_fable_day_${dayStr}_compressed.mp4`;

  console.log(`=======================================================`);
  console.log(`[DITA-04 Pipeline] Executing Daily Fable Pipeline: Day ${dayNum} (Cycle Day ${cycleDay})`);
  console.log(`[DITA-04 Pipeline] Packet: ${packetPath}`);
  console.log(`[DITA-04 Pipeline] State: Active Day ${campaignState.active_day || 1}, Next Day ${dayNum}`);
  console.log(`=======================================================`);

  if (!fs.existsSync(packetPath)) {
    console.error(`[DITA-04 Pipeline] Error: Content packet not found: ${packetPath}`);
    process.exit(1);
  }

  // 2. Ensure Voiceover Audio Exists
  const audioFile = `public/voiceover_day_${cycleDayStr}.mp3`;
  const metaPath = `public/audio_meta_day_${cycleDayStr}.json`;
  if (!fs.existsSync(audioFile) || fs.statSync(audioFile).size < 1000) {
    console.log(`
--- Step 1: Synthesizing Warm Bedtime Voiceover ---`);
    execSync(`python scripts/generate-voiceover.py "${packetPath}" "${audioFile}" "${metaPath}"`, {
      stdio: "inherit",
    });
  } else {
    console.log(`
--- Step 1: Pre-synthesized Voiceover Verified (${audioFile}) ---`);
  }

  // 2.5 Ensure Storyboard Plates & Manifest Exist
  const manifestFile = `public/broll_manifest_day_${cycleDayStr}.json`;
  if (!fs.existsSync(manifestFile)) {
    console.log(`
--- Step 1.5: Generating Storyboard Plates & Manifest ---`);
    try {
      execSync(`python scripts/build_day_plates.py --day ${cycleDay}`, {
        stdio: "inherit",
      });
    } catch (e) {
      console.warn("[DITA-04 Pipeline] Warning generating day plates:", e);
    }
  }

  // 3. Render Master Video via Remotion (or reuse pre-rendered master)
  fs.mkdirSync(path.join(rootDir, "output"), { recursive: true });
  if (fs.existsSync(outputVideo) && !forceRender && fs.statSync(outputVideo).size > 5000000) {
    console.log(`
--- Step 2: Master Deliverable already exists, skipping re-render: ${outputVideo} ---`);
  } else {
    console.log(`
--- Step 2: Rendering 1080x1920 Remotion Video ---`);
    execSync(`npx tsx scripts/render-video.ts --packet "${packetPath}" --out "${outputVideo}" --comp FableStorybookShorts`, {
      stdio: "inherit",
    });
  }

  // 4. Video Compression for Social Distribution (Zernio & YouTube Fast Upload)
  console.log(`
--- Step 3: Preparing Encoded Video Deliverable ---`);
  if (!fs.existsSync(compressedVideo) || fs.statSync(compressedVideo).size < 1000) {
    console.log(`[DITA-04 Pipeline] Compressing video for social delivery (< 10 MB)...`);
    try {
      execSync(
        `ffmpeg -y -i "${outputVideo}" -vf "scale=720:1280" -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k -ar 44100 "${compressedVideo}"`,
        { stdio: "inherit" }
      );
    } catch (e) {
      console.warn("[DITA-04 Pipeline] Video compression warning:", e);
    }
  }
  const finalVideoToPublish = fs.existsSync(compressedVideo) ? compressedVideo : outputVideo;

  // 5. Multi-Platform Publication (YouTube Shorts, TikTok, Instagram)
  console.log(`
--- Step 4: Tri-Platform Publication ---`);
  execSync(`python scripts/publish_video.py --day ${dayNum} --video "${finalVideoToPublish}"`, {
    stdio: "inherit",
  });

  // 6. Advance Campaign State Atomically
  campaignState.channel = "@ditafable";
  campaignState.active_day = dayNum;
  campaignState.next_day = dayNum + 1;
  campaignState.total_published = (campaignState.total_published || 0) + 1;
  campaignState.last_updated = new Date().toISOString();
  campaignState.pipeline_status = campaignState.pipeline_status || {};
  campaignState.pipeline_status[`day_${dayStr}`] = "PUBLISHED";
  campaignState.last_published_video = finalVideoToPublish;

  fs.writeFileSync(statePath, JSON.stringify(campaignState, null, 2), "utf-8");
  console.log(`
[DITA-04 Pipeline] Updated campaign_state.json: active_day=${campaignState.active_day}, next_day=${campaignState.next_day}`);

  console.log(`
=======================================================`);
  console.log(`[DITA-04 Pipeline] Day ${dayNum} Pipeline Completed Successfully!`);
  console.log(`[DITA-04 Pipeline] Master Deliverable: ${path.resolve(outputVideo)}`);
  console.log(`=======================================================`);
}

runDailyPipeline().catch((e) => {
  console.error("[DITA-04 Pipeline] Execution failed:", e);
  process.exit(1);
});
