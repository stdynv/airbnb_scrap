import streamlit as st 
import pandas as pd

st.title('AIRBNB DATASET ')
option = st.selectbox(
     'Destination desired ?',
     ('Paris', 'Ibiza', 'Montpellier'))


destination = option
st.markdown(f'{destination} airbnb dataset from 01 April - 14 April (13 nights) ')
def load_data():
    
    try : 
        DATA_URL = f'http://127.0.0.1:5000/{destination}'
        data = pd.read_csv('airbnb.csv')
        data.drop(['_id'],axis=1,inplace=True)
        return data
    except Exception as ex : 
        st.exception(ex)

df = load_data()

# convertir dataframe en csv 
@st.cache
def convert_df(df):
    
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

    # Download filtred dataset
    data_csv = convert_df(df_filtred)
    download_data = st.sidebar.download_button('Download Data',data=data_csv,mime='text/csv')
filter_daset()


