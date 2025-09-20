# # """
# # NetCDF to Parquet conversion module for ARGO float data ingestion.

# # This module provides the scaffold for converting NetCDF files from ARGO floats
# # into Parquet format for efficient storage and querying. The actual NetCDF parsing
# # logic needs to be implemented based on specific ARGO data formats.

# # TODO: Complete implementation with actual NetCDF processing logic.
# # """

# # import logging
# # from pathlib import Path
# # from typing import Dict, List, Optional, Tuple, Any
# # from datetime import datetime
# # import pandas as pd
# # import numpy as np

# # # TODO: Uncomment when implementing actual NetCDF processing
# # # import xarray as xr
# # # import netCDF4 as nc

# # logger = logging.getLogger(__name__)


# # class NetCDFProcessor:
# #     """
# #     Processes ARGO float NetCDF files and converts them to Parquet format.
    
# #     This class handles the complete pipeline from NetCDF ingestion to
# #     structured data storage suitable for the FloatChat application.
# #     """
    
# #     def __init__(self, output_dir: str = "./processed_data"):
# #         """
# #         Initialize NetCDF processor.
        
# #         Args:
# #             output_dir: Directory to store processed Parquet files
# #         """
# #         self.output_dir = Path(output_dir)
# #         self.output_dir.mkdir(exist_ok=True, parents=True)
        
# #         # Metadata tracking
# #         self.processing_log = []
# #         self.error_log = []
    
# #     def validate_netcdf_file(self, file_path: Path) -> Tuple[bool, List[str]]:
# #         """
# #         Validate NetCDF file structure and required variables.
        
# #         TODO: Implement actual validation logic
        
# #         Args:
# #             file_path: Path to NetCDF file
            
# #         Returns:
# #             Tuple of (is_valid, error_messages)
# #         """
# #         errors = []
        
# #         if not file_path.exists():
# #             errors.append(f"File not found: {file_path}")
# #             return False, errors
        
# #         if not file_path.suffix.lower() == '.nc':
# #             errors.append(f"File is not NetCDF format: {file_path}")
# #             return False, errors
        
# #         # TODO: Implement actual NetCDF validation
# #         # Example validation structure:
# #         """
# #         try:
# #             with xr.open_dataset(file_path) as ds:
# #                 # Check for required dimensions
# #                 required_dims = ['N_PROF', 'N_LEVELS']
# #                 missing_dims = [dim for dim in required_dims if dim not in ds.dims]
# #                 if missing_dims:
# #                     errors.append(f"Missing required dimensions: {missing_dims}")
                
# #                 # Check for required variables
# #                 required_vars = ['TEMP', 'PSAL', 'PRES', 'TIME', 'LONGITUDE', 'LATITUDE']
# #                 missing_vars = [var for var in required_vars if var not in ds.variables]
# #                 if missing_vars:
# #                     errors.append(f"Missing required variables: {missing_vars}")
                
# #                 # Validate data quality flags if present
# #                 if 'TEMP_QC' in ds.variables:
# #                     qc_values = ds['TEMP_QC'].values
# #                     if not all(qc in ['1', '2', '3', '4', '8', '9'] for qc in qc_values.flatten()):
# #                         errors.append("Invalid quality control values found")
        
# #         except Exception as e:
# #             errors.append(f"Error reading NetCDF file: {str(e)}")
# #         """
        
# #         # Placeholder validation - always returns True for now
# #         logger.info(f"TODO: Implement NetCDF validation for {file_path}")
        
# #         return len(errors) == 0, errors
    
# #     def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
# #         """
# #         Extract metadata from NetCDF file.
        
# #         TODO: Implement actual metadata extraction
        
# #         Args:
# #             file_path: Path to NetCDF file
            
# #         Returns:
# #             Dictionary containing extracted metadata
# #         """
# #         metadata = {
# #             "file_path": str(file_path),
# #             "processing_date": datetime.now().isoformat(),
# #             "float_id": None,
# #             "deployment_date": None,
# #             "data_center": None,
# #             "instrument_type": None,
# #             "parameter_list": [],
# #             "profile_count": 0,
# #             "date_range": {"start": None, "end": None},
# #             "spatial_bounds": {"lat_min": None, "lat_max": None, "lon_min": None, "lon_max": None},
# #             "quality_summary": {}
# #         }
        
# #         # TODO: Implement actual metadata extraction
# #         """
# #         Example xarray-based metadata extraction:
        
# #         try:
# #             with xr.open_dataset(file_path) as ds:
# #                 # Extract global attributes
# #                 metadata["float_id"] = ds.attrs.get('platform_number', '').strip()
# #                 metadata["data_center"] = ds.attrs.get('data_centre', '').strip()
# #                 metadata["instrument_type"] = ds.attrs.get('instrument_type', '').strip()
                
# #                 # Extract temporal information
# #                 if 'JULD' in ds.variables:
# #                     time_data = ds['JULD'].values
# #                     # Convert ARGO Julian days to datetime
# #                     # (ARGO uses days since 1950-01-01 00:00:00 UTC)
# #                     reference_date = pd.to_datetime('1950-01-01')
# #                     dates = pd.to_datetime(time_data, unit='D', origin=reference_date)
                    
# #                     metadata["date_range"] = {
# #                         "start": dates.min().isoformat(),
# #                         "end": dates.max().isoformat()
# #                     }
                
# #                 # Extract spatial bounds
# #                 if 'LONGITUDE' in ds.variables and 'LATITUDE' in ds.variables:
# #                     lons = ds['LONGITUDE'].values
# #                     lats = ds['LATITUDE'].values
                    
# #                     metadata["spatial_bounds"] = {
# #                         "lat_min": float(np.nanmin(lats)),
# #                         "lat_max": float(np.nanmax(lats)),
# #                         "lon_min": float(np.nanmin(lons)),
# #                         "lon_max": float(np.nanmax(lons))
# #                     }
                
# #                 # Count profiles
# #                 if 'N_PROF' in ds.dims:
# #                     metadata["profile_count"] = ds.dims['N_PROF']
                
# #                 # List available parameters
# #                 parameter_vars = ['TEMP', 'PSAL', 'PRES', 'DOXY', 'CHLA', 'BBP700']
# #                 metadata["parameter_list"] = [var for var in parameter_vars if var in ds.variables]
                
