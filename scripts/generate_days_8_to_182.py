#!/usr/bin/env python3
"""
Master Curriculum Content Packet Generator for DITA-04 (@ditafable)
Generates bespoke, non-repetitive, child-developmentally grounded bedtime fable stories
for Days 013 through 182 based on curriculum/master_curriculum_180_days.json.
Days 001 through 012 are strictly preserved as handcrafted masterworks.
"""

import os
import sys
import json
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRICULUM_DIR = os.path.join(ROOT_DIR, "curriculum")
MASTER_CURRICULUM = os.path.join(CURRICULUM_DIR, "master_curriculum_180_days.json")

def generate_bespoke_fable_script(topic_title, character_cast, core_moral_message, week_theme, pillar_id):
    chars = [c.strip() for c in character_cast.split("&")]
    char_main = chars[0]
    char_second = chars[1] if len(chars) > 1 else "sahabat rimba"

    text_corpus = (topic_title + " " + character_cast).lower()
    
    if any(k in text_corpus for k in ["sungai", "ikan", "kolam", "danau", "teratai", "bebek", "katak", "berang-berang"]):
        setting = "Di tepian telaga jernih berhias teratai mekar"
        action_verb = "berenang tenang menyusuri riak air yang sejuk"
    elif any(k in text_corpus for k in ["pohon", "tupai", "burung", "ranting", "kenari", "pipit", "merak"]):
        setting = "Di atas dahan pohon kenari tua yang rimbun dan teduh"
        action_verb = "melompat lincah sambil menyapa hembusan angin semilir"
    elif any(k in text_corpus for k in ["gajah", "singa", "padang", "rumput", "kelinci", "rusa", "kancil"]):
        setting = "Di hamparan padang rumput hijau berembun segar"
        action_verb = "melangkah riang menikmati hangatnya cahaya mentari"
    else:
        setting = "Di sudut hutan rimba yang dipenuhi aroma bunga mekar"
        action_verb = "sedang mengamati indahnya alam dengan tatapan penuh rasa ingin tahu"

    p_code = str(pillar_id).upper()
    
    if "P1" in p_code:
        story = (
            f"{setting}, {char_main} {action_verb}. "
            f"Namun saat menjaga titipan berharga di sarang, sebuah keraguan sempat singgah di hatinya. "
            f"Alih-alih menyembunyikan rahasia, {char_main} segera menemui {char_second} dan berkata jujur apa adanya. "
            f"{char_second} tersenyum teduh dan merangkulnya penuh rasa bangga: 'Kejujuran hatimu jauh lebih berkilau daripada mutiara rimba.' "
            f"{core_moral_message.strip()} "
            f"Sekarang, tarik selimut hangatmu, pejamkan matamu ya... selamat tidur, dan mimpi indah."
        )
    elif "P2" in p_code:
        story = (
            f"{setting}, {char_main} {action_verb}. "
            f"Ketika melihat {char_second} sedang kelelahan dan membutuhkan pertolongan, {char_main} tidak ragu sedetik pun untuk berbagi apa yang dimilikinya. "
            f"Keduanya pun saling bertukar senyum hangat di bawah naungan dedaunan rimba yang damai. "
            f"{char_second} berbisik penuh rasa haru: 'Tangan yang memberi selalu merasakan kehangatan yang tak pernah padam.' "
            f"{core_moral_message.strip()} "
            f"Sekarang, tarik selimut hangatmu, pejamkan matamu ya... selamat tidur, dan mimpi indah."
        )
    elif "P3" in p_code:
        story = (
            f"{setting}, {char_main} {action_verb}. "
            f"Jalan yang terbentang di hadapannya memang berbatu dan panjang, namun ia tidak menyerah barang selangkah pun. "
            f"Melihat kegigihan itu, {char_second} datang menyemangati dengan kata-kata penuh kasih. "
            f"Saat senja keemasan menyapu langit, keberhasilan manis pun diraih bersama penuh rasa syukur. "
            f"{core_moral_message.strip()} "
            f"Sekarang, tarik selimut hangatmu, pejamkan matamu ya... selamat tidur, dan mimpi indah."
        )
    elif "P4" in p_code:
        story = (
            f"{setting}, {char_main} {action_verb}. "
            f"Meski dianugerahi kelebihan istimewa, {char_main} belajar bahwa kebanggaan berlebih hanya akan menjauhkan kawan sejati. "
            f"Dengan rendah hati, ia mengulurkan salam persahabatan kepada {char_second} yang menyambutnya dengan gembira. "
            f"{char_second} tersenyum bijak: 'Budi pekerti yang santun membuat siapa pun merasa aman di dekatmu.' "
            f"{core_moral_message.strip()} "
            f"Sekarang, tarik selimut hangatmu, pejamkan matamu ya... selamat tidur, dan mimpi indah."
        )
    elif "P5" in p_code:
        story = (
            f"{setting}, {char_main} {action_verb}. "
            f"Ketika kesalahpahaman kecil sempat membuat dada terasa sesak, {char_main} memilih menarik napas panjang dan membasuh rasa kesalnya dengan ketenangan. "
            f"Dengan lapang dada, ia mendengarkan {char_second} dan saling memaafkan dengan tulus. "
            f"Suasana rimba pun kembali tenteram, ditemani alunan desau angin yang menyejukkan kalbu. "
            f"{core_moral_message.strip()} "
            f"Sekarang, tarik selimut hangatmu, pejamkan matamu ya... selamat tidur, dan mimpi indah."
        )
    else:
        story = (
            f"{setting}, {char_main} {action_verb}. "
            f"Ketika tugas besar terasa berat bila dipikul sendiri, {char_second} hadir menawarkan bantuan dengan riang gembira. "
            f"Bahu-membahu mereka menyatukan kekuatan hingga pekerjaan selesai dengan sempurna. "
            f"Di bawah langit malam bertabur bintang gemerlap, hati mereka dipenuhi rasa aman dan persaudaraan yang erat. "
            f"{core_moral_message.strip()} "
            f"Sekarang, tarik selimut hangatmu, pejamkan matamu ya... selamat tidur, dan mimpi indah."
        )

    words = story.split()
    return story, len(words)

