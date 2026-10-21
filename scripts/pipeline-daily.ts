import fs from "fs";
import path from "path";
import { execSync } from "child_process";

async function runDailyPipeline() {
  const args = process.argv.slice(2);
  let dayNum = 1;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--day" && args[i + 1]) dayNum = parseInt(args[i + 1], 10);
  }

  const dayStr = String(dayNum).padStart(3, "0");
  const packetPath = `curriculum/content_packet_day_${dayStr}.json`;
  const outputVideo = `output/dita_fable_day_${dayStr}_master.mp4`;

  console.log(`=======================================================`);
  console.log(`[DITA-04 Pipeline] Executing Daily Fable Pipeline: Day ${dayNum}`);
  console.log(`[DITA-04 Pipeline] Packet: ${packetPath}`);
  console.log(`=======================================================`);

  if (!fs.existsSync(packetPath)) {
    console.error(`[DITA-04 Pipeline] Error: Packet not found: ${packetPath}`);
    process.exit(1);
  }

  // 1. Generate Voiceover TTS
  console.log(`\n--- Step 1: Synthesizing Warm Bedtime Voiceover ---`);
  execSync(`python scripts/generate-voiceover.py "${packetPath}" "public/voiceover_day_${dayStr}.mp3" "public/audio_meta.json"`, {
    stdio: "inherit",
  });

  // 2. Fetch B-Roll & Visual Plates
  console.log(`\n--- Step 2: Preparing 3D Storybook Visual Assets ---`);
  execSync(`python scripts/fetch-broll.py`, {
    stdio: "inherit",
  });

  // 3. Render Master Video via Remotion Engine
  console.log(`\n--- Step 3: Rendering 1080x1920 Remotion Video ---`);
  execSync(`npx tsx scripts/render-video.ts --packet "${packetPath}" --out "${outputVideo}" --comp FableStorybookShorts`, {
    stdio: "inherit",
  });

  // 4. Optimize Video for Social Distribution (H.264 Fast)
  console.log(`\n--- Step 4: Optimizing Video Encoding ---`);
  const compressedVideo = `output/dita_fable_day_${dayStr}_compressed.mp4`;
  try {
    execSync(`ffmpeg -y -i "${outputVideo}" -vf "scale=1080:1920" -c:v libx264 -crf 22 -preset fast -c:a aac -b:a 128k -ar 44100 "${compressedVideo}"`, {
      stdio: "inherit",
    });
    console.log(`[DITA-04 Pipeline] Compressed deliverable ready: ${compressedVideo}`);
  } catch (err: any) {
    console.warn(`[DITA-04 Pipeline] Compression fallback to master video: ${err.message}`);
  }

  // 5. Multi-Platform Publication (YouTube Shorts, TikTok, Instagram)
  console.log(`\n--- Step 5: Multi-Platform Publication ---`);
  const finalPublishVideo = fs.existsSync(compressedVideo) ? compressedVideo : outputVideo;
  execSync(`python scripts/publish_video.py --day ${dayNum} --video "${finalPublishVideo}"`, {
    stdio: "inherit",
  });

  // 6. Update Campaign State
  const stateDir = path.resolve("state");
  fs.mkdirSync(stateDir, recursive: true);
  const statePath = path.join(stateDir, "campaign_state.json");
  let state: any = {
    channel_id: "DITA-04",
    handle: "@ditafable",
    active_day: dayNum,
    next_day: dayNum + 1,
    pipeline_status: {},
    distribution: {
      tiktok: { username: "ditafable", account_id: "6ad8acf3c24aa78753a651ef", status: "CONNECTED" },
      instagram: { username: "ditafable", account_id: "6ad8acd9aad76462b1a71e23", status: "CONNECTED" },
      youtube: { username: "@ditafable", channel_id: "UCxEyHnK7ru1XM7Ri0EWywLw", status: "CONNECTED" }
    }
  };

  if (fs.existsSync(statePath)) {
    try {
      state = JSON.parse(fs.readFileSync(statePath, "utf-8"));
    } catch (e) {
      // use default
    }
  }

  state.active_day = Math.max(state.active_day || 1, dayNum);
  state.next_day = state.active_day + 1;
  state.last_rendered_day = dayNum;
  state.last_rendered_file = outputVideo;
  state.pipeline_status = state.pipeline_status || {};
  state.pipeline_status[`day_${dayStr}`] = "PUBLISHED";
  state.updated_at = new Date().toISOString();

  fs.writeFileSync(statePath, JSON.stringify(state, null, 2), "utf-8");

  console.log(`\n=======================================================`);
  console.log(`[DITA-04 Pipeline] Day ${dayNum} Pipeline Completed Successfully!`);
  console.log(`[DITA-04 Pipeline] Master Deliverable: ${path.resolve(outputVideo)}`);
  console.log(`[DITA-04 Pipeline] Campaign State: active_day=${state.active_day}, next_day=${state.next_day}`);
  console.log(`=======================================================`);
}

runDailyPipeline().catch((e) => {
  console.error("[DITA-04 Pipeline] Execution failed:", e);
  process.exit(1);
});
