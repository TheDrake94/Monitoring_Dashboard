import streamlit as st
st.set_page_config(layout='wide', page_title='Dashboard Stock')
st.write('# Dashboard Apple')
import asyncio
from client_python import client

asyncio.run(client('monitoring'))
