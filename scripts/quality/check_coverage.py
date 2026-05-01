import json

with open("coverage.json", "r") as f:
    cov = json.load(f)

for filename, data in cov["files"].items():
    if "classic_service.py" in filename or "fulltext_search.py" in filename:
        percent = data["summary"]["percent_covered"]
        missing = data["missing_lines"]
        fname = filename.split("/")[-1] if "/" in filename else filename.split("\\")[-1]
        print("")
        print(f"{fname}: {percent:.0f}%")
        if missing:
            print(
                f"  Missing lines ({len(missing)}): {missing[:15]}{'...' if len(missing) > 15 else ''}"
            )