# #                 # Quality control summary
# #                 qc_vars = [var for var in ds.variables if var.endswith('_QC')]
# #                 quality_summary = {}
# #                 for qc_var in qc_vars:
# #                     qc_data = ds[qc_var].values.flatten()
# #                     qc_counts = pd.Series(qc_data).value_counts().to_dict()
# #                     quality_summary[qc_var] = qc_counts
                
# #                 metadata["quality_summary"] = quality_summary
                
# #         except Exception as e:
# #             logger.error(f"Error extracting metadata from {file_path}: {e}")
# #             metadata["error"] = str(e)
# #         """
        
# #         logger.info(f"TODO: Implement metadata extraction for {file_path}")
# #         return metadata
    
# #     def process_profiles_to_dataframe(self, file_path: Path) -> pd.DataFrame:
# #         """
# #         Convert NetCDF profile data to structured DataFrame.
        
# #         TODO: Implement actual profile processing
        
# #         Args:
# #             file_path: Path to NetCDF file
            
# #         Returns:
# #             DataFrame with processed profile data
# #         """
        
# #         # TODO: Implement actual NetCDF to DataFrame conversion
# #         """
# #         Example implementation with xarray:
        
# #         profiles_data = []
        
# #         try:
# #             with xr.open_dataset(file_path) as ds:
# #                 n_profiles = ds.dims.get('N_PROF', 0)
# #                 n_levels = ds.dims.get('N_LEVELS', 0)
                
# #                 for profile_idx in range(n_profiles):
# #                     # Extract profile metadata
# #                     profile_time = ds['JULD'].values[profile_idx]
# #                     profile_lat = ds['LATITUDE'].values[profile_idx]
# #                     profile_lon = ds['LONGITUDE'].values[profile_idx]
                    
# #                     # Convert ARGO time to datetime
# #                     reference_date = pd.to_datetime('1950-01-01')
# #                     profile_datetime = pd.to_datetime(profile_time, unit='D', origin=reference_date)
                    
# #                     # Extract measurements for each level
# #                     for level_idx in range(n_levels):
# #                         # Skip if no data at this level
# #                         temp = ds['TEMP'].values[profile_idx, level_idx]
# #                         pres = ds['PRES'].values[profile_idx, level_idx]
# #                         psal = ds['PSAL'].values[profile_idx, level_idx]
                        
# #                         # Skip NaN values
# #                         if np.isnan([temp, pres, psal]).any():
# #                             continue
                        
# #                         # Quality control
# #                         temp_qc = ds.get('TEMP_QC', ds.get('TEMP_QUALITY_FLAG'))
# #                         psal_qc = ds.get('PSAL_QC', ds.get('PSAL_QUALITY_FLAG'))
                        
# #                         temp_qc_val = temp_qc.values[profile_idx, level_idx] if temp_qc is not None else '1'
# #                         psal_qc_val = psal_qc.values[profile_idx, level_idx] if psal_qc is not None else '1'
                        
# #                         # Only include good quality data (QC flags 1, 2)
# #                         if temp_qc_val in ['1', '2'] and psal_qc_val in ['1', '2']:
# #                             profiles_data.append({
# #                                 'time': profile_datetime,
# #                                 'latitude': profile_lat,
# #                                 'longitude': profile_lon,
# #                                 'pressure': pres,
# #                                 'depth': self._pressure_to_depth(pres, profile_lat),
# #                                 'temperature': temp,
# #                                 'salinity': psal,
# #                                 'temp_qc': temp_qc_val,
# #                                 'psal_qc': psal_qc_val,
# #                                 'profile_id': profile_idx,
# #                                 'level_id': level_idx
# #                             })
        
# #         except Exception as e:
# #             logger.error(f"Error processing profiles from {file_path}: {e}")
# #             return pd.DataFrame()  # Return empty DataFrame on error
        
# #         return pd.DataFrame(profiles_data)
# #         """
        
# #         # Placeholder implementation - return empty DataFrame
# #         logger.info(f"TODO: Implement profile processing for {file_path}")
# #         return pd.DataFrame()
    
# #     def _pressure_to_depth(self, pressure: float, latitude: float) -> float:
# #         """
# #         Convert pressure to depth using UNESCO algorithm.
        
# #         TODO: Implement actual pressure to depth conversion
        
# #         Args:
# #             pressure: Pressure in dbar
# #             latitude: Latitude in degrees
            
# #         Returns:
# #             Depth in meters
# #         """
# #         # TODO: Implement UNESCO pressure to depth conversion
# #         # This is a simplified approximation - use proper oceanographic formula
# #         # Rough approximation: 1 dbar ≈ 1 meter depth
# #         return pressure * 1.019716  # More accurate conversion factor
    
# #     def save_to_parquet(self, df: pd.DataFrame, output_path: Path, 
# #                        partition_cols: Optional[List[str]] = None) -> bool:
# #         """
# #         Save DataFrame to Parquet format with optional partitioning.
        
# #         Args:
# #             df: DataFrame to save
# #             output_path: Output file path
# #             partition_cols: Columns to use for partitioning
            
# #         Returns:
# #             Success status
# #         """
# #         try:
# #             if df.empty:
# #                 logger.warning(f"Cannot save empty DataFrame to {output_path}")
# #                 return False
            
# #             # Ensure output directory exists
# #             output_path.parent.mkdir(exist_ok=True, parents=True)
            
# #             # Save with compression
# #             df.to_parquet(
# #                 output_path,
# #                 engine='pyarrow',
# #                 compression='snappy',
# #                 index=False
# #             )
            
# #             logger.info(f"Saved {len(df)} records to {output_path}")
# #             return True
            
# #         except Exception as e:
# #             logger.error(f"Error saving DataFrame to Parquet: {e}")
# #             return False
    
# #     def process_netcdf_file(self, file_path: Path, float_id: Optional[str] = None) -> Dict[str, Any]:
# #         """
# #         Main processing function for a single NetCDF file.
        
# #         Args:
# #             file_path: Path to NetCDF file
# #             float_id: Optional float ID override
            
# #         Returns:
# #             Processing result summary
# #         """
# #         result = {
# #             "file_path": str(file_path),
# #             "success": False,
# #             "records_processed": 0,
# #             "output_files": [],
# #             "errors": [],
# #             "metadata": {}
# #         }
        
