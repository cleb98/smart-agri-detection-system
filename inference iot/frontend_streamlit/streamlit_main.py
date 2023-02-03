
import streamlit as st
import requests
import pandas as pd





API_URL_GET = 'https://so624x.deta.dev/books/'
API_URL_POST = 'https://so624x.deta.dev/books/addbook/'



class data_object:
    def __init__(self, id, name, description, price):
        self.id : str = id 
        self.name : str = name
        self.description : str = description
        self.price : float = price

def ritrieve_table():
    response = requests.get(url=API_URL_GET)
    response.json()
    df = pd.DataFrame.from_dict(response.json())
    return df

def main():
    
    st.markdown("<h1 style='text-align: center;'>📚    Book Test   📚</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Tabella books proveniente dal database</h3>", unsafe_allow_html=True)
    
    table = ritrieve_table()
    st.dataframe(table, use_container_width=True)

    if st.button('refresh'):
        st.experimental_rerun()

    
    st.markdown("<h3 style='text-align: center;'>Inserisci un nuovo book nel database</h3>", unsafe_allow_html=True)

    with st.form(key="test_form", clear_on_submit=True):
        
        my_df = ritrieve_table()

        id_input = int(my_df['id'].tail(1).values[0] + 1)
        name_input = st.text_input(label="inserisci nome del libro")
        description_input = st.text_input(label="inserisci descrizione del libro")
        price_input = st.text_input(label="inserisci il prezzo del libro")

        submitted = st.form_submit_button("Submit")

        if submitted:
            myobj = data_object(id=id_input, name=name_input, description=description_input, price=float(price_input))
            response = requests.post(url=API_URL_POST, json=vars(myobj))
            print(response)


if __name__ == '__main__':
    main()


