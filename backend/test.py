# scripts/test_tempsal_ingest.py
import sys
from pathlib import Path
import pandas as pd

# Adjust import to your package layout
from ingest.netcdf_to_parquet import GridNetCDFProcessor

def main():
    if len(sys.argv) < 2:
        print("Usage: python test.py <path_to_netcdf_file>")
        sys.exit(1)
    nc_path = Path(sys.argv[1]).resolve()
    print(f"Input: {nc_path}")

    proc = GridNetCDFProcessor(output_dir="./processed_argo_data")
    res = proc.process_file(nc_path)
    print("Result:", res)

    if res.get("success") and res.get("output_file"):
        out = Path(res["output_file"])
        df = pd.read_parquet(out)  # requires pyarrow
        print("\nParquet columns:", list(df.columns))
        print("\nHead:\n", df.head(10))
        print("\nCounts:", len(df), "rows")
        # Optional minimal stats
        for c in ["temperature", "salinity"]:
            if c in df.columns:
                print(f"{c}: min={df[c].min()} max={df[c].max()} mean={df[c].mean()}")

if __name__ == "__main__":
    main()
