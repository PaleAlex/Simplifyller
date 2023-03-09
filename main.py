import streamlit as st
import pandas as pd
import seaborn as sns
sns.set_theme(style="whitegrid")
import matplotlib.pylab as pylab
import func

params = {
          'figure.figsize': (14, 6),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',        
         }

pylab.rcParams.update(params)


st.set_page_config(page_title="Simplifyller",
                   page_icon="🕳️",
                   layout="wide")
                                    
st.write("<h1 style='text-align: center; background-color: #F9DBBB'>🕳️ Welcome in Simplifyller 🕳️</h1>", unsafe_allow_html=True)
st.write("<h3 style='text-align: center;'> A simple tool to fill missing values in your datesets!</h3>", unsafe_allow_html=True)
st.write("##")
col1,col2,col3 = st.columns([2,3,2])

with col2:
    uploaded = st.file_uploader("Upload your data in a .csv format", type='csv')
if uploaded:
    try:
        df = pd.read_csv(uploaded)
    except:
        st.warning("Encoding error while trying to read the file with utf-8")
    
    st.write("#")
    if not func.findNA(df):
        st.info("Seems like your dataset is already ok")
        
    else:
        na, len_na, rows_to_inspect = func.findNA(df)
        cc = func.criticalColumns(df)
        st.write(f"Seems like your dataset has **{len_na} rows** with missing values in column(s) **{', '.join(cc)}**")
        
        modified_rows = st.experimental_data_editor(na)

        go = st.button("Save changes")
        if go:
            for i in rows_to_inspect:
                df.iloc[i] = modified_rows.loc[i]

            def convert_df(df_to_csv):
                return df_to_csv.to_csv().encode('utf-8')

            csv = convert_df(df)

            st.download_button(
                label="Download the dataset",
                data=csv,
                file_name='elaborated.csv',
                mime='text/csv',
            )

        st.write("#")
        st.write("Here below you can set some simple statistics helping out for the task.")
        with st.form(key="nan"):
            col1, col2= st.columns([1,1])
            with col1:
                row = st.selectbox("Select the row index to examinate", options=rows_to_inspect)
            with col2:
                column_with_na = st.selectbox("Select column with the missing value", options=cc)
            submit_na = st.form_submit_button(label="Select", type='primary')
        
        st.write("#")
        groupings = []
        col1, col2 = st.columns([1,1])
        with col1:
            first_column = st.text_input("Stratified by: *column name*", placeholder='fill or leave empty', help='should be a categorical column', key="groupby1")
        with col2:
            second_column = st.text_input("Stratified by: *column name*", placeholder='fill or leave empty', help='should be a categorical column', key="groupby2")
        
        if first_column in df.columns:
            groupings.append(first_column)
        if second_column in df.columns:
            groupings.append(second_column)

        st.write("##")
        col1, col2, col3 = st.columns([1,10,1])
        with col2:
            st.pyplot(func.boxpl(df, groupings, column_with_na))
            st.write("##")
            st.pyplot(func.histpl(df, groupings, column_with_na, row))
        st.write("##")
        st.dataframe(func.stratifiedView(df, groupings, column_with_na), use_container_width=True)


if not uploaded:
    st.write("#")
    st.write("#")


    with st.expander("**See how Simplifyller works with a sample dataset**"):
        df = pd.read_csv("car_prices.csv")
        st.write("🕳️**Simplifyller**🕳️ selects all the rows with missing values (if any). User can interact with these rows modifying them. This is the beauty of st.experimental_data_editor!")

        if not func.findNA(df):
            st.write("Seems like your dataset is already ok")
        else:
            na, len_na, rows_to_inspect = func.findNA(df)
            cc = func.criticalColumns(df)
            st.write(f"Seems like your dataset has {len_na} rows with missing values in column(s) {', '.join(cc)}")
            
            modified_rows = st.experimental_data_editor(na)

            go = st.button("Save changes")
            if go:
                for i in rows_to_inspect:
                    df.iloc[i] = modified_rows.loc[i]

                def convert_df(df_to_csv):
                    return df_to_csv.to_csv().encode('utf-8')

                csv = convert_df(df)

                st.download_button(
                    label="Download the dataset",
                    data=csv,
                    file_name='elaborated.csv',
                    mime='text/csv',
                )

            st.write("#")
            st.write("Here below you can set some simple statistics helping out for the task.")
            with st.form(key="nan"):
                col1, col2= st.columns([1,1])
                with col1:
                    row = st.selectbox("Select the row index to examinate", options=rows_to_inspect)
                with col2:
                    column_with_na = st.selectbox("Select column with the missing value", options=cc)
                submit_na = st.form_submit_button(label="Select", type='primary')
            
            st.write("#")
            groupings = []
            col1, col2 = st.columns([1,1])
            with col1:
                first_column = st.text_input("Stratified by: *column name*", placeholder='fill or leave empty', help='should be a categorical column', key="groupby1")
            with col2:
                second_column = st.text_input("Stratified by: *column name*", placeholder='fill or leave empty', help='should be a categorical column', key="groupby2")
            
            if first_column in df.columns:
                groupings.append(first_column)
            if second_column in df.columns:
                groupings.append(second_column)

            st.write("##")
            col1, col2, col3 = st.columns([1,10,1])
            with col2:
                st.pyplot(func.boxpl(df, groupings, column_with_na))
                st.write("##")
                st.pyplot(func.histpl(df, groupings, column_with_na, row))
            st.write("##")
            st.dataframe(func.stratifiedView(df, groupings, column_with_na), use_container_width=True)


st.write("#")
st.write("Made by [Alessandro Ciocchetti](https://www.linkedin.com/in/ac-palealex/))









        