# #         try:
# #             # Step 1: Validate file
# #             is_valid, validation_errors = self.validate_netcdf_file(file_path)
# #             if not is_valid:
# #                 result["errors"].extend(validation_errors)
# #                 return result
            
# #             # Step 2: Extract metadata
# #             metadata = self.extract_metadata(file_path)
# #             result["metadata"] = metadata
            
# #             # Use provided float_id or extract from metadata
# #             if float_id:
# #                 metadata["float_id"] = float_id
            
# #             # Step 3: Process profiles
# #             df = self.process_profiles_to_dataframe(file_path)
            
# #             if df.empty:
# #                 result["errors"].append("No valid profile data found")
# #                 return result
            
# #             # Step 4: Save to Parquet
# #             float_id_str = metadata.get("float_id", "unknown")
# #             output_filename = f"argo_profiles_{float_id_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
# #             output_path = self.output_dir / output_filename
            
# #             if self.save_to_parquet(df, output_path):
# #                 result["success"] = True
# #                 result["records_processed"] = len(df)
# #                 result["output_files"].append(str(output_path))
# #             else:
# #                 result["errors"].append("Failed to save Parquet file")
            
# #         except Exception as e:
# #             error_msg = f"Unexpected error processing {file_path}: {str(e)}"
# #             logger.error(error_msg)
# #             result["errors"].append(error_msg)
        
# #         return result
    
# #     def process_directory(self, input_dir: Path) -> Dict[str, Any]:
# #         """
# #         Process all NetCDF files in a directory.
        
# #         Args:
# #             input_dir: Directory containing NetCDF files
            
# #         Returns:
# #             Summary of processing results
# #         """
# #         summary = {
# #             "total_files": 0,
# #             "successful": 0,
# #             "failed": 0,
# #             "total_records": 0,
# #             "output_files": [],
# #             "errors": []
# #         }
        
# #         # Find all NetCDF files
# #         netcdf_files = list(input_dir.glob("*.nc")) + list(input_dir.glob("**/*.nc"))
# #         summary["total_files"] = len(netcdf_files)
        
# #         logger.info(f"Found {len(netcdf_files)} NetCDF files in {input_dir}")
        
# #         for file_path in netcdf_files:
# #             logger.info(f"Processing {file_path}")
# #             result = self.process_netcdf_file(file_path)
            
# #             if result["success"]:
# #                 summary["successful"] += 1
# #                 summary["total_records"] += result["records_processed"]
# #                 summary["output_files"].extend(result["output_files"])
# #             else:
# #                 summary["failed"] += 1
# #                 summary["errors"].extend(result["errors"])
        
# #         logger.info(f"Processing complete: {summary['successful']} successful, {summary['failed']} failed")
# #         return summary


# # def main():
# #     """
# #     Example usage of NetCDF processor.
    
# #     TODO: Replace with actual NetCDF files for testing.
# #     """
    
# #     # Configure logging
# #     logging.basicConfig(level=logging.INFO)
    
# #     # Initialize processor
# #     processor = NetCDFProcessor(output_dir="./processed_argo_data")
    
# #     # Example: Process a single file
# #     # TODO: Replace with actual NetCDF file path
# #     example_file = Path("./example_data/argo_float_12345.nc")
    
# #     if example_file.exists():
# #         result = processor.process_netcdf_file(example_file)
# #         print(f"Processing result: {result}")
# #     else:
# #         print("Example NetCDF file not found. Please provide actual ARGO NetCDF files for processing.")
# #         print("Place NetCDF files in the input directory and run the processor.")
    
# #     # Example: Process entire directory
# #     input_directory = Path("./input_netcdf_files")
# #     if input_directory.exists():
# #         summary = processor.process_directory(input_directory)
# #         print(f"Directory processing summary: {summary}")


# # if __name__ == "__main__":
# #     main()


# """
# NetCDF to Parquet conversion module for ARGO float data ingestion.

# Implements validation, metadata extraction, profile processing (TEMP/PSAL/PRES),
# QC filtering, and Parquet export with optional directory batching.
# """

# import logging
# from pathlib import Path
# from typing import Dict, List, Optional, Tuple, Any
# from datetime import datetime
# import pandas as pd
# import numpy as np

# # Core readers
# import xarray as xr  # pip install xarray
# import netCDF4 as nc  # pip install netCDF4

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)


# def _first_present(ds: xr.Dataset, candidates: List[str]) -> Optional[str]:
#     """Return the first variable name present in the dataset from candidates."""
#     for name in candidates:
#         if name in ds.variables:
#             return name
#     return None


# def _juld_to_datetime(juld_value: Any) -> Optional[pd.Timestamp]:
#     """Convert ARGO JULD (days since 1950-01-01) to pandas Timestamp."""
#     try:
#         ref = pd.to_datetime("1950-01-01")
#         # juld_value may be masked/np.nan; guard it
#         if juld_value is None or (isinstance(juld_value, float) and np.isnan(juld_value)):
#             return None
#         return pd.to_datetime(juld_value, unit="D", origin=ref)
#     except Exception:
#         return None


# class NetCDFProcessor:
#     """
#     Processes ARGO float NetCDF files and converts them to Parquet format.

#     This class handles the complete pipeline from NetCDF ingestion to
#     structured data storage suitable for the FloatChat application.
#     """

#     def __init__(self, output_dir: str = "./processed_argo_data"):
#         """
#         Initialize NetCDF processor.

#         Args:
#             output_dir: Directory to store processed Parquet files
#         """
#         self.output_dir = Path(output_dir)
#         self.output_dir.mkdir(exist_ok=True, parents=True)
#         self.processing_log: List[Dict[str, Any]] = []
#         self.error_log: List[str] = []

#     # ---------------------- Validation ----------------------

#     def validate_netcdf_file(self, file_path: Path) -> Tuple[bool, List[str]]:
#         """
#         Validate NetCDF file structure and required variables.

#         Returns:
#             Tuple of (is_valid, error_messages)
#         """
#         errors: List[str] = []

#         if not file_path.exists():
#             errors.append(f"File not found: {file_path}")
#             return False, errors

#         if file_path.suffix.lower() != ".nc":
#             errors.append(f"File is not NetCDF format: {file_path}")
#             return False, errors

