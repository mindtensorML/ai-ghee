#!/usr/bin/env python3
"""Draw the wiring of The Beast, wide and narrow.

    python3 make_schematic.py

Everything here was read off the rig rather than remembered. The pin numbers,
the PWM frequency, the sample rate and the trip currents come from
bilona_ramped.py on the Pi, and the sensor address and scaling from
current_test.py. The one thing software cannot tell you is the physical order
of the fuse, the button and the sensor around the loop, and the caption on
the page says so.

The drawing has two line weights and they mean something. Thin is signal,
where nothing carries more than a few milliamps. Thick is the motor loop,
where fifteen amps is a normal afternoon. The Pi only ever touches the thin
lines.
"""

import base64
import os
import re
import struct

HERE = os.path.dirname(os.path.abspath(__file__))

INK, GOLD, DEEP = "#2a2118", "#c08a2e", "#a8681a"
CREAM, PAPER, LINE = "#f4ead7", "#fff8ec", "#e3d2b4"
FAINT, RED = "#9a836a", "#b0402c"
SANS = '"Avenir Next","Segoe UI",sans-serif'
SANS_NE = ('"Avenir Next","Segoe UI","Kohinoor Devanagari",'
           '"Devanagari Sangam MN","Nirmala UI","Noto Sans Devanagari",sans-serif')
SANS_ZH = ('"Avenir Next","Segoe UI","PingFang SC","Hiragino Sans GB",'
           '"Microsoft YaHei","Noto Sans CJK SC","Noto Sans SC",sans-serif')
SANS_KA = ('"Avenir Next","Segoe UI","Noto Sans Georgian",Sylfaen,sans-serif')
SANS_BN = ('"Avenir Next","Segoe UI","Kohinoor Bangla","Bangla Sangam MN",'
           '"Nirmala UI","Noto Sans Bengali",Vrinda,sans-serif')
SANS_JA = ('"Avenir Next","Segoe UI","Hiragino Sans","Hiragino Kaku Gothic ProN",'
           '"Yu Gothic",Meiryo,"Noto Sans CJK JP","Noto Sans JP",sans-serif')
SANS_YUE = ('"Avenir Next","Segoe UI","PingFang HK","Hiragino Sans CNS",'
            '"Microsoft JhengHei","Noto Sans CJK HK","Noto Sans CJK TC",'
            '"Noto Sans HK",sans-serif')
SANS_AR = ('"Avenir Next","Segoe UI","Geeza Pro","Segoe UI Arabic",'
           '"Noto Sans Arabic","Noto Naskh Arabic",Tahoma,sans-serif')

# A language that reads right to left sets `iso`, and every label it supplies
# is wrapped in a pair of Unicode isolates. This drawing is held together by
# absolute coordinates and by text-anchor, and direction:rtl in the stylesheet
# would flip what start and end mean and move every label on it. The isolates
# set the base direction of the label and nothing else, so a line like the
# supply block reads as an Arabic reader expects while the box it sits in
# stays exactly where it is for the other eighteen languages.
#
# Part numbers and pin names are untouched, because a label that is not in the
# table is drawn as the code writes it and those are bare Latin either way.
RLI, LRI, PDI = "\u2067", "\u2066", "\u2069"

# A Latin technical run inside a right to left label.
#
# `12 V SUPPLY` becomes `تغذية 12 V` in Arabic, and written as it stands that
# draws as `تغذية V 12`. The digits are read as an Arabic number, because the
# word before them is Arabic, the unit is read as Latin, the space between
# belongs to the Arabic, and the two end up as separate pieces laid out right
# to left. The Unicode algorithm is doing the right thing with a string that
# did not say what it meant. A value and its unit are one object and have to
# be marked as one, which is what the left to right isolate does.
#
# Only a run holding a Latin letter is wrapped. A bare number is already laid
# out correctly and wrapping one would change nothing.
TECH_RUN = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9.+\-/_]*(?:[ \u00a0][A-Za-z0-9][A-Za-z0-9.+\-/_]*)*")


def protect(text):
    """Hold each Latin technical run together inside a right to left label."""
    return TECH_RUN.sub(
        lambda m: (LRI + m.group(0) + PDI
                   if re.search("[A-Za-z]", m.group(0)) else m.group(0)),
        text)



SIG, PWR = 1.9, 6.2          # the two line weights

# The drawing is written in every language the site has. Part numbers, pin
# names and the rig's own name do not translate, so only the words that
# describe something are listed. Anything missing from a table is drawn as it
# is written in the code, which is the right answer for a term an engineer
# would say in English whatever language the sentence around it is in.
WORDS_NE = {
    "12 V SUPPLY": "12 V सप्लाई",
    "MAINS": "मेन्स",
    "DRILL": "ड्रिल",
    "EMERGENCY STOP": "आपत्कालीन स्टप",
    "EMERGENCY": "आपत्कालीन",
    "STOP": "स्टप",
    "SIGNAL": "सिग्नल",
    "MOTOR LOOP": "मोटर लुप",
    "POWER AND SENSE": "पावर र सेन्सिङ",
}

# French translates all of these except SIGNAL, which is the same word. ALIM is
# the normal abbreviation on a French schematic and fits the box the way the
# English did. The emergency stop is drawn stacked on the narrow version, one
# word above the other, so the pair has to split the way French reads it, with
# ARRET above D'URGENCE rather than the English order. The accents stay on the
# capitals, which is correct modern French.
WORDS_FR = {
    "12 V SUPPLY": "ALIM 12 V",
    "MAINS": "SECTEUR",
    "DRILL": "PERCEUSE",
    "EMERGENCY STOP": "ARR\u00caT D'URGENCE",
    "EMERGENCY": "ARR\u00caT",
    "STOP": "D'URGENCE",
    "MOTOR LOOP": "BOUCLE MOTEUR",
    "POWER AND SENSE": "PUISSANCE ET MESURE",
}

# Kinyarwanda keeps the part numbers, the supply and the mains in English the
# way an engineer in Kigali writes them, and translates only what is actually
# described. The emergency stop is safety text and has real Kinyarwanda, and
# the verb leads, so the stacked pair on the narrow drawing puts GUHAGARIKA on
# top where the English has EMERGENCY. The two words are the same length,
# which stacks more evenly than the English pair does.
WORDS_RW = {
    "DRILL": "PERCEUSE",
    "EMERGENCY STOP": "GUHAGARIKA|BYIHUTIRWA",
    "EMERGENCY": "GUHAGARIKA",
    "STOP": "BYIHUTIRWA",
    "MOTOR LOOP": "URUZIGA RWA MOTEUR",
    "POWER AND SENSE": "INGUFU NO KUMVA",
}

# Luganda keeps most of this drawing in English, which is what an educated
# Luganda speaker writing about electronics actually does. The two headings
# take English nouns joined by Luganda grammar rather than coined equivalents,
# because that is how the phrase is really said.
#
# The emergency stop stays English deliberately. Luganda for it exists, but it
# reverses, YIMIRIZA MU KABENJE, stop in an emergency, so the stacked pair on
# the narrow drawing would have to invert as well. It is nineteen characters
# against a budget of about fifteen, EMERGENCY STOP is moulded into the actual
# button in the photographs, and it is the phrase a Ugandan technician says out
# loud. A safety marking is the wrong place to make a reader decode a word.
WORDS_LG = {
    "MOTOR LOOP": "LOOP YA MOTOR",
    "POWER AND SENSE": "POWER NE SENSE",
}

