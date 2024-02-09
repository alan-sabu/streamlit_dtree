import streamlit as st
from streamlit_binary_tree import binary_tree
import pandas as pd
from st_aggrid import AgGrid
st.set_page_config(layout="wide")

def getstage():
    if 'stage' not in st.session_state:
        st.session_state['stage'] = 'getdata'
    return st.session_state['stage']

def go_next(next_stage_name,dataframe):
     st.session_state['stage'] = next_stage_name
     if next_stage_name == 'show':
          st.session_state['user_data'] = dataframe.copy()
     

if getstage() == 'getdata':    
    uploaded_file = st.file_uploader("Please upload a CSV", type=["CSV",])
    if uploaded_file:
            uploaded_df = pd.read_csv(uploaded_file)
            uploaded_df = uploaded_df.drop(uploaded_df.tail(2).index)
            st.divider()
            st.dataframe(uploaded_df)
            st.divider()
            st.write(uploaded_df.shape)
            st.button("Next", on_click=go_next, args=("show",uploaded_df))

elif getstage() == "show":
    data = st.session_state['user_data']
    #  response = AgGrid(data)
    #  st.write(response)
    features = st.multiselect("select features",sorted(data.columns.tolist()),
                            default=sorted(data.columns.tolist()))
    target_name = st.selectbox("select target",sorted(data.columns.tolist()),
                            index=len(data.columns)-1)
    
    binary_tree(
        "Analysis_Result",
        data_set=data,
        features=features,
        clf_params={
            "max_depth": 6,     
            "min_samples_leaf": 2 * 1e-2,
            # some required variables from defaults of the library
            "class_weight": "balanced",
            "min_impurity_decrease": 1e-4,
            "random_state": 108,
        },
        target=target_name,
        expanded_depth=2,  # explore leafes one by one
        binary_formatting=True,
        class_names=["not_resolved", target_name],
        class_colors=["#fa4d56","#198038"]
    )

# import streamlit as st
# import pandas as pd
# from streamlit_binary_tree import binary_tree

# # Function to retrieve data from Power BI based on URL
# def get_powerbi_data(url):
#     # Code to connect to Power BI and retrieve data from the specified table URL
#     # Placeholder for demonstration
#     data = pd.read_csv(url)
#     return data

# st.set_page_config(layout="wide")

# def getstage():
#     if 'stage' not in st.session_state:
#         st.session_state['stage'] = 'getdata'
#     return st.session_state['stage']

# def go_next(next_stage_name, dataframe=None):
#     st.session_state['stage'] = next_stage_name
#     if next_stage_name == 'show' and dataframe is not None:
#         st.session_state['user_data'] = dataframe.copy()

# if getstage() == 'getdata':
#     powerbi_url = st.text_input("Enter Power BI Table URL:")
#     if powerbi_url:
#         data = get_powerbi_data(powerbi_url)
#         st.write("Data from Power BI Table:")
#         st.dataframe(data)
#         st.button("Next", on_click=go_next, args=("show", data))

# elif getstage() == "show":
#     data = st.session_state.get('user_data')
#     if data is not None:
#         features = st.multiselect("Select features", sorted(data.columns.tolist()),
#                                   default=sorted(data.columns.tolist()))
#         target_name = st.selectbox("Select target", sorted(data.columns.tolist()),
#                                    index=len(data.columns) - 1)

#         binary_tree(
#             "Analysis_Result",
#             data_set=data,
#             features=features,
#             clf_params={
#                 "max_depth": 6,
#                 "min_samples_leaf": 2 * 1e-2,
#                 # some required variables from defaults of the library
#                 "class_weight": "balanced",
#                 "min_impurity_decrease": 1e-4,
#                 "random_state": 108,
#             },
#             target=target_name,
#             expanded_depth=2,  # explore leaves one by one
#             binary_formatting=True,
#             class_names=["good", target_name],
#         )
#     else:
#         st.warning("No data available. Please provide a valid Power BI Table URL.")