#         try:
#             with xr.open_dataset(file_path) as ds:
#                 # Required dimensions
#                 req_dims = ["N_PROF", "N_LEVELS"]
#                 missing_dims = [d for d in req_dims if d not in ds.dims]
#                 if missing_dims:
#                     errors.append(f"Missing required dimensions: {missing_dims}")

#                 # Required variables (allow adjusted fallbacks)
#                 temp_var = _first_present(ds, ["TEMP_ADJUSTED", "TEMP"])
#                 psal_var = _first_present(ds, ["PSAL_ADJUSTED", "PSAL"])
#                 pres_var = _first_present(ds, ["PRES_ADJUSTED", "PRES"])
#                 time_var = _first_present(ds, ["JULD", "TIME"])
#                 lat_var = _first_present(ds, ["LATITUDE"])
#                 lon_var = _first_present(ds, ["LONGITUDE"])

#                 missing = []
#                 if temp_var is None:
#                     missing.append("TEMP or TEMP_ADJUSTED")
#                 if psal_var is None:
#                     missing.append("PSAL or PSAL_ADJUSTED")
#                 if pres_var is None:
#                     missing.append("PRES or PRES_ADJUSTED")
#                 if time_var is None:
#                     missing.append("JULD or TIME")
#                 if lat_var is None:
#                     missing.append("LATITUDE")
#                 if lon_var is None:
#                     missing.append("LONGITUDE")
#                 if missing:
#                     errors.append(f"Missing required variables: {missing}")

#                 # Optional QC checks (do not fail if missing)
#                 # Valid QC codes are characters '0'-'9'; we primarily keep '1' or '2'
#                 # No strict validation to avoid format variance issues

#         except Exception as e:
#             errors.append(f"Error reading NetCDF file: {e}")

#         return len(errors) == 0, errors

#     # ---------------------- Metadata ----------------------

#     def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
#         """
#         Extract metadata from NetCDF file.
#         """
#         metadata: Dict[str, Any] = {
#             "file_path": str(file_path),
#             "processing_date": datetime.now().isoformat(),
#             "float_id": None,
#             "deployment_date": None,
#             "data_center": None,
#             "instrument_type": None,
#             "parameter_list": [],
#             "profile_count": 0,
#             "date_range": {"start": None, "end": None},
#             "spatial_bounds": {"lat_min": None, "lat_max": None, "lon_min": None, "lon_max": None},
#             "quality_summary": {},
#         }

#         try:
#             with xr.open_dataset(file_path) as ds:
#                 # Global attrs and common metadata
#                 # platform_number may also exist as a variable; check attrs first
#                 platform = ds.attrs.get("platform_number")
#                 if platform is None and "PLATFORM_NUMBER" in ds.variables:
#                     # PLATFORM_NUMBER can be bytes/char array; decode if needed
#                     try:
#                         v = ds["PLATFORM_NUMBER"].values
#                         if hasattr(v, "tobytes"):
#                             platform = v.tobytes().decode(errors="ignore").strip()
#                         else:
#                             platform = str(v).strip()
#                     except Exception:
#                         platform = None
#                 metadata["float_id"] = (str(platform).strip() if platform is not None else None) or None

#                 metadata["data_center"] = (str(ds.attrs.get("data_centre", "")).strip() or None)
#                 metadata["instrument_type"] = (str(ds.attrs.get("instrument_type", "")).strip() or None)

#                 # Date range from JULD/TIME
#                 time_var = _first_present(ds, ["JULD", "TIME"])
#                 if time_var:
#                     times = ds[time_var].values
#                     # times can be 1D (N_PROF) or masked; convert robustly
#                     try:
#                         times = np.array(times).astype(float)
#                         valid = times[np.isfinite(times)]
#                         if valid.size:
#                             dts = pd.to_datetime(valid, unit="D", origin=pd.Timestamp("1950-01-01"))
#                             metadata["date_range"] = {"start": dts.min().isoformat(), "end": dts.max().isoformat()}
#                     except Exception:
#                         pass

#                 # Spatial bounds
#                 if "LATITUDE" in ds and "LONGITUDE" in ds:
#                     lats = np.array(ds["LATITUDE"].values, dtype=float)
#                     lons = np.array(ds["LONGITUDE"].values, dtype=float)
#                     if lats.size and lons.size:
#                         metadata["spatial_bounds"] = {
#                             "lat_min": float(np.nanmin(lats)),
#                             "lat_max": float(np.nanmax(lats)),
#                             "lon_min": float(np.nanmin(lons)),
#                             "lon_max": float(np.nanmax(lons)),
#                         }

#                 # Profile count and parameter list
#                 metadata["profile_count"] = int(ds.dims.get("N_PROF", 0))
#                 param_vars = ["TEMP", "TEMP_ADJUSTED", "PSAL", "PSAL_ADJUSTED", "PRES", "PRES_ADJUSTED",
#                               "DOXY", "CHLA", "BBP700", "NITRATE", "PH_IN_SITU_TOTAL"]
#                 metadata["parameter_list"] = [v for v in param_vars if v in ds.variables]

#                 # QC summary (optional)
#                 qc_vars = [v for v in ds.variables if v.endswith("_QC")]
#                 qsum: Dict[str, Dict[str, int]] = {}
#                 for q in qc_vars:
#                     try:
#                         s = pd.Series(np.array(ds[q].values).astype("U1").flatten())
#                         counts = s.value_counts(dropna=False).to_dict()
#                         qsum[q] = {str(k): int(v) for k, v in counts.items()}
#                     except Exception:
#                         continue
#                 metadata["quality_summary"] = qsum

#         except Exception as e:
#             logger.error(f"Error extracting metadata from {file_path}: {e}")
#             metadata["error"] = str(e)

#         return metadata

#     # ---------------------- Processing ----------------------

#     def process_profiles_to_dataframe(self, file_path: Path) -> pd.DataFrame:
#         """
#         Convert NetCDF profile data to a tidy DataFrame with QC filtering.

#         Returns columns:
#           time, latitude, longitude, pressure, depth, temperature, salinity,
#           temp_qc, psal_qc, profile_id, level_id
#         """
#         try:
#             with xr.open_dataset(file_path) as ds:
#                 n_prof = int(ds.dims.get("N_PROF", 0))
#                 n_lev = int(ds.dims.get("N_LEVELS", 0))
#                 if n_prof == 0 or n_lev == 0:
#                     return pd.DataFrame()

