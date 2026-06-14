# Sales Report Generator

This script demonstrates automated sales data processing by reading multiple CSV sales logs, cleaning the data, aggregating monthly totals, and exporting a formatted Excel report with summary charts.

## Features

- Reads multiple CSV files with sales data
- Cleans and validates data entries
- Aggregates monthly sales totals
- Generates formatted Excel report with summary charts
- Handles missing or malformed data gracefully

## How to Run

1. Ensure you have Python 3.6+ installed
2. Install required dependencies: `pip install pandas openpyxl matplotlib`
3. Place your CSV sales logs in the `data/` directory
4. Run the script: `python sales_report_generator.py`
5. Find the generated report at `output/sales_report.xlsx`

## Example

The script includes sample data. Running it will process the sample CSV files and generate a complete Excel report with charts in the output directory.