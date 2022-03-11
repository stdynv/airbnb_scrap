import csv
from optparse import Values
import streamlit as st 
import pandas as pd
import plotly.express as px

st.title('PARIS AIRBNB DATASET ')

@st.cache
def load_data():
    try : 
        DATA_URL = 'http://127.0.0.1:5000/'
        data = pd.read_json(DATA_URL)
        data.drop(['_id'],axis=1,inplace=True)
        return data
    except Exception as ex : 
        st.exception(ex)
df = load_data()

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def filter_daset() : 
    # Filtrer par prix
    price_range = st.sidebar.slider(
        'Price range', 
        min_value = int(df['Price per Night'].min()), 
        max_value =int(df['Price per Night'].max()),
        value=int(df['Price per Night'].max())
    )
    # maximum nombre d'invités
    allowed_guests = st.sidebar.number_input('Maximum Allowed Guest',
    min_value=1,max_value=int(df['Allowed Guests'].max()),value=int(df['Allowed Guests'].max()))
    
    df_filtred = df.loc[(df['Price per Night'] <= price_range) & (df['Allowed Guests'] <= allowed_guests)]
    st.dataframe(df_filtred)

    csv = convert_df(df_filtred)
    
    download_data = st.sidebar.download_button('Download Data',data=csv,mime='text/csv')
filter_daset()



# filter per price 




