---
output: beast-de.html
title: Das Biest &middot; Ghee, von einer KI gemacht
description: Ein Akkuschrauber, ein Schneidebrett, eine Kochplatte und ein Raspberry Pi. Was jedes Teil des Ghee-Aufbaus tut.
og_title: Das Biest
og_description: Ein Akkuschrauber, ein Schneidebrett und ein Raspberry Pi. Was jedes Teil des Ghee-Aufbaus tut.
schema_image: images/beast.jpg
og_image_alt: Die Ghee-Maschine, beschriftet mit KI macht Ghee
og_image: images/card-de.jpg
og_url: https://mindtensorml.github.io/ai-ghee/beast-de.html
skip_text: Zum Inhalt springen
lang: de
stem: beast
locale: de_DE
mark: Die Maschine
nav_text: Die Geschichte
nav_href: index-de.html
nav_side: left
kicker: Der Aufbau
headline: Das Biest
standfirst: Alles an diesem Aufbau kam aus dem Baumarkt oder aus einer Küchenschublade. Hier steht, was jedes Teil tatsächlich tut.
next_text: Zurück zur Geschichte
next_href: index-de.html
next_blurb: Joghurt, der Quirl, der Bruch, und eine Stunde lang der Farbe zusehen.
credit: Die Fotos stammen alle aus einem einzigen Durchlauf im August 2026. Der Quirl, die fertigen Gläser und die zweite Charge wurden später fotografiert.
contact_text: Fragen, Korrekturen, oder Sie haben selbst so etwas gebaut.
---

## Woraus sie besteht

Ein Akkuschrauber übernimmt das Drehen. Er sitzt in einer Klemme, die auf ein Schneidebrett geschraubt ist, und das Brett hält alles über dem Topf in einer Flucht. Der Quirlkopf ist Hartholz auf einer Stahlwelle, geschraubt statt geklebt, und genau deshalb habe ich ihn gebaut statt gekauft.

Die Elektronik wohnt in einer durchsichtigen Frischhaltedose, vor allem damit ich sehen kann, ob etwas Feuer gefangen hat. Ein Raspberry Pi übernimmt die Aufzeichnung. Der große gelbe Knopf trennt den Strom zum Motor, und keine Software darf ihn überstimmen.

![Akkuschrauber, Brett, Dose, Knopf](images/beast-wide.jpg "Der Aufbau auf einer Küchenarbeitsfläche, mit dem Akkuschrauber in seiner Klemme, dem Holzbrett, der durchsichtigen Elektronikdose und einem Raspberry Pi am Fuß.")

| Motor | Akkuschrauber, geklemmt, läuft weit unter voller Drehzahl |
| Quirl | Hartholz und Edelstahl, gebaut statt gekauft |
| Hitze | Kochplatte, von einem Leistungsregler ein- und ausgeschaltet |
| Rahmen | Ein Schneidebrett und eine Frischhaltedose |
| Strom | Schaltnetzteil mit 12 V, aus der Steckdose |
| Hirn | Raspberry Pi, schreibt in eine CSV |
| Sinn | Strom und Spannung beim Buttern, ein Fühler im Topf beim Kochen |
| Stopp | Ein großer Knopf, fest verdrahtet |

## Wie sie verdrahtet ist

Vier Signalleitungen und ein dicker Kreis. Der Pi rechnet aus, wie stark und in welche Richtung, die H-Brücke schiebt den Strom tatsächlich, und die beiden treffen sich nie. Nichts, was der Pi berührt, führt mehr als ein paar Milliampere.

Der Knopf ist das Teil, das man sich ansehen sollte. Er ist überhaupt nicht mit dem Pi verbunden. Er sitzt im Motorkreis und trennt ihn, also kann kein Softwarefehler ihm das Anhalten ausreden. Was der Pi kann, ist es zu merken. Wenn er dreißig Prozent anfordert und der Sensor mit weniger als zweihundert Milliampere zurückkommt, schließt er daraus, dass der Kreis offen ist, und hört auf zu fordern.

Der Sensor sitzt im selben Kreis, aber seine Logikseite hängt am Pi, und deshalb antwortet er auch dann noch, wenn die Versorgung aus ist. Das ist der ganze Trick hinter der Knopfprüfung.

![Schaltplan](images/schematic-de.svg "Schaltplan des Ghee-Aufbaus. Ein Raspberry Pi steuert eine H-Brücke BTS7960 über vier Signalleitungen und liest einen Stromsensor INA260 über I2C. Ein Netzteil mit 12 V, eine Sicherung mit 15 A, der Not-Aus-Knopf und der Sensor liegen in Reihe im Motorkreis, den der Pi nie berührt.")

## Wo sie steht

Über der Spüle. Der Topf kommt ins Becken, darauf liegt ein flacher Deckel mit einem Loch für die Welle, und was entwischt, landet irgendwo, wo es nicht stört.

Das ist der Teil, den niemand in die Visualisierung packt. Die halbe Arbeit, etwas in einer Küche zu bauen, besteht darin zu entscheiden, wohin die Sauerei darf.

![In Position, mitten im Durchlauf](images/rig-sink.jpg "Der Aufbau sitzt festgeklemmt über der Küchenspüle, darunter ein Laptop mit laufenden Diagrammen.")

## Was sie beobachtet

Beim Buttern Strom und Spannung auf der Motorleitung, etwa einmal pro Sekunde abgetastet und direkt in eine Datei geschrieben. Beim Kochen stattdessen ein Fühler im Topf, und der Regler schaltet die Kochplatte zu und weg, um die Zahl zu halten.

Kein Mikrofon und keine Kamera, und das ist das Nächste, was ich ändern will. Die Wette war bisher, dass der Rest warten kann, wenn die Last allein reicht, um den Bruch zu finden.

![Die Live-Kurve während eines Durchlaufs](images/laptop.jpg "Ein Laptop-Bildschirm zeigt zwei laufende Diagramme der Motorwerte über einem scrollenden Terminal-Log.")

## Was sie entscheidet

Zwei Dinge. Ob die Last weit genug gestiegen und dann gefallen ist, um den Bruch auszurufen, und ob die Platte an oder aus sein soll, um auf 250 F zu bleiben.

Sie weiß nicht, was Joghurt ist. Sie weiß nicht, was Butter ist. Sie weiß, dass eine Zahl eine Weile lang stieg und dann abfiel, und dass diese Form bedeutet, dass die Arbeit erledigt ist.

![Wofür die Form gut ist](images/batch-big.jpg "Zwei hohe Gläser mit blassem festem Ghee, mit Schraubdeckeln und klaren Etiketten, stehen auf einem Terrassengeländer, dahinter unscharf kleinere Bügelgläser.")
