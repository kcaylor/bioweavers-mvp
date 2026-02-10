# Export Tutorial

This walkthrough builds each function in `src/export.py` step by step.

## `export_species_csv`

**1. Function definition and docstrings**
```python
import pandas as pd
from pathlib import Path
from datetime import datetime


def export_species_csv(
    species_df: pd.DataFrame,
    output_path: str | Path,
    project_name: str = "Project",
) -> Path:
    """
    Export species list to CSV.

    Parameters
    ----------
    species_df : pd.DataFrame
        Species DataFrame from get_unique_species()
    output_path : str or Path
        Output file path
    project_name : str
        Project name for metadata

    Returns
    -------
    Path
        Path to saved file
    """
    raise NotImplementedError
```

**2. Stub out functional code**
```python
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    species_df.to_csv(output_path, index=False)
    return output_path
```

**3. Function implementation**
```python
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = species_df.copy()
    df["project"] = project_name
    df["generated_at"] = datetime.now().isoformat()

    df.to_csv(output_path, index=False)
    return output_path
```

**4. Example usage**
```python
from src.export import export_species_csv

export_species_csv(species, "output/species.csv", project_name="Sample Project")
```

## `export_species_excel`

**1. Function definition and docstrings**
```python
def export_species_excel(
    species_df: pd.DataFrame,
    listed_df: pd.DataFrame,
    output_path: str | Path,
    project_name: str = "Project",
) -> Path:
    """
    Export species data to Excel with multiple sheets.

    Sheets:
    - All Species
    - Federal Listed
    - Summary
    """
    raise NotImplementedError
```

**2. Stub out functional code**
```python
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        species_df.to_excel(writer, sheet_name="All Species", index=False)
    return output_path
```

**3. Function implementation**
```python
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        species_df.to_excel(writer, sheet_name="All Species", index=False)
        if not listed_df.empty:
            listed_df.to_excel(writer, sheet_name="Federal Listed", index=False)

        summary = pd.DataFrame(
            {
                "Metric": [
                    "Project Name",
                    "Generated At",
                    "Total Species",
                    "Federally Listed Species",
                    "Total Observations",
                ],
                "Value": [
                    project_name,
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    len(species_df),
                    len(listed_df),
                    species_df["observation_count"].sum()
                    if "observation_count" in species_df
                    else "N/A",
                ],
            }
        )
        summary.to_excel(writer, sheet_name="Summary", index=False)

    return output_path
```

**4. Example usage**
```python
from src.export import export_species_excel

export_species_excel(
    species,
    listed,
    "output/species.xlsx",
    project_name="Sample Project",
)
```