#                 # Resolve variable names (prefer adjusted)
#                 temp_var = _first_present(ds, ["TEMP_ADJUSTED", "TEMP"])
#                 psal_var = _first_present(ds, ["PSAL_ADJUSTED", "PSAL"])
#                 pres_var = _first_present(ds, ["PRES_ADJUSTED", "PRES"])
#                 time_var = _first_present(ds, ["JULD", "TIME"])
#                 lat_var = "LATITUDE"
#                 lon_var = "LONGITUDE"

#                 if not all([temp_var, psal_var, pres_var, time_var, lat_var in ds, lon_var in ds]):
#                     return pd.DataFrame()

#                 # QC variables (optional); prefer adjusted QC
#                 temp_qc_var = _first_present(ds, ["TEMP_ADJUSTED_QC", "TEMP_QC"])
#                 psal_qc_var = _first_present(ds, ["PSAL_ADJUSTED_QC", "PSAL_QC"])

#                 temp = np.array(ds[temp_var].values, dtype=float)         # shape (N_PROF, N_LEVELS)
#                 psal = np.array(ds[psal_var].values, dtype=float)         # shape (N_PROF, N_LEVELS)
#                 pres = np.array(ds[pres_var].values, dtype=float)         # shape (N_PROF, N_LEVELS)
#                 juld = np.array(ds[time_var].values, dtype=float)         # shape (N_PROF,)
#                 lats = np.array(ds[lat_var].values, dtype=float)          # shape (N_PROF,)
#                 lons = np.array(ds[lon_var].values, dtype=float)          # shape (N_PROF,)

#                 if temp_qc_var:
#                     t_qc = np.array(ds[temp_qc_var].values).astype("U1")
#                 else:
#                     t_qc = np.full_like(temp, "1", dtype="U1")

#                 if psal_qc_var:
#                     s_qc = np.array(ds[psal_qc_var].values).astype("U1")
#                 else:
#                     s_qc = np.full_like(psal, "1", dtype="U1")

#                 good_qc = {"1", "2"}

#                 rows: List[Dict[str, Any]] = []
#                 for p in range(n_prof):
#                     tstamp = _juld_to_datetime(juld[p])
#                     lat = float(lats[p]) if np.isfinite(lats[p]) else None
#                     lon = float(lons[p]) if np.isfinite(lons[p]) else None
#                     if tstamp is None or lat is None or lon is None:
#                         continue

#                     for k in range(n_lev):
#                         T = temp[p, k]
#                         P = pres[p, k]
#                         S = psal[p, k]
#                         if not (np.isfinite(T) and np.isfinite(P) and np.isfinite(S)):
#                             continue
#                         tq = str(t_qc[p, k]) if t_qc is not None else "1"
#                         sq = str(s_qc[p, k]) if s_qc is not None else "1"
#                         if tq not in good_qc or sq not in good_qc:
#                             continue

#                         rows.append(
#                             {
#                                 "time": pd.Timestamp(tstamp),
#                                 "latitude": lat,
#                                 "longitude": lon,
#                                 "pressure": float(P),
#                                 "depth": float(self._pressure_to_depth(P, lat)),
#                                 "temperature": float(T),
#                                 "salinity": float(S),
#                                 "temp_qc": tq,
#                                 "psal_qc": sq,
#                                 "profile_id": p,
#                                 "level_id": k,
#                             }
#                         )

#                 return pd.DataFrame(rows)
#         except Exception as e:
#             logger.error(f"Error processing profiles from {file_path}: {e}")
#             return pd.DataFrame()

#     # ---------------------- Physics helper ----------------------

#     def _pressure_to_depth(self, pressure: float, latitude: float) -> float:
#         """
#         Approximate conversion from pressure (dbar) to depth (m).

#         Uses a commonly used UNESCO/Saunders-Fofonoff style approximation with
#         weak latitude dependence; sufficient for visualization and PoC.
#         """
#         try:
#             # Latitude in radians
#             phi = np.deg2rad(latitude if latitude is not None else 0.0)
#             sin2 = np.sin(phi) ** 2
#             # Gravity as function of latitude (m/s^2)
#             g = 9.780318 * (1.0 + 5.2788e-3 * sin2 + 2.36e-5 * (sin2**2))
#             # Depth approximation (m); pressure in dbar ~ 1e4 Pa
#             # Empirical polynomial in pressure (dbar)
#             P = float(pressure)
#             depth = (((-1.82e-15 * P + 2.279e-10) * P - 2.2512e-5) * P + 9.72659) * P
#             # Small latitude correction via gravity ratio
#             depth *= (9.80665 / g)
#             return float(max(depth, 0.0))
#         except Exception:
#             # Fallback simple scale if anything goes wrong
#             return float(pressure) * 1.019716

#     # ---------------------- Output ----------------------

#     def save_to_parquet(self, df: pd.DataFrame, output_path: Path) -> bool:
#         """Save DataFrame to Parquet (Snappy, pyarrow)."""
#         try:
#             if df.empty:
#                 logger.warning(f"Cannot save empty DataFrame to {output_path}")
#                 return False
#             output_path.parent.mkdir(exist_ok=True, parents=True)
#             df = df.sort_values(["time", "profile_id", "level_id"])
#             df.to_parquet(output_path, engine="pyarrow", compression="snappy", index=False)
#             logger.info(f"Saved {len(df)} records to {output_path}")
#             return True
#         except Exception as e:
#             logger.error(f"Error saving DataFrame to Parquet: {e}")
#             return False

#     # ---------------------- Orchestration ----------------------

#     def process_netcdf_file(self, file_path: Path, float_id: Optional[str] = None) -> Dict[str, Any]:
#         """
#         Process a single NetCDF file end-to-end.
#         """
#         result: Dict[str, Any] = {
#             "file_path": str(file_path),
#             "success": False,
#             "records_processed": 0,
#             "output_files": [],
#             "errors": [],
#             "metadata": {},
#         }

#         # 1) Validate
#         is_valid, errs = self.validate_netcdf_file(file_path)
#         if not is_valid:
#             result["errors"].extend(errs)
#             return result

#         # 2) Metadata
#         metadata = self.extract_metadata(file_path)
#         if float_id:
#             metadata["float_id"] = float_id
#         fid = metadata.get("float_id") or "unknown"
#         result["metadata"] = metadata

