import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, VizzuChart

###############################################################################
# Header of page
###############################################################################
st.set_page_config(layout="wide", page_title="Data Editor and Vizzu", page_icon="🧮")
c1, c2 = st.columns([3, 1])
c1.header("Editable dataframes and Vizzu charts")
c2.button("Useless button")
warning_placeholder = st.empty()

###############################################################################
# The editable dataframe
###############################################################################
c1, c2 = st.columns(2)

initial_df = pd.DataFrame({
            "pokemon": ["Bulbasaur", "Charmander", "Pikachu", "Rattata", "Snorlax"],
            "active": [False, True, True, True, False],
            "count": [1, 2, 1, 10, 1],
        })
if "current_df" not in st.session_state:
    st.session_state.current_df = initial_df
    
with c1:
    st.subheader("My Pokedex (editable table)")
    edited_df = st.data_editor(
        initial_df,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
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
# Create/Update the data - use the data stored in session_state as previous data
current_data = Data()
current_df = st.session_state.current_df
current_data.add_data_frame(current_df[current_df["active"]])
edited_data = Data()
edited_data.add_data_frame(clean_df[clean_df["active"]])
# Create the chart
chart = VizzuChart()
# Add the first chart
chart.animate(current_data)
chart.animate(
    Config({"x": "pokemon", "y": "count", "color":"pokemon", "title": "My Pokedex (Graph)"}),
)
# Add the edited chart
chart.animate(edited_data)
chart.animate(
    #Data.filter("record['active'] == true"), # This is not working
    Config({"x": "pokemon", "y": "count", "color":"pokemon", "title": "My Pokedex (Graph)"}),
)
with c2:
    chart.show()

# Update the dataframe
st.session_state.current_df = clean_df

# Some other links
_, c1, c2, c3 = st.columns([1,2,2,2])
c1.caption("[streamlit-vizzu documentation](https://github.com/vizzu-streamlit/streamlit-vizzu/)")
c2.caption("[streamlit documentation](https://docs.streamlit.io/)")
c3.caption("[(ipy)vizzu documentation](https://ipyvizzu.vizzuhq.com/latest/)")
