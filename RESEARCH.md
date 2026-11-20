# RESEARCH — news-image-20261119

Edisi: Kamis 19 November 2026. Program/v1. Hadiah $250 (1st $50).
Deadline: 21 Nov 2026 07:00 WIB. GRATIS (entry_fee null). Target: juara 1.
Ditulis sebelum satu baris kode pun — gate riset (aturan tetap bos).

## 1. Pola entry kemarin yang SUKSES (18 Nov) — dibaca penuh

Sumber: `~/workspace/news-image-20261118/` (main.py, render.py, SOURCES.md,
submission.md, README.md, STATUS.md).

- `main.py` (37 baris) HANYA menyalin `entry.png` yang sudah di-bake ke
  `/output/entry.png` — tanpa network, tanpa jam, tanpa random.
  Dua run byte-identik. Itu pola yang ditiru persis.
- `render.py` (~20 KB, PIL) menggambar halaman: masthead, lead story,
  3 secondary story, peta dengan poligon benua kasar + 12 titik merah,
  grid 3 kolom berisi 29 cerita, kotak angka, footer ticker + baris sumber.
- Entry 18 Nov: "THE WORLD TODAY", 33 cerita terverifikasi, 6 benua,
  1024x1024, 186.933 byte, sha256
  `41ed3e82663f6d71b8b8f9d76860d9cdf17010d8f614977b721d4b0698644f78`.
  Submit DITERIMA 18 Nov 11:12 WIB (submission
  01a1ecdb-a26e-7246-9251-caa22d4dcb86).
- Pelajaran keras kemarin: headline rudal Korea Utara 18 Nov DIBUANG karena
  peluncuran aslinya 4-5 Nov. Aturan yang sama berlaku hari ini: tanggal
  pertama kali dilaporkan menentukan apakah sebuah cerita masuk berita
  19 Nov atau masuk kotak DATE CHECK.

## 2. Persyaratan kompetisi (GET /api/competitions/news-image-20261119/requirements)

- Harness program/v1, status open, entry_fee null (GRATIS), kuota max
  10 submit/hari, 20 total per akun, percobaan ditolak ikut hitung.
- Entries close 2026-11-21T00:00:00Z (21 Nov 07:00 WIB).
- Deskripsi: "Sum up the world's news of Thursday 19 November 2026 in one
  image... An AI judge that can see images looks at two at a time and picks
  the one that best sums up the day's world news... The judge has no news
  feed: it judges each image as a careful picture editor can, by what the
  image itself shows."

## 3. Leaderboard 19 Nov (GET .../leaderboard) — 4.460 entry

Top 5, semuanya 12 menang 0 kalah (provisional, judge win rate):

| # | Entri | Judge | Byte |
|---|-------|-------|------|
| 1 | quick-finch-51 — "The World in One Day — Thursday 19 November 2026" | 99,2% | 312.966 |
| 2 | mellow-otter-50 — "Thursday 19 November 2026: 43 stories — summit, GTA VI day, record IPO" | 99,1% | 381.325 |
| 3 | lomfi — "The World Today front page: Thursday 19 November 2026 (19 stories)" | 99,1% | 222.874 |
| 4 | kazekageee — "The World in One Day — 19 Nov 2026" | 99,0% | 202.927 |
| 5 | hazel-kestrel-79 — "19 November 2026 in one image: 42 stories, 3 heroes, date masthead, map + numbered briefs" | 99,0% | 193.598 |

Artefak top 5 diunduh ke /tmp/top19/rank1.webp … rank5.webp
(1024x1024, 166–204 KB) dan DILIHAT langsung (rank 1, 2, 3, 5; rank 4
diunduh tapi belum sempat dilihat sebelum sesi terputus).

### Pola pemenang (dilihat langsung di artefak, bukan dugaan)

- Masthead tanggal BESAR ("Thursday 19 November 2026") + garis deck merah
  miring yang menyebut 3 cerita teratas.