#         # 3) Profiles -> DataFrame
#         df = self.process_profiles_to_dataframe(file_path)
#         if df.empty:
#             result["errors"].append("No valid profile data found")
#             return result

#         # 4) Output filename
#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         out_name = f"argo_profiles_{fid}_{ts}.parquet"
#         out_path = self.output_dir / out_name

#         # 5) Save
#         if self.save_to_parquet(df, out_path):
#             result["success"] = True
#             result["records_processed"] = int(len(df))
#             result["output_files"].append(str(out_path))
#         else:
#             result["errors"].append("Failed to save Parquet file")

#         return result

#     def process_directory(self, input_dir: Path) -> Dict[str, Any]:
#         """
#         Process all NetCDF files under a directory (recursive).
#         """
#         summary = {
#             "total_files": 0,
#             "successful": 0,
#             "failed": 0,
#             "total_records": 0,
#             "output_files": [],
#             "errors": [],
#         }

#         files = list(input_dir.glob("*.nc")) + list(input_dir.glob("**/*.nc"))
#         summary["total_files"] = len(files)
#         logger.info(f"Found {len(files)} NetCDF files in {input_dir}")

#         for fp in files:
#             try:
#                 res = self.process_netcdf_file(fp)
#                 if res.get("success"):
#                     summary["successful"] += 1
#                     summary["total_records"] += int(res.get("records_processed", 0))
#                     summary["output_files"].extend(res.get("output_files", []))
#                 else:
#                     summary["failed"] += 1
#                     errs = res.get("errors", [])
#                     summary["errors"].extend([f"{fp}: {e}" for e in errs] if errs else [f"{fp}: unknown error"])
#             except Exception as e:
#                 summary["failed"] += 1
#                 summary["errors"].append(f"{fp}: {e}")

#         logger.info(f"Processing complete: {summary['successful']} successful, {summary['failed']} failed")
#         return summary


# def main():
#     """Simple CLI to test processing."""
#     logging.basicConfig(level=logging.INFO)
#     proc = NetCDFProcessor(output_dir="./processed_argo_data")

#     # Single file example (replace with a real file)
#     example = Path("./example_data/argo_float_example.nc")
#     if example.exists():
#         res = proc.process_netcdf_file(example)
#         print("Single-file result:\n", res)
#     else:
#         print("Example NetCDF file not found at ./example_data/argo_float_example.nc")

#     # Directory example (replace with a real directory)
#     indir = Path("./input_netcdf_files")
#     if indir.exists():
#         summary = proc.process_directory(indir)
#         print("Directory summary:\n", summary)


# if __name__ == "__main__":
#     main()


# # netcdf_to_parquet_grid.py

# import logging
# from pathlib import Path
# from typing import Dict, List, Optional, Tuple, Any
# from datetime import datetime
# import pandas as pd
# import numpy as np
# import xarray as xr

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# # Adapted to tempsal.nc coordinate and variable names
# GRID_TEMP_NAMES = ["TEMP", "temp", "temperature", "thetao", "sst"]
# GRID_SAL_NAMES  = ["SAL", "salinity", "psal", "PSAL"]
# TIME_CANDIDATES = ["TAXIS", "time", "TIME"]
# LAT_CANDIDATES  = ["YAXIS", "lat", "latitude", "LATITUDE"]
# LON_CANDIDATES  = ["XAXIS", "lon", "longitude", "LONGITUDE"]
# DEPTH_CANDS     = ["ZAX", "depth", "lev", "level", "z"]

# def _first_present(ds: xr.Dataset, names: List[str]) -> Optional[str]:
#     for n in names:
#         if n in ds.variables or n in ds.coords:
#             return n
#     return None

# class GridNetCDFProcessor:
#     """
#     Ingests gridded NetCDF like tempsal.nc with dims (TAXIS, ZAX?, YAXIS, XAXIS)
#     and variables TEMP/SAL, then exports a tidy Parquet table.
#     """

#     def __init__(self, output_dir: str = "./processed_argo_data"):
#         self.output_dir = Path(output_dir)
#         self.output_dir.mkdir(exist_ok=True, parents=True)

#     # -------- validation --------
#     def validate(self, fp: Path) -> Tuple[bool, List[str]]:
#         errs: List[str] = []
#         if not fp.exists():
#             return False, [f"File not found: {fp}"]
#         if fp.suffix.lower() != ".nc":
#             return False, [f"Not a NetCDF file: {fp}"]
#         try:
#             with xr.open_dataset(fp) as ds:
#                 t = _first_present(ds, TIME_CANDIDATES)
#                 la = _first_present(ds, LAT_CANDIDATES)
#                 lo = _first_present(ds, LON_CANDIDATES)
#                 tv = _first_present(ds, GRID_TEMP_NAMES)
#                 sv = _first_present(ds, GRID_SAL_NAMES)
#                 if not all([t, la, lo]):
#                     missing = []
#                     if not t: missing.append("TAXIS/time")
#                     if not la: missing.append("YAXIS/lat")
#                     if not lo: missing.append("XAXIS/lon")
#                     errs.append(f"Missing required coords: {missing}")
#                 if not (tv or sv):
#                     errs.append("No temperature/salinity variables found (TEMP/SAL)")
#         except Exception as e:
#             errs.append(f"Error opening dataset: {e}")
#         return len(errs) == 0, errs

#     # -------- metadata --------
#     def extract_metadata(self, fp: Path) -> Dict[str, Any]:
#         meta = {
#             "file_path": str(fp),
#             "processing_date": datetime.now().isoformat(),
#             "variables": [],
#             "dims": {},
#             "date_range": {"start": None, "end": None},
#             "spatial_bounds": {"lat_min": None, "lat_max": None, "lon_min": None, "lon_max": None},
#             "has_depth": False,
#         }
#         try:
#             with xr.open_dataset(fp) as ds:
#                 meta["variables"] = list(ds.data_vars)
#                 meta["dims"] = {k: int(v) for k, v in ds.dims.items()}
#                 t = _first_present(ds, TIME_CANDIDATES)
#                 la = _first_present(ds, LAT_CANDIDATES)
#                 lo = _first_present(ds, LON_CANDIDATES)
#                 if t and ds[t].size:
#                     try:
#                         times = pd.to_datetime(ds[t].values)
#                         meta["date_range"] = {"start": times.min().isoformat(), "end": times.max().isoformat()}
#                     except Exception:
#                         pass
#                 if la and lo:
#                     lats = np.asarray(ds[la].values, dtype=float)
#                     lons = np.asarray(ds[lo].values, dtype=float)
#                     meta["spatial_bounds"] = {
#                         "lat_min": float(np.nanmin(lats)), "lat_max": float(np.nanmax(lats)),
#                         "lon_min": float(np.nanmin(lons)), "lon_max": float(np.nanmax(lons)),
#                     }
#                 dvar = _first_present(ds, DEPTH_CANDS)
#                 meta["has_depth"] = dvar is not None
#         except Exception as e:
#             meta["error"] = str(e)
#         return meta