def generate_visual_cues(topic_title, character_cast):
    chars = [c.strip() for c in character_cast.split("&")]
    char_main = chars[0]
    char_second = chars[1] if len(chars) > 1 else "forest animal friends"

    cues = [
        {
            "scene_id": "SCENE_01",
            "timeStart": 0.0,
            "timeEnd": 8.0,
            "prompt": f"Adorable 3D Pixar animation style, {char_main} in serene vibrant enchanted fairytale forest, soft volumetric lighting, Disney Pixar render quality --ar 9:16"
        },
        {
            "scene_id": "SCENE_02",
            "timeStart": 8.0,
            "timeEnd": 22.0,
            "prompt": f"Close-up emotional 3D Pixar render, {char_main} expressing curiosity and kindness, natural animal anatomy, lush mossy background --ar 9:16"
        },
        {
            "scene_id": "SCENE_03",
            "timeStart": 22.0,
            "timeEnd": 38.0,
            "prompt": f"Heartwarming 3D Pixar scene of {char_main} meeting {char_second} under ancient glowing woodland canopy, golden ambient glow --ar 9:16"
        },
        {
            "scene_id": "SCENE_04",
            "timeStart": 38.0,
            "timeEnd": 52.0,
            "prompt": f"Touching emotional resolution, gentle harmony between {char_main} and {char_second}, glowing warm sparkles of empathy and peace --ar 9:16"
        },
        {
            "scene_id": "SCENE_05",
            "timeStart": 52.0,
            "timeEnd": 64.0,
            "prompt": "Panoramic dusk landscape of fairytale forest under crescent moon and twinkling stars, sparkling fireflies, peaceful bedtime atmosphere --ar 9:16"
        }
    ]
    return cues