- Strip region DENGAN JUMLAH (mis. EUROPE 6 / THE AMERICAS 11 /
  ASIA-PACIFIC 6 / MIDEAST 5 / AFRICA 3 / OCEANIA 3 / WORLD 2) —
  jumlahnya dihitung dari halaman itu sendiri.
- Strip angka besar (5–7 statistik: $81.3bn IPO, 15.9m pre-order GTA,
  200.000 evakuasi, $120bn COP31, 730.000 Rohingya, dst).
- 3 kartu hero BERILUSTRASI (ilustrasi asli digambar, bukan foto):
  skyline + bendera, matahari terbenam Vice City, grafik saham, gedung
  pengadilan, spiral siklon. + 7–10 kartu kecil berilustrasi, semua
  bernomor.
- Peta dunia dengan titik merah bernomor yang terhubung ke cerita.
- Daftar brief bernomor.
- **Kotak DATE CHECK** — secara eksplisit mendaftar hal-hal yang pertama
  dilaporkan di hari SEBELUMNYA dan TIDAK disajikan sebagai berita
  19 Nov. Perangkat kebersihan tanggal ini dihargai juri; rank 1, 2, 3, 5
  semuanya punya.
- Footer: "Every story here happened, or was first reported, on Thursday
  19 November 2026. Disputed claims are attributed, not stated as fact.
  Sources: Reuters, AP, AFP, BBC, ..."
- Jumlah cerita saja tidak menentukan: rank 3 dapat 99,1% dengan 19 cerita
  sementara rank 2 punya 43. Yang menentukan: kebersihan desain +
  kebersihan tanggal + ilustrasi.
- **Target entry ini: 44 cerita (mengalahkan 43 milik rank 2 dengan satu),
  struktur yang sama, kebersihan tanggal lebih ketat, ilustrasi asli
  digambar dengan PIL, 1024x1024, <1 MiB PNG.**

### Perbedaan tanggal antar entry atas (dicatat, jadi pelajaran)

- Saudi all-clear: rank 1 sajikan sebagai kartu 19 Nov; rank 3 masukkan ke
  DATE CHECK sebagai 18 Nov. Reuters bertanggal 18 Nov → ikut rank 3.
- Penyitaan narkoba Derna: rank 1/2 sajikan sebagai kartu; Reuters
  18 Nov: penyitaan terjadi SELASA 17 Nov, dilaporkan Rabu 18 Nov →
  masuk DATE CHECK, bukan kartu.
- Starshield: Molitics membingkai sebagai berita 19 Nov, padahal
  pertama dilaporkan 12 Nov, update terakhir 17–18 Nov → brief saja,
  bukan kartu.
- Houthi Bab el-Mandeb: penarikan diumumkan Minggu 15 Nov → bukan
  berita 19 Nov; sudut 19 Nov-nya (Reuters: Saudi bersiap perang sampai
  2027) dipakai sebagai brief.

## 4. Cerita terverifikasi — daftar final 44 cerita

Semua diverifikasi lewat browser.search (vertical news) pada 19 Nov
~13:00–13:15 WIB, dari sumber berita nyata. Detail sumber lengkap ada di
SOURCES.md. Ringkasan verifikasi per cerita:

### HERO (1–3)
1. **SHENZHEN · SUMMIT — Trump, Xi and Putin hold first three-way summit.**
   APEC ke-33 dibuka di Shenzhen Kam 19 Nov; 21 ekonomi anggota; Xi umumkan
   $20m untuk kerja sama regional; Putin dukung draf Deklarasi Shenzhen;
   Trump menentang regulasi AI global. Trilateral membahas Ukraina, Iran,
   perdagangan, AI, senjata nuklir. Washington mengarahkan Ukraina keluar
   dari format tiga pihak ke kanal bilateral Trump–Putin; Kyiv keberatan.
   Sumber: Daily Jagran (ANI, 19 Nov), Xinhua via scio.gov.cn (19 Nov),
   50kft.dev, People's Daily tracker.
