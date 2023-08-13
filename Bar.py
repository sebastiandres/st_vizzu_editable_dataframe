import pandas as pd
import streamlit as st
from streamlit.components.v1 import html
from ipyvizzu import Data, Config, Style, Chart, DisplayTarget

###############################################################################
# Parameters
###############################################################################
height = 600

###############################################################################
# Header of page
###############################################################################
st.set_page_config(layout="wide", page_title="Data Editor", page_icon="🧮")
st.header("Editable dataframes and Vizzu charts")
warning_placeholder = st.empty()

###############################################################################
# The editable dataframe
###############################################################################
c1, c2 = st.columns(2)

with c1:
    df = pd.DataFrame({
                "pokemon": ["Bulbasaur", "Charmander", "Pikachu", "Rattata", "Snorlax"],
                "active": [False, True, True, True, False],
                "count": [1, 2, 1, 10, 1],
            })
    st.subheader("My Pokedex (editable table)")
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            #"pokemon": st.column_config.TextColumn(default="Ditto?"),
            "active": st.column_config.CheckboxColumn(default=True),
            "count": st.column_config.NumberColumn(default=1),
        },
    )
    st.caption("If not familiar with how to work with editable dataframes, check the [documentation](http://docs.streamlit.io/library/advanced-features/dataframes#edit-data-with-stdata_editor).")

###############################################################################
# The visualization
###############################################################################
# Clean the dataframe
if edited_df.isnull().values.sum()!=0:
    warning_placeholder.warning("Rows with None, Null or NaN values will not be shown in the visualization.")
else:
    warning_placeholder.empty()
clean_df = edited_df.dropna()
clean_df = clean_df[clean_df["active"]]
# Create/Update the data
data = Data()
data.add_data_frame(clean_df)
# Create the chart
chart = Chart(width=f"100%", display=DisplayTarget.MANUAL)
chart.animate(data)
# Add the first chart
chart.animate(
    #Data.filter("record['active'] == true"), # This is not working
    Config({"x": "pokemon", "y": "count", "color":"pokemon", "title": "My Pokedex (Graph)"}),
)
with c2:
    html(chart._repr_html_(), height=height)