# German has a real word for every label here, and the standards body has
# already settled most of them. NETZ is what a German drawing calls the mains,
# NETZTEIL the supply block, MOTORKREIS the loop. SIGNAL is the same word and is
# left out.
#
# NETZTEIL drops the voltage the English label carries. 12 V SUPPLY measures
# 104 px against the 120 px of box it has to sit in, so there was never much
# room, and NETZTEIL 12 V comes to 121 px and runs through the border into the
# positive terminal. There is no second line to fall to either, because the
# supply symbol starts 13 px under the baseline. The rail voltage is still on
# the fuse side of the drawing in the label text a screen reader reads, and on
# the build page in the table of parts, so only the drawing goes without it.
#
# BOHRER rather than BOHRMASCHINE, which is the better word and does not fit.
# The motor label is centred under the motor on a canvas 460 wide with its
# centre at 412, so it has 48 px either side before it runs off the edge.
# BOHRMASCHINE needs 55 and AKKUSCHRAUBER 59, and both came back clipped.
# BOHRER is what someone hands you across a workshop anyway, the prose on the
# page says Akkuschrauber where there is room to say it properly, and the motor
# symbol next to the label already says the rest.
#
# NOT-AUS is the marking for cutting power in an emergency, where NOT-HALT means
# bringing a machine to a controlled stop. This button sits in the motor loop and
# breaks it, so NOT-AUS is the correct one of the two. It is also a single word
# and shorter than the English, so the narrow drawing has nothing to put on its
# second line and STOP is deliberately left empty.
WORDS_DE = {
    "12 V SUPPLY": "NETZTEIL",
    "MAINS": "NETZ",
    "DRILL": "BOHRER",
    "EMERGENCY STOP": "NOT-AUS",
    "EMERGENCY": "NOT-AUS",
    "STOP": "",
    "MOTOR LOOP": "MOTORKREIS",
    "POWER AND SENSE": "LEISTUNG UND MESSUNG",
}

# Chinese is compact enough that nothing here had to be cut. 急停 is what is
# printed on an emergency stop in a Chinese workshop, it is two characters
# against fourteen in English, and like the German it is a single word, so the
# narrow drawing skips its second line.
#
# 市电 is the mains, 电钻 the drill, 电机回路 the motor loop. The part numbers,
# the pin names and the rig's own name stay as they are drawn, which is what a
# Chinese engineer writes anyway.
WORDS_ZH = {
    "12 V SUPPLY": "12 V \u7535\u6e90",
    "MAINS": "\u5e02\u7535",
    "DRILL": "\u7535\u94bb",
    "EMERGENCY STOP": "\u6025\u505c",
    "EMERGENCY": "\u6025\u505c",
    "STOP": "",
    "SIGNAL": "\u4fe1\u53f7",
    "MOTOR LOOP": "\u7535\u673a\u56de\u8def",
    "POWER AND SENSE": "\u4f9b\u7535\u4e0e\u68c0\u6d4b",
}

# Russian takes БП, the abbreviation every Russian schematic uses for a power
# supply, the way the French drawing takes ALIM. ИСТОЧНИК is the full word and
# runs 138 px against 108 of box, so it was never going to sit there. The
# emergency stop splits АВАРИЙНЫЙ over СТОП, which is the order Russian reads
# it in and matches the two lines the narrow drawing already has.
WORDS_RU = {
    "12 V SUPPLY": "БП 12 V",
    "MAINS": "СЕТЬ",
    "DRILL": "ДРЕЛЬ",
    "EMERGENCY STOP": "АВАРИЙНЫЙ|СТОП",
    "EMERGENCY": "АВАРИЙНЫЙ",
    "STOP": "СТОП",
    "SIGNAL": "СИГНАЛ",
    "MOTOR LOOP": "КОНТУР ДВИГАТЕЛЯ",
    "POWER AND SENSE": "ПИТАНИЕ И ИЗМЕРЕНИЕ",
}

# Ukrainian abbreviates the supply the way Russian does. ЖИВЛЕННЯ 12 V measures
# 142 px against 108 of room, and БЖ is what a Ukrainian electronics drawing
# writes for блок живлення anyway. POWER AND SENSE names the sensor rather than
# the act of sensing, because ЖИВЛЕННЯ І ВИМІРЮВАННЯ measures 170 px and would
# sit 24 px wider than the widest one shipping, hard against the title box.
WORDS_UK = {
    "12 V SUPPLY": "БЖ 12 V",
    "MAINS": "МЕРЕЖА",
    "DRILL": "ДРИЛЬ",
    "EMERGENCY STOP": "АВАРІЙНИЙ СТОП",
    "EMERGENCY": "АВАРІЙНИЙ",
    "STOP": "СТОП",
    "SIGNAL": "СИГНАЛ",
    "MOTOR LOOP": "КОНТУР ДВИГУНА",
    "POWER AND SENSE": "ЖИВЛЕННЯ І ДАТЧИК",
}

# Spanish translates all of these. The stop cannot drop its preposition without
# breaking the grammar, so it splits after it, PARADA DE above EMERGENCIA.
WORDS_ES = {
    "12 V SUPPLY": "FUENTE 12 V",
    "MAINS": "RED",
    "DRILL": "TALADRO",
    "EMERGENCY STOP": "PARADA DE|EMERGENCIA",
    "EMERGENCY": "PARADA DE",
    "STOP": "EMERGENCIA",
    "SIGNAL": "SEÑAL",
    "MOTOR LOOP": "CIRCUITO DEL MOTOR",
    "POWER AND SENSE": "ALIMENTACIÓN Y MEDIDA",
}

# Hindi takes the Nepali treatment, same script and same span class. इमरजेंसी
# स्टॉप rather than the formal आपातकालीन, for the reason the German entry gives
# for NOT-AUS. It is what is moulded into the button, what a technician says
# out loud, and the formal word is government register that reads as heritage.
WORDS_HI = {
    "12 V SUPPLY": "12 V सप्लाई",
    "MAINS": "मेन्स",
    "DRILL": "ड्रिल",
    "EMERGENCY STOP": "इमरजेंसी स्टॉप",
    "EMERGENCY": "इमरजेंसी",
    "STOP": "स्टॉप",
    "SIGNAL": "सिग्नल",
    "MOTOR LOOP": "मोटर लूप",
    "POWER AND SENSE": "पावर और सेंसिंग",
}

# Turkish writes every label here itself. The dotted İ in SİNYAL and MOTOR
# DEVRESİ is the reason none of this can be left to a text-transform.
#
# BESLEME drops the voltage, the way the German NETZTEIL does. 12 V BESLEME
# measures 116 px against 108 of box and would run into the terminal, and
# Turkish has no settled short form the way French has ALIM or Russian БП.
# The rail voltage is on the build page in the table of parts, in the label
# text a screen reader reads, and in the prose.
WORDS_TR = {
    "12 V SUPPLY": "BESLEME",
    "MAINS": "ŞEBEKE",
    "DRILL": "MATKAP",
    "EMERGENCY STOP": "ACİL|STOP",
    "EMERGENCY": "ACİL",
    "STOP": "STOP",
    "SIGNAL": "SİNYAL",
    "MOTOR LOOP": "MOTOR DEVRESİ",
    "POWER AND SENSE": "GÜÇ VE ÖLÇÜM",
}

