import React from "react";
import { Composition } from "remotion";
import {
  FableStorybookShorts,
  type FableStorybookShortsProps,
} from "./components/FableStorybookShorts";

export const Root: React.FC = () => {
  const defaultScenes = [
    {
      scene_id: "SCENE_01_KANCIL_APEL",
      timeStart: 0.0,
      timeEnd: 4.86,
      videoSrc: "broll/broll_1.mp4",
      imageSrc: "images/scene1_kancil_apel.jpg",
      description: "Kancil Ciko memegang belahan apel emas di tanah berlumut senja",
    },
    {
      scene_id: "SCENE_02_POHON_KENARI",
      timeStart: 4.86,
      timeEnd: 16.34,
      videoSrc: "broll/broll_2.mp4",
      imageSrc: "images/scene2_pohon_kenari.jpg",
      description: "Pohon kenari raksasa berongga hangat dengan lentera menyala",
    },
    {
      scene_id: "SCENE_03_PENGAKUAN_CIKO",
      timeStart: 16.34,
      timeEnd: 36.11,
      videoSrc: "broll/broll_3.mp4",
      imageSrc: "images/scene3_pengakuan_ciko.jpg",
      description: "Kakek Beruang berlutut lembut menyambut pengakuan jujur Ciko",
    },
    {
      scene_id: "SCENE_04_PELUKAN_HANGAT",
      timeStart: 36.11,
      timeEnd: 51.01,
      videoSrc: "broll/broll_4.mp4",
      imageSrc: "images/scene4_pelukan_hangat.jpg",
      description: "Pelukan hangat penuh kasih & daun-daun emas berguguran",
    },
    {
      scene_id: "SCENE_05_MALAM_BINTANG",
      timeStart: 51.01,
      timeEnd: 56.1,
      videoSrc: "broll/broll_5.mp4",
      imageSrc: "images/scene5_malam_bintang.jpg",
      description: "Langit malam berhias bintang, bulan sabit & kunang-kunang",
    },
  ];

  const defaultProps: FableStorybookShortsProps = {
    channelName: "Dita Dongeng & Fabel",
    channelHandle: "@ditafable",
    title: "Kancil Ciko & Apel Emas yang Terbelah",
    script:
      "Jangan sembunyikan apel yang sudah terbelah itu di balik semak! Kancil kecil bernama Ciko gemetar saat apel emas kesayangan kakek beruang pecah karena kecerobohannya. Ia sempat ingin lari dan berbohong. Tapi di dalam dadanya, detak jantungnya berbisik bahwa rasa bersalah itu terasa jauh lebih berat daripada hukuman apapun. Dengan napas pelan, Ciko menghampiri kakek beruang dan berkata jujur: 'Kakek, Ciko minta maaf, Ciko yang memecahkannya.' Kakek beruang tersenyum hangat, lalu memeluknya erat: 'Mengakui kesalahan butuh keberanian ksatria sejati, Ciko.' Karena kejujuran selalu membasuh rasa takut menjadi rasa tenang. Maka malam ini sebelum tidur, ingatlah selalu pesan ini...",
    audioFile: "voiceover_day_001.mp3",
    bgmFile: "bgm/bgm_bedtime_lullaby.mp3",
    sfxSparkleFile: "sfx/magic_sparkle.mp3",
    scenes: defaultScenes,
    showSafeZoneGuide: false,
  };

  return (
    <>
      {/* 1. Production Master: 1080x1920 (Native 9:16 High-Res) */}
      <Composition
        id="FableStorybookShorts"
        component={FableStorybookShorts as React.ComponentType}
        durationInFrames={1346} // 56.09s @ 24fps
        fps={24}
        width={1080}
        height={1920}
        defaultProps={defaultProps}
      />

      {/* 2. Fast Render / Preview Edition: 720x1280 (Fast CI/CD) */}
      <Composition
        id="FableStorybookShorts720p"
        component={FableStorybookShorts as React.ComponentType}
        durationInFrames={1346}
        fps={24}
        width={720}
        height={1280}
        defaultProps={defaultProps}
      />
    </>
  );
};
