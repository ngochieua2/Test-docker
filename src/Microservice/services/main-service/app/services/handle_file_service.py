from shared.utils import get_logger
import pandas as pd
import io
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings


logger = get_logger(__name__, settings.LOG_LEVEL, settings.LOG_FORMAT)

class HandleFileService:
    """
    Business logic for file handling operations
    """
    
    async def generate_data_summary(file: UploadFile, file_type: str) -> Optional[str]:
        logger.info("Start to generate data summary")
        summary_lines = []

        contents = await file.read()
        main_dataframe = pd.read_csv(io.BytesIO(contents)) if file_type == '.csv' else pd.read_excel(io.BytesIO(contents))

        summary_lines.append("\n🔍 FIRST 10 ROWS (original):")
        for index, row in main_dataframe.head(10).iterrows():
            row_text = ', '.join(str(value) for value in row)
            summary_lines.append(f"row {index + 1}: {row_text}")

        main_dataframe.dropna(how='all', inplace=True)
        main_dataframe.dropna(axis=1, how='all', inplace=True)
        main_dataframe.columns = main_dataframe.columns.str.strip()

        columns = main_dataframe.columns

        summary_lines.append("🧾 DATA SUMMARY\n")
        summary_lines.append(f"🔢 Total Records: {len(main_dataframe)}")
        summary_lines.append(f"🧱 Columns: {list(columns)}\n")

        summary_lines.append("📌 COLUMN DETAILS:")

        for column in columns:
            sample_values = main_dataframe[column].dropna().astype(str).unique()[:3]
            is_unique = main_dataframe[column].is_unique
            dtype = main_dataframe[column].dtype

            summary_lines.append(f"\n🧷 Column: {column}")
            summary_lines.append(f"    - Data type: {dtype}")
            summary_lines.append(f"    - Sample values: {sample_values}")
            summary_lines.append(f"    - Unique: {'Yes ✅' if is_unique else 'No ❌'}")
            summary_lines.append(f"    - Null values: {main_dataframe[column].isnull().sum()}")

            if pd.api.types.is_numeric_dtype(main_dataframe[column]):
                summary_lines.append(f"    - Min: {main_dataframe[column].min()}, Max: {main_dataframe[column].max()}")
            elif pd.api.types.is_datetime64_any_dtype(main_dataframe[column]) or "time" in column.lower():
                try:
                    main_dataframe[column] = pd.to_datetime(main_dataframe[column])
                    summary_lines.append(
                        f"    - Date range: {main_dataframe[column].min()} to {main_dataframe[column].max()}")
                except:
                    summary_lines.append("    - ⚠️ Could not parse datetime")

            summary_lines.append("-" * 60)

        summary_lines.append("\n📊 VALUE DISTRIBUTION SUMMARY:")
        summary = []
        for column in main_dataframe.columns:
            value_counts = main_dataframe[column].value_counts(dropna=True)
            unique_count = value_counts.shape[0]
            median_freq = value_counts.median()
            top3 = value_counts.head(3).to_dict()
            summary.append({
                'Column': column,
                'Unique Values': unique_count,
                'Median Frequency': median_freq,
                'Top 3 Most Common': top3
            })
        summary_dataframe = pd.DataFrame(summary)
        summary_lines.append(summary_dataframe.to_string(index=False))

        summary_lines.append("\n📈 KNOWN DIMENSION DISTRIBUTIONS (if present):")
        for key in ['imsi', 'subscriptionId', 'offerName', 'zone', 'requestType', 'mccmnc']:
            if key in main_dataframe.columns:
                summary_lines.append(f"\n▶ {key} distribution:")
                summary_lines.append(main_dataframe[key].value_counts().describe().to_string())
                summary_lines.append(main_dataframe[key].value_counts().head(5).to_string())

        if 'requestType' in main_dataframe.columns:
            summary_lines.append("\n📂 Request Type Breakdown:")
            summary_lines.append(main_dataframe['requestType'].value_counts().to_string())

        return "\n".join(summary_lines)
    