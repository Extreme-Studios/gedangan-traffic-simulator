# STORAGE AUDIT AFTER
| Category | Bytes | GiB |
|---|---:|---:|
| Workspace BEFORE | 19,856,241,289 | 18.493 |
| Workspace AFTER | 15,921,890,998 | 14.828 |
| Actual files deleted | 3,998,478,872.0 | 3.724 |
| Net reduction incl new audit/QA | 3,934,350,291 | 3.664 |
| Retained research (simulation/geodata/data) | 12,511,771,516 | 11.652 |
| Source Git allowlist | 4,121,399 | 0.004 |
| Application runtime payload | 138,561,597 | 0.129 |
| Unpacked canonical release | 174,105,704 | 0.162 |
| Presentation documents | 6,042,934 | 0.006 |
| Separate Full HD video | 23,935,211 | 0.022 |
| Portable ZIP | 149,515,535 | 0.139 |

Reduction: 19.81% net. 8,075 file benar-benar dihapus. Ukuran logis byte isi file, bukan allocated clusters/free-space Windows. Junction eksternal tidak diikuti atau dihapus. Folder bertingkat saling mencakup. BEFORE tidak memasukkan script audit baru; AFTER memasukkan seluruh bukti audit/QA baru, sehingga net reduction lebih kecil dari bytes deleted. Pengukuran diambil tepat sebelum penulisan laporan ini; hanya pertumbuhan kecil teks laporan/JSON setelah titik ukur yang terpisah.

## Deleted categories
| Category | Bytes | GiB |
|---|---:|---:|
| Chart authoring scratch | 11,627,241 | 0.011 |
| Generated Python/Vite cache | 47,788,886 | 0.045 |
| Obsolete reproducible package ZIPs | 367,348,048 | 0.342 |
| Disposable extracted smoke-test copies | 734,227,199 | 0.684 |
| Intermediate executable build | 56,460,008 | 0.053 |
| Unused duplicate publicDir assets | 2,296,034,466 | 2.138 |
| Duplicate task-local FFmpeg | 484,993,024 | 0.452 |

## Remaining largest 20 folders
| Remaining folder | Bytes | GiB | % workspace |
|---|---:|---:|---:|
| simulation | 12,477,966,162 | 11.621 | 78.37% |
| simulation/runs | 12,282,127,359 | 11.439 | 77.14% |
| simulation/runs/m08 | 6,169,411,073 | 5.746 | 38.75% |
| simulation/runs/m07 | 3,088,589,130 | 2.876 | 19.40% |
| simulation/runs/m051 | 1,951,556,333 | 1.818 | 12.26% |
| frontend | 1,272,494,026 | 1.185 | 7.99% |
| simulation/runs/m05 | 922,252,962 | 0.859 | 5.79% |
| documentation | 831,071,263 | 0.774 | 5.22% |
| documentation/m051 | 663,370,328 | 0.618 | 4.17% |
| toolchain | 606,295,443 | 0.565 | 3.81% |
| frontend/public | 560,465,172 | 0.522 | 3.52% |
| frontend/dist-m05 | 439,932,579 | 0.410 | 2.76% |
| frontend/dist-m05/m05 | 439,192,859 | 0.409 | 2.76% |
| frontend/public/m05 | 439,192,859 | 0.409 | 2.76% |
| toolchain/sumo-win64-1.28.0 | 420,879,809 | 0.392 | 2.64% |
| simulation/runs/m08/9c9e07a0a18d0cfec64f | 361,087,904 | 0.336 | 2.27% |
| FINAL_RELEASE | 323,622,091 | 0.301 | 2.03% |
| simulation/runs/m051/F_high_signal_seed42 | 298,805,387 | 0.278 | 1.88% |
| simulation/runs/m051/F_high_signal_seed43 | 268,764,825 | 0.250 | 1.69% |
| presentation_demo | 263,908,430 | 0.246 | 1.66% |

## Regression
338 functional tests pass / 339 run; 1 service-dependent skip. Five old complete-workspace hash checks explicitly replaced by maintenance retained-file hashes, not silently passed. 21,990 surviving baseline files match SHA256; 5,072 source/input files and 4,710 research files unchanged. 866 final release manifest members match. Actual EXE, external-network-blocked Chrome, 23 indexes/chunks, playback, year/growth, split, signal/rail, presentation, exports, survey browser persistence and host restart/clean shutdown PASS. Main user workspace never used for test fixtures.

## Remaining release hygiene limitation
Two upstream pytest-only source data files, 1,106 bytes, remain in the frozen release. Automatic approval review rejected their additional removal with reason "blocked by policy". No workaround/retry. EXE, runtime manifests and canonical ZIP remain unchanged. No venv/node_modules/developer SDK/browser cache/QA database is shipped. QA_EVIDENCE remains deliberately shipped evidence, not test execution dependency.
