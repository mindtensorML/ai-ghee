---
output: beast-tr.html
title: Canavar · Yapay zekânın yaptığı ghee
description: Akülü bir matkap, bir kesme tahtası, elektrikli bir ocak ve bir Raspberry Pi. Ghee düzeneğinin her parçası ne yapıyor.
og_title: Canavar
og_description: Akülü bir matkap, bir kesme tahtası ve bir Raspberry Pi. Ghee düzeneğinin her parçası ne yapıyor.
schema_image: images/beast.jpg
og_image_alt: Ghee makinesi, üzerinde Yapay zekâdan Ghee yazısıyla
og_image: images/card-tr.jpg
og_url: https://mindtensorml.github.io/ai-ghee/beast-tr.html
skip_text: İçeriğe geç
lang_label: Dil
lang: tr
stem: beast
locale: tr_TR
mark: Makine
nav_text: Hikâye
nav_href: index-tr.html
nav_side: left
kicker: Yapım
headline: Canavar
standfirst: Bu düzenekteki her şey ya bir hırdavatçıdan ya da bir mutfak çekmecesinden geldi. Her parçanın gerçekte ne yaptığı burada yazıyor.
next_text: Hikâyeye dön
next_href: index-tr.html
next_blurb: Yoğurt, yayık, kopma ve bir saat boyunca renge bakmak.
credit: Fotoğrafların tamamı 2026 Ağustos'undaki tek bir çalışmadan. Yayık, dolu kavanozlar ve ikinci parti sonradan çekildi.
contact_text: Sorular, düzeltmeler, ya da siz de böyle bir şey yaptıysanız.
---

## Nelerden yapıldığı

Çevirme işini akülü bir matkap yapıyor. Kesme tahtasına vidalanmış bir mengenenin içinde duruyor, tahta da her şeyi tencerenin üzerinde hizada tutan parça. Yayık kafası çelik bir mil üzerinde sert ahşap, tutkalla değil vidayla birleştirildi, onu satın almak yerine kendim yapmamın sebebi de tam olarak bu.

Elektronik şeffaf plastik bir saklama kabının içinde yaşıyor, çoğunlukla bir şeyin alev alıp almadığını görebilmem için. Kaydı bir Raspberry Pi tutuyor. Büyük sarı düğme motora giden akımı kesiyor ve yazılımdaki hiçbir şey onu geçersiz kılamıyor.

![Matkap, tahta, kutu, düğme](images/beast-wide.jpg "Mutfak tezgahındaki düzenek, mengenesindeki matkap, ahşap tahta, şeffaf elektronik kutusu ve en altta bir Raspberry Pi görünüyor.")

| Motor | Akülü matkap, mengeneli, tam hızın çok altında çalışıyor |
| Yayık | Sert ahşap ve paslanmaz çelik, satın alınmadı yapıldı |
| Isı | Elektrikli ocak, bir güç regülatörüyle açılıp kapanıyor |
| İskelet | Bir kesme tahtası ve bir plastik saklama kabı |
| Güç | 12 V anahtarlamalı güç kaynağı, prizden |
| Beyin | Raspberry Pi, bir CSV dosyasına kaydediyor |
| Algı | Yayıklamada akım ve gerilim, pişirmede tencerede bir sonda |
| Durdurma | Tek büyük düğme, sabit kablolu |

## Nasıl bağlandığı

Dört sinyal kablosu ve bir kalın güç devresi. Pi ne kadar sert ve hangi yöne diye hesaplıyor, akımı gerçekte iten şey H köprüsü. İkisi hiç buluşmuyor. Pi'nin dokunduğu hiçbir şey birkaç miliamperden fazlasını taşımıyor.

Düğme bakmaya değer parça. Pi'ye hiç bağlı değil. Motor devresinin üzerinde duruyor ve devreyi kesiyor, yani hiçbir yazılım hatası onu durmamaya ikna edemiyor. Pi'nin yapabildiği şey bunu fark etmek. Yüzde otuz istiyorsa ve sensörden iki yüz miliamperden azı dönüyorsa, devrenin açık olduğunu anlayıp istemeyi bırakıyor.

Sensör aynı devrenin üzerinde ama mantık tarafı Pi'den besleniyor, kaynak kapalıyken bile cevap vermesinin sebebi bu. Düğme kontrolünün arkasındaki bütün numara da bu.

![Devre şeması](images/schematic-tr.svg "Ghee düzeneğinin devre şeması. Bir Raspberry Pi, dört sinyal kablosu üzerinden BTS7960 H köprüsünü sürüyor ve INA260 akım sensörünü I2C üzerinden okuyor. 12 V güç kaynağı, 15 A sigorta, acil durdurma düğmesi ve sensör, Pi'nin hiç dokunmadığı motor devresinde seri olarak duruyor.")

## Nerede durduğu

Lavabonun üstünde. Tencere gözün içine giriyor, üstüne mil için delik açılmış düz bir kapak oturuyor, kaçan her şey de önemsiz bir yere düşüyor.

Bu, kimsenin görsele koymadığı kısım. Bir mutfakta bir şey yapmanın yarısı, pisliğin nereye gitmesine izin verildiğine karar vermek.

![Yerinde, çalışmanın ortasında](images/rig-sink.jpg "Mutfak lavabosunun üzerine kelepçelenmiş düzenek, altında canlı grafikleri gösteren bir dizüstü bilgisayar.")

## Neyi izlediği

Yayıklarken motor hattındaki akım ve gerilim, saniyede bir kez örneklenip doğrudan bir dosyaya yazılıyor. Pişirirken onun yerine tencerede bir sonda var, regülatör de sayıyı tutmak için ocağı devreye alıp çıkarıyor.

Mikrofon yok, kamera yok. Düzeltmek istediğim ilk şey de bu. Şimdiye kadarki bahis şuydu, yük tek başına kopmayı bulmaya yetiyorsa gerisi bekleyebilir.

![Çalışma sırasında canlı eğri](images/laptop.jpg "Bir dizüstü bilgisayar ekranında, kayan terminal kaydının üstünde motor ölçümlerinin iki canlı grafiği.")

## Neye karar verdiği

İki şey. Yükün kopmayı ilan etmeye yetecek kadar yükselip sonra düşüp düşmediği. Bir de plakanın 250 F'de kalmak için açık mı kapalı mı olması gerektiği.

Yoğurdun ne olduğunu bilmiyor. Tereyağının ne olduğunu bilmiyor. Bir sayının bir süre yükseldiğini sonra geri düştüğünü biliyor. Bu biçimin işin bittiği anlamına geldiğini de biliyor.

![Biçim ne işe yarıyor](images/batch-big.jpg "Vida kapaklı ve şeffaf etiketli, soluk donmuş ghee dolu iki uzun kavanoz bir teras korkuluğunda duruyor, arkalarında bulanık küçük mandal kapaklı kavanozlar var.")