#     # -------- conversion --------
#     def to_dataframe(self, fp: Path) -> pd.DataFrame:
#         """
#         Flatten to tidy rows with columns: time, latitude, longitude, [depth], temperature, salinity.
#         """
#         with xr.open_dataset(fp) as ds:
#             t = _first_present(ds, TIME_CANDIDATES)   # TAXIS
#             la = _first_present(ds, LAT_CANDIDATES)   # YAXIS
#             lo = _first_present(ds, LON_CANDIDATES)   # XAXIS
#             d = _first_present(ds, DEPTH_CANDS)       # ZAX (optional)
#             temp_var = _first_present(ds, GRID_TEMP_NAMES)  # TEMP
#             sal_var  = _first_present(ds, GRID_SAL_NAMES)   # SAL

#             vars_to_keep = [v for v in [temp_var, sal_var] if v]
#             coords = [c for c in [t, la, lo, d] if c]
#             sub = ds[vars_to_keep].set_coords(coords).transpose(...)

#             # Stack dims in a consistent order
#             stack_dims = [dim for dim in [t, d, la, lo] if dim in sub.dims]
#             stacked = sub.stack(index=stack_dims).dropna(dim="index", how="all")

#             df = stacked.to_dataframe().reset_index()

#             # Rename to canonical column names
#             if t in df: df.rename(columns={t: "time"}, inplace=True)
#             if la in df: df.rename(columns={la: "latitude"}, inplace=True)
#             if lo in df: df.rename(columns={lo: "longitude"}, inplace=True)
#             if d and d in df: df.rename(columns={d: "depth"}, inplace=True)
#             if temp_var and temp_var in df: df.rename(columns={temp_var: "temperature"}, inplace=True)
#             if sal_var and sal_var in df: df.rename(columns={sal_var: "salinity"}, inplace=True)

#             keep = ["time", "latitude", "longitude", "depth", "temperature", "salinity"]
#             df = df[[c for c in keep if c in df.columns]]

#             # Drop rows with neither temperature nor salinity
#             meas_cols = [c for c in ["temperature", "salinity"] if c in df.columns]
#             if meas_cols:
#                 df = df.dropna(subset=meas_cols, how="all")

#             # Ensure types
#             if "time" in df.columns:
#                 try:
#                     df["time"] = pd.to_datetime(df["time"])
#                 except Exception:
#                     pass
#             for col in ["latitude", "longitude", "depth", "temperature", "salinity"]:
#                 if col in df.columns:
#                     df[col] = pd.to_numeric(df[col], errors="coerce")
#             return df

#     # -------- saving --------
#     def save_parquet(self, df: pd.DataFrame, out: Path) -> bool:
#         try:
#             if df.empty:
#                 logger.warning("No data to save.")
#                 return False
#             out.parent.mkdir(parents=True, exist_ok=True)
#             df.to_parquet(out, engine="pyarrow", compression="snappy", index=False)
#             logger.info(f"Saved {len(df)} rows to {out}")
#             return True
#         except Exception as e:
#             logger.error(f"Parquet write failed: {e}")
#             return False

#     # -------- end-to-end --------
#     def process_file(self, fp: Path) -> Dict[str, Any]:
#         ok, errs = self.validate(fp)
#         result = {
#             "file_path": str(fp),
#             "success": False,
#             "errors": errs.copy(),
#             "records": 0,
#             "output_file": None,
#             "metadata": {},
#         }
#         if not ok:
#             return result

#         meta = self.extract_metadata(fp)
#         result["metadata"] = meta
#         df = self.to_dataframe(fp)
#         if df.empty:
#             result["errors"].append("Empty data after flattening")
#             return result

#         ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#         out_name = f"grid_tempsal_{ts}.parquet"
#         out_path = self.output_dir / out_name
#         if self.save_parquet(df, out_path):
#             result["success"] = True
#             result["records"] = int(len(df))
#             result["output_file"] = str(out_path)
#         else:
#             result["errors"].append("Failed to save parquet")
#         return result


# netcdf_to_parquet_grid.py

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import pandas as pd
import numpy as np
import xarray as xr

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Coordinate and variable names for tempsal.nc
GRID_TEMP_NAMES = ["TEMP", "temp", "temperature", "thetao", "sst"]
GRID_SAL_NAMES  = ["SAL", "salinity", "psal", "PSAL"]
TIME_CANDIDATES = ["TAXIS", "time", "TIME"]
LAT_CANDIDATES  = ["YAXIS", "lat", "latitude", "LATITUDE"]
LON_CANDIDATES  = ["XAXIS", "lon", "longitude", "LONGITUDE"]
DEPTH_CANDS     = ["ZAX", "depth", "lev", "level", "z"]

def _first_present(ds: xr.Dataset, names: List[str]) -> Optional[str]:
    for n in names:
        if n in ds.variables or n in ds.coords:
            return n
    return None

