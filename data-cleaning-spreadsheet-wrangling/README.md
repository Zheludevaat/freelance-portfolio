# Customer Database Merge & Deduplication

This project demonstrates merging three disordered customer spreadsheets, standardizing formats, identifying and removing duplicate entries, and outputting a single clean master file.

## Files
- `customers_1.csv`: First sample customer data
- `customers_2.csv`: Second sample customer data
- `customers_3.csv`: Third sample customer data
- `merge_deduplicate.py`: Python script to merge and clean data
- `cleaned_customers.csv`: Final cleaned output

## How to Run

1. Ensure Python 3 is installed
2. Install pandas: `pip install pandas`
3. Run the script: `python merge_deduplicate.py`

The script will process the three input files and generate `cleaned_customers.csv` as output.

## Process

1. Load all three CSV files
2. Standardize column names and data formats
3. Combine all records into one dataset
4. Remove duplicate entries based on email addresses
5. Sort final output by customer ID
6. Save cleaned data to new CSV file