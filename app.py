
import streamlit as st
from datetime import date
from datetime import datetime, timedelta
import pandas as pd
import requests
import time
from streamlit_kpi_metric import metric_row


### --------------SURF WAVES STREAMLIT CODE -------------------------###

# ------------------------Header Section-----------------------------#

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide",page_title='SurfWaves Project',page_icon=':surfer:')
st.title("""SURFWAVES PROJECT :surfer:""")




# ------------------------SideBar Section-----------------------------#
st.sidebar.header(':round_pushpin: Where would you like to surf?')

#Add a select box to choose the location

api_input = st.sidebar.selectbox(
    '',
    ('DePanne', 'Oostend', 'Knokke')
)

if api_input == 'DePanne':
    st.sidebar.markdown('''<h4 style='text-align: justify; color: black;'>It is
                        situated close to the border with France in the south-west
                        of Belgian coast. Known for its elongated dunes,
                        the Panne is the place of birth of beach sailing.</h4>
                        ''', unsafe_allow_html=True)
    st.sidebar.write('                                   ')
    st.sidebar.image('DePanne_blue.jpg',use_column_width='always')
    st.sidebar.write('                                   ')
elif api_input == 'Oostend':
    st.sidebar.write('''<h4 style='text-align: justify; color: black;'> As Belgium’s largest coastal outpost, Ostend offers a rare taste of Flemish beach culture.
                     Inland visitors flock to sandy beaches and the seaside promenade, while
                     reminders of the city’s military and maritime history run deep in the old harbor town.</h4>
                     ''', unsafe_allow_html=True)
    st.sidebar.write('                                   ')
    st.sidebar.image('oostend_blue.jpg',use_column_width='always')
    st.sidebar.write('                                   ')
else:
    st.sidebar.write('''<h4 style='text-align: justify; color: black;'>
                     Knokke is the most north-eastern seaside resort on the Belgian coast.
                     It lies adjacent to the Dutch border;
                     separated from the Dutch territory by the Zwin nature reserve.</h4>
                     ''',
                     unsafe_allow_html=True)
    st.sidebar.write('                                   ')
    st.sidebar.image('knokke.jpg',use_column_width='always')
    st.sidebar.write('                                   ')

# --------------------- Left Column Section/Column1------------------#

#Add a time stamp selection
now = datetime.now()

timestamp =pd.to_datetime(now)
# Print the current date only
today = date.today()
tomorrow = today + timedelta(1)

# --------------------- API loading------------------#

#the API I will receive from the API

def get_prediction():
    with st.spinner('Loading data...'):

        url = f'http://127.0.0.1:8000/predict?location={api_input}'
        response = requests.get(url).json()
        api = {"rating": response['rating'],
        'wind_speed': response['wind_speed'],
        'wind_direction':response['wind_direction'],
            'tide': response['tide'],
            'wave_height': response['wave_height'],
            'forecast_high': response['forecast_high'],
            'forecast_low': response['forecast_low'],
            'img_1':response['img_1'],
            'img_2':response['img_2']}

        # -----------------------Add a bar progess -----------------------------------#
    return api

if st.sidebar.button('Click to see the result'):

    api = get_prediction()




#------------------------- Real time information --------------------------------#
    st.markdown('---------------------------------------------------------------')
    st.markdown(f"<h3 style='text-align: center; color: black;'> Forecast for {today}</h3>", unsafe_allow_html=True )
    st.markdown('---------------------------------------------------------------')

    #categorize the tide variation
    if api['tide'] < 200:
        api['tide'] = 'Low Tide'
    elif api['tide'] >= 200 and api['tide'] < 300:
        api['tide'] = 'Middle Tide'
    else:
        api['tide'] = 'High Tide'

    #categorize the wind direction
    if api['wind_direction'] >= 348.75:
        api['wind_direction'] = 'N'

    elif api['wind_direction'] < 11.25:
        api['wind_direction'] ='N'

    elif api['wind_direction'] >= 11.25 and api['wind_direction'] < 33.75:
        api['wind_direction'] = 'NNE'

    elif api['wind_direction'] >= 33.75 and api['wind_direction'] < 56.25:
        api['wind_direction'] = 'NE'

    elif api['wind_direction'] >= 56.25 and api['wind_direction'] < 78.75:
        api['wind_direction'] = 'ENE'

    elif api['wind_direction'] >= 78.75 and api['wind_direction'] < 101.25:
        api['wind_direction'] ='E'

    elif api['wind_direction']>= 101.25 and api['wind_direction']< 123.75:
        api['wind_direction']='ESE'

    elif api['wind_direction'] >= 123.75 and api['wind_direction'] < 146.25:
       api['wind_direction'] = 'SE'

    elif api['wind_direction']>= 146.25 and api['wind_direction']< 168.75:
        api['wind_direction'] = 'SSE'

    elif api['wind_direction']>= 168.75 and api['wind_direction']< 191.25:
        api['wind_direction'] = 'S'

    elif api['wind_direction'] >= 191.25 and api['wind_direction']< 213.75:
       api['wind_direction'] = 'SSW'

    elif api['wind_direction'] >= 213.75 and api['wind_direction'] < 236.25:
        api['wind_direction'] = 'SW'

    elif api['wind_direction'] >= 236.25 and api['wind_direction'] < 258.75:
        api['wind_direction'] = 'WSW'

    elif api['wind_direction'] >= 258.75 and api['wind_direction']< 281.25:
        api['wind_direction'] = 'W'

    elif api['wind_direction'] >= 281.25 and api['wind_direction'] < 303.75:
        api['wind_direction'] = 'WNW'

    elif api['wind_direction']>= 303.75 and api['wind_direction'] < 326.25:
        api['wind_direction'] ='NW'

    elif api['wind_direction'] >= 326.25 and api['wind_direction'] < 348.75:
        api['wind_direction'] = 'NNW'

    metric_row(
            {
                "The direction of the wind": api['wind_direction'],
                "The wind speed in m/s": api['wind_speed'],
                "The Tide ": api['tide']
            }
        )
    metric_row(
        {"prediction for the height": api['wave_height']}
    )

#-------------------------Add forecast------------------------------------------
    st.markdown('''---------------------------------------------------------------''')
    st.markdown(f"<h3 style='text-align: center; color: black'> Forecast for {tomorrow}</h3>", unsafe_allow_html=True )
    st.markdown('''---------------------------------------------------------------''')

    metric_row(
            {
                "Prediction for a High Tide": round(api['forecast_high'],1),
                "Prediction for a Low tide": round(api['forecast_low'],1),
            }
        )

    st.markdown('''  ''')
    st.markdown('''  ''')

    im1, im2, im3 = st.columns([1.5, 3, 1.5])

    with im1:
        st.write('              ')

    with im2:
        st.image(api['img_1'],use_column_width='auto')
        st.image(api['img_2'],use_column_width='auto')

    with im3:
            st.write('       ')

#--------------------------- End of for loop -----------------------------------

else:
    st.write('👈 **Choose your location and click on the button on the sidebar to see if it is a good day to go surfing**')

#-------------------------------Background image--------------------------------
import base64

@st.cache
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

@st.cache
def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="data:image/png;base64,{encoded}">'
    return tag

@st.cache
def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style

image_path = 'pexels-negative-space-127582.jpg'
image_link = 'https://docs.python.org/3/'

st.write(background_image_style(image_path), unsafe_allow_html=True)
