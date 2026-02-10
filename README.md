# Bio Weavers MVP

Proof-of-life pipeline for querying iNaturalist observations around a project boundary, buffering the area, and exporting species lists.

## Goals (Session 1)
1. Get dev environments working
2. Establish repo structure
3. Implement core geometry/species/export functions
4. Add tests for core logic (no network required)

## Project Structure
```
bioweavers-mvp/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── geometry.py
│   ├── species.py
│   └── export.py
├── tests/
│   ├── test_geometry.py
│   └── test_species.py
├── data/
│   └── sample_boundary.geojson
├── output/
├── notebooks/
└── docs/
    └── PLAN.md
```

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Core Pipeline (Proof-of-Life)
1. Load GeoJSON/KML boundary
2. Create buffer (2/5/10 miles)
3. Query iNaturalist API with bounding box
4. Build species list + filter federal listed
5. Export CSV/Excel

## Notes
- Buffering uses EPSG:3310 (CA Albers) for meter-accurate buffers, then returns to EPSG:4326 for API usage.
- iNaturalist requests are not executed in tests; network tests can be added later.


## Jupyter Kernel Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install ipykernel
python -m ipykernel install --user --name bioweavers --display-name "Bio Weavers"
```

In Jupyter, select the **Bio Weavers** kernel.
