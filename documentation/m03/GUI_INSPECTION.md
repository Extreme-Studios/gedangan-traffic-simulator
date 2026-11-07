# Pemeriksaan desktop SUMO — 31 Oktober 2026

SUMO-GUI 1.28.0 membuka `strict/inspect.sumocfg`. NETEDIT 1.28.0 membuka `provisional/network.net.xml` bersama `rail-reference.add.xml`. Keduanya berasal dari toolchain portable M02 yang sama. Judul window dan tampilan jaringan diperiksa langsung; load selesai tanpa fatal error. Tidak ada playback, demand atau perubahan/simpan network dari GUI.

Screenshot `sumo-gui-strict.jpg` dan `netedit-provisional-context.jpg` merekam tampilan aplikasi aktual. Koridor utama, jalur frontage yang sejajar, cabang pengumpan, konteks simpang dan referensi rel/crossing terlihat pada overview. Boundary mengikuti data sumber yang dikonversi; pasangan node sumber yang sedikit melewati area seleksi dipertahankan.

Pemeriksaan overview bukan validasi setiap lane connector atau legalitas belok. Arah edge, from/to, whitelist koneksi aktual dan identitas sumber diperiksa lebih rinci melalui XML, automated tests dan viewer browser. Warning radius/angle, connector belok yang saling berpotongan serta koneksi masuk/keluar yang ditahan tetap unresolved dan tersimpan dalam log NETCONVERT. Tidak ada klaim validasi lapangan.
