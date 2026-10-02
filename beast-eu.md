---
output: beast-eu.html
title: Piztia &middot; Adimen artifizialak egindako ghee
description: Bateriazko zulagailu bat, ebakitzeko ohol bat, plaka elektriko bat eta Raspberry Pi bat. Ghee egiteko makinaren zati bakoitzak zer egiten duen.
og_title: Piztia
og_description: Bateriazko zulagailu bat, ebakitzeko ohol bat eta Raspberry Pi bat. Ghee egiteko makinaren zati bakoitzak zer egiten duen.
schema_image: images/beast.jpg
og_image_alt: Ghee egiteko makina, AAk egina Ghee hitzekin
og_image: images/card-eu.jpg
og_url: https://mindtensorml.github.io/ai-ghee/beast-eu.html
skip_text: Edukira joan
lang: eu
stem: beast
locale: eu_ES
mark: Makina
nav_text: Istorioa
nav_href: index-eu.html
nav_side: left
kicker: Eraikuntza
headline: Piztia
standfirst: Makina honetan dagoen guztia burdindegi batetik edo sukaldeko tiradera batetik atera da. Hona hemen zati bakoitzak benetan zer egiten duen.
next_text: Istoriora itzuli
next_href: index-eu.html
next_blurb: Jogurta, irabiagailua, haustura, eta ordu bat kolorea begiratzen.
credit: Argazkiak saio bakar batekoak dira, 2026ko abuztukoak. Irabiagailua, poto beteak eta bigarren sorta geroago atera ziren.
contact_text: Galderak, zuzenketak, edo zuk zeuk horrelako bat eraiki duzu.
---

## Zerez dago eginda

Biratzen duena bateriazko zulagailu bat da. Ebakitzeko ohol bati torlojuz lotutako estukailu batean dago, eta oholak mantentzen du dena lapikoaren gainean lerrokatuta. Irabiagailuaren burua zur gogorrezkoa da, altzairuzko ardatz baten gainean, torlojuz muntatua eta ez itsatsia, eta hori da erosi beharrean neuk egiteko arrazoia.

Elektronika plastikozko janari-ontzi garden batean bizi da, batez ere zerbaitek su hartu duen ikusteko. Erregistroaz Raspberry Pi bat arduratzen da. Botoi hori handiak motorraren korrontea eteten du, eta softwareak ez du hori baliogabetzeko modurik.

![Zulagailua, ohola, kutxa, botoia](images/beast-wide.jpg "Makina sukaldeko mahaigainean, zulagailua bere estukailuan, egurrezko ohola, elektronikaren kutxa gardena eta Raspberry Pi bat oinarrian.")

| Motorra | Bateriazko zulagailua, estututa, abiadura osotik oso behera |
| Irabiagailua | Zur gogorra eta altzairu herdoilgaitza, egina eta ez erosia |
| Beroa | Plaka elektrikoa, erregulagailu batek piztu eta itzalita |
| Egitura | Ebakitzeko ohol bat eta plastikozko janari-ontzi bat |
| Elikadura | 12 V-ko iturri komutatua, hormatik |
| Burmuina | Raspberry Pi, CSV batean erregistratzen |
| Zentzumena | Korrontea eta tentsioa irabiatzean, zunda bat lapikoan egostean |
| Gelditzea | Botoi handi bat, zuzenean kableatua |

## Nola dago kableatuta

Lau seinale-kable eta begizta lodi bat. Pi-ak kalkulatzen du zenbat indarrez eta zein aldera, H zubia da korrontea benetan bultzatzen duena, eta biek ez dute inoiz bat egiten. Pi-ak ukitzen duen ezerk ez du miliampere gutxi batzuk baino gehiago eramaten.

Botoia da begiratzea merezi duen zatia. Ez dago Pi-ari kableatuta inondik ere. Motorraren begiztan dago eta begizta hori eteten du, beraz softwareko akats batek ezin du konbentzitu ez gelditzeko. Pi-ak egin dezakeena konturatzea da. Ehuneko hogeita hamar eskatzen ari bada eta sentsoreak berrehun miliampere baino gutxiago ematen badu, begizta irekita dagoela ondorioztatzen du eta eskatzeari uzten dio.

Sentsorea begizta berean dago, baina bere alde logikoa Pi-tik elikatzen da, eta horregatik erantzuten du oraindik elikadura itzalita dagoenean. Horretan datza botoiaren egiaztapenaren truku osoa.

![Zirkuituaren eskema](images/schematic-eu.svg "Ghee egiteko makinaren zirkuitu-eskema. Raspberry Pi batek BTS7960 H zubi bat gidatzen du lau seinale-kableren bitartez eta INA260 korronte-sentsore bat irakurtzen du I2C bidez. 12 V-ko iturri bat, 15 A-ko fusible bat, larrialdiko gelditze-botoia eta sentsorea seriean daude motorraren begiztan, eta Pi-ak ez du inoiz ukitzen.")

## Non jartzen da

Harraskaren gainean. Lapikoa harraskaren barruan doa, gainean estalki lau bat jartzen da ardatzarentzat zulo bat eginda, eta ihes egiten duen guztia inporta ez duen toki batera erortzen da.

Hau da inork 3D irudietan jartzen ez duen zatia. Sukaldean zerbait eraikitzearen erdia zikinkeria nora joan daitekeen erabakitzea da.

![Kokatuta, saioaren erdian](images/rig-sink.jpg "Makina posizioan estututa sukaldeko harraskaren gainean, azpian ordenagailu eramangarri bat zuzeneko grafikoak erakusten.")

## Zer zaintzen du

Irabiatzen ari denean, korrontea eta tentsioa motorraren linean, segundoko behin inguru neurtuta eta zuzenean fitxategi batera idatzita. Egosten ari denean, horren ordez zunda bat lapikoan, eta erregulagailuak plaka sartu eta kentzen du zenbakiari eusteko.

Mikrofonorik ez eta kamerarik ez, eta hori da konpondu nahi dudan hurrengo gauza. Orain arteko apustua zen kargak berak bakarrik haustura topatzeko balio badu, gainerakoa zain egon daitekeela.

![Zuzeneko trazua saio batean](images/laptop.jpg "Ordenagailu eramangarriaren pantaila, motorraren irakurketen bi grafiko zuzenean, azpian terminaleko erregistro bat pasatzen.")

## Zer erabakitzen du

Bi gauza. Karga nahikoa igo eta gero nahikoa jaitsi den, haustura dela esateko, eta plaka piztuta edo itzalita egon behar duen 250 F-tan egoteko.

Ez daki zer den jogurta. Ez daki zer den gurina. Badaki zenbaki bat igo zela tarte batez eta gero behera joan zela, eta forma horrek lana eginda dagoela esan nahi duela.

![Zertarako da forma hori](images/batch-big.jpg "Ghee zurbil eta gatzatuz beteta bi poto altu, torloju-tapekin eta etiketa gardenekin, terrazako eskudel baten gainean, atzean klip-itxieradun poto txikiagoak lauso.")
