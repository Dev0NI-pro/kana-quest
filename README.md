# 🌸 Kana Quest

> **Learn Japanese through adventure!** — A pixel-art RPG where you explore a Japanese elementary school and master hiragana, katakana, and JLPT N5 kanji.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green?logo=pygame)
![License](https://img.shields.io/badge/License-MIT-pink)
![Language](https://img.shields.io/badge/Language-EN%20%7C%20FR-sakura)

---

## 🎮 Gameplay

Walk around **Sakura Elementary School** as a chibi student. Talk to teachers and classmates to unlock Japanese lessons — each conversation triggers a quiz mini-game. Complete all lessons in a grade to unlock the next classroom!

```
CP (Grade 1) → CE1 (Grade 2) → CE2 (Grade 3) → CM1 (Grade 4) → CM2 (Grades 5-6)
```

### Controls

| Key | Action |
|-----|--------|
| `↑ ↓ ← →` | Move your character |
| `SPACE` | Talk to teachers & students |
| `ESC` | Back to menu |
| `1 2 3 4` | Pick quiz answer |
| `Click` | Navigate menus / answer quiz |

---

## 📚 Content

### Grade 1 — CP
- Japanese greetings (おはよう, こんにちは…)
- Hiragana vowels (あいうえお)
- Numbers 1–10 (いち、に、さん…)
- Colors (あか、あお、きいろ…)

### Grade 2 — CE1
- Hiragana TA/NA/HA rows
- School supplies (えんぴつ、ほん、かばん…)
- Days of the week (げつようび、かようび…)
- Family members (おとうさん、おかあさん…)

### Grade 3 — CE2
- Katakana basics (ア、イ、ウ、エ、オ…)
- Japanese food (ごはん、すし、ラーメン…)
- Telling time (いまなんじですか？)
- Body parts (あたま、め、はな…)

### Grade 4 — CM1
- Katakana loanwords (テレビ、スマホ、コンピュータ…)
- Adjectives (おおきい、ちいさい、やさしい…)
- Basic verbs (たべます、いきます、みます…)

### Grade 5 — CM2
- JLPT N5 Kanji — Numbers & Time (一、二、三、年、月、日…)
- Basic Japanese sentences (〜はなんですか？)

### Grade 6 — CM2
- JLPT N5 Kanji — Nature & People (山、川、木、森、人…)
- Grammar — て-form (食べてください、食べています…)

---

## 🏫 School Map

```
┌─────────────────────────────────────┐
│       CM2 Classroom (Grades 5-6)    │  🔒 Unlock after CM1
├──────────────┬──────────────────────┤
│ CE2 (Gr. 3)  │     CM1 (Gr. 4)      │  🔒 Unlock after CP+CE1
├──────────────┼──────────────────────┤
│  CP (Gr. 1)  │     CE1 (Gr. 2)      │  ✅ Start here
├──────────────┴──────────────────────┤
│            Entrance Hall            │
│          👩‍🏫 Principal NPC           │
└─────────────────────────────────────┘
```

---

## ✨ Features

- 🎨 **Pastel Japanese aesthetic** — sakura pink, soft lavender, warm wood tones
- 👧 **Cute chibi characters** — big round heads, rosy cheeks, school uniforms (randoseru backpack!)
- 📈 **Grade progression** — locked doors open as you complete each level
- 📖 **4-page tutorial** — teaches controls and game mechanics on first launch
- 💬 **Typewriter dialog** — NPCs speak with animated text bubbles
- 🌸 **Falling sakura petals** — animated menus
- 🌐 **Bilingual** — full English and French UI support
- ❤️ **Lives system** — 3 hearts per quiz, score tracking, star rating

---

## 🚀 Installation

### Requirements
- Python 3.10+
- pygame 2.x

```bash
# Clone the repository
git clone https://github.com/Dev0NI-pro/kana-quest.git
cd kana-quest

# Install dependency
pip install pygame

# Run the game
python main.py
```

---

## 📁 Project Structure

```
kana-quest/
├── main.py               # Entry point & game loop
├── settings.py           # Colors, tile IDs, font loader
├── data/
│   ├── lessons.py        # All Japanese content (grades 1-6)
│   ├── hiragana.py       # Hiragana table
│   ├── katakana.py       # Katakana table
│   └── kanji_n5.py       # JLPT N5 kanji
├── game/
│   ├── player.py         # Chibi player sprite & movement
│   ├── npc.py            # NPC sprites (grade-based sizing)
│   └── tilemap.py        # School map + tile rendering
└── states/
    ├── lang_select.py    # Language selection screen
    ├── tutorial.py       # 4-page tutorial
    ├── overworld.py      # Walking world + grade progression
    ├── minigame.py       # Quiz mini-game
    └── result.py         # Lesson results screen
```

---

## 🗺️ Roadmap

- [ ] Sound effects & background music
- [ ] Hiragana writing practice (stroke order)
- [ ] More sentence patterns & grammar
- [ ] Save / load progress
- [ ] Middle school & high school levels
- [ ] Vocabulary flashcard mode

---

## 🤝 Contributing

Pull requests welcome! If you want to add more vocabulary, fix a translation, or improve the sprites — go for it.

---

## 📄 License

MIT — free to use, modify and share.

---

*Made with ❤️ and pygame — がんばって！*
