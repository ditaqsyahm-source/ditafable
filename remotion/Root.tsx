import React from "react";
import { Composition } from "remotion";
import {
  FableStorybookShorts,
  type FableStorybookShortsProps,
} from "./components/FableStorybookShorts";

export const Root: React.FC = () => {
  const defaultScenes = [
    {
      scene_id: "SCENE_01_HUTAN_RIANG",
      timeStart: 0.0,
      timeEnd: 10.5,
      videoSrc: undefined,
      imageSrc: "images/scene1_ciko_hutan_apel.jpg",
      description: "Ciko si kancil kecil melompat riang di padang rumput dekat pohon apel emas",
    },
    {
      scene_id: "SCENE_02_APEL_TERBELAH",
      timeStart: 10.5,
      timeEnd: 24.0,
      videoSrc: undefined,
      imageSrc: "images/scene2_apel_emas_terbelah.jpg",
      description: "Kletuk! Apel emas bercahaya terbelah di atas lumut, Ciko tertegun cemas",
    },
    {
      scene_id: "SCENE_03_JALAN_SETAPAK",
      timeStart: 24.0,
      timeEnd: 50.0,
      videoSrc: undefined,
      imageSrc: "images/scene3_jalan_pondok_kabut.jpg",
      description: "Ciko berjalan pelan di jalan setapak hutan berkabut menuju pondok Kakek Beruang",
    },
    {
      scene_id: "SCENE_04_PENGAKUAN_JUJUR",
      timeStart: 50.0,
      timeEnd: 70.0,
      videoSrc: undefined,
      imageSrc: "images/scene4_pintu_pengakuan_jujur.jpg",
      description: "Pintu kayu terbuka, Ciko menatap ke atas dan berbisik meminta maaf dengan tulus",
    },
    {
      scene_id: "SCENE_05_PELUKAN_KASIH",
      timeStart: 70.0,
      timeEnd: 90.5,
      videoSrc: undefined,
      imageSrc: "images/scene5_kakek_beruang_memeluk.jpg",
      description: "Kakek Beruang berlutut dan memeluk Ciko penuh kehangatan serta partikel cinta berkilau",
    },
    {
      scene_id: "SCENE_06_MALAM_PENGANTAR_TIDUR",
      timeStart: 90.5,
      timeEnd: 105.0,
      videoSrc: undefined,
      imageSrc: "images/scene6_malam_tidur_bintang.jpg",
      description: "Panorama hutan malam yang damai, bulan sabit keemasan, dan bintang berkelap-kelip pengantar tidur",
    },
  ];

  const defaultProps: FableStorybookShortsProps = {
    channelName: "Dita Dongeng & Fabel",
    channelHandle: "@ditafable",
    title: "Kancil Ciko & Apel Emas yang Terbelah",
    script:
      "Sore itu di Hutan Kenari yang sejuk, Ciko si kancil kecil melompat riang di dekat pohon apel emas milik Kakek Beruang. Tapi... kletuk! Aduh! Tanpa sengaja, kaki Ciko menyenggol dahan pohon. Sebuah apel emas yang ranum terjatuh dan terbelah dua di tanah. Ciko terkejut sekali. Telinganya turun karena cemas. Deg-deg-deg, jantung kecilnya berdebar kencang. Ciko sempat ingin sembunyi di balik semak. Tapi Ciko ingat pesan Ibu: anak hebat selalu berani jujur. Dengan langkah pelan, Ciko berjalan menuju pondok kayu Kakek Beruang. Tok, tok, tok! Pintu kayu pun terbuka. Kakek Beruang menyambutnya dengan senyum teduh. Ciko menunduk, lalu berbisik jujur: 'Kakek... maafkan Ciko ya. Ciko tidak sengaja memecahkan apel emas Kakek...' Mendengar itu, Kakek Beruang berlutut dan memeluk Ciko erat: 'Tidak apa-apa, Ciko sayang. Apel bisa dipetik lagi, tapi kejujuran Ciko jauh lebih berharga daripada sepuluh apel emas.' Hati Ciko pun terasa sangat lega dan damai. Nah adik-adik manis, jujur itu membuat tidur kita nyenyak. Sekarang, tarik selimutmu, pejamkan matamu ya... selamat tidur, dan mimpi indah.",
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
        durationInFrames={2508} // 104.5s @ 24fps
        fps={24}
        width={1080}
        height={1920}
        defaultProps={defaultProps}
      />

      {/* 2. Fast Render / Preview Edition: 720x1280 (Fast CI/CD) */}
      <Composition
        id="FableStorybookShorts720p"
        component={FableStorybookShorts as React.ComponentType}
        durationInFrames={2508} // 104.5s @ 24fps
        fps={24}
        width={720}
        height={1280}
        defaultProps={defaultProps}
      />
    </>
  );
};
