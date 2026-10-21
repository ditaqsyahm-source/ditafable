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

  // 4. Update Campaign State
  const stateDir = path.resolve("state");
  fs.mkdirSync(stateDir, recursive: true);
  const statePath = path.join(stateDir, "campaign_state.json");
  const state = {
    channel_id: "DITA-04",
    handle: "@ditafable",
    last_rendered_day: dayNum,
    last_rendered_file: outputVideo,
    updated_at: new Date().toISOString(),
  };
  fs.writeFileSync(statePath, JSON.stringify(state, null, 2), "utf-8");

  console.log(`\n=======================================================`);
  console.log(`[DITA-04 Pipeline] Day ${dayNum} Pipeline Completed Successfully!`);
  console.log(`[DITA-04 Pipeline] Master Deliverable: ${path.resolve(outputVideo)}`);
  console.log(`=======================================================`);
}

runDailyPipeline().catch((e) => {
  console.error("[DITA-04 Pipeline] Execution failed:", e);
  process.exit(1);
});
