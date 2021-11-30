import streamlit as st
from airlinefunctions2 import *
from datetime import date
import json
from streamlit.type_util import Key


with open('final_flights_output.json', 'r') as myfile: #flights data
    pstate=myfile.read()
flights = json.loads(pstate) 
myfile.close()

st.set_page_config(layout="wide")


header = st.container() #inititalize containers for the inputs that will go  into the searcher
dataset= st.container()
features = st.container()
model_training= st.container()
col1, col2, col3, col4 = st.columns(4) 

with header: #next few lines creates the headers, search inputs for searcher
    st.title('Welcome to the Airfare Website!')
    st.text('Please enter your flight details')
    
with dataset: 
    st.header('Flights dates:')
    with col1:
        d1 = st.date_input(
            "When do you want to leave?",
            date(2022, 2, 26))

    with col2:
        d2 = st.date_input(
            "When do you want to comeback?",
            date(2022, 3, 1))

    with col3:
        d3 = st.selectbox(
            "From",
            ['DTW', 'MSY', 'MIA','LAX', 'SEA'])
            
    with col4:
        d4 = st.text_input(
            "To",
            value="Anywhere")

if st.button('Search'):
    if d4.lower()=='anywhere': #if someone searches anywhere, they will get prices from anywhere
        simple = ConcreteComponent([['2022-02-26', d2.strftime("%Y-%m-%d"), d3, d4], flights['data']])   #only need to use 2nd decorator for search
        decorator1 = DateDecorator(simple)
        decorator2 = ObDecorator(decorator1)
        output=cheapest25(decorator2.operation()[1]) #output is list of flight information
    else: #get the exact price for exact flight they want
        simple = ConcreteComponent([['2022-02-26', d2.strftime("%Y-%m-%d"), d3, d4], flights['data']])   #initialize components for decorator
        decorator1 = DateDecorator(simple)
        decorator2 = ObDecorator(decorator1)
        decorator3 = IbDecorator(decorator2)
        output=cheapest25(decorator3.operation()[1]) #output is list of flight information
    if len(output)==0:
        st.write('No Flights Found. Try a different search!') #sometimes flights not found 
    else:
        for i in range(len(output)): #list if flight is found
            st.markdown("""---""")
            cols = st.columns(5)
            cols[0].write('Outbound: ')
            cols[0].write(output[i]['obd_time']+ " - "+ output[i]['oba_time'])
            cols[0].write(output[i]['ob_carrier'])
            cols[1].write(output[i]['ob']+ " - "+ output[i]['ib'])
            cols[1].write(output[i]['obfl'])
            cols[1].write(output[i]['ob_stops'])
            cols[2].write('Inbound: ')
            cols[2].write(output[i]['ibd_time']+ " - "+ output[i]['iba_time'])
            cols[2].write(output[i]['ob_carrier'])
            cols[3].write(output[i]['ib']+ " - "+ output[i]['ob'])
            cols[3].write(output[i]['ibfl'])
            cols[3].write(output[i]['ib_stops'])
            cols[4].write('Price:')
            cols[4].write("$"+ str(output[i]["price"]))
            url=output[i]['ob']+"-"+output[i]['ib']+'/'+"2022-02-26"+'/'+d2.strftime("%Y-%m-%d")+'?sort=price_a'
            link= f'[Purchase](https://www.kayak.com/flights/{url})'
            cols[4].markdown(link, unsafe_allow_html=True)
        
        

