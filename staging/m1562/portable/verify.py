"""Verify a fresh extraction through the launcher, HTTP UI and bundled SUMO."""
import json
import subprocess
import time
import uuid
import sys
from pathlib import Path

from build import ROOT, NAME

QA = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "staging/m1562/portable/qa"


def fetch(base, path, body=None):
    command = ["curl.exe", "--noproxy", "*", "--silent", "--show-error",
               "--fail-with-body", "--compressed", "--max-time", "45", base + path]
    data = None
    if body is not None:
        command += ["-H", "Content-Type: application/json", "--data-binary", "@-"]
        data = json.dumps(body).encode()
    result = subprocess.run(command, input=data, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{path}: {result.stderr.decode()} {result.stdout[:500]!r}")
    return result.stdout


def main():
    package = QA / NAME
    ready = QA / ("launcher-url-" + uuid.uuid4().hex + ".txt")
    process = subprocess.Popen([str(package / "GEDANGAN_TRAFFIC_SIMULATOR.exe"),
                                "--no-browser", str(ready)])
    try:
        for _ in range(120):
            if ready.exists() and ready.stat().st_size:
                break
            time.sleep(.25)
        else:
            raise RuntimeError("Launcher did not start. See App/portable-launch.log.")
        base = ready.read_text().strip()
        html = fetch(base, "")
        assert b"assets/" in html
        import re
        for asset in re.findall(rb'(?:src|href)="(/assets/[^"]+)"', html):
            assert fetch(base, asset.decode().lstrip("/"))
        api = lambda path, body=None: json.loads(fetch(base, "api/" + path, body))
        catalog = api("catalog")
        print("Catalog ready", flush=True)
        scene = api("scene")
        assert len(scene["environment"]["buildings"]) == 953
        demo = next(r for r in api("runs") if r["request"]["name"] == "M15.5 baseline-3000")
        index = api("packed/" + demo["run_id"] + "/index.json")
        assert index["positions"] == 3441615
        chunk = index["chunks"][0]
        assert len(fetch(base, "api/packed/" + demo["run_id"] + "/" + chunk["file"])) == chunk["byte_length"]
        results = []
        for count in (12, 36):
            req = catalog["default"]
            req.update(name="Portable QA " + str(count), duration_s=120, execution_horizon_s=120,
                       warmup_s=0, total=count, volume_interpretation="total")
            req["rail"]["arrivals_s"] = []
            assert api("preview", req)["total"] == count
            job = api("generate", req)["job_id"]
            print(f"SUMO job queued: {count}", flush=True)
            deadline = time.monotonic() + 150
            while time.monotonic() < deadline:
                record = api("jobs/" + job)
                if record["status"] == "FAILED":
                    raise RuntimeError(record["error"])
                if record["status"] == "COMPLETE":
                    break
                time.sleep(.25)
            else:
                raise TimeoutError("SUMO portable run did not finish")
            result = record["result"]
            assert result["requested"] == count and result["moved"] > 0
            packed = api("packed/" + result["run_id"] + "/index.json")
            assert packed["frame_count"] == 240 and packed["positions"] > 0
            results.append({key: result[key] for key in
                            ("run_id", "requested", "departed", "moved", "arrived", "not_departed", "sumo_version")})
        assert results[1]["departed"] > results[0]["departed"]
        report = {"status": "PASS", "demo_positions": index["positions"], "new_runs": results}
        (QA / "result.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report))
    finally:
        # Exercise the launcher window close path, then use a scoped process-tree fallback.
        subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                        f"(Get-Process -Id {process.pid} -ErrorAction SilentlyContinue).CloseMainWindow()"],
                       capture_output=True)
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)


if __name__ == "__main__":
    main()
