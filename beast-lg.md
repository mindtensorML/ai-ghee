---
output: beast-lg.html
skip_text: Genda ku bikwatibwako
lang: lg
stem: beast
locale: lg_UG
title: Ensolo &middot; Omuzigo gwa AI
description: Cordless drill, olubaawo olusalirako, hotplate ne Raspberry Pi. Buli kitundu ky'ekyuma ky'omuzigo kikola ki.
og_title: Ensolo
og_description: Cordless drill, olubaawo olusalirako ne Raspberry Pi. Buli kitundu ky'ekyuma ky'omuzigo kikola ki.
og_image: images/beast.jpg
og_url: https://mindtensorml.github.io/ai-ghee/beast-lg.html
mark: Ekyuma
nav_text: Olugero
nav_href: index-lg.html
nav_side: left
kicker: Enzimba
headline: Ensolo
standfirst: Byonna ebiri ku kyuma kino byava mu dduuka ly'ebyuma oba mu kabada k'omu ffumbiro. Buli kitundu kikola ki, kiri wano.
next_text: Ddayo ku lugero
next_href: index-lg.html
next_blurb: Amata agakutte, ekisundo, akadde omuzigo lwe gwavaayo, n'essaawa emu ng'otunuulira langi.
credit: Ebifaananyi byonna byakubibwa mu kusunda okumu mu August 2026. Ebifaananyi by'ekisundo, eby'eccupa ez'omuzigo omuweze n'eby'omulundi ogwokubiri byakubibwa oluvannyuma.
contact_text: Ebibuuzo, ensobi ze wasanze, oba nga naawe wazimba ekifaanana nga kino.
---

## Kyakolebwa ku ki

Cordless drill ekola omulimu gw'okwetooloosa. Etudde mu clamp enywezebbwa ku lubaawo olusalirako. Olubaawo lwe lukuuma byonna nga bisimbiddwa bulungi waggulu w'entamu. Omutwe gw'ekisundo gwa muti omukalubo ku muggo gwa stainless steel, nga gunywezebbwa sikuluvu so si gaamu. Eyo nsonga lwaki nnakikola nzennyini mu kifo ky'okukigula.

Electronics ziri mu ssanduuko ya pulasitiika entangaavu ey'okuterekamu emmere, okusinga olw'okusobola okulaba oba waliwo ekikwatidde omuliro. Raspberry Pi ye awandiika log. Ebbatani eddene erya kyenvu lisala amasannyalaze agagenda ku motor, era tewali kya software kisobola okulikyusa.

![Drill, olubaawo, essanduuko, ebbatani](images/beast-wide.jpg "Ekyuma ku kaawunta y'omu ffumbiro, nga kiraga drill mu clamp, olubaawo olw'omuti, essanduuko entangaavu erimu electronics ne Raspberry Pi wansi.")

| Motor | Cordless drill, nga enywezebbwa mu clamp, era nga ekola wansi nnyo w'amaanyi gaayo gonna |
| Ekisundo | Omuti omukalubo ne stainless steel, nnakikola so saakigula |
| Ebbugumu | Hotplate, nga AC regulator egikoleeza n'egizikiza |
| Omubiri | Olubaawo olusalirako n'essanduuko ya pulasitiika |
| Amasannyalaze | 12 V switch mode supply, nga eva ku kisenge |
| Obwongo | Raspberry Pi, nga awandiika mu CSV |
| Okuwulira | Current ne voltage nga kisunda, probe mu ntamu nga kifumba |
| Okuyimiriza | Ebbatani limu eddene, nga liyungibwa butereevu |

## Engeri gye kiyungibwa

Waya nnya za signal, ne loop emu ennene ya motor. Pi ye asalawo amaanyi meka n'oludda ki, H bridge ye esindika current yennyini, era ebibiri tebituukagana. Waya yonna Pi akwatako eyitamu current entonotono nnyo.

Ekitundu ekisaanira okutunuulirwa ye bbatani. Teriyungibwa ku Pi n'akatono. Libeera mu loop ya motor, era lye lisala loop, kale tewali nsobi ya software eyinza okulisendasenda obutayimirira. Kye Pi asobola kwe kukitegeera. Bw'aba asaba ebitundu 30 ku kikumi ate sensor n'eddamu n'ekiri wansi wa 200 mA, ategeera nti loop eggule. Alekera awo okusaba.

Sensor eri ku loop y'emu, naye oludda lwayo olulowooza lufuna amasannyalaze okuva ku Pi. Kyekyo ekigireetera okuddamu ne bwe supply eba nga ezikidde. Obukodyo bwonna obw'okukebera bbatani buli mu kyo.

![Enkola y'okuyungibwa](images/schematic-lg.svg "Diagram y'ekyuma ky'omuzigo. Raspberry Pi akoleeza H bridge ya BTS7960 ng'ayita mu waya nnya za signal, era asoma sensor ya current ya INA260 ng'ayita mu I2C. Supply ya 12 V, fyuuzi ya 15 A, ebbatani ery'okuyimiriza mu kabenje ne sensor byonna biyungibwa olukalala lumu mu loop ya motor, loop Pi atakwatako n'akatono.")

## Kiteekebwa wa

Waggulu wa sinki. Entamu egenda mu sinki, ekisaanikira ekitereevu ekiriko ekituli ky'omuggo kitudde waggulu, era buli kifuluma kigwa mu kifo ekitali kya nsonga.

Ekitundu kino tewali akiteeka mu bifaananyi ebirangirira. Ekitundu kimu ku bibiri eby'okuzimba ekintu mu ffumbiro kiri mu kusalawo akasasiro akakkirizibwa okugenda wa.

![Mu kifo kyakyo, nga kikola](images/rig-sink.jpg "Ekyuma nga kinywezebbwa mu kifo kyakyo waggulu wa sinki y'omu ffumbiro, nga wansi waliwo laptop eraga plots eziri mu kukola.")

## Ki kye kyetegereza

Nga kisunda, current ne voltage ku layini ya motor, nga kipima omulundi gumu buli ssekonda era nga kiwandiika butereevu mu fayiro. Nga kifumba, probe mu ntamu, era regulator ekoleeza n'ezikiza hotplate okukuuma namba.

Tewali maayikolofooni, tewali kamera, era ekyo kye kyaddako okutereezebwa. Okutuusa kaakano, nnasuubira nti omugugu gwokka bwe gusobola okuzuula omuzigo lwe guvaayo, ebirala biyinza okulindirira.

![Trace eyita mu kiseera ky'okukola](images/laptop.jpg "Skrini ya laptop eraga plots bbiri eziri mu kukola ez'ebipimo bya motor, waggulu wa terminal log egenda etambula.")

## Ki kye kisalawo

Bintu bibiri. Oba omugugu gulinnye n'oluvannyuma gugudde okumala okukakasa nti omuzigo gwavuddeyo, n'oba hotplate erina kukoleezebwa oba kuzikizibwa okusigala ku 250 F.

Tekimanyi amata agakutte. Tekimanyi n'omuzigo. Ekimanyi kiri nti namba yalinnya okumala akadde, oluvannyuma n'egwa, era nti enkula eyo etegeeza nti omulimu guweze.

![Enkula eyo kye kikola](images/batch-big.jpg "Eccupa bbiri empanvu z'omuzigo ogukutte ogwa kyenvu okumpi n'omweru, nga zirina ebisaanikira ebizingibwa n'ebipande ebitangaavu, nga ziyimiridde ku lubaawo lw'olubalaza, n'eccupa entono ez'ebisaanikira ebikwata nga zitalabika bulungi emabega.")
