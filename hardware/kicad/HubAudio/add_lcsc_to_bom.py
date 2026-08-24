#!/usr/bin/env python3

import csv
import sys
from pathlib import Path


def norm(value):
    return (value or "").strip().strip('"').strip()


def read_kicad_bom(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_lcsc_export(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        lines = f.readlines()

    header = None

    for i, line in enumerate(lines):
        if line.startswith("LCSC#;"):
            header = i
            break

    if header is None:
        raise RuntimeError("Non trovo la sezione 'LCSC Matching Results'.")

    return list(
        csv.DictReader(
            lines[header:],
            delimiter=";"
        )
    )


def build_lcsc_map(rows):
    result = {}

    for row in rows:
        mpn = norm(row.get("Mrf#", ""))
        lcsc = norm(row.get("LCSC#", ""))
        status = norm(row.get("Matched status", ""))
        url = norm(row.get("Product Link", ""))

        if not mpn:
            continue

        # IMPORTANTE:
        # accettiamo automaticamente solo Exact Matches
        if status == "Exact Matches" and lcsc:
            result[mpn] = {
                "lcsc": lcsc,
                "status": status,
                "url": url,
            }

    return result


def main():

    if len(sys.argv) != 3:
        print()
        print("Uso:")
        print(
            "  python3 add_lcsc_to_bom.py "
            "HubAudio.csv export_project_20260822_065729.csv"
        )
        print()
        sys.exit(1)

    bom_file = Path(sys.argv[1])
    lcsc_file = Path(sys.argv[2])

    if not bom_file.exists():
        print(f"ERRORE: BOM non trovata: {bom_file}")
        sys.exit(1)

    if not lcsc_file.exists():
        print(f"ERRORE: export LCSC non trovato: {lcsc_file}")
        sys.exit(1)

    print("Leggo BOM KiCad...")
    bom = read_kicad_bom(bom_file)

    print("Leggo export LCSC...")
    lcsc_rows = read_lcsc_export(lcsc_file)

    lcsc_map = build_lcsc_map(lcsc_rows)

    # Manteniamo tutte le colonne originali di KiCad
    columns = list(bom[0].keys())

    for column in [
        "LCSC#",
        "LCSC_Status",
        "LCSC_URL",
    ]:
        if column not in columns:
            columns.append(column)

    exact = 0
    missing = 0

    for row in bom:

        # Prima scelta: PNM
        mpn = norm(row.get("PNM", ""))

        # Fallback: Value
        if not mpn:
            mpn = norm(row.get("Value", ""))

        match = lcsc_map.get(mpn)

        if match:

            row["LCSC#"] = match["lcsc"]
            row["LCSC_Status"] = "Exact Matches"
            row["LCSC_URL"] = match["url"]

            exact += 1

        else:

            row["LCSC#"] = ""
            row["LCSC_Status"] = ""
            row["LCSC_URL"] = ""

            missing += 1

    output = bom_file.with_name(
        bom_file.stem + "_Pinscope_BOM.csv"
    )

    with open(
        output,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=columns,
            quoting=csv.QUOTE_ALL
        )

        writer.writeheader()
        writer.writerows(bom)

    print()
    print("=" * 50)
    print("       LCSC → PINSCOPE BOM")
    print("=" * 50)
    print()
    print(f"BOM originale : {bom_file.name}")
    print(f"Export LCSC   : {lcsc_file.name}")
    print(f"Output        : {output.name}")
    print()
    print(f"Righe BOM     : {len(bom)}")
    print(f"Exact Match   : {exact}")
    print(f"Senza LCSC    : {missing}")
    print()
    print("Solo 'Exact Matches' sono stati accettati.")
    print("Partial Matches NON sono stati inseriti.")
    print("No Matches NON sono stati inseriti.")
    print()
    print(f"FILE CREATO: {output}")
    print()


if __name__ == "__main__":
    main()
