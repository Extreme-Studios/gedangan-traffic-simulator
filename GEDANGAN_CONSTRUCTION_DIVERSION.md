# Gedangan — Construction and Diversion

Dibuat dari actual outputs, 1 November 2026. Status penelitian: **belum dikalibrasi terhadap observasi Gedangan 2026**.

## Parameter dan batas

S07 one_lane menutup satu lane; full_closure menutup seluruh edge uji `w512351908_s3_p0_0_f`. Custom closed_edge harus existing ordinary road. Connection/lane/via permissions dipersempit, tidak dibuat jalan pengalihan baru. Work zone ini skenario teknis, bukan approved construction traffic management plan. Worksite detail, temporary signage, ROW, KAI agreement dan akses persil lapangan belum cukup.

Izin kelas dan conditional access tetap berlaku. Frontage bukan kapasitas tak terbatas; kendaraan berat yang tidak memenuhi screen tetap ditolak. Local access di graph lain dipertahankan, tetapi akses langsung pada edge yang ditutup dapat tidak terlayani dan dicatat.

| State | Requested | Routed | Failed | Arrived | Not departed |
| --- | --- | --- | --- | --- | --- |
| before | 1938 | 1920 | 18 | 96 | 766 |
| one_lane | 1938 | 1920 | 18 | 95 | 1043 |
| full_closure | 1938 | 1844 | 94 | 48 | 847 |
| post_concept_A | 1938 | 1920 | 18 | 504 | 949 |

Full closure: **884 rerouted, 76 lost routes**, gagal total94 (baseline18). Tidak seluruh overflow bisa dialihkan legal.

Triplet [construction-triplet.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/construction-triplet.json>) memuat 1832 kendaraan dengan route before/during/after berubah, origin/destination/class, additional distance, transferred assigned volume per existing alternative edge. Added actual travel time hanya bila kendaraan yang sama tiba pada kedua run; lainnya null+censored. Free-flow additional cost tidak disamakan dengan actual travel-time gain.

Volume assigned per edge bukan kendaraan unik seluruh network. Actual entered volume tersedia di edge-impact dan per-vehicle traces. Post-construction adalah executable concept A, bukan rancangan operasi resmi.