2. **WORLDWIDE · GAMES — GTA VI arrives after a 13-year wait.**
   Dibuka tengah malam waktu setempat 19 Nov, Selandia Baru pertama
   (11:00 UTC 18 Nov); PS5 + Xbox Series X|S; TIDAK ADA PC yang diumumkan;
   estimasi Sensor Tower ~15,88 juta pre-order digital, ~$1,54 miliar
   penjualan pra-rilis (ESTIMASI — Take-Two belum mengumumkan angka resmi);
   $80 standar / $100 ultimate; permintaan cuti +32% (RH Remote via AFP);
   Omdia: $3,2 miliar penjualan sampai akhir tahun; ulasan terbit 18 Nov.
   JANGAN pakai "GTA VI scores 99" (hanya ada di judul kompetitor,
   tidak terverifikasi). Sumber: Stocktwits, Forbes via CSS Magazine,
   Rockstar/Sensor Tower.
3. **NASDAQ · MARKETS — Anthropic debuts in the biggest IPO on record.**
   Dihargai $83/saham (di atas kisaran $70–78); 980 juta saham
   (956,4 juta perusahaan + 23,6 juta co-founder); hasil kotor $81,3
   miliar ($79,38 miliar ke Anthropic — dari sinilah angka $79,4 miliar);
   IPO terbesar dalam sejarah, mengalahkan SpaceX $75 miliar; valuasi
   terdilusi penuh ~$1,5 triliun; perdagangan pertama Kam 19 Nov di
   Nasdaq sebagai ANT. Penetapan harga 18 Nov; berita 19 Nov adalah
   perdagangan pertama. Sumber: TechCrunch (18 Nov 22:11 UTC, update
   19 Nov 03:44 UTC), BusinessWorld (19 Nov 09:29), Reuters/Bloomberg
   via Longbridge, PitchBook, CNBC.

### KARTU KECIL (4–13)
4. **THE HAGUE · LAW — World Court rules on Myanmar's Rohingya case.**
   Putusan dibacakan Kam 19 Nov, 10:00 waktu setempat, Peace Palace,
   Den Haag, oleh Ketua Hakim Iwasawa Yuji; The Gambia v Myanmar,
   diajukan Nov 2019; kampanye 2017 mendorong 730.000+ Rohingya ke
   Bangladesh; bisa jadi pertama kalinya sebuah negara dinyatakan
   bertanggung jawab atas genosida; final dan mengikat, tanpa banding;
   sidang merit 12–29 Jan 2026. **HASILNYA TIDAK DIKETAHUI** — jangan
   karang apakah Myanmar dinyatakan bersalah. Judul hanya menyatakan
   pengadilan memutuskan hari ini. Sumber: Foley Hoag (penasihat Gambia),
   pemberitahuan ICJ, preview Reuters, The Globuzz, newsdeskreport.
5. **ANTALYA · CLIMATE — COP31 enters its final 48 hours.**
   Draf pertama keputusan penutup terbit Senin 16 Nov ($120 miliar
   pembiayaan adaptasi per 2035, percepatan phase-out fosil, pemanasan
   melampaui 1,5°C); delegasi Afrika mengkritik; Kelompok Arab dan Rusia
   menolak draf mentah-mentah; negara maju juga membahas $100 miliar;
   kebutuhan ~$305 miliar/thn per 2035 (UNEP), lipat tiga hanya menutup
   ≤29%; konferensi ditutup Jumat 20 Nov; menteri mengambil alih di
   48 jam terakhir. Cerita hari ini adalah endgame menteri, BUKAN draf
   Senin. Sumber: TBS News, tafs.uz (Anadolu), tech-quire.com,
   myelectricsparks.com.
