import snowflake.connector as sf
import pandas as pd
import sqlalchemy as sa
from snowflake.connector.pandas_tools import write_pandas
import requests


# Variables
url = 'https://a.klaviyo.com/api/profiles'
headers = {
    'revision': '2022-12-31',
    'Accept': 'application/json',
    'Authorization': 'Klaviyo-API-Key pk_d5e028c1df82e29914b8f4a2f0acd0bff8',
}

# Script Start


try:
    print("Fetching data")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    api_data = response.json()

    profiles = api_data.get('data', [])
    df = pd.json_normalize(profiles)


    data_frame = pd.DataFrame(df)
    column_names = data_frame.columns.tolist()
    formatted_values = []

    for col in column_names:
        if '.' in col:
            split_col = col.lower().replace(" ", "_").replace("$", "").split('.')
            formatted_values.append(split_col[-1])
        else:
            formatted_values.append(col)

    data_frame.columns = formatted_values
    print("Data Fetched...", len(data_frame.columns))


    # Connecting Snowflake Database
    print("Establishing snowflake connection")
    connection  = sf.connect(
        user = "GBP",
        password = "Groupadmin@123",
        account = "ncwanha-ck09425",
        warehouse = 'COMPUTE_WH',
        database = "GBP_HEVO", 
        schema = "KLAVIYO_COV_US",
        role = 'ACCOUNTADMIN',
    )

    conn  = connection.cursor()

    print("Database connection established")


    excel_file_path = "C:/Users/HP/Downloads/Klavio Script/profiles_dsdfsda.xlsx"
    data = pd.read_excel(excel_file_path)
    print("Inserting data into Snowflake table...")

    query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'PERSON' AND table_schema = 'KLAVIYO_COV_US'"

    conn.execute(query)
    column_names = conn.fetchall()
    column_list = [col[0].lower() for col in column_names]


    non_matching_elements = []

    for element in column_list:
        if element not in formatted_values and element not in non_matching_elements:
            non_matching_elements.append(element)

    # Find elements in formatted_values not present in array1
    for element in formatted_values:
        if element not in column_list and element not in non_matching_elements:
            non_matching_elements.append(element)

    print(len(non_matching_elements))


    for _, row in data.iterrows():
        placeholder = ", ".join(['%s']*len(row))
        insert_query = f'INSERT INTO PERSON VALUES ({placeholder})'
        conn.execute(insert_query, tuple(row))

    conn.close()

finally:
    conn.close()




