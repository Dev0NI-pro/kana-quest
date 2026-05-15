# Content organized by school grade — real Japanese elementary school curriculum
# Each lesson: id, grade, subject, items list
# Each item: { "jp": str, "romaji": str, "en": str, "fr": str, "example_en": str, "example_fr": str }

GRADES = {

    1: {
        "name":    {"en": "1st Grade", "fr": "CP"},
        "lessons": [
            {
                "id": "greetings",
                "name": {"en": "Greetings", "fr": "Salutations"},
                "icon": "👋",
                "items": [
                    {"jp":"おはよう",       "romaji":"ohayou",          "en":"Good morning",     "fr":"Bonjour (matin)"},
                    {"jp":"おはようございます","romaji":"ohayou gozaimasu","en":"Good morning (polite)","fr":"Bonjour (poli)"},
                    {"jp":"こんにちは",      "romaji":"konnichiwa",      "en":"Hello / Good day",  "fr":"Bonjour (journée)"},
                    {"jp":"こんばんは",      "romaji":"konbanwa",        "en":"Good evening",      "fr":"Bonsoir"},
                    {"jp":"さようなら",      "romaji":"sayounara",       "en":"Goodbye",           "fr":"Au revoir"},
                    {"jp":"ありがとう",      "romaji":"arigatou",        "en":"Thank you",         "fr":"Merci"},
                    {"jp":"ごめんなさい",    "romaji":"gomen nasai",     "en":"I'm sorry",         "fr":"Pardon"},
                    {"jp":"はい",          "romaji":"hai",             "en":"Yes",               "fr":"Oui"},
                    {"jp":"いいえ",         "romaji":"iie",             "en":"No",                "fr":"Non"},
                    {"jp":"よろしくおねがいします","romaji":"yoroshiku onegaishimasu","en":"Nice to meet you","fr":"Ravi de vous rencontrer"},
                ],
            },
            {
                "id": "hiragana_vowels",
                "name": {"en": "Hiragana — Vowels", "fr": "Hiragana — Voyelles"},
                "icon": "あ",
                "items": [
                    {"jp":"あ","romaji":"a", "en":"a","fr":"a"},
                    {"jp":"い","romaji":"i", "en":"i","fr":"i"},
                    {"jp":"う","romaji":"u", "en":"u","fr":"ou"},
                    {"jp":"え","romaji":"e", "en":"e","fr":"é"},
                    {"jp":"お","romaji":"o", "en":"o","fr":"o"},
                ],
            },
            {
                "id": "hiragana_ka",
                "name": {"en": "Hiragana — KA row", "fr": "Hiragana — ligne KA"},
                "icon": "か",
                "items": [
                    {"jp":"か","romaji":"ka","en":"ka","fr":"ka"},
                    {"jp":"き","romaji":"ki","en":"ki","fr":"ki"},
                    {"jp":"く","romaji":"ku","en":"ku","fr":"kou"},
                    {"jp":"け","romaji":"ke","en":"ke","fr":"ké"},
                    {"jp":"こ","romaji":"ko","en":"ko","fr":"ko"},
                ],
            },
            {
                "id": "hiragana_sa",
                "name": {"en": "Hiragana — SA row", "fr": "Hiragana — ligne SA"},
                "icon": "さ",
                "items": [
                    {"jp":"さ","romaji":"sa", "en":"sa","fr":"sa"},
                    {"jp":"し","romaji":"shi","en":"shi","fr":"chi"},
                    {"jp":"す","romaji":"su", "en":"su","fr":"sou"},
                    {"jp":"せ","romaji":"se", "en":"se","fr":"sé"},
                    {"jp":"そ","romaji":"so", "en":"so","fr":"so"},
                ],
            },
            {
                "id": "numbers_1_10",
                "name": {"en": "Numbers 1–10", "fr": "Chiffres 1–10"},
                "icon": "１",
                "items": [
                    {"jp":"いち","romaji":"ichi","en":"one",  "fr":"un"},
                    {"jp":"に",  "romaji":"ni",  "en":"two",  "fr":"deux"},
                    {"jp":"さん","romaji":"san", "en":"three","fr":"trois"},
                    {"jp":"し/よん","romaji":"shi/yon","en":"four","fr":"quatre"},
                    {"jp":"ご",  "romaji":"go",  "en":"five", "fr":"cinq"},
                    {"jp":"ろく","romaji":"roku","en":"six",  "fr":"six"},
                    {"jp":"しち/なな","romaji":"shichi/nana","en":"seven","fr":"sept"},
                    {"jp":"はち","romaji":"hachi","en":"eight","fr":"huit"},
                    {"jp":"く/きゅう","romaji":"ku/kyuu","en":"nine","fr":"neuf"},
                    {"jp":"じゅう","romaji":"juu","en":"ten","fr":"dix"},
                ],
            },
            {
                "id": "colors",
                "name": {"en": "Colors", "fr": "Couleurs"},
                "icon": "🎨",
                "items": [
                    {"jp":"あか",  "romaji":"aka",   "en":"red",   "fr":"rouge"},
                    {"jp":"あお",  "romaji":"ao",    "en":"blue",  "fr":"bleu"},
                    {"jp":"きいろ","romaji":"kiiro",  "en":"yellow","fr":"jaune"},
                    {"jp":"しろ",  "romaji":"shiro", "en":"white", "fr":"blanc"},
                    {"jp":"くろ",  "romaji":"kuro",  "en":"black", "fr":"noir"},
                    {"jp":"みどり","romaji":"midori","en":"green", "fr":"vert"},
                    {"jp":"オレンジ","romaji":"orenji","en":"orange","fr":"orange"},
                    {"jp":"むらさき","romaji":"murasaki","en":"purple","fr":"violet"},
                ],
            },
        ],
    },

    2: {
        "name":    {"en": "2nd Grade", "fr": "CE1"},
        "lessons": [
            {
                "id": "hiragana_ta",
                "name": {"en": "Hiragana — TA/NA/HA rows", "fr": "Hiragana — lignes TA/NA/HA"},
                "icon": "た",
                "items": [
                    {"jp":"た","romaji":"ta", "en":"ta","fr":"ta"},
                    {"jp":"ち","romaji":"chi","en":"chi","fr":"tchi"},
                    {"jp":"つ","romaji":"tsu","en":"tsu","fr":"tsou"},
                    {"jp":"て","romaji":"te", "en":"te","fr":"té"},
                    {"jp":"と","romaji":"to", "en":"to","fr":"to"},
                    {"jp":"な","romaji":"na", "en":"na","fr":"na"},
                    {"jp":"に","romaji":"ni", "en":"ni","fr":"ni"},
                    {"jp":"ぬ","romaji":"nu", "en":"nu","fr":"nou"},
                    {"jp":"ね","romaji":"ne", "en":"ne","fr":"né"},
                    {"jp":"の","romaji":"no", "en":"no","fr":"no"},
                    {"jp":"は","romaji":"ha", "en":"ha","fr":"ha"},
                    {"jp":"ひ","romaji":"hi", "en":"hi","fr":"hi"},
                    {"jp":"ふ","romaji":"fu", "en":"fu","fr":"fou"},
                    {"jp":"へ","romaji":"he", "en":"he","fr":"hé"},
                    {"jp":"ほ","romaji":"ho", "en":"ho","fr":"ho"},
                ],
            },
            {
                "id": "school_items",
                "name": {"en": "School Items", "fr": "Fournitures scolaires"},
                "icon": "✏️",
                "items": [
                    {"jp":"えんぴつ","romaji":"enpitsu","en":"pencil",  "fr":"crayon"},
                    {"jp":"けしごむ","romaji":"keshigomu","en":"eraser","fr":"gomme"},
                    {"jp":"ほん",   "romaji":"hon",     "en":"book",    "fr":"livre"},
                    {"jp":"かばん", "romaji":"kaban",   "en":"bag",     "fr":"sac"},
                    {"jp":"つくえ", "romaji":"tsukue",  "en":"desk",    "fr":"bureau"},
                    {"jp":"いす",   "romaji":"isu",     "en":"chair",   "fr":"chaise"},
                    {"jp":"こくばん","romaji":"kokuban","en":"blackboard","fr":"tableau"},
                    {"jp":"ノート", "romaji":"nooto",   "en":"notebook","fr":"cahier"},
                    {"jp":"じょうぎ","romaji":"jougi",  "en":"ruler",   "fr":"règle"},
                    {"jp":"はさみ", "romaji":"hasami",  "en":"scissors","fr":"ciseaux"},
                ],
            },
            {
                "id": "days_of_week",
                "name": {"en": "Days of the Week", "fr": "Jours de la semaine"},
                "icon": "📅",
                "items": [
                    {"jp":"にちようび","romaji":"nichiyoubi","en":"Sunday",   "fr":"dimanche"},
                    {"jp":"げつようび","romaji":"getsuyoubi","en":"Monday",   "fr":"lundi"},
                    {"jp":"かようび",  "romaji":"kayoubi",   "en":"Tuesday",  "fr":"mardi"},
                    {"jp":"すいようび","romaji":"suiyoubi",  "en":"Wednesday","fr":"mercredi"},
                    {"jp":"もくようび","romaji":"mokuyoubi", "en":"Thursday", "fr":"jeudi"},
                    {"jp":"きんようび","romaji":"kin'youbi", "en":"Friday",   "fr":"vendredi"},
                    {"jp":"どようび",  "romaji":"doyoubi",   "en":"Saturday", "fr":"samedi"},
                ],
            },
            {
                "id": "family",
                "name": {"en": "Family", "fr": "Famille"},
                "icon": "👨‍👩‍👧",
                "items": [
                    {"jp":"おとうさん","romaji":"otousan","en":"father","fr":"père"},
                    {"jp":"おかあさん","romaji":"okaasan","en":"mother","fr":"mère"},
                    {"jp":"おにいさん","romaji":"oniisan","en":"older brother","fr":"grand frère"},
                    {"jp":"おねえさん","romaji":"oneesan","en":"older sister","fr":"grande sœur"},
                    {"jp":"おとうと",  "romaji":"otouto","en":"younger brother","fr":"petit frère"},
                    {"jp":"いもうと",  "romaji":"imouto","en":"younger sister","fr":"petite sœur"},
                    {"jp":"おじいさん","romaji":"ojiisan","en":"grandfather","fr":"grand-père"},
                    {"jp":"おばあさん","romaji":"obaasan","en":"grandmother","fr":"grand-mère"},
                ],
            },
        ],
    },

    3: {
        "name":    {"en": "3rd Grade", "fr": "CE2"},
        "lessons": [
            {
                "id": "katakana_basic",
                "name": {"en": "Katakana — Basics", "fr": "Katakana — Bases"},
                "icon": "ア",
                "items": [
                    {"jp":"ア","romaji":"a", "en":"a","fr":"a"},
                    {"jp":"イ","romaji":"i", "en":"i","fr":"i"},
                    {"jp":"ウ","romaji":"u", "en":"u","fr":"ou"},
                    {"jp":"エ","romaji":"e", "en":"e","fr":"é"},
                    {"jp":"オ","romaji":"o", "en":"o","fr":"o"},
                    {"jp":"カ","romaji":"ka","en":"ka","fr":"ka"},
                    {"jp":"キ","romaji":"ki","en":"ki","fr":"ki"},
                    {"jp":"ク","romaji":"ku","en":"ku","fr":"kou"},
                    {"jp":"ケ","romaji":"ke","en":"ke","fr":"ké"},
                    {"jp":"コ","romaji":"ko","en":"ko","fr":"ko"},
                ],
            },
            {
                "id": "food",
                "name": {"en": "Food", "fr": "Nourriture"},
                "icon": "🍱",
                "items": [
                    {"jp":"ごはん",  "romaji":"gohan",    "en":"rice / meal","fr":"riz / repas"},
                    {"jp":"パン",    "romaji":"pan",      "en":"bread",      "fr":"pain"},
                    {"jp":"ラーメン","romaji":"raamen",   "en":"ramen",      "fr":"ramen"},
                    {"jp":"すし",    "romaji":"sushi",    "en":"sushi",      "fr":"sushi"},
                    {"jp":"てんぷら","romaji":"tenpura",  "en":"tempura",    "fr":"tempura"},
                    {"jp":"みそしる","romaji":"misoshiru","en":"miso soup",  "fr":"soupe miso"},
                    {"jp":"おにぎり","romaji":"onigiri",  "en":"rice ball",  "fr":"boulette de riz"},
                    {"jp":"べんとう","romaji":"bentou",   "en":"lunch box",  "fr":"boîte bento"},
                    {"jp":"みず",    "romaji":"mizu",     "en":"water",      "fr":"eau"},
                    {"jp":"おちゃ",  "romaji":"ocha",     "en":"green tea",  "fr":"thé vert"},
                ],
            },
            {
                "id": "telling_time",
                "name": {"en": "Telling Time", "fr": "Dire l'heure"},
                "icon": "🕐",
                "items": [
                    {"jp":"なんじ",     "romaji":"nanji",       "en":"what time",     "fr":"quelle heure"},
                    {"jp":"いちじ",     "romaji":"ichiji",      "en":"1 o'clock",     "fr":"1 heure"},
                    {"jp":"にじ",       "romaji":"niji",        "en":"2 o'clock",     "fr":"2 heures"},
                    {"jp":"さんじ",     "romaji":"sanji",       "en":"3 o'clock",     "fr":"3 heures"},
                    {"jp":"ごぜん",     "romaji":"gozen",       "en":"AM / morning",  "fr":"matin / AM"},
                    {"jp":"ごご",       "romaji":"gogo",        "en":"PM / afternoon","fr":"après-midi / PM"},
                    {"jp":"はん",       "romaji":"han",         "en":"half past",     "fr":"et demie"},
                    {"jp":"ふん/ぷん",  "romaji":"fun/pun",     "en":"minutes",       "fr":"minutes"},
                    {"jp":"いまなんじ", "romaji":"ima nanji",   "en":"What time is it?","fr":"Quelle heure est-il ?"},
                ],
            },
            {
                "id": "body_parts",
                "name": {"en": "Body Parts", "fr": "Parties du corps"},
                "icon": "🧍",
                "items": [
                    {"jp":"あたま","romaji":"atama","en":"head",  "fr":"tête"},
                    {"jp":"め",   "romaji":"me",   "en":"eye",   "fr":"œil"},
                    {"jp":"はな", "romaji":"hana", "en":"nose",  "fr":"nez"},
                    {"jp":"みみ", "romaji":"mimi", "en":"ear",   "fr":"oreille"},
                    {"jp":"くち", "romaji":"kuchi","en":"mouth", "fr":"bouche"},
                    {"jp":"て",   "romaji":"te",   "en":"hand",  "fr":"main"},
                    {"jp":"あし", "romaji":"ashi", "en":"foot / leg","fr":"pied / jambe"},
                    {"jp":"おなか","romaji":"onaka","en":"stomach","fr":"ventre"},
                    {"jp":"せなか","romaji":"senaka","en":"back","fr":"dos"},
                ],
            },
        ],
    },

    4: {
        "name":    {"en": "4th Grade", "fr": "CM1"},
        "lessons": [
            {
                "id": "katakana_loanwords",
                "name": {"en": "Katakana — Loanwords", "fr": "Katakana — Mots étrangers"},
                "icon": "カ",
                "items": [
                    {"jp":"テレビ",   "romaji":"terebi",  "en":"TV / television","fr":"télévision"},
                    {"jp":"コンピュータ","romaji":"konpyuuta","en":"computer","fr":"ordinateur"},
                    {"jp":"スマホ",   "romaji":"sumaho",  "en":"smartphone","fr":"smartphone"},
                    {"jp":"アイスクリーム","romaji":"aisukuriimu","en":"ice cream","fr":"glace"},
                    {"jp":"ケーキ",   "romaji":"keeki",   "en":"cake",      "fr":"gâteau"},
                    {"jp":"ジュース", "romaji":"juusu",   "en":"juice",     "fr":"jus"},
                    {"jp":"バス",     "romaji":"basu",    "en":"bus",       "fr":"bus"},
                    {"jp":"タクシー", "romaji":"takushii","en":"taxi",      "fr":"taxi"},
                    {"jp":"ホテル",   "romaji":"hoteru",  "en":"hotel",     "fr":"hôtel"},
                    {"jp":"レストラン","romaji":"resutoran","en":"restaurant","fr":"restaurant"},
                ],
            },
            {
                "id": "adjectives",
                "name": {"en": "Adjectives", "fr": "Adjectifs"},
                "icon": "✨",
                "items": [
                    {"jp":"おおきい","romaji":"ookii",   "en":"big",       "fr":"grand"},
                    {"jp":"ちいさい","romaji":"chiisai", "en":"small",     "fr":"petit"},
                    {"jp":"たかい",  "romaji":"takai",   "en":"tall / expensive","fr":"grand / cher"},
                    {"jp":"やすい",  "romaji":"yasui",   "en":"cheap",     "fr":"bon marché"},
                    {"jp":"あたらしい","romaji":"atarashii","en":"new",    "fr":"nouveau"},
                    {"jp":"ふるい",  "romaji":"furui",   "en":"old",       "fr":"vieux"},
                    {"jp":"むずかしい","romaji":"muzukashii","en":"difficult","fr":"difficile"},
                    {"jp":"やさしい","romaji":"yasashii","en":"easy / kind","fr":"facile / gentil"},
                    {"jp":"おもしろい","romaji":"omoshiroi","en":"interesting","fr":"intéressant"},
                    {"jp":"たのしい","romaji":"tanoshii","en":"fun",       "fr":"amusant"},
                ],
            },
            {
                "id": "verbs_basic",
                "name": {"en": "Basic Verbs", "fr": "Verbes de base"},
                "icon": "🏃",
                "items": [
                    {"jp":"たべます","romaji":"tabemasu","en":"eat",         "fr":"manger"},
                    {"jp":"のみます","romaji":"nomimasu","en":"drink",       "fr":"boire"},
                    {"jp":"みます",  "romaji":"mimasu",  "en":"see / watch","fr":"voir / regarder"},
                    {"jp":"ききます","romaji":"kikimasu","en":"listen / ask","fr":"écouter / demander"},
                    {"jp":"かきます","romaji":"kakimasu","en":"write",       "fr":"écrire"},
                    {"jp":"よみます","romaji":"yomimasu","en":"read",        "fr":"lire"},
                    {"jp":"いきます","romaji":"ikimasu", "en":"go",          "fr":"aller"},
                    {"jp":"きます",  "romaji":"kimasu",  "en":"come",        "fr":"venir"},
                    {"jp":"かえります","romaji":"kaerimasu","en":"go home",  "fr":"rentrer"},
                    {"jp":"ねます",  "romaji":"nemasu",  "en":"sleep",       "fr":"dormir"},
                ],
            },
        ],
    },

    5: {
        "name":    {"en": "5th Grade", "fr": "CM2"},
        "lessons": [
            {
                "id": "sentences_basic",
                "name": {"en": "Basic Sentences", "fr": "Phrases de base"},
                "icon": "💬",
                "items": [
                    {"jp":"〜はなんですか",  "romaji":"~ wa nan desu ka","en":"What is ~?",         "fr":"Qu'est-ce que ~ ?"},
                    {"jp":"〜はどこですか",  "romaji":"~ wa doko desu ka","en":"Where is ~?",       "fr":"Où est ~ ?"},
                    {"jp":"〜はいくらですか","romaji":"~ wa ikura desu ka","en":"How much is ~?",   "fr":"Combien coûte ~ ?"},
                    {"jp":"〜がすきです",    "romaji":"~ ga suki desu",   "en":"I like ~",           "fr":"J'aime ~"},
                    {"jp":"〜がきらいです",  "romaji":"~ ga kirai desu",  "en":"I dislike ~",        "fr":"Je n'aime pas ~"},
                    {"jp":"〜をください",    "romaji":"~ wo kudasai",     "en":"Please give me ~",   "fr":"Donnez-moi ~ s'il vous plaît"},
                    {"jp":"〜がわかります",  "romaji":"~ ga wakarimasu",  "en":"I understand ~",     "fr":"Je comprends ~"},
                    {"jp":"〜がわかりません","romaji":"~ ga wakarimasen", "en":"I don't understand ~","fr":"Je ne comprends pas ~"},
                ],
            },
            {
                "id": "seasons_weather",
                "name": {"en": "Seasons & Weather", "fr": "Saisons & Météo"},
                "icon": "🌸",
                "items": [
                    {"jp":"はる",    "romaji":"haru",    "en":"spring", "fr":"printemps"},
                    {"jp":"なつ",    "romaji":"natsu",   "en":"summer", "fr":"été"},
                    {"jp":"あき",    "romaji":"aki",     "en":"autumn", "fr":"automne"},
                    {"jp":"ふゆ",    "romaji":"fuyu",    "en":"winter", "fr":"hiver"},
                    {"jp":"はれ",    "romaji":"hare",    "en":"sunny",  "fr":"ensoleillé"},
                    {"jp":"くもり",  "romaji":"kumori",  "en":"cloudy", "fr":"nuageux"},
                    {"jp":"あめ",    "romaji":"ame",     "en":"rain",   "fr":"pluie"},
                    {"jp":"ゆき",    "romaji":"yuki",    "en":"snow",   "fr":"neige"},
                    {"jp":"かぜ",    "romaji":"kaze",    "en":"wind",   "fr":"vent"},
                    {"jp":"あつい",  "romaji":"atsui",   "en":"hot",    "fr":"chaud"},
                    {"jp":"さむい",  "romaji":"samui",   "en":"cold",   "fr":"froid"},
                ],
            },
            {
                "id": "kanji_n5_numbers",
                "name": {"en": "Kanji — Numbers & Time", "fr": "Kanji — Nombres & Temps"},
                "icon": "一",
                "items": [
                    {"jp":"一","romaji":"ichi / hito","en":"one",       "fr":"un"},
                    {"jp":"二","romaji":"ni / futa",  "en":"two",       "fr":"deux"},
                    {"jp":"三","romaji":"san / mit",  "en":"three",     "fr":"trois"},
                    {"jp":"四","romaji":"shi / yon",  "en":"four",      "fr":"quatre"},
                    {"jp":"五","romaji":"go / itsu",  "en":"five",      "fr":"cinq"},
                    {"jp":"六","romaji":"roku / mut", "en":"six",       "fr":"six"},
                    {"jp":"七","romaji":"shichi/nana","en":"seven",     "fr":"sept"},
                    {"jp":"八","romaji":"hachi / ya", "en":"eight",     "fr":"huit"},
                    {"jp":"九","romaji":"ku / kyuu",  "en":"nine",      "fr":"neuf"},
                    {"jp":"十","romaji":"juu / too",  "en":"ten",       "fr":"dix"},
                    {"jp":"百","romaji":"hyaku",      "en":"hundred",   "fr":"cent"},
                    {"jp":"千","romaji":"sen",        "en":"thousand",  "fr":"mille"},
                    {"jp":"年","romaji":"nen / toshi","en":"year",      "fr":"année"},
                    {"jp":"月","romaji":"tsuki/gatsu","en":"month/moon","fr":"mois/lune"},
                    {"jp":"日","romaji":"hi / nichi", "en":"day / sun", "fr":"jour / soleil"},
                ],
            },
        ],
    },

    6: {
        "name":    {"en": "6th Grade", "fr": "6ème"},
        "lessons": [
            {
                "id": "kanji_n5_nature",
                "name": {"en": "Kanji — Nature & People", "fr": "Kanji — Nature & Personnes"},
                "icon": "山",
                "items": [
                    {"jp":"山","romaji":"yama/san","en":"mountain","fr":"montagne"},
                    {"jp":"川","romaji":"kawa/sen","en":"river",   "fr":"rivière"},
                    {"jp":"田","romaji":"ta/den",  "en":"rice field","fr":"rizière"},
                    {"jp":"木","romaji":"ki/moku", "en":"tree",    "fr":"arbre"},
                    {"jp":"林","romaji":"hayashi", "en":"grove",   "fr":"bosquet"},
                    {"jp":"森","romaji":"mori/shin","en":"forest", "fr":"forêt"},
                    {"jp":"水","romaji":"mizu/sui","en":"water",   "fr":"eau"},
                    {"jp":"火","romaji":"hi/ka",   "en":"fire",    "fr":"feu"},
                    {"jp":"空","romaji":"sora/kuu","en":"sky",     "fr":"ciel"},
                    {"jp":"人","romaji":"hito/jin","en":"person",  "fr":"personne"},
                    {"jp":"男","romaji":"otoko/dan","en":"man",    "fr":"homme"},
                    {"jp":"女","romaji":"onna/jo", "en":"woman",   "fr":"femme"},
                    {"jp":"子","romaji":"ko/shi",  "en":"child",   "fr":"enfant"},
                ],
            },
            {
                "id": "grammar_te_form",
                "name": {"en": "Grammar — て-form", "fr": "Grammaire — forme en て"},
                "icon": "📖",
                "items": [
                    {"jp":"食べてください", "romaji":"tabete kudasai",  "en":"Please eat",      "fr":"Mangez s'il vous plaît"},
                    {"jp":"みてください",   "romaji":"mite kudasai",    "en":"Please look",     "fr":"Regardez s'il vous plaît"},
                    {"jp":"きいてください", "romaji":"kiite kudasai",   "en":"Please listen",   "fr":"Écoutez s'il vous plaît"},
                    {"jp":"まってください", "romaji":"matte kudasai",   "en":"Please wait",     "fr":"Attendez s'il vous plaît"},
                    {"jp":"はいってください","romaji":"haitte kudasai", "en":"Please come in",  "fr":"Entrez s'il vous plaît"},
                    {"jp":"食べています",   "romaji":"tabete imasu",    "en":"(I am) eating",   "fr":"(Je suis) en train de manger"},
                    {"jp":"みています",     "romaji":"mite imasu",      "en":"(I am) watching", "fr":"(Je suis) en train de regarder"},
                    {"jp":"べんきょうしています","romaji":"benkyou shite imasu","en":"studying","fr":"en train d'étudier"},
                ],
            },
        ],
    },
}

def get_lesson(grade: int, lesson_id: str):
    g = GRADES.get(grade)
    if not g:
        return None
    for lesson in g["lessons"]:
        if lesson["id"] == lesson_id:
            return lesson
    return None

def get_all_items_for_grade(grade: int):
    items = []
    g = GRADES.get(grade)
    if g:
        for lesson in g["lessons"]:
            items.extend(lesson["items"])
    return items
