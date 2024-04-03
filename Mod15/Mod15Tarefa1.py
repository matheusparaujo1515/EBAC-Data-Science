import streamlit as st
import pandas as pd
import numpy as np
import time
# import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk


st.set_page_config(page_title='Mod 15 Tarefa 01', layout='wide',
                   page_icon='https://seeklogo.com/images/E/ebac-logo-CC73A39D07-seeklogo.com.png')


st.markdown("<h1 style='text-align: center; color: yellow;'> Mod 15 Tarefa 01 </h1>",
            unsafe_allow_html=True)
st.title('1) Crie uma aplicação com streamlit reproduzindo pelo menos 20 códigos extraídos da documentação do Streamlit')


st.markdown('## a) Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data = load_data(10000)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
st.markdown(
    'Referência: [Create an app](ttps://docs.streamlit.io/get-started/tutorials/create-an-app) ')


st.markdown('--------')
st.markdown('## b) How to animate elements?')

progress_bar = st.progress(0)
status_text = st.empty()
chart = st.line_chart(np.random.randn(10, 2))

for i in range(100):
    # Update progress bar.
    progress_bar.progress(i + 1)

    new_rows = np.random.randn(10, 2)

    # Update status text.
    status_text.text(
        'The latest random number is: %s' % new_rows[-1, 1])

    # Append data to the chart.
    chart.add_rows(new_rows)

    # Pretend we're doing some computation that takes time.
    time.sleep(0.04)

status_text.text('Done!')
st.balloons()
st.markdown(
    'Referência: [How to animate elements?](https://docs.streamlit.io/knowledge-base/using-streamlit/animate-elements)')


st.markdown('--------')
st.markdown('## c) st.metric')

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

st.metric(label="Gas price", value=4, delta=-0.5,
          delta_color="inverse")

st.metric(label="Active developers", value=123, delta=123,
          delta_color="off")
st.markdown(
    'Referência: [st.metric](https://docs.streamlit.io/library/api-reference/data/st.metric)')


# st.markdown('--------')
# st.markdown('## d) st.pyplot')

# arr = np.random.normal(1, 1, size=100)
# fig, ax = plt.subplots()
# ax.hist(arr, bins=20)

# st.pyplot(fig)
# st.markdown(
#     'Referência: [st.pyplot](https://docs.streamlit.io/library/api-reference/charts/st.pyplot)')


st.markdown('--------')
st.markdown('## d) st.scatter_chart')

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.scatter_chart(chart_data)
chart_data = pd.DataFrame(np.random.randn(
    20, 3), columns=["col1", "col2", "col3"])
chart_data['col4'] = np.random.choice(['A', 'B', 'C'], 20)

st.scatter_chart(
    chart_data,
    x='col1',
    y='col2',
    color='col4',
    size='col3',
)
chart_data = pd.DataFrame(np.random.randn(20, 4), columns=[
                          "col1", "col2", "col3", "col4"])

st.scatter_chart(
    chart_data,
    x='col1',
    y=['col2', 'col3'],
    size='col4',
    color=['#FF0000', '#0000FF'],  # Optional
)
st.markdown(
    'Referência: [st.scatter_chart](https://docs.streamlit.io/library/api-reference/charts/st.scatter_chart)')


st.markdown('--------')
st.markdown('## e) st.area_chart')
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.area_chart(chart_data)

chart_data = pd.DataFrame(
    {
        "col1": np.random.randn(20),
        "col2": np.random.randn(20),
        "col3": np.random.choice(["A", "B", "C"], 20),
    }
)

st.area_chart(chart_data, x="col1", y="col2", color="col3")

chart_data = pd.DataFrame(np.random.randn(
    20, 3), columns=["col1", "col2", "col3"])

st.area_chart(
    # Optional
    chart_data, x="col1", y=["col2", "col3"], color=["#FF0000", "#0000FF"]
)
st.markdown(
    'Referência: [st.area_chart](https://docs.streamlit.io/library/api-reference/charts/st.area_chart)')


st.markdown('--------')
st.markdown('## f) st.pydeck_chart')
chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=chart_data,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))
st.markdown(
    'Referência: [st.pydeck_chart](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)')