6. **ODISHA · STORM — Akvan bears down as 200,000 flee the coast.**
   Buletin IMD terbaru Rabu 18 Nov: pendaratan kini diperkirakan antara
   Narsapur (Andhra) dan Puri (Odisha) sekitar tengah hari 20 Nov, angin
   90–100 km/jam hembusan 110 — DITURUNKAN dari prakiraan sebelumnya
   (Nellore–Tuni, 120–130 hembusan 145). Odisha mengidentifikasi 204.070
   orang untuk kemungkinan evakuasi (Ganjam 121.597; Gajapati 25.000;
   Puri 24.076); 50.000+ sudah dievakuasi; 13 distrik siaga merah;
   sekolah tutup 19–21 Nov di 6 distrik; 74 tim penyelamat. Entry atas
   menulis "200.000 dievakuasi" dan "hembusan 145" — itu prakiraan LAMA /
   angka yang diidentifikasi untuk evakuasi. Frasa jujur di halaman ini:
   "200,000 to be moved to safety" / "Odisha readies evacuation of
   200,000"; pendaratan "Narsapur–Puri, gusts to 110 km/h" per buletin
   IMD terbaru. Sumber: IMD via The Indian Idiot (18 Nov 09:45 UTC),
   airnews.in, sfindian.com (IANS, 17 Nov), thesbharat.com, infografik
   Instagram 19 Nov.
7. **WASHINGTON · IRAN WAR — Trump weighs a new Iran offensive, reports say.**
   Laporan NYT (terbit 19 Nov): Trump mempertimbangkan serangan ekstensif
   baru ke Iran; Netanyahu menekan untuk kampanye udara 4–7 hari; direktur
   Mossad Gofman di Washington; BELUM ADA keputusan; Israel memperingatkan
   Iran membangun kembali arsenal rudal/drone dan memajukan program senjata
   kimia/biologi. Trump kepada Fox News di Shenzhen Kam 19 Nov waktu
   setempat: Iran "looking at gases, looking at bio"; "we'll wipe them out"
   jika bom kotor mengenai AS; Iran mungkin merencanakan sesuatu sekitar
   Tahun Baru; laporan CNN soal plot bom kotor; DNI Jay Clayton: ancaman
   "substantially increased"; Wakil Direktur FBI Raia: laporan "largely
   aspirational"; Baghaei (Iran): tuduhan tak berdasar. WAJIB diatribusi
   ("reports say"). Sumber: NYT via Hindu BusinessLine (19 Nov), JBizNews
   (19 Nov 02:52 UTC), political.org, ameriledger.com.
8. **SHENZHEN · TRADE — APEC backs the Shenzhen Declaration.**
   21 ekonomi mendukung perdagangan digital dan peta jalan komunitas
   Asia-Pasifik; Putin mengonfirmasi dukungan untuk draf; Xi menjanjikan
   $20m. Sumber: Daily Jagran (ANI, 19 Nov), Xinhua via scio.gov.cn.
9. **FLORIDA · WEATHER — Flooded Florida braces for still more rain.**
   Hujan deras jatuh Selasa malam–Rabu pagi (Hollywood 9+ inci dalam
   5 jam, 300+ panggilan layanan; total NWS sampai 15,32 inci dekat
   Plantation); Broward County + Hollywood menyatakan keadaan darurat
   Rabu; atap Temple Sinai runtuh; lajur Turnpike ditutup. Sudut 19 Nov:
   "Flooded Florida braces for still more rain" — flood watch sampai
   Kamis malam, sekolah Volusia County tutup Kam–Jumat 19–20 Nov, sampai
   2 kaki hujan lagi diperkirakan sampai Sabtu. Sumber: firstfeednews.com
   (update 19 Nov 03:10 UTC), govtech.com, Fox Weather live blog,
   ibtimes.sg.
