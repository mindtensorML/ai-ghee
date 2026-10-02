---
output: beast-fil.html
skip_text: Dumiretso sa nilalaman
lang: fil
stem: beast
locale: fil_PH
title: Ang Halimaw &middot; Ghee na Gawa ng AI
description: Isang cordless drill, isang sangkalan, isang hotplate at isang Raspberry Pi. Kung ano ang ginagawa ng bawat parte ng makina ng ghee.
og_title: Ang Halimaw
og_description: Isang cordless drill, isang sangkalan at isang Raspberry Pi. Kung ano ang ginagawa ng bawat parte ng makina ng ghee.
schema_image: images/beast.jpg
og_image_alt: Ang makinang gumagawa ng ghee, may nakasulat na Gumagawa ng Ghee ang AI
og_image: images/card-fil.jpg
og_url: https://mindtensorml.github.io/ai-ghee/beast-fil.html
mark: Ang makina
nav_text: Ang kuwento
nav_href: index-fil.html
nav_side: left
kicker: Ang pagbuo
headline: Ang Halimaw
standfirst: Lahat ng nasa makinang ito ay galing sa hardware o sa drawer ng kusina. Ito ang talagang ginagawa ng bawat parte.
next_text: Pabalik sa kuwento
next_href: index-fil.html
next_blurb: Yogurt, ang pambati, ang paghiwalay, at isang oras ng pagtitig sa kulay.
credit: Lahat ng larawan ay mula sa isang takbo noong Agosto 2026. Ang pambati, ang mga punong garapon at ang ikalawang batch ay kinunan nang mas huli.
contact_text: Mga tanong, mga pagwawasto, o kung may ganito ka na ring naitayo.
---

## Kung saan ito gawa

Isang cordless drill ang gumagawa ng pagpaikot. Nakaupo ito sa clamp na nabolt sa isang sangkalan, at ang sangkalan ang nagpapanatiling nakahanay ang lahat sa ibabaw ng kaldero. Ang ulo ng pambati ay matigas na kahoy sa bakal na shaft, tinurnilyo at hindi pinandikit, at iyon ang dahilan kung bakit ako gumawa kaysa bumili.

Nakatira ang electronics sa malinaw na plastik na lalagyan ng pagkain, pangunahin nang para makita ko kung may nagliyab na. Ang Raspberry Pi ang nag-aasikaso sa pagtatala. Ang malaking dilaw na pindutan ang pumapatay sa kuryente ng motor, at walang software na makapagpapawalang-bisa rito.

![Drill, sangkalan, kahon, pindutan](images/beast-wide.jpg "Ang makina sa counter ng kusina, kita ang drill sa clamp nito, ang kahoy na sangkalan, ang malinaw na kahon ng electronics at isang Raspberry Pi sa ilalim.")

| Motor | Cordless drill, nakaipit, umaandar nang mas mabagal pa sa buong bilis |
| Pambati | Matigas na kahoy at stainless, ginawa hindi binili |
| Init | Hotplate, sinisindi at pinapatay ng AC regulator |
| Balangkas | Isang sangkalan at isang plastik na lalagyan ng pagkain |
| Kuryente | 12 V switch mode supply, mula sa saksakan |
| Utak | Raspberry Pi, nagtatala sa isang CSV |
| Pandama | Kuryente at boltahe habang nagbabati, isang probe sa kaldero habang nagluluto |
| Hinto | Isang malaking pindutan, nakakabit nang tuwiran |

## Kung paano ito nakakabit

Apat na signal wire at isang matabang loop. Ang Pi ang nag-iisip kung gaano kalakas at kung saang direksyon, ang H bridge ang talagang nagtutulak ng kuryente, at hindi sila nagtatagpo kahit kailan. Wala sa hinihipo ng Pi ang may dalang higit sa ilang milliamp.

Ang pindutan ang parteng sulit tingnan. Wala talaga itong kable papunta sa Pi. Nakaupo ito sa loop ng motor at pinapatid ito, kaya walang depekto sa software ang makakakumbinsi ritong huwag tumigil. Ang kaya ng Pi ay makaalam. Kung humihingi ito ng tatlumpung porsiyento at ang isinasagot ng sensor ay mas mababa pa sa dalawang daang milliamp, nalalaman nito na bukas ang loop at tumitigil na sa paghingi.

Nasa parehong loop ang sensor pero ang logic side nito ay kumukuha ng kuryente sa Pi, at iyon ang dahilan kung bakit sumasagot pa rin ito kapag patay ang supply. Iyon ang buong diskarte sa likod ng pagsusuri sa pindutan.

![Diagram ng sirkito](images/schematic-fil.svg "Isang eskematiko ng makina ng ghee. Isang Raspberry Pi ang nagpapaandar sa BTS7960 H bridge sa apat na signal wire at nagbabasa ng INA260 current sensor sa I2C. Ang labindalawang bolt na supply, ang labinlimang amp na fuse, ang emergency stop button at ang sensor ay nakasunod-sunod sa loop ng motor, na hindi hinihipo ng Pi kahit kailan.")

## Kung saan ito nakalagay

Sa ibabaw ng lababo. Ang kaldero ay inilalagay sa loob ng lababo, may patag na takip sa itaas na may butas para sa shaft, at kung may tumalsik man ay babagsak ito sa lugar na hindi mahalaga.

Ito ang parteng walang naglalagay sa render. Kalahati ng paggawa ng kahit ano sa kusina ay ang pagpapasya kung saan puwedeng mapunta ang kalat.

![Nakapuwesto, kalahati ng takbo](images/rig-sink.jpg "Ang makina na nakaipit sa puwesto sa ibabaw ng lababo ng kusina, at may laptop sa ilalim nito na nagpapakita ng mga live na plot.")

## Ang binabantayan nito

Habang nagbabati, ang kuryente at boltahe sa linya ng motor, kinukuha nang mga isang beses kada segundo at diretsong isinusulat sa isang file. Habang nagluluto, isang probe sa kaldero ang pumapalit, at ang regulator ang sumisindi at pumapatay sa hotplate para mahawakan ang numero.

Walang mikropono at walang kamera, at iyon ang susunod kong gustong ayusin. Ang pusta hanggang ngayon ay kung sapat na ang load mag-isa para makita ang paghiwalay, makakahintay ang iba.

![Ang live na trace sa gitna ng takbo](images/laptop.jpg "Isang screen ng laptop na nagpapakita ng dalawang live na plot ng mga reading ng motor sa ibabaw ng gumugulong na terminal log.")

## Ang ipinapasya nito

Dalawang bagay. Kung umakyat na ba at pagkatapos ay bumagsak nang sapat ang load para ideklara ang paghiwalay, at kung dapat bang sindihan o patayin ang plate para manatili sa 250 F.

Hindi nito alam kung ano ang yogurt. Hindi nito alam kung ano ang mantekilya. Alam nito na may numerong umakyat nang ilang sandali at pagkatapos ay bumagsak, at ang hugis na iyon ay nangangahulugang tapos na ang trabaho.

![Para saan ang hugis](images/batch-big.jpg "Dalawang matatangkad na garapon ng maputla at namuong ghee na may pinipihit na takip at malinaw na etiketa, nakatayo sa barandilya, at may mas maliliit na de-klip na garapong malabo sa likod nila.")
