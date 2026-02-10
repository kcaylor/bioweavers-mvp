# Bio Weavers MVP Plan

Date: February 9, 2026
Session: Environment Setup & Core Functions

## Session Goals
- Get everyone's dev environment working
- Establish shared GitHub repo & project structure
- Whiteboard the proof-of-life architecture
- Write core functions (with tests?)

## Pre-Session Checklist
- [ ] All students have Python 3.10+ installed
- [ ] Conda or venv environment ready
- [ ] VS Code or preferred editor
- [ ] GitHub account & git configured
- [ ] iNaturalist API docs reviewed

## Proof-of-Life Pipeline
1. Upload KML/GeoJSON
2. Create buffer (2/5/10 miles)
3. Query iNaturalist API (bounding box)
4. Get species observations
5. Filter by federal status
6. Export CSV (then Excel)

## Key Design Decisions
- Input format: GeoJSON (KML stretch)
- Buffer CRS: EPSG:3310 (CA Albers)
- Species API: iNaturalist
- Federal list: USFWS ECOS or hardcoded fallback
- Output: CSV first, then Excel

## Core Functions
- `src/geometry.py`: `load_boundary`, `create_buffer`, `get_bounding_box`
- `src/species.py`: `query_inaturalist`, `get_unique_species`, `filter_federally_listed`
- `src/export.py`: `export_species_csv`, `export_species_excel`

## Tests
- Geometry tests: load boundary, buffer, bounding box
- Species tests: unique species aggregation, federal filtering

## End of Session Checklist
- [ ] Everyone can run `import geopandas` without errors
- [ ] Repo created and all can push/pull
- [ ] `geometry.py` functions written and tested
- [ ] Sample boundary loads successfully
- [ ] Buffer function produces valid output
- [ ] Architecture diagram captured

## Homework Before Tuesday (Feb 10, 2026)
1. Run through the code locally
2. Test `query_inaturalist()` with sample bbox
3. Find issues / edge cases to discuss
