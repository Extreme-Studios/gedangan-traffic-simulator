"""Test the delivered simple application from a fresh ZIP extraction."""
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

from verify import fetch

ROOT = Path(__file__).resolve().parents[3]
NAME = "GEDANGAN_TRAFFIC_SIMULATOR_SIMPLE_20K_PORTABLE"


def main():
    qa = ROOT / "staging/simple/portable/qa"
    app = qa / NAME
    ready = qa / ("url-" + uuid.uuid4().hex + ".txt")
    process = subprocess.Popen([str(app / "GEDANGAN_TRAFFIC_SIMULATOR.exe"), "--no-browser", str(ready)])
    try:
        for _ in range(120):
            if ready.exists():
                break
            time.sleep(.25)
        else:
            raise RuntimeError("Portable launcher did not publish URL")
        base = ready.read_text().strip()
        api = lambda path, body=None: json.loads(fetch(base, "api/" + path, body))
        assert b"simple-" in fetch(base, "")
        preview = api("preview", {"total": 20000})
        assert preview["total"] == sum(preview["composition"].values()) == 20000
        assert preview["composition"]["angkot"] == 1200
        assert preview["composition"]["trailer"] == 200
        try:
            api("generate", {"total": 20001})
        except RuntimeError:
            pass
        else:
            raise AssertionError("20001 should be rejected")
        job = api("generate", {"total": 100})["job_id"]
        deadline = time.monotonic() + 180
        while time.monotonic() < deadline:
            state = api("jobs/" + job)
            if state["status"] == "FAILED":
                raise RuntimeError(state["error"])
            if state["status"] == "COMPLETE":
                break
            time.sleep(.5)
        else:
            raise TimeoutError("SUMO run did not complete")
        result = state["result"]
        assert result["requested"] == 100
        for vehicle in ["motorcycle", "car", "angkot", "light_truck", "heavy_truck", "trailer"]:
            assert result["classes"][vehicle]["moved"] > 0, vehicle
        index = api("packed/" + result["run_id"] + "/index.json")
        assert index["frame_count"] == 7200
        for chunk in index["chunks"]:
            raw = fetch(base, "api/packed/" + result["run_id"] + "/" + chunk["file"])
            assert len(raw) == chunk["byte_length"]
        report = {"status": "PASS", "source": "Fresh ZIP extraction, EXE launcher and bundled Python/SUMO",
                  "input_max": 20000, "reject_20001": True, "new_run": result,
                  "packed_frames": index["frame_count"], "packed_positions": index["positions"],
                  "all_chunks_downloaded": len(index["chunks"])}
        (ROOT / "documentation/simple/portable-test.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({k: report[k] for k in ["status", "input_max", "reject_20001", "packed_frames", "packed_positions"]}), flush=True)
    finally:
        subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                        f"(Get-Process -Id {process.pid} -ErrorAction SilentlyContinue).CloseMainWindow()"],
                       capture_output=True)
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)


if __name__ == "__main__":
    main()