# Basque has a real word for every label here and only one had to be weighed.
# ZULAGAILUA is the modern word for the machine and measures 86 px against the
# 96 the centred position allows, so it goes in rather than the older BARAUTSA
# that a tighter estimate had argued for. The stop splits after its first word,
# which is where Basque reads the break.
WORDS_EU = {
    "12 V SUPPLY": "12 V ITURRIA",
    "MAINS": "SAREA",
    "DRILL": "ZULAGAILUA",
    "EMERGENCY STOP": "LARRIALDIKO|GELDIALDIA",
    "EMERGENCY": "LARRIALDIKO",
    "STOP": "GELDIALDIA",
    "SIGNAL": "SEINALEA",
    "MOTOR LOOP": "MOTOR-BEGIZTA",
    "POWER AND SENSE": "POTENTZIA ETA NEURKETA",
}

# Georgian fits everywhere with room to spare, and only the supply block had
# to be shortened. კვების ბლოკი 12 V measures 150 px against 108 of box, so it
# drops to 12 V კვება, which is the same word the build page's table of parts
# uses for that row and keeps the voltage the German and Turkish drawings both
# had to give up.
WORDS_KA = {
    "12 V SUPPLY": "12 V კვება",
    "MAINS": "ქსელი",
    "DRILL": "ბურღი",
    "EMERGENCY STOP": "ავარიული|გაჩერება",
    "EMERGENCY": "ავარიული",
    "STOP": "გაჩერება",
    "SIGNAL": "სიგნალი",
    "MOTOR LOOP": "მოტორის კონტური",
    "POWER AND SENSE": "კვება და გაზომვა",
}

# Bangla hangs from a headline bar the way Devanagari does, so it takes the
# `dv` treatment rather than one of its own. Everything here fits with room.
# The widest is the supply block at 87 px against 108 of box, so unlike the
# German and Turkish drawings this one keeps its voltage.
#
# ইমার্জেন্সি স্টপ rather than the formal আপৎকালীন বন্ধকরণ, which is the same call
# the German NOT-AUS entry makes. It is what is moulded into the button in the
# photographs and what a technician in Dhaka says out loud. A safety marking
# is the wrong place to make a reader decode a word.
WORDS_BN = {
    "12 V SUPPLY": "12 V সাপ্লাই",
    "MAINS": "মেইন্স",
    "DRILL": "ড্রিল",
    "EMERGENCY STOP": "ইমার্জেন্সি স্টপ",
    "EMERGENCY": "ইমার্জেন্সি",
    "STOP": "স্টপ",
    "SIGNAL": "সিগন্যাল",
    "MOTOR LOOP": "মোটর লুপ",
    "POWER AND SENSE": "পাওয়ার ও সেন্সিং",
}

# Filipino keeps four of these in English, which is what a Filipino drawing
# actually does rather than a failure to translate. Philippine wiring diagrams
# and parts lists are written in English and SUPPLY and DRILL are the words
# said out loud. BARENA is a real Tagalog word but it means an auger or a
# drill bit rather than a power tool, so a reader would picture the wrong
# object. EMERGENCY STOP is moulded into the button, and the formal
# PANGHINTONG PANG-EMERHENSIYA is both far over budget and pure officialese.
#
# MAINS does translate, and has to. Nobody in the Philippines says mains. Wall
# power is kuryente. At 58 px it is the widest this label has ever been here,
# against 49 px for the French SECTEUR, and it is centred just outside the
# supply box, so it is the one label on this drawing worth looking at.
WORDS_FIL = {
    "MAINS": "KURYENTE",
    "SIGNAL": "SINYAL",
    "MOTOR LOOP": "LOOP NG MOTOR",
    "POWER AND SENSE": "POWER AT SENSE",
}

# Japanese has a settled term for every one of these and nothing is close to
# its budget. 非常停止 is what is written on an emergency stop in a Japanese
# workshop and what JIS calls it. It is four characters on one line, so like
# the German and the Chinese it leaves the narrow drawing's second line empty.
# 計測 rather than 検出 for the sensing, because the INA260 measures a value
# rather than detecting an event.
WORDS_JA = {
    "12 V SUPPLY": "12 V 電源",
    "MAINS": "商用電源",
    "DRILL": "ドリル",
    "EMERGENCY STOP": "非常停止",
    "EMERGENCY": "非常停止",
    "STOP": "",
    "SIGNAL": "信号",
    "MOTOR LOOP": "モーター回路",
    "POWER AND SENSE": "電源と計測",
}

# Cantonese is not the Chinese table with different characters. Hong Kong says
# 馬達 where the mainland says 電機, 訊號 where it says 信號, 迴路 where it says
# 回路, and 急停掣 where it says 急停, the 掣 being the Cantonese word for a
# switch or button. 急停掣 is three characters on one line, so the narrow
# drawing's second line is empty here too.
WORDS_YUE = {
    "12 V SUPPLY": "12 V 電源",
    "MAINS": "市電",
    "DRILL": "電鑽",
    "EMERGENCY STOP": "急停掣",
    "EMERGENCY": "急停掣",
    "STOP": "",
    "SIGNAL": "訊號",
    "MOTOR LOOP": "馬達迴路",
    "POWER AND SENSE": "供電同感應",
}

# Arabic, the first language on this drawing that reads right to left. The
# labels are written in plain logical order, the way anyone types Arabic, and
# the isolates that put them in the right visual order are added by T().
#
# The two halves of the emergency stop are swapped against the English. Arabic
# puts the stopping first and the emergency second, so the top line is إيقاف
# and the bottom is الطوارئ. Taking the English order would give الطوارئ إيقاف,
# which is not a phrase. Kinyarwanda needed the same inversion for the same
# kind of reason.
#
# Nothing here is near its budget. مثقاب is six characters where Basque needed
# ten, and تغذية 12 V keeps the voltage that the German and Turkish drawings
# both had to give up.
WORDS_AR = {
    "12 V SUPPLY": "تغذية 12 V",
    "MAINS": "الكهرباء",
    "DRILL": "مثقاب",
    "EMERGENCY STOP": "إيقاف|الطوارئ",
    "EMERGENCY": "إيقاف",
    "STOP": "الطوارئ",
    "SIGNAL": "إشارة",
    "MOTOR LOOP": "حلقة المحرك",
    "POWER AND SENSE": "الطاقة والقياس",
}

# Newari, that is Nepal Bhasa. The same script as Nepali and a different
# language. बः is the real Nepal Bhasa word for power and is attested, so the
# sensing heading does not need a loanword for its first half.
#
# आपत्कालीन स्टप is the phrase actually painted on equipment in the Valley and
# is what the page body says, so the drawing and the prose agree. There is a
# better native alternative, हथाय् दिकेगु, and it is flagged in the handover
# for a native speaker to rule on. A safety marking is the one place to choose
# instant recognition over the finer word.
WORDS_NEW = {
    "12 V SUPPLY": "12 V सप्लाई",
    "MAINS": "मेन्स",
    "DRILL": "ड्रिल",
    "EMERGENCY STOP": "आपत्कालीन स्टप",
    "EMERGENCY": "आपत्कालीन",
    "STOP": "स्टप",
    "SIGNAL": "सिग्नल",
    "MOTOR LOOP": "मोटर लुप",
    "POWER AND SENSE": "बः व सेन्सिङ",
}

