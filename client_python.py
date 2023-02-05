from collections import deque, defaultdict
from functools import partial
import aiohttp
import pandas as pd
import streamlit as st
import altair as alt

placeholder = st.empty()

async def client(stock):
    windows = defaultdict(partial(deque, [], maxlen=60))
    CONNECTION = f"ws://localhost:5000/monitoring/{stock}"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.ws_connect(CONNECTION) as websocket:
            async for message in websocket:
                
                data = message.json()
                
                windows['time'].append(data['time'])
                windows['value'].append(data['value'])
                
                df = pd.DataFrame({'time':list(windows['time']),
                                   'value':list(windows['value'])
                                  })
                
                with placeholder.container():
                    chart_finance = alt.Chart(df).mark_line(color='#e45756', point={'filled': True,
                                                                                    "fill": '#e45756'        
                                                            }).encode(
                                                                x = alt.X('time:T', 
                                                                          title='Time'),
                                                                y = alt.Y('value:Q',
                                                                          title='Stock',
                                                                          scale=alt.Scale(zero=False))
                                                            ).properties(
                                                                height=500,
                                                                
                                                            ).configure_axis(
                                                                labelFontSize=20,
                                                                titleFontSize=20
                                                            )
                    
                    st.altair_chart(chart_finance, use_container_width=True)
                    