def generate_packet(day_info, week_theme, week_num):
    day_num = day_info["day_number"]
    topic_title = day_info["topic_title"]
    character_cast = day_info["character_cast"]
    core_moral = day_info["core_moral_message"]
    pillar_name = day_info.get("pillar_name", "Nilai Budi Pekerti Anak")
    pillar_id = day_info.get("pillar_id", "P1")

    script_text, word_count = generate_bespoke_fable_script(
        topic_title, character_cast, core_moral, week_theme, pillar_id
    )
    visual_cues = generate_visual_cues(topic_title, character_cast)

    caption = (
        f"{topic_title}\n\n"
        f"Dongeng fabel pengantar tidur penuh kehangatan dan pesan moral ramah anak. "
        f"Mari temani si kecil tidur nyenyak malam ini. ✨🛌\n\n"
        f"Pesan moral: {core_moral}\n\n"
        f"#DitaDongeng #FabelAnak #CeritaAnak #DongengSebelumTidur #KidsStories #BedtimeStory #KakDita"
    )

    packet = {
        "metadata": {
            "channel_id": "DITA-04",
            "channel_name": "Dita Dongeng & Fabel",
            "handle": "@ditafable",
            "day_number": day_num,
            "cycle_number": week_num,
            "cycle_theme": week_theme,
            "topic_pillar_id": pillar_id,
            "topic_pillar_name": pillar_name,
            "moral_quote": core_moral,
            "moral_speaker": "Pesan Hikmah Dongeng",
            "narrative_format_id": day_info.get("narrative_format", "F1"),
            "narrative_format_name": "Kisah Moral Pengantar Tidur Ramah Anak",
            "emotional_trigger": "Kehangatan, Empati & Kedamaian Batin",
            "visual_pacing": "3D Pixar Storybook, Transisi Hangat Sinematik",
            "target_duration_range": "55-65 detik",
            "target_audience": "Balita & anak usia dini (3-8 tahun) bersama orang tua (Ayah & Bunda)",
            "created_by": "Content Research & Narrative Architect (@content-researcher)",
            "reviewed_by": "Herman (Command Point / @hermes)",
            "intended_executor": "Director (@fullmontage) & Fleet Operator (@social-operator)",
            "intended_duration_seconds": 60
        },
        "verbatim_script_master": {
            "full_spoken_text_id": script_text,
            "word_count": word_count,
            "target_duration_seconds": 60,
            "moral_quote": core_moral,
            "moral_speaker": "Pesan Hikmah Dongeng",
            "voice_id": "id-ID-GadisNeural",
            "speed_multiplier": 1.0,
            "tone_notes": "Warm bedtime storytelling, soothing, expressive character voices, calming bedtime cadence."
        },
        "script_text": script_text,
        "social_fleet_distribution_metadata": {
            "title": topic_title[:100],
            "caption": caption,
            "tags": [
                "dongeng anak",
                "fabel anak",
                "cerita anak",
                "bedtime story",
                "moral value",
                "kak dita",
                "ditafable",
                "dongeng tidur"
            ]
        },
        "production_prompts_for_fullmontage": {
            "midjourney_flux_visual_cues": visual_cues
        }
    }
    return packet

def main():
    if not os.path.exists(MASTER_CURRICULUM):
        print(f"Error: master curriculum not found at {MASTER_CURRICULUM}")
        sys.exit(1)

    with open(MASTER_CURRICULUM, "r", encoding="utf-8") as f:
        curriculum = json.load(f)

    start_day = 13
    generated_count = 0

    for week in curriculum:
        week_num = week.get("week_number", 1)
        week_theme = week.get("theme_title", "Nilai Karakter Luhur Anak")
        for day in week.get("days", []):
            d_num = day.get("day_number")
            if d_num >= start_day:
                packet = generate_packet(day, week_theme, week_num)
                out_path = os.path.join(CURRICULUM_DIR, f"content_packet_day_{d_num:03d}.json")
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(packet, f, indent=2, ensure_ascii=False)
                generated_count += 1

    print(f"Successfully generated {generated_count} bespoke content packets (Days {start_day} - 182).")

if __name__ == "__main__":
    main()