ARIA = {
    "en": "Circuit diagram of the ghee rig. A Raspberry Pi drives a BTS7960 "
          "H-bridge over four signal wires and reads an INA260 current sensor "
          "over I2C. A 12 volt supply, a 15 amp fuse, the emergency stop "
          "button and the sensor sit in series in the motor loop, which the "
          "Pi never touches.",
    "fr": "Sch\u00e9ma \u00e9lectrique de la machine \u00e0 ghee. Un Raspberry Pi "
          "pilote un pont en H BTS7960 par quatre fils de signal et lit un "
          "capteur de courant INA260 en I2C. Une alimentation de 12 volts, un "
          "fusible de 15 amp\u00e8res, le bouton d'arr\u00eat d'urgence et le capteur "
          "sont en s\u00e9rie dans la boucle du moteur, que le Pi ne touche jamais.",
    "rw": "Igishushanyo cy'umuyoboro wa rig ya ghee. Raspberry Pi itwara pont H "
          "ya BTS7960 inyuze mu nsinga enye za signal kandi isoma capteur ya "
          "courant INA260 inyuze kuri I2C. Alimentation ya 12 V, fusible ya 15 A, "
          "buto yo guhagarika byihutirwa na capteur biri ku murongo umwe mu "
          "ruziga rwa moteur, uruziga Pi itakoraho na rimwe.",
    "lg": "Diagram y'ekyuma ky'omuzigo. Raspberry Pi akoleeza H bridge ya "
          "BTS7960 ng'ayita mu waya nnya za signal, era asoma sensor ya current "
          "ya INA260 ng'ayita mu I2C. Supply ya 12 V, fyuuzi ya 15 A, ebbatani "
          "ery'okuyimiriza mu kabenje ne sensor byonna biyungibwa olukalala lumu "
          "mu loop ya motor, loop Pi atakwatako n'akatono.",
    "de": "Schaltplan des Ghee-Aufbaus. Ein Raspberry Pi steuert eine "
          "H-Brücke BTS7960 über vier Signalleitungen und liest einen "
          "Stromsensor INA260 über I2C. Ein Netzteil mit 12 Volt, eine "
          "Sicherung mit 15 Ampere, der Not-Aus-Taster und der Sensor liegen in "
          "Reihe im Motorkreis, den der Pi nie berührt.",
    "zh": "酥油机的电路图。树莓派通过四根信号线驱动 BTS7960 H 桥，"
          "并通过 I2C 读取 INA260 电流传感器。12 V 电源、15 A 保险丝、"
          "急停按钮和传感器串联在电机回路里，而树莓派从不接触这个回路。",
    "ru": "Схема установки для гхи. Raspberry Pi управляет H-мостом "
          "BTS7960 по четырём сигнальным линиям и читает датчик тока INA260 "
          "по I2C. Блок питания 12 V, предохранитель 15 A, кнопка аварийного "
          "останова и датчик включены последовательно в контур двигателя, "
          "которого Pi никогда не касается.",
    "uk": "Схема установки для гхі. Raspberry Pi керує H-мостом BTS7960 "
          "по чотирьох сигнальних лініях і читає датчик струму INA260 по I2C. "
          "Блок живлення 12 V, запобіжник 15 A, кнопка аварійного стопу і "
          "датчик увімкнені послідовно в контур двигуна, якого Pi ніколи не "
          "торкається.",
    "es": "Esquema eléctrico de la máquina de ghee. Una Raspberry Pi controla "
          "un puente en H BTS7960 por cuatro cables de señal y lee un sensor "
          "de corriente INA260 por I2C. Una fuente de 12 V, un fusible de "
          "15 A, el botón de parada de emergencia y el sensor están en serie "
          "en el circuito del motor, que la Pi nunca toca.",
    "tr": "Ghee düzeneğinin devre şeması. Bir Raspberry Pi, dört sinyal "
          "kablosu üzerinden BTS7960 H köprüsünü sürüyor ve INA260 akım "
          "sensörünü I2C üzerinden okuyor. 12 V güç kaynağı, 15 A sigorta, "
          "acil durdurma düğmesi ve sensör, Pi'nin hiç dokunmadığı motor "
          "devresinde seri olarak duruyor.",
    "ka": "ერბოს დანადგარის სქემა. Raspberry Pi ოთხი სიგნალის ხაზით მართავს "
          "BTS7960 H-ხიდს და I2C-ით კითხულობს INA260 დენის სენსორს. 12 V "
          "კვების ბლოკი, 15 A დამცველი, ავარიული გაჩერების ღილაკი და სენსორი "
          "მიმდევრობით არის ჩართული მოტორის კონტურში, რომელსაც Pi არასდროს "
          "ეხება.",
    "eu": "Ghee egiteko makinaren zirkuitu-eskema. Raspberry Pi batek BTS7960 "
          "H zubi bat gidatzen du lau seinale-kableren bitartez eta INA260 "
          "korronte-sentsore bat irakurtzen du I2C bidez. 12 V-ko iturri bat, "
          "15 A-ko fusible bat, larrialdiko geldialdiaren botoia eta "
          "sentsorea seriean daude motorraren begiztan, eta Pi-ak ez du "
          "inoiz ukitzen.",
    "hi": "घी बनाने वाले रिग का सर्किट डायग्राम। रास्पबेरी पाई चार सिग्नल तारों से "
          "BTS7960 एच ब्रिज चलाता है और I2C से INA260 करेंट सेंसर पढ़ता है। 12 V की "
          "सप्लाई, 15 एम्पियर का फ़्यूज़, इमरजेंसी स्टॉप बटन और सेंसर मोटर के उसी लूप में "
          "एक के बाद एक जुड़े हैं, जिस लूप को पाई कभी नहीं छूता।",
    "ar": "مخطط دائرة آلة السمن. راسبيري باي يقود جسر BTS7960 عبر أربعة أسلاك "
          "إشارة، ويقرأ مستشعر التيار INA260 عبر I2C. مزود طاقة 12 فولت، ومصهر "
          "15 أمبير، وزر إيقاف الطوارئ، والمستشعر، كلها موصولة على التوالي في "
          "حلقة المحرك. وهي حلقة لا يلمسها راسبيري باي أبدا.",
    "new": "घ्यः दय्कीगु रिगया सर्किट डायग्राम। रास्पबेरी पाईं प्यंगू सिग्नल "
           "तारं BTS7960 एच ब्रिज न्ह्याकी अले I2C पाखें INA260 करेन्ट सेन्सर "
           "ब्वनी। 12 भोल्टया सप्लाई, 15 एम्पियरया फ्युज, आपत्कालीन स्टप बटन व "
           "सेन्सर मोटरयागु हे लुपय् छगू लिपा मेगु कसातःगु दु, उगु लुप पाईं "
           "गुबलें थीइमखु।",
    "bn": "ঘি বানানোর যন্ত্রের সার্কিট ডায়াগ্রাম। রাস্পবেরি পাই চারটি সিগন্যাল তার "
          "দিয়ে BTS7960 এইচ ব্রিজ চালায় আর I2C দিয়ে INA260 কারেন্ট সেন্সর পড়ে। "
          "12 V-র একটা সাপ্লাই, 15 অ্যাম্পিয়ারের একটা ফিউজ, ইমার্জেন্সি স্টপ বোতাম "
          "আর সেন্সর মোটরের লুপে একের পরে এক লাগানো। ওই লুপ পাই কখনও ছোঁয় না।",
    "fil": "Diagram ng sirkito ng makina ng ghee. Isang Raspberry Pi ang "
           "nagpapaandar sa BTS7960 H bridge sa apat na signal wire at "
           "nagbabasa ng INA260 current sensor sa pamamagitan ng I2C. Ang "
           "12 V na supply, ang 15 A na fuse, ang emergency stop button at "
           "ang sensor ay nakasunod-sunod sa loop ng motor. Hindi hinihipo ng "
           "Pi ang loop na iyon kahit kailan.",
    "ja": "ギーを作る装置の回路図。Raspberry Pi が四本の信号線で BTS7960 の H "
          "ブリッジを駆動し、I2C で INA260 の電流センサーを読む。12 V の電源、"
          "15 A のヒューズ、非常停止ボタン、電流センサーがモーターのループに"
          "直列に入っていて、そのループに Pi は一度も触れない。",
    "yue": "整酥油嘅機嘅電路圖。Raspberry Pi 用四條訊號線推 BTS7960 H 橋，"
           "再用 I2C 讀 INA260 電流感應器。12 V 電源、15 A 保險絲、急停掣同"
           "感應器係串喺馬達迴路入面，呢個迴路 Pi 完全冇掂過。",
    "ne": "घ्यू बनाउने रिगको सर्किट डायग्राम। रास्पबेरी पाईले चार वटा सिग्नल "
          "तारबाट BTS7960 एच ब्रिज चलाउँछ र I2C बाट INA260 करेन्ट सेन्सर पढ्छ। "
          "12 भोल्टको सप्लाई, 15 एम्पियरको फ्युज, आपत्कालीन स्टप बटन र सेन्सर "
          "मोटरकै लुपमा एकपछि अर्को जोडिएका छन्, जुन लुप पाईले कहिल्यै छुँदैन।",
}