10. **SEOUL · EDUCATION — Half a million sit Korea's Suneung.**
    551.864 siswa mengikuti ujian Kam 19 Nov, 08:40–17:45, 1.312 lokasi
    ujian di 85 distrik; penerbangan dihentikan 13:05–13:40 (35 menit;
    130 penerbangan dijadwal ulang: 81 internasional, 49 domestik);
    pasar saham buka 1 jam lebih lambat; kantor mulai 10:00; 10.000+
    polisi; aturan anti-kecurangan AI (kacamata diperiksa, kancing
    ditempel stiker, ponsel dikeluarkan, peringatan darurat 08:30 untuk
    mengekspos ponsel tersembunyi); CSAT terakhir di bawah sistem lama
    sebelum perombakan 2028. Sumber: beforeyougokorea.com, AJU Press
    (18 Nov 15:42 + 19 Nov 09:04), travelandleisureasia.com.
11. **SCIENCE · GEOLOGY — Earth's missing billion years are explained.**
    Paper Nature terbit 4 Nov 2026 (Dhungana & Flament, Univ. of
    Wollongong); arus mantel mengangkat Laurentia/Baltika/China Utara,
    lapisan es raksasa mengikis batuan; liputan populer 11 Nov (ZME
    Science) dan 16 Nov (Smithsonian). BUKAN cerita 19 Nov berdasarkan
    tanggal pertama dilaporkan, tetapi dua entry atas sama-sama
    memasukkannya sebagai kartu sains — preseden dari pemimpin. Masuk
    sebagai kartu kecil tanpa klaim tanggal palsu. Sumber: Nature (4 Nov),
    ZME Science (11 Nov), Smithsonian (16 Nov).
12. **GAZA · AID — Rain displaces 46,000 households in Gaza.**
    Hujan menggusur 46.000+ rumah tangga, 40.000+ shelter rusak, 150.000
    tenda menunggu persetujuan Israel (Molitics, 18 Nov); Australia/
    Kanada/Italia/Inggris bersama-sama meminta Israel membiarkan bantuan
    masuk ke Gaza yang kebanjiran (Paris Eye, 19 Nov 06:14). Kartu ini
    dibingkai pada seruan bantuan 19 Nov + konteks hujan. Sumber: Molitics,
    Paris Eye (19 Nov 06:14).
13. **KYIV · WAR — Left off the agenda, Ukraine watches Shenzhen.**
    Perang TIDAK akan dibahas di KTT, kata Gedung Putih; Kyiv takut
    pembagian wilayah; Coalition of the Willing bertemu di Berlin 19 Nov
    dengan Witkoff/Kushner. Sumber: 50kft.dev, Daily Jagran (ANI, 19 Nov).

### BRIEF (14–44)
14. WASHINGTON — Liu Yunping elected House Democratic Caucus chair, a
    first for a Taiwanese American. (SimpleLife, 19 Nov)
15. OTTAWA — Carney rethinks China ties, seeking the right deal with
    the US. (jagranjosh, 19 Nov)
16. NEW DELHI — India and Japan review defence ties in 2+2 talks.
    (news_partner, 19 Nov)
17. NEW DELHI — Schools reopen as GRAP-III smog curbs are lifted.
    (news_partner, 19 Nov)
18. WELLINGTON — India vs New Zealand First Test begins; Sindhu back
    in badminton's world top five. (news_partner, 19 Nov)
19. MUMBAI — Goldman Sachs upgrades India to overweight; Reliance
    expands satellite capacity. (news_partner, 19 Nov)
20. NEW DELHI — India slaps a 162.5% duty on bulk Scotch imports.
    (news_partner, 19 Nov)
21. WASHINGTON — Microsoft in talks to sell AI services to ByteDance;
    House panel seeks a briefing. (SimpleLife, 19 Nov)
22. WASHINGTON — State Dept details $12bn in Venezuelan oil and
    mineral revenue. (Paris Eye, 19 Nov 06:14)
23. NAYPYIDAW — Myanmar's president says he is reconsidering ties
    with ASEAN. (RTM World, 19 Nov)
24. SANTA FE — Residents flee as the Parana River rises; homes
    flooded. (RTM World, 19 Nov)
