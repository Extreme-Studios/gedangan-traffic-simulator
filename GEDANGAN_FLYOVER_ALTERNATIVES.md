# Gedangan — Executable Flyover Alternatives

Dibuat dari actual outputs, 1 November 2026. Status penelitian: **belum dikalibrasi terhadap observasi Gedangan 2026**.

## Batas sumber resmi

[Pemkab22September2026](https://www.sidoarjokab.go.id/berita/detail/1790214058/0) membahas enam lajur **di bawah** flyover. [Pemkab1Oktober2026](https://www.sidoarjokab.go.id/berita/detail/1790902516/0) membahas ROW dan koordinasi lintas instansi. Angka tersebut tidak diterapkan sebagai deck lane count. Final DED, georeferenced approved alignment, lahan, clearance KAI, izin dan swept path belum tersedia/terverifikasi. Pengumuman lokasi dicatat sebagai sumber, bukan DED yang sudah didigitasi.

## Konsep executable

Keduanya **UNVERIFIED ENGINEERING CONCEPT**, hanya sensitivitas lalu lintas. A:1lane/direction; B:2lanes/direction. Ground existing2lanes/direction dipertahankan. East offset20m/35m, deckz8m (input6–10m) adalah parameter konsep, bukan clearance legal.

NB: existing approach `w562358500_s13_p0_0_f` menuju exit `w266287935_s6_p0_0_f`. SB: `w512351908_s1_p0_0_f` menuju `w562358499_s1_p0_0_f`. Enam deck/ramp edges dan empat intermediate elevated nodes; koneksi hanya di endpoint koridor yang ada. Tidak ada ramp instan ke frontage/local. Grade screen maksimum6%; geometric grade screen bukan persetujuan struktur.

Motor/car/pickup/minibus/bus/light/medium truck diizinkan dalam konsep; heavy/trailer/oversize ditolak karena special-vehicle clearance belum memadai. Rail route dan at-grade crossing tetap ada; kendaraan deck melewati level berbeda. Ground controller tetap, tidak dihapus untuk memberi keuntungan semu. Local access ground dipertahankan dalam konsep operasi; constructability belum dibuktikan.

NETCONVERT1.28.0 mengekspor ulang dengan projection/offset asli, menjaga existing edge IDs dan movements; tidak menambah existing-to-existing movement. Build manifest menyimpan parent/spec/builder hashes, commands dan screening constraints.

| Run | Network SHA256 | Actual deck vehicles | FCD max z m | Arrived | Not departed |
| --- | --- | --- | --- | --- | --- |
| morning_base | 0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c | 0 | 0 | 96 | 766 |
| flyover_A | c083d998c2d4c886dcbfb7e92efe7910a74cf5ebead1d0a0d546de07a5dbf1a3 | 769 | 8.0 | 504 | 949 |
| flyover_B | 3a7265114059147fcc508034a183a17878db8c37e3f92accd9b895f3e22f45c4 | 1084 | 8.0 | 508 | 522 |

Baseline tiba96; A504 tetapi not-departed meningkat766→949. B508 dan522not-departed. Angka ini tradeoff pada demand/controller asumsi yang sama, **bukan persentase pengurangan kemacetan Gedangan yang tervalidasi**. Kendaraan benar-benar tercatat pada deck, bukan sekadar assigned.

Manifest/network: [realism_recovery](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/simulation/network/realism_recovery>); actual route/FCD analysis: [network-impact-analysis.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/network-impact-analysis.json>). Rebuild berdasarkan request/spec dari result.json dan runner revision yang dicatat; sumber generator revisi awal diarsipkan bila berubah.

