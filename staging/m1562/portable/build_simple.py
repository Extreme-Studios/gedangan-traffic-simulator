"""Build the Windows x64 portable distribution using the local project runtime."""
import json
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
NAME = "GEDANGAN_TRAFFIC_SIMULATOR_SIMPLE_20K_PORTABLE"


def copy(source, destination, excluded=()):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", *excluded))
    else:
        shutil.copy2(source, destination)


def main():
    parent = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "FINAL_RELEASE"
    release = parent / NAME
    app = release / "App"
    app.mkdir(parents=True, exist_ok=True)
    paths = [
        "backend", "frontend/dist-simple", "configuration",
        "simulation/network/m051/provisional/network.net.xml",
        "simulation/network/m051/provisional/rail-provenance.json",
        "simulation/network/m155/provisional/network.net.xml",
        "simulation/network/m045/provisional/inspection.json",
        "simulation/network/m03/strict/source-to-edge.json",
        "simulation/network/m03/provisional/source-to-edge.json",
        "simulation/demand/m04/od-matrix.fixture.json",
        "documentation/simple/scene.json", "documentation/m155/technical-map.json",
        "documentation/m155/network-reality-audit.json", "documentation/m155/edge-inspection",
    ]
    for path in paths:
        copy(ROOT / path, app / path)
    home = Path(sys.base_prefix)
    python = app / "Python"
    for name in ("python.exe", "python3.dll", "python312.dll", "vcruntime140.dll",
                 "vcruntime140_1.dll", "LICENSE.txt", "DLLs", "Lib"):
        copy(home / name, python / name, ("site-packages", "ensurepip", "test", "tests"))
    site = Path(sysconfig.get_path("purelib"))
    packages = ("attr", "attrs", "jsonschema", "jsonschema_specifications",
                "referencing", "rpds", "typing_extensions")
    for path in site.iterdir():
        if any(path.name == name or path.name.startswith((name + "-", name + "."))
               for name in packages):
            copy(path, python / "Lib/site-packages" / path.name)

    sumo = Path("toolchain/sumo-win64-1.28.0")
    for name in ("LICENSE", "NOTICE.md", "AUTHORS", "data/xsd", "tools/traci", "tools/sumolib", "bin/sumo.exe"):
        copy(ROOT / sumo / name, app / sumo / name)
    for dll in (ROOT / sumo / "bin").glob("*.dll"):
        copy(dll, app / sumo / "bin" / dll.name)
    copy(HERE / "host_simple.py", app / "host.py")
    launcher = release / "GEDANGAN_TRAFFIC_SIMULATOR.exe"
    compiler = Path("C:/Windows/Microsoft.NET/Framework64/v4.0.30319/csc.exe")
    subprocess.run([str(compiler), "/nologo", "/target:winexe", "/platform:x64",
                    "/reference:System.Windows.Forms.dll", "/out:" + str(launcher),
                    str(HERE / "Launcher.cs")], check=True)
    (release / "BACA_DULU.txt").write_text(
        "GEDANGAN TRAFFIC SIMULATOR SIMPLE20K - WINDOWS x64 PORTABLE\n\n"
        "1. Ekstrak seluruh ZIP ke folder yang dapat ditulis.\n"
        "2. Klik dua kali GEDANGAN_TRAFFIC_SIMULATOR.exe.\n"
        "3. Dashboard terbuka di browser default. Gunakan Chrome atau Edge dengan WebGL2.\n"
        "4. Isi Jumlah kendaraan (1 sampai 20.000), lalu klik Jalankan simulasi. Komposisi otomatis untuk satu jam.\n"
        "5. Tunggu simulasi selesai sebelum menutup launcher dengan tombol Tutup Simulator.\n\n"
        "Python dan SUMO 1.28.0 ada dalam paket. Hasil baru tersimpan di App/simulation/runs/simple.\n"
        "Komposisi asumsi: Motor 65%, Mobil 22%, Angkot 6%, Truk ringan 4%, Truk berat 2%, Trailer 1%. Angkot memakai model van. Pejalan kaki belum tersedia karena belum ada jalur legal.\n"
        "Mode pemutaran dan simulasi lokal tidak memerlukan internet.\n"
        "Status visual REVIEW REQUIRED. Jaringan provisional dan belum terkalibrasi terhadap data lapangan.\n"
        "Data bangunan OpenStreetMap contributors (ODbL 1.0), https://www.openstreetmap.org/copyright.\n"
        "Lisensi Python dan SUMO tersedia di App/Python dan App/toolchain.\n",
        encoding="utf-8",
    )
    print(release)


if __name__ == "__main__":
    main()