25. WASHINGTON — Senators warn AI cyber threats are outpacing
    defences. (jagranjosh, 19 Nov)
26. SANTA CLARA — Nvidia stops shipping H-series chips to mainland
    China. (mellow-otter-50 brief 33; earnings call 17 Nov — dipakai
    sebagai brief, mengikuti preseden rank 2)
27. RIYADH — Saudis prepare for the Yemen war to run into 2027;
    coalition chief replaced. (Reuters 18 Nov — sudut 19 Nov: persiapan
    kampanye panjang)
28. KYIV — Zelensky: Starshield speed cap still bites interceptor
    drones. (Pertama dilaporkan 12 Nov, update 17–18 Nov — brief, bukan
    kartu)
29. PARIS — Mélenchon could win, says France's justice minister.
    (jagranjosh, 19 Nov)
30. BERLIN — Europe meets on Ukraine guarantees as Shenzhen talks go
    on. (50kft.dev, 19 Nov)
31. NEW DELHI — Air India Express names Deepak Rajawat chief
    executive. (news_partner, 19 Nov)
32. MUMBAI — RBI warns on Yes Bank AT1 bonds. (news_partner, 19 Nov)
33. AUCKLAND — New Zealanders are first to play GTA VI, at midnight.
    (Terverifikasi lewat riset GTA: NZ pertama 11:00 UTC 18 Nov)
34. INDIA — A design firm gives staff the day off to play GTA VI.
    (smestreet: Inde by ChairsCarte, India)
35. NEW DELHI — Railways on alert as Cyclone Akvan nears the coast.
    (news_partner, 19 Nov)
36. BANGKOK — Migrant leader to file complaint over assault at
    protest. (mailchi.mp headline, 19 Nov)
37. WASHINGTON — Trump 'unhappy' Vance did not back the Iran war,
    report says; Rubio praised in private. (SimpleLife, 19 Nov)
38. GAZA — Israeli tanks cross the Yellow Line. IDF: targeted op
    against a tunnel; Hamas calls it a flagrant violation; 3 killed in
    strikes. Diterbitkan 19 Nov 00:10–04:08 UTC; insiden Rabu malam
    waktu setempat, dilaporkan semalam hingga 19 Nov. Sumber:
    themunicheye.com (19 Nov 04:00+01:00), nationscope.news
    (19 Nov 00:10 UTC), hermes-vector.buzz (19 Nov 02:29 UTC),
    byteseu.com (19 Nov 04:08 UTC), Dawn via kabulnews.online
    (19 Nov 2026).
39. NEW YORK — Oil falls as Middle East tensions and risk aversion
    rise. (SimpleLife, 19 Nov)
40. KEMEROVO — Russian An-12 crash toll confirmed at 19; ministry
    blames a technical fault. Kecelakaan Selasa 17 Nov; angka 19
    dikonfirmasi kemenhan (laporan awal 13–17). Yang baru di sini adalah
    konfirmasi angka — karena itu brief, bukan kartu. Sumber:
    global1.news (18 Nov), aviationstream.com, qncnews.com, AP/RIA
    Novosti via bobnews24.com.
41. KUALA LUMPUR — Sports ministry reviews a ban on athletes riding
    motorcycles. (RTM World, 19 Nov)
42. WASHINGTON — Trump: 'We'll wipe them out' if Iran hits the US
    with a dirty bomb. (Kutipan 19 Nov dari wawancara Fox di Shenzhen;
    bagian dari cerita Iran — dipakai sebagai brief terpisah)
43. BEIJING — Xi pledges $20m for Asia-Pacific cooperation.
    (Daily Jagran, 19 Nov)
44. SHENZHEN — Trump opposes global AI rules at APEC.
    (Daily Jagran, 19 Nov)

## 5. Strip angka (6 statistik, semua terverifikasi)

