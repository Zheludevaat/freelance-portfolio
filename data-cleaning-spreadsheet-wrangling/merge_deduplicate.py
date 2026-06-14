import pandas as pd

def standardize_columns(df, column_mapping):
    """Standardize column names based on mapping"""
    df = df.rename(columns=column_mapping)
    return df

def main():
    # Define column mappings to standardize different column names
    mapping_1 = {
        'customer_id': 'customer_id',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',
        'phone': 'phone',
        'registration_date': 'registration_date'
    }
    
    mapping_2 = {
        'ID': 'customer_id',
        'FirstName': 'first_name',
        'LastName': 'last_name',
        'Email': 'email',
        'Phone': 'phone',
        'RegDate': 'registration_date'
    }
    
    mapping_3 = {
        'cust_id': 'customer_id',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email_address': 'email',
        'phone_number': 'phone',
        'sign_up_date': 'registration_date'
    }
    
    # Load the three CSV files
    df1 = pd.read_csv('customers_1.csv')
    df2 = pd.read_csv('customers_2.csv')
    df3 = pd.read_csv('customers_3.csv')
    
    # Standardize column names
    df1 = standardize_columns(df1, mapping_1)
    df2 = standardize_columns(df2, mapping_2)
    df3 = standardize_columns(df3, mapping_3)
    
    # Combine all dataframes
    combined_df = pd.concat([df1, df2, df3], ignore_index=True)
    
    # Remove duplicates based on email (assuming email is unique identifier)
    cleaned_df = combined_df.drop_duplicates(subset=['email'], keep='first')
    
    # Sort by customer_id for consistent output
    cleaned_df = cleaned_df.sort_values('customer_id').reset_index(drop=True)
    
    # Save to new CSV
    cleaned_df.to_csv('cleaned_customers.csv', index=False)
    
    print(f"Original records: {len(combined_df)}")
    print(f"After deduplication: {len(cleaned_df)}")
    print(f"Duplicates removed: {len(combined_df) - len(cleaned_df)}")
    print("Cleaned data saved to 'cleaned_customers.csv'")

if __name__ == "__main__":
    main()