# One entry per language. `span` is the class a translated label is wrapped
# in, for a script that cannot take the letter spacing the Latin labels are
# drawn with and does not sit at the same optical size as a Latin capital.
# The class names the treatment rather than the script. Bengali is not
# Devanagari, but it is built the same way, it objects to tracking for the
# same reason, and measured at a matched size the body of a letter in each is
# 7.0px against a Latin capital's 8.25px. So Bangla takes `dv` as it stands
# rather than a second class holding the same two numbers.
# Devanagari hangs from a bar along the top of a word, which tracking cuts
# into pieces, and it fills less of its em, so `dv` turns the tracking off and
# sets it larger. A Han character fills its whole em, so `han` turns the
# tracking off and sets it smaller. Mkhedruli has no capitals at all, and it
# turns out not to need a lift either. Measured at a matched size its body is
# 8.8px against a Latin capital's 8.5px, and its ascenders and descenders then
# carry it to 11.2px, so it reads as the larger of the two and `ka` takes it
# down slightly and keeps only a trace of the tracking. Latin script languages
# need none of this and reuse the Latin stack and tracking.
LANGS = {
    "en": dict(suffix="",    stack=SANS,    span=None,  words={}),
    "ne": dict(suffix="-ne", stack=SANS_NE, span="dv",  words=WORDS_NE),
    "fr": dict(suffix="-fr", stack=SANS,    span=None,  words=WORDS_FR),
    "rw": dict(suffix="-rw", stack=SANS,    span=None,  words=WORDS_RW),
    "lg": dict(suffix="-lg", stack=SANS,    span=None,  words=WORDS_LG),
    "de": dict(suffix="-de", stack=SANS,    span=None,  words=WORDS_DE),
    "zh": dict(suffix="-zh", stack=SANS_ZH, span="han", words=WORDS_ZH),
    "ru": dict(suffix="-ru", stack=SANS,    span=None,  words=WORDS_RU),
    "es": dict(suffix="-es", stack=SANS,    span=None,  words=WORDS_ES),
    "hi": dict(suffix="-hi", stack=SANS_NE, span="dv",  words=WORDS_HI),
    "tr": dict(suffix="-tr", stack=SANS,    span=None,  words=WORDS_TR),
    "eu": dict(suffix="-eu", stack=SANS,    span=None,  words=WORDS_EU),
    "ka": dict(suffix="-ka", stack=SANS_KA, span="ka",   words=WORDS_KA),
    "bn": dict(suffix="-bn", stack=SANS_BN, span="dv",  words=WORDS_BN),
    "fil": dict(suffix="-fil", stack=SANS,  span=None,  words=WORDS_FIL),
    "ja": dict(suffix="-ja", stack=SANS_JA, span="han", words=WORDS_JA),
    "yue": dict(suffix="-yue", stack=SANS_YUE, span="han", words=WORDS_YUE),
    "ar": dict(suffix="-ar", stack=SANS_AR, span="ar", words=WORDS_AR, iso=True),
    "new": dict(suffix="-new", stack=SANS_NE, span="dv", words=WORDS_NEW),
    "uk": dict(suffix="-uk", stack=SANS,    span=None,  words=WORDS_UK),
}

LANG = "en"


def L():
    return LANGS[LANG]


def stack():
    return L()["stack"]


def T(word):
    """A drawn label, in the language being written.

    A translated word comes back inside a span that carries no tracking and
    a little more size. Devanagari joins along a bar across the top of the
    word, which letter spacing cuts into pieces, and it fills less of its em
    than a Latin capital, so at a matched size it reads as the smaller of the
    two. The part numbers around it keep the size and tracking they were
    drawn with.
    """
    translated = L()["words"].get(word)
    if translated is None:
        return word
    if L().get("iso"):
        translated = f"{RLI}{protect(translated)}{PDI}"
    if not L()["span"]:
        return translated
    return f'<tspan class="{L()["span"]}">{translated}</tspan>'


def T_stacked(word, x):
    """A label that may need two lines, stacked around where one line sat.

    A translation can be written with a bar between its halves to ask for a
    stack. Kinyarwanda needs it, because the emergency stop is twenty one
    characters against fourteen in English and the one line form runs into
    the sensor card. The label is centred, so trimming characters only moves
    its right hand edge by half as much and there is no honest short form, so
    it goes on two lines the way the narrow drawing already does.
    """
    translated = L()["words"].get(word)
    if translated is None or "|" not in translated:
        return T(word)
    first, second = translated.split("|", 1)
    if L().get("iso"):
        first = f"{RLI}{protect(first)}{PDI}"
        second = f"{RLI}{protect(second)}{PDI}"
    return (f'<tspan x="{x}" dy="-1.5em">{first}</tspan>'
            f'<tspan x="{x}" dy="1.5em">{second}</tspan>')


def out_path(name):
    stem = name.replace("schematic", "schematic" + L()["suffix"])
    return os.path.join(HERE, "images", stem)



PARTS = os.path.join(HERE, "images", "parts")


def jpeg_size(path):
    """Width and height from the JPEG start of frame, no dependencies."""
    with open(path, "rb") as fh:
        fh.read(2)
        while True:
            b = fh.read(1)
            while b == b"\xff":
                b = fh.read(1)
            if not b:
                raise ValueError(f"no frame header in {path}")
            marker, = struct.unpack("B", b)
            length, = struct.unpack(">H", fh.read(2))
            if marker in set(range(0xC0, 0xD0)) - {0xC4, 0xC8, 0xCC}:
                h, w = struct.unpack(">HH", fh.read(5)[1:])
                return w, h
            fh.seek(length - 2, 1)