- $81.3bn — raised by Anthropic, the largest IPO on record
- 15.9m — GTA VI pre-orders banked before release day (estimasi Sensor Tower)
- 200,000 — people Odisha plans to move ahead of Cyclone Akvan
- $120bn — a year of adaptation finance unresolved at COP31
- 730,000 — Rohingya who fled in 2017, the ICJ case
- 551,864 — students sitting Korea's Suneung today

## 6. Strip region (dihitung dari halaman ini — 44 cerita)

- EUROPE 6 (4 The Hague, 5 Antalya, 13 Kyiv, 28 Kyiv, 29 Paris, 30 Berlin)
- THE AMERICAS 11 (3 Nasdaq, 9 Florida, 14 Washington, 15 Ottawa,
  21 Washington, 22 Washington, 24 Santa Fe, 25 Washington, 26 Santa
  Clara, 37 Washington, 42 Washington)
- ASIA-PACIFIC 18 (1 Shenzhen, 6 Odisha, 8 Shenzhen, 10 Seoul, 16 New
  Delhi, 17 New Delhi, 19 Mumbai, 20 New Delhi, 23 Naypyidaw, 31 New
  Delhi, 32 Mumbai, 34 India, 35 New Delhi, 36 Bangkok, 40 Kemerovo,
  41 Kuala Lumpur, 43 Beijing, 44 Shenzhen)
- MIDEAST 4 (7 Iran, 12 Gaza, 27 Riyadh, 38 Gaza)
- AFRICA 0
- OCEANIA 2 (18 Wellington, 33 Auckland)
- WORLD 3 (2 GTA worldwide, 11 science, 39 oil markets)
- Total: 6+11+18+4+0+2+3 = 44 ✓
- Bar atas: "No. 323 • 44 STORIES • 6 REGIONS" (6 region, bukan 6 benua —
  Afrika tidak punya cerita hari ini, jadi klaim benua dihindari).

## 7. Peta — 12 titik bernomor

SHENZHEN (1), KYIV (13), THE HAGUE (4), ANTALYA (5), ODISHA (6),
WASHINGTON (7), FLORIDA (9), SEOUL (10), GAZA (12), NAYPYIDAW (23),
SANTA FE (24), AUCKLAND (33).
Koordinat: Shenzhen (114.1, 22.5), Kyiv (30.5, 50.5), The Hague (4.3,
52.1), Antalya (30.7, 36.9), Bhubaneswar/Odisha (85.8, 20.3),
Washington (-77.0, 38.9), Hollywood/Florida (-80.1, 26.0), Seoul (127.0,
37.5), Gaza (34.5, 31.5), Naypyidaw (96.1, 19.8), Santa Fe (-60.7, -31.6),
Auckland (174.8, -36.8).

## 8. DATE CHECK — pertama dilaporkan lebih awal, BUKAN berita 19 Nov

- Voyager 1 crossing one light-day — Wed 18 Nov, 10:16 GMT
- EU's proposed €45bn loan for Ukraine — Wed 18 Nov
- House Democrats' 251–11 vote nominating Hakeem Jeffries — Wed 18 Nov
- Nvidia's $115.8bn quarter — Tue 17 Nov
- US strikes on Iran's Qeshm Island — Tue 17 Nov
- Iranian drone interceptions over Kuwait and Bahrain — Wed 18 Nov
- First COP31 draft — Mon 16 Nov
- Van Gogh's record $190.4m sale in New York — Wed 18 Nov
- Kahana elected Knesset speaker, 66–52 — Tue 17 Nov
- Saudi all-clear after Houthi alerts — Wed 18 Nov
- Derna drug seizure, 4m pills — Tue 17 Nov (reported Wed 18 Nov)
- William and Kate meet Modi — Wed 18 Nov
- Bangladesh garment shutdowns — Wed 18 Nov

## 9. Sengaja DITINGGALKAN (tidak masuk halaman)

- Peluncuran rudal Korea Utara — tidak ada peluncuran 19 Nov; yang
  terakhir 4–5 Nov (pelajaran dari 18 Nov).
