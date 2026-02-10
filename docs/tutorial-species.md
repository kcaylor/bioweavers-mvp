# Species Tutorial

This walkthrough builds each function in `src/species.py` step by step.

## `query_inaturalist`

**1. Function definition and docstrings**
```python
import pandas as pd
from typing import Optional


def query_inaturalist(
    bbox: tuple[float, float, float, float],
    taxon_id: Optional[int] = None,
    quality_grade: str = "research",
    limit: int = 200,
) -> pd.DataFrame:
    """
    Query iNaturalist observations within a bounding box.

    Parameters
    ----------
    bbox : tuple
        Bounding box as (min_lng, min_lat, max_lng, max_lat)
    taxon_id : int, optional
        Filter to specific taxon
    quality_grade : str
        'research', 'needs_id', or 'casual'
    limit : int
        Maximum observations to return (max 200 per request)

    Returns
    -------
    pd.DataFrame
        DataFrame with observation data including species info
    """
    raise NotImplementedError
```

**2. Stub out functional code**
```python
    min_lng, min_lat, max_lng, max_lat = bbox
    return pd.DataFrame()
```

**3. Function implementation**
```python
    min_lng, min_lat, max_lng, max_lat = bbox

    params = {
        "nelat": max_lat,
        "nelng": max_lng,
        "swlat": min_lat,
        "swlng": min_lng,
        "quality_grade": quality_grade,
        "per_page": limit,
        "order": "desc",
        "order_by": "observed_on",
    }
    if taxon_id:
        params["taxon_id"] = taxon_id

    response = requests.get(f"{INAT_API_BASE}/observations", params=params)
    response.raise_for_status()

    data = response.json()
    records = []
    for obs in data.get("results", []):
        taxon = obs.get("taxon", {})
        records.append({
            "observation_id": obs.get("id"),
            "observed_on": obs.get("observed_on"),
            "scientific_name": taxon.get("name"),
            "common_name": taxon.get("preferred_common_name"),
            "taxon_id": taxon.get("id"),
            "iconic_taxon": taxon.get("iconic_taxon_name"),
            "conservation_status": taxon.get("conservation_status", {}).get("status"),
            "latitude": obs.get("geojson", {}).get("coordinates", [None, None])[1],
            "longitude": obs.get("geojson", {}).get("coordinates", [None, None])[0],
            "place_guess": obs.get("place_guess"),
        })

    return pd.DataFrame(records)
```

**4. Example usage**
```python
from src.species import query_inaturalist

bbox = (-119.85, 34.42, -119.82, 34.45)
observations = query_inaturalist(bbox, limit=50)
observations.head()
```

## `get_unique_species`

**1. Function definition and docstrings**
```python
def get_unique_species(observations: pd.DataFrame) -> pd.DataFrame:
    """
    Get unique species from observations with counts.
    """
    raise NotImplementedError
```

**2. Stub out functional code**
```python
    return observations
```

**3. Function implementation**
```python
    species = (
        observations.groupby(["scientific_name", "common_name", "conservation_status"])
        .agg(
            observation_count=("observation_id", "count"),
            first_observed=("observed_on", "min"),
            last_observed=("observed_on", "max"),
        )
        .reset_index()
    )
    return species.sort_values("observation_count", ascending=False)
```

**4. Example usage**
```python
from src.species import get_unique_species

species = get_unique_species(observations)
species.head()
```

## `filter_federally_listed`

**1. Function definition and docstrings**
```python
def filter_federally_listed(species_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter species list to only federally listed species.
    """
    raise NotImplementedError
```

**2. Stub out functional code**
```python
    return species_df[species_df["scientific_name"].isna()]
```

**3. Function implementation**
```python
    species_df = species_df.copy()
    species_df["federal_status"] = species_df["scientific_name"].map(FEDERAL_LISTED_TAXA)
    listed = species_df[species_df["federal_status"].notna()].copy()
    return listed
```

**4. Example usage**
```python
from src.species import filter_federally_listed

listed = filter_federally_listed(species)
listed.head()
```