def photo(name, x, y, w):
    """Place a part photograph, sized from the file so it never distorts.

    The bytes travel inside the drawing. An SVG loaded in an img tag is not
    allowed to fetch anything, so a linked file would simply not appear.
    """
    path = os.path.join(PARTS, name)
    pw, ph = jpeg_size(path)
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    return (f'<image x="{x}" y="{y}" width="{w}" height="{w*ph/pw:.1f}" '
            f'preserveAspectRatio="xMidYMid meet" '
            f'href="data:image/jpeg;base64,{b64}"/>')


def css(s=1.0):
    return f"""
 .grid{{stroke:{LINE};stroke-width:{0.7*s:.2f};opacity:.45}}
 .box{{fill:{PAPER};stroke:{INK};stroke-width:{2.0*s:.2f}}}
 .chip{{fill:{PAPER};stroke:{DEEP};stroke-width:{1.7*s:.2f}}}
 .sig{{fill:none;stroke:{INK};stroke-width:{SIG*s:.2f};stroke-linecap:round;stroke-linejoin:round}}
 .pwr{{fill:none;stroke:{GOLD};stroke-width:{PWR*s:.2f};stroke-linecap:round;stroke-linejoin:round}}
 .pwrk{{fill:none;stroke:{DEEP};stroke-width:{PWR*s:.2f};stroke-linecap:round;stroke-linejoin:round}}
 .ttl{{font:700 {14*s:.1f}px {stack()};fill:{INK};letter-spacing:{0.16*s:.2f}em}}
 .nm{{font:700 {15*s:.1f}px {stack()};fill:{INK};letter-spacing:{0.10*s:.2f}em}}
 .sub{{font:500 {11*s:.1f}px {stack()};fill:{FAINT};letter-spacing:{0.05*s:.2f}em}}
 .pin{{font:600 {12*s:.1f}px {stack()};fill:{DEEP};letter-spacing:{0.04*s:.2f}em}}
 .val{{font:700 {12.5*s:.1f}px {stack()};fill:{INK}}}
 .dv{{letter-spacing:0;font-size:1.18em}}
 .han{{letter-spacing:0;font-size:0.92em}}
 .ka{{letter-spacing:0.02em;font-size:0.97em}}
 .ar{{letter-spacing:0;font-size:1.08em}}
 .note{{font:italic 400 {11*s:.1f}px Georgia,serif;fill:{FAINT}}}
 .notek{{font:italic 400 {11*s:.1f}px Georgia,serif;fill:{DEEP}}}
 .lead{{fill:none;stroke:{FAINT};stroke-width:{0.9*s:.2f};stroke-dasharray:{2.5*s:.1f} {2.5*s:.1f}}}
 .red{{fill:none;stroke:{RED};stroke-width:{PWR*s:.2f};stroke-linecap:round}}
"""


def grid(w, h, step=26):
    out = []
    x = step
    while x < w:
        out.append(f'<line class="grid" x1="{x}" y1="0" x2="{x}" y2="{h}"/>')
        x += step
    y = step
    while y < h:
        out.append(f'<line class="grid" x1="0" y1="{y}" x2="{w}" y2="{y}"/>')
        y += step
    return "".join(out)


def block(x, y, w, h, name, sub="", cls="box", r=6):
    return (f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
            f'<text class="nm" x="{x+13}" y="{y+24}">{name}</text>'
            + (f'<text class="sub" x="{x+13}" y="{y+41}">{sub}</text>' if sub else ""))


def dot(x, y, r=3.4, fill=None):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill or INK}"/>'


def estop(cx, cy, s=1.0):
    """A break in the loop with a mushroom head over it.

    Drawn as an open lever, which is the usual convention even for a switch
    that is closed in normal use, because a closed one drawn flat is
    indistinguishable from plain wire.
    """
    L, R = cx - 24 * s, cx + 24 * s
    return (f'<line class="red" x1="{L-16*s}" y1="{cy}" x2="{L}" y2="{cy}"/>'
            f'<line class="red" x1="{R}" y1="{cy}" x2="{R+16*s}" y2="{cy}"/>'
            f'<line x1="{L}" y1="{cy}" x2="{cx+13*s}" y2="{cy-19*s}" stroke="{RED}" '
            f'stroke-width="{3.0*s:.2f}" stroke-linecap="round"/>'
            f'<line x1="{cx-5*s}" y1="{cy-11*s}" x2="{cx-5*s}" y2="{cy-33*s}" stroke="{RED}" '
            f'stroke-width="{2.6*s:.2f}"/>'
            f'<rect x="{cx-24*s}" y="{cy-46*s}" width="{38*s}" height="{13*s}" rx="{6.5*s}" '
            f'fill="{RED}"/>'
            + dot(L, cy, 3.6 * s, RED) + dot(R, cy, 3.6 * s, RED))


def estop_v(cx, cy, s=1.0):
    """The same break, drawn for a vertical run. The head is left off here
    because at phone size it turns into a blob and the label does the work."""
    T, B = cy - 22 * s, cy + 22 * s
    return (f'<line class="red" x1="{cx}" y1="{T-18*s}" x2="{cx}" y2="{T}"/>'
            f'<line class="red" x1="{cx}" y1="{B}" x2="{cx}" y2="{B+18*s}"/>'
            f'<line x1="{cx}" y1="{B}" x2="{cx+21*s}" y2="{T+6*s}" stroke="{RED}" '
            f'stroke-width="{3.2*s:.2f}" stroke-linecap="round"/>'
            + dot(cx, T, 4.0 * s, RED) + dot(cx, B, 4.0 * s, RED))


def fuse(cx, cy, s=1.0):
    return (f'<rect x="{cx-17*s}" y="{cy-8*s}" width="{34*s}" height="{16*s}" rx="{3*s}" '
            f'fill="{PAPER}" stroke="{DEEP}" stroke-width="{1.8*s:.2f}"/>'
            f'<line x1="{cx-17*s}" y1="{cy}" x2="{cx+17*s}" y2="{cy}" stroke="{DEEP}" '
            f'stroke-width="{1.6*s:.2f}"/>')


def battery(x, y, s=1.0):
    """Cells drawn long-short, long plate is the positive terminal."""
    o = []
    for i, (dx, hh) in enumerate(((0, 20), (9, 10), (18, 20), (27, 10))):
        o.append(f'<line x1="{x+dx*s}" y1="{y-hh*s}" x2="{x+dx*s}" y2="{y+hh*s}" '
                 f'stroke="{GOLD}" stroke-width="{(3.4 if hh > 15 else 2.4)*s:.2f}" stroke-linecap="round"/>')
    return "".join(o)


def motor(cx, cy, r, s=1.0):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}" stroke="{GOLD}" '
            f'stroke-width="{PWR*s:.2f}"/>'
            f'<text class="nm" x="{cx}" y="{cy+5*s}" text-anchor="middle">M</text>')


def note(x, y, lines, cls="note", anchor="start", lh=15):
    return "".join(f'<text class="{cls}" x="{x}" y="{y+i*lh}" text-anchor="{anchor}">{t}</text>'
                   for i, t in enumerate(lines))


def supply(x, y, w, h, s=1.0, mains_left=True):
    """The 12 V open frame switch mode supply, and its lead to the wall."""
    o = [f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>',
         f'<text class="nm" x="{x+12}" y="{y+27}">{T("12 V SUPPLY")}</text>']
    for i in range(7):
        vx = x + 14 + i * 9
        o.append(f'<line x1="{vx}" y1="{y+h-30}" x2="{vx}" y2="{y+h-9}" stroke="{LINE}" '
                 f'stroke-width="{1.4*s:.2f}"/>')
    if mains_left:
        o.append(f'<line class="sig" x1="{x-54*s}" y1="{y+h/2}" x2="{x}" y2="{y+h/2}"/>')
        # Anchored to the box rather than centred on the lead. Centred, how
        # close this label comes to the supply box depends on how long the
        # word is, and the Filipino KURYENTE is 58 px against the English
        # MAINS at 37, so its last letter was drawn through the border. The
        # offset is chosen so the English label does not move, and a longer
        # word now grows away from the box instead of into it.
        o.append(f'<text class="sub" x="{x-8.75*s}" y="{y+h/2-9}" '
                 f'text-anchor="end">{T("MAINS")}</text>')
    return "".join(o)


def wide():
    """Symbols, names and values, and a photograph of each board."""
    W, H = 1120, 740
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="{ARIA[LANG]}">',
         f'<rect width="{W}" height="{H}" fill="{CREAM}"/>',
         f'<style>{css()}</style>', f'<g>{grid(W, H, 24)}</g>']

    PI = (60, 88, 210, 204)
    HB = (600, 88, 240, 204)
    o.append(block(*PI, "RASPBERRY PI 3"))
    o.append(photo("pi.jpg", 78, 128, 174))
    o.append(block(*HB, "BTS7960 H-BRIDGE"))
    o.append(photo("bts.jpg", 645, 128, 150))

    px, hx = PI[0] + PI[2], HB[0]
    for i, (gpio, fn, val) in enumerate((("GPIO 18", "RPWM", "1 kHz"), ("GPIO 19", "LPWM", "1 kHz"),
                                         ("GPIO 23", "R_EN", ""), ("GPIO 24", "L_EN", ""))):
        y = 138 + i * 35
        o.append(f'<line class="sig" x1="{px}" y1="{y}" x2="{hx}" y2="{y}"/>')
        o.append(dot(px, y) + dot(hx, y))
        o.append(f'<text class="pin" x="{px+12}" y="{y-9}">{gpio}</text>')
        o.append(f'<text class="pin" x="{hx-12}" y="{y-9}" text-anchor="end">{fn}</text>')
        if val:
            o.append(f'<text class="sub" x="{(px+hx)/2}" y="{y-9}" text-anchor="middle">{val}</text>')

    o.append(motor(960, 190, 52))
    for y in (172, 208):
        o.append(f'<line class="pwr" x1="{HB[0]+HB[2]}" y1="{y}" x2="911" y2="{y}"/>')
    o.append(f'<text class="pin" x="{HB[0]+HB[2]+10}" y="164">M+</text>')
    o.append(f'<text class="pin" x="{HB[0]+HB[2]+10}" y="228">M&#8722;</text>')
    o.append(f'<text class="sub" x="960" y="266" text-anchor="middle">{T("DRILL")}</text>')

    RAIL, RET = 480, 620
    INA = (430, 406, 250, 148)
    PSU = (76, 445, 132, 70)
    BPX, BMX = 706, 776
    ES, FU = 350, 262
    SDA_X, SCL_X = 470, 506
    PB = PI[1] + PI[3]

    o.append(f'<path class="sig" d="M186,{PB} L186,356 L{SDA_X},356 L{SDA_X},{INA[1]}"/>')
    o.append(f'<path class="sig" d="M214,{PB} L214,336 L{SCL_X},336 L{SCL_X},{INA[1]}"/>')
    o.append(dot(186, PB) + dot(214, PB))
    o.append(f'<text class="pin" x="178" y="{PB+24}" text-anchor="end">I2C</text>')
    o.append(f'<text class="pin" x="{SDA_X+9}" y="392">SDA</text>')
    o.append(f'<text class="pin" x="{SCL_X+9}" y="372">SCL</text>')

    o.append(f'<rect class="chip" x="{INA[0]}" y="{INA[1]}" width="{INA[2]}" '
             f'height="{INA[3]}" rx="6"/>')
    o.append(f'<text class="nm" x="{INA[0]+14}" y="{INA[1]+27}">INA260</text>')
    o.append(f'<text class="sub" x="{INA[0]+14}" y="{INA[1]+45}">0x40</text>')
    o.append(photo("ina.jpg", 566, 432, 96))
    o.append(f'<text class="pin" x="{INA[0]-10}" y="{RAIL-12}" text-anchor="end">IN+</text>')
    o.append(f'<text class="pin" x="{INA[0]+INA[2]+10}" y="{RAIL-12}">IN&#8722;</text>')

    o.append(supply(*PSU))
    PR = PSU[0] + PSU[2]
    o.append(f'<text class="val" x="{PR+11}" y="{PSU[1]+14}">+</text>')
    o.append(f'<text class="val" x="{PR+11}" y="{PSU[1]+68}">&#8722;</text>')
    o.append(f'<path class="pwr" d="M{PR},{PSU[1]+18} L240,{PSU[1]+18} L240,{RAIL} L{ES-24},{RAIL}"/>')
    o.append(f'<path class="pwr" d="M{ES+24},{RAIL} L{INA[0]},{RAIL}"/>')
    o.append(f'<path class="pwr" d="M{INA[0]+INA[2]},{RAIL} L{BPX},{RAIL} L{BPX},{HB[1]+HB[3]}"/>')
    o.append(f'<path class="pwr" d="M{BMX},{HB[1]+HB[3]} L{BMX},{RET} L240,{RET} '
             f'L240,{PSU[1]+52} L{PR},{PSU[1]+52}"/>')
    o.append(f'<text class="pin" x="{BPX-10}" y="{HB[1]+HB[3]+24}" text-anchor="end">B+</text>')
    o.append(f'<text class="pin" x="{BMX+10}" y="{HB[1]+HB[3]+24}">B&#8722;</text>')

    o.append(fuse(FU, RAIL))
    o.append(f'<text class="val" x="{FU}" y="{RAIL-21}" text-anchor="middle">15 A</text>')
    o.append(estop(ES, RAIL))
    o.append(f'<text class="pin" x="{ES}" y="{RAIL-60}" text-anchor="middle">{T_stacked("EMERGENCY STOP", ES)}</text>')

    o.append('<line class="sig" x1="62" y1="48" x2="98" y2="48"/>')
    o.append(f'<text class="sub" x="106" y="52">{T("SIGNAL")}</text>')
    o.append('<line class="pwr" x1="200" y1="48" x2="236" y2="48"/>')
    o.append(f'<text class="sub" x="244" y="52">{T("MOTOR LOOP")}</text>')

    tb = (900, 640, 190, 58)
    o.append(f'<rect x="{tb[0]}" y="{tb[1]}" width="{tb[2]}" height="{tb[3]}" rx="4" '
             f'fill="none" stroke="{FAINT}" stroke-width="1"/>')
    o.append(f'<line x1="{tb[0]}" y1="{tb[1]+26}" x2="{tb[0]+tb[2]}" y2="{tb[1]+26}" '
             f'stroke="{FAINT}" stroke-width="1"/>')
    o.append(f'<text class="ttl" x="{tb[0]+11}" y="{tb[1]+18}">THE BEAST</text>')
    o.append(f'<text class="sub" x="{tb[0]+11}" y="{tb[1]+44}">{T("POWER AND SENSE")}</text>')
    o.append("</svg>")
    return "".join(o)