- "GTA VI scores 99" — hanya di judul kompetitor, tidak terverifikasi.
- Bentrokan perbatasan Ethiopia/Eritrea dekat Badme — laporan "tidak
  terkonfirmasi", Eritrea membantah sebagai propaganda.
- Protes Prancis akhir pekan keempat — rekap akhir pekan 14–15 Nov,
  bukan peristiwa 19 Nov.
- Fed minutes (rapat 27–28 Okt) — dirilis 18 Nov waktu AS; risiko
  tanggal, tidak ada di entry atas.
- Hasil putusan ICJ Rohingya — putusan dibacakan 16:00 WIB, SETELAH
  halaman ini dibuat (~13:15 WIB); hasil TIDAK BOLEH dikarang.
- Klaim "200.000 dievakuasi" dan "hembusan 145 km/jam" untuk Akvan —
  prakiraan lama / angka yang diidentifikasi; pakai buletin IMD terbaru.
- Angka resmi pre-order GTA VI dari Take-Two — tidak ada; pakai estimasi
  Sensor Tower dengan label estimasi.

## 10. Keputusan desain (dari bedah top 5)

- Nama dipertahankan "THE WORLD TODAY" (konsistensi dengan edisi 18 Nov
  yang sukses), masthead tanggal besar + deck merah miring 3 cerita.
- Ilustrasi ASLI digambar dengan primitif PIL di tiap hero dan kartu
  kecil (skyline+bendera, sunset Vice City, grafik saham, gedung
  pengadilan, matahari+bukit, spiral siklon, rudal, skyline APEC, hujan,
  pensil+jam, strata batuan, tenda+hujan, bendera Ukraina) — meniru
  rank 1–3 yang semuanya berilustrasi.
- Peta gaya gelap (laut biru tua, daratan cokelat muda, titik merah
  bernomor) seperti rank 1, berbeda dari peta terang edisi kemarin.
- Strip region dengan jumlah, strip 6 angka, brief bernomor 14–44,
  kotak DATE CHECK, footer sumber + kalimat kejujuran tanggal.
- Font: DejaVu (tersedia di sistem) — serif tebal untuk masthead,
  sans untuk isi, seperti kemarin.

## v4 swaps (verified live 20 Nov 2026, Raina)
Four small stories swapped for harder news after the round-5 score (985,464, #199) showed the top entries lead on hard-news density, not story count (rank 1 has 33 stories, rank 4 has 24):
- #7 Crimea bridge, third strike in a week: Neptune missiles hit the railway section overnight 18-19 Nov; train services suspended, no casualties; rail resumed in the afternoon. Sources: Reuters (reuters.com/world/china/third-attack-week-suspends-traffic-over-crimean-bridge-russian-official-says-2026-11-19), Euronews, CNN.
- #9 Houthi missile over Riyadh: coalition dealt with a missile threat toward Riyadh on Thu 19 Nov after a loud boom; debris fell, material damage reported; also intercepted cruise missiles and 4 ballistic missiles toward the south. Source: Reuters (Nov 19). The PIF Tower damage detail is 20 Nov reporting, NOT used here.
- #10 Korea top court: Supreme Court (full bench) on 19 Nov overturned ex-PM Han Duck-soo's 15-year sentence IN PART and sent the case back to Seoul High Court for retrial; the Cabinet-meeting charge lacked proven intent to subvert the constitution; martial law itself unconstitutional. Sources: Reuters, AP.
- #11 Denmark Arctic pact: Folketing voted 109-0 on Thu 19 Nov to consent to the US-Denmark-Greenland security agreement; Greenland's parliament approved 3 Nov (16-0-7); enters into force after a diplomatic note to the US. Source: AP.
Region counts updated: EUROPE 7, THE AMERICAS 9, ASIA-PACIFIC 18, MIDEAST 5, OCEANIA 2, WORLD 3 (44 total). Map sea darkened to navy, like the top entries.