class GridNetCDFProcessor:
    """
    Ingest gridded NetCDF with dims (TAXIS, ZAX?, YAXIS, XAXIS) and variables
    TEMP/SAL; export tidy Parquet with columns: time, latitude, longitude, [depth], temperature, salinity.
    """

    def __init__(self, output_dir: str = "./processed_argo_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)

    # -------- validation --------
    def validate(self, fp: Path) -> Tuple[bool, List[str]]:
        errs: List[str] = []
        if not fp.exists():
            return False, [f"File not found: {fp}"]
        if fp.suffix.lower() != ".nc":
            return False, [f"Not a NetCDF file: {fp}"]
        try:
            with xr.open_dataset(fp) as ds:
                t = _first_present(ds, TIME_CANDIDATES)
                la = _first_present(ds, LAT_CANDIDATES)
                lo = _first_present(ds, LON_CANDIDATES)
                tv = _first_present(ds, GRID_TEMP_NAMES)
                sv = _first_present(ds, GRID_SAL_NAMES)
                if not all([t, la, lo]):
                    missing = []
                    if not t: missing.append("TAXIS/time")
                    if not la: missing.append("YAXIS/lat")
                    if not lo: missing.append("XAXIS/lon")
                    errs.append(f"Missing required coords: {missing}")
                if not (tv or sv):
                    errs.append("No temperature/salinity variables found (TEMP/SAL)")
        except Exception as e:
            errs.append(f"Error opening dataset: {e}")
        return len(errs) == 0, errs

    # -------- metadata --------
    def extract_metadata(self, fp: Path) -> Dict[str, Any]:
        meta = {
            "file_path": str(fp),
            "processing_date": datetime.now().isoformat(),
            "variables": [],
            "dims": {},
            "date_range": {"start": None, "end": None},
            "spatial_bounds": {"lat_min": None, "lat_max": None, "lon_min": None, "lon_max": None},
            "has_depth": False,
        }
        try:
            with xr.open_dataset(fp) as ds:
                meta["variables"] = list(ds.data_vars)
                # Use sizes to avoid dims future warning
                meta["dims"] = {k: int(v) for k, v in ds.sizes.items()}
                t = _first_present(ds, TIME_CANDIDATES)
                la = _first_present(ds, LAT_CANDIDATES)
                lo = _first_present(ds, LON_CANDIDATES)
                if t and ds[t].size:
                    try:
                        times = pd.to_datetime(ds[t].values)
                        meta["date_range"] = {"start": times.min().isoformat(), "end": times.max().isoformat()}
                    except Exception:
                        pass
                if la and lo:
                    lats = np.asarray(ds[la].values, dtype=float)
                    lons = np.asarray(ds[lo].values, dtype=float)
                    meta["spatial_bounds"] = {
                        "lat_min": float(np.nanmin(lats)), "lat_max": float(np.nanmax(lats)),
                        "lon_min": float(np.nanmin(lons)), "lon_max": float(np.nanmax(lons)),
                    }
                dvar = _first_present(ds, DEPTH_CANDS)
                meta["has_depth"] = dvar is not None
        except Exception as e:
            meta["error"] = str(e)
        return meta

    # -------- conversion --------
    def to_dataframe(self, fp: Path) -> pd.DataFrame:
        """
        Flatten to tidy rows while avoiding reset_index column collisions.
        """
        with xr.open_dataset(fp) as ds:
            t_name = _first_present(ds, TIME_CANDIDATES)
            la_name = _first_present(ds, LAT_CANDIDATES)
            lo_name = _first_present(ds, LON_CANDIDATES)
            d_name  = _first_present(ds, DEPTH_CANDS)
            temp_var = _first_present(ds, GRID_TEMP_NAMES)
            sal_var  = _first_present(ds, GRID_SAL_NAMES)

            vars_to_keep = [v for v in [temp_var, sal_var] if v]
            coords = [c for c in [t_name, la_name, lo_name, d_name] if c]
            sub = ds[vars_to_keep].set_coords(coords).transpose(...)

            stack_dims = [dim for dim in [t_name, d_name, la_name, lo_name] if dim in sub.dims]
            stacked = sub.stack(index=stack_dims).dropna(dim="index", how="all")

            # Build index columns explicitly to avoid collisions on reset_index
            idx_df = stacked.indexes["index"].to_frame(index=False)
            # Rename to canonical names
            rename_map = {}
            if t_name in idx_df: rename_map[t_name] = "time"
            if la_name in idx_df: rename_map[la_name] = "latitude"
            if lo_name in idx_df: rename_map[lo_name] = "longitude"
            if d_name and d_name in idx_df: rename_map[d_name] = "depth"
            idx_df.rename(columns=rename_map, inplace=True)

            # Convert data variables to a plain DataFrame (no index columns yet)
            values_df = stacked.to_dataframe().reset_index(drop=True)

            # Concatenate coords and values
            df = pd.concat([idx_df.reset_index(drop=True), values_df], axis=1)

            # Rename data variables
            if temp_var and temp_var in df: df.rename(columns={temp_var: "temperature"}, inplace=True)
            if sal_var and sal_var in df: df.rename(columns={sal_var: "salinity"}, inplace=True)

            # Keep expected columns and drop empty rows
            keep = ["time", "latitude", "longitude", "depth", "temperature", "salinity"]
            df = df[[c for c in keep if c in df.columns]]
            meas_cols = [c for c in ["temperature", "salinity"] if c in df.columns]
            if meas_cols:
                df = df.dropna(subset=meas_cols, how="all")

            # Enforce dtypes
            if "time" in df.columns:
                try: df["time"] = pd.to_datetime(df["time"])
                except Exception: pass
            for col in ["latitude", "longitude", "depth", "temperature", "salinity"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            return df

    # -------- saving --------
    def save_parquet(self, df: pd.DataFrame, out: Path) -> bool:
        try:
            if df.empty:
                logger.warning("No data to save.")
                return False
            out.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(out, engine="pyarrow", compression="snappy", index=False)
            logger.info(f"Saved {len(df)} rows to {out}")
            return True
        except Exception as e:
            logger.error(f"Parquet write failed: {e}")
            return False

    # -------- end-to-end --------
    def process_file(self, fp: Path) -> Dict[str, Any]:
        ok, errs = self.validate(fp)
        result = {
            "file_path": str(fp),
            "success": False,
            "errors": errs.copy(),
            "records": 0,
            "output_file": None,
            "metadata": {},
        }
        if not ok:
            return result

        meta = self.extract_metadata(fp)
        result["metadata"] = meta

        df = self.to_dataframe(fp)
        if df.empty:
            result["errors"].append("Empty data after flattening")
            return result

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_name = f"grid_tempsal_{ts}.parquet"
        out_path = self.output_dir / out_name

        if self.save_parquet(df, out_path):
            result["success"] = True
            result["records"] = int(len(df))
            result["output_file"] = str(out_path)
        else:
            result["errors"].append("Failed to save parquet")
        return result