def narrow():
    """The same circuit as one vertical chain, which is how a phone reads it."""
    W, H = 460, 900
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="{ARIA[LANG]}">',
         f'<rect width="{W}" height="{H}" fill="{CREAM}"/>',
         f'<style>{css(1.18)}</style>', f'<g>{grid(W, H, 22)}</g>']

    o.append('<line class="sig" x1="26" y1="28" x2="58" y2="28"/>')
    o.append(f'<text class="sub" x="66" y="32">{T("SIGNAL")}</text>')
    o.append('<line class="pwr" x1="182" y1="28" x2="214" y2="28"/>')
    o.append(f'<text class="sub" x="222" y="32">{T("MOTOR LOOP")}</text>')

    PI = (26, 56, 408, 118)
    HB = (62, 300, 298, 122)
    PB = PI[1] + PI[3]
    o.append(f'<rect class="box" x="{PI[0]}" y="{PI[1]}" width="{PI[2]}" height="{PI[3]}" rx="6"/>')
    o.append(photo("pi.jpg", 42, 74, 104))
    o.append(f'<text class="nm" x="166" y="{PI[1]+66}">RASPBERRY PI 3</text>')

    for i, (gpio, fn) in enumerate((("GPIO 18", "RPWM &#183; 1 kHz"), ("GPIO 19", "LPWM &#183; 1 kHz"),
                                    ("GPIO 23", "R_EN"), ("GPIO 24", "L_EN"))):
        x = 112 + i * 68
        mid = (PB + HB[1]) / 2
        o.append(f'<line class="sig" x1="{x}" y1="{PB}" x2="{x}" y2="{HB[1]}"/>')
        o.append(dot(x, PB, 4) + dot(x, HB[1], 4))
        o.append(f'<text class="pin" x="{x-8}" y="{mid}" text-anchor="middle" '
                 f'transform="rotate(-90 {x-8} {mid})">{gpio}</text>')
        o.append(f'<text class="sub" x="{x+11}" y="{mid}" text-anchor="middle" '
                 f'transform="rotate(-90 {x+11} {mid})">{fn}</text>')

    o.append(f'<rect class="box" x="{HB[0]}" y="{HB[1]}" width="{HB[2]}" height="{HB[3]}" rx="6"/>')
    o.append(f'<text class="nm" x="{HB[0]+14}" y="{HB[1]+28}">BTS7960</text>')
    o.append(f'<text class="sub" x="{HB[0]+14}" y="{HB[1]+46}">H-BRIDGE</text>')
    o.append(photo("bts.jpg", 262, 316, 84))

    o.append(motor(412, 345, 31, 1.18))
    for y in (332, 358):
        o.append(f'<line class="pwr" x1="{HB[0]+HB[2]}" y1="{y}" x2="382" y2="{y}"/>')
    o.append(f'<text class="sub" x="412" y="396" text-anchor="middle">{T("DRILL")}</text>')

    CH, RTX, RET = 112, 332, 866
    INA = (62, 470, 232, 124)
    o.append(f'<line class="pwr" x1="{CH}" y1="{HB[1]+HB[3]}" x2="{CH}" y2="{INA[1]}"/>')
    o.append(f'<text class="pin" x="{CH+11}" y="{HB[1]+HB[3]+24}">B+</text>')

    o.append(f'<path class="sig" d="M42,{PB} L42,492 L{INA[0]},492"/>')
    o.append(f'<path class="sig" d="M56,{PB} L56,516 L{INA[0]},516"/>')
    o.append(dot(42, PB, 4) + dot(56, PB, 4))
    o.append('<text class="pin" x="26" y="300" text-anchor="middle" '
             'transform="rotate(-90 26 300)">I2C &#183; SDA &#183; SCL</text>')

    o.append(f'<rect class="chip" x="{INA[0]}" y="{INA[1]}" width="{INA[2]}" '
             f'height="{INA[3]}" rx="6"/>')
    o.append(f'<text class="nm" x="{INA[0]+14}" y="{INA[1]+28}">INA260</text>')
    o.append(f'<text class="sub" x="{INA[0]+14}" y="{INA[1]+46}">0x40</text>')
    o.append(photo("ina.jpg", 202, 500, 78))
    o.append(f'<text class="pin" x="{CH+11}" y="{INA[1]+INA[3]+22}">IN+</text>')

    o.append(f'<line class="pwr" x1="{CH}" y1="{INA[1]+INA[3]}" x2="{CH}" y2="616"/>')
    o.append(estop_v(CH, 640, 1.18))
    o.append(f'<text class="pin" x="{CH+46}" y="636">{T("EMERGENCY")}</text>')
    # A language whose marking is one word leaves the second line empty.
    if T("STOP"):
        o.append(f'<text class="pin" x="{CH+46}" y="654">{T("STOP")}</text>')
    o.append(f'<line class="pwr" x1="{CH}" y1="672" x2="{CH}" y2="704"/>')
    o.append(f'<g transform="rotate(90 {CH} 722)">{fuse(CH, 722, 1.18)}</g>')
    o.append(f'<text class="val" x="{CH+32}" y="726">15 A</text>')
    o.append(f'<line class="pwr" x1="{CH}" y1="740" x2="{CH}" y2="760"/>')

    PSU = (58, 760, 176, 70)
    o.append(supply(*PSU, s=1.18, mains_left=False))
    o.append(f'<line class="sig" x1="{PSU[0]+PSU[2]}" y1="{PSU[1]+42}" '
             f'x2="{PSU[0]+PSU[2]+34}" y2="{PSU[1]+42}"/>')
    # Above the lead and anchored to the box, the way the wide drawing does it.
    # Sitting on the lead, the word ran towards the motor return wire at x 332
    # and how near it came depended on its length. The Filipino KURYENTE is
    # 69 px here against the English MAINS at 44, and it was drawn straight
    # through the wire. The French SECTEUR touched it. Both were published.
    # There is 79 px of room now and the longest of the twenty asks for 69.
    o.append(f'<text class="sub" x="{PSU[0]+PSU[2]+10}" y="{PSU[1]+31}">'
             f'{T("MAINS")}</text>')
    o.append(f'<text class="val" x="{CH+13}" y="{PSU[1]-8}">+</text>')
    o.append(f'<text class="val" x="{CH+13}" y="{PSU[1]+PSU[3]+22}">&#8722;</text>')
    o.append(f'<path class="pwr" d="M{CH},{PSU[1]+PSU[3]} L{CH},{RET} L{RTX},{RET} '
             f'L{RTX},{HB[1]+HB[3]}"/>')
    o.append(f'<text class="pin" x="{RTX+11}" y="{HB[1]+HB[3]+24}">B&#8722;</text>')
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "images"), exist_ok=True)
    for LANG in LANGS:
        globals()["LANG"] = LANG
        for name, draw in (("schematic.svg", wide),
                           ("schematic-narrow.svg", narrow)):
            path = out_path(name)
            with open(path, "w") as fh:
                fh.write(draw())
            print("wrote", os.path.relpath(path, HERE))
