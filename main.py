import uuid

import streamlit as st
import list_loader.list_loader as list_load
from table_parsing.table_parser import TableParser
import utils.utils as utils
import multiple_tables_parser.multiple_tables_parser as tables_parser


def submit_name_list(names_list):
    if names_list is not None:
       utils.copy_file_input_stream(names_list, "names_list.csv")

       st.session_state["names_list"] = list_load.load_names_list()
       st.session_state["submitted_name_list"] = True
       st.rerun()
    else:
        st.warning("Please upload a valid csv file")

def submit_table(uploaded_file, name_colon_number, country_colon_number, ranking_colon_number, regatta_name, class_name):
    print([uploaded_file, name_colon_number, country_colon_number, ranking_colon_number, regatta_name, class_name])
    utils.copy_file_input_stream(uploaded_file, f"table{len(st.session_state["table_parsers_list"])}.csv")
    parser = TableParser(path=f"table{len(st.session_state["table_parsers_list"])}.csv",
                         name_colon_number = name_colon_number,
                         country_colon_number=country_colon_number,
                         ranking_colon_number=ranking_colon_number,
                         regatta_name=regatta_name,
                         sailing_class_name=class_name
                         )
    if parser.is_parsable():
        st.session_state["table_parsers_list"].append(parser)
        st.text(f"Succesfully uploaded: {uploaded_file.name}")
        st.session_state.uploaded_key = str(uuid.uuid4())
    else:
        st.warning("Something went wrong while parsing (please check row numbers, file etc...)")
    print(st.session_state["table_parsers_list"])

def restart_process():
    st.session_state.submitted_name_list = False
    st.session_state.choosing_files = True

def start_exporting():
    table_parser_list = st.session_state["table_parsers_list"]
    names_list = st.session_state["names_list"]
    tables_parser.create_file_with_tables(table_parser_list, names_list)
    st.session_state.choosing_files = False

"""
First create the form to open the actual file
"""
st.title("Export event results into csv")

if "submitted_name_list" not in st.session_state:
    st.session_state["submitted_name_list"] = False

if "names_list" not in st.session_state:
    st.session_state["names_list"] = []

if "table_parsers_list" not in st.session_state:
    st.session_state["table_parsers_list"] = []

if "choosing_files" not in st.session_state:
    st.session_state["choosing_files"] = True

if "uploaded_key" not in st.session_state:
    st.session_state["uploaded_key"] = str(uuid.uuid4())

"""
First stage of the platform: submit the names list
"""
if st.session_state.submitted_name_list is False:
    with st.form("name_upload_form"):
        uploaded_file = st.file_uploader("Choose the name list csv", type="csv")
        submitted = st.form_submit_button("Submit name list")
        if submitted and uploaded_file is not None:
            submit_name_list(uploaded_file)
elif st.session_state.choosing_files is True:
    """
    Second stage of the platform: chose the tables you want to upload
    """
    with st.form("chose_files_form"):
        uploaded_file = st.file_uploader("Choose the table to upload", type="csv", key=st.session_state.uploaded_key)
        name_colon_number = st.number_input("Please enter the colon number of the name's (starting from 1)", step=1, format="%d")
        country_colon_number = st.number_input("Please enter the colon number of the countries (starting from 1)",step=1, format="%d")
        ranking_colon_number = st.number_input("Please enter the colon number of the rankings (starting from 1)",step=1, format="%d")
        regatta_name = st.text_input("Please enter the regatta name for the event")
        class_name = st.text_input("Please enter the class name for the event")
        submitted = st.form_submit_button("Submit table")
        if submitted:
            if uploaded_file is not None and name_colon_number is not None and ranking_colon_number is not None and regatta_name is not None and class_name is not None:
                submit_table(uploaded_file,name_colon_number,country_colon_number, ranking_colon_number, regatta_name, class_name)
            else:
                st.warning("Please fill the form correctly.")

    export_csv_button = st.button("Export uploaded tables", on_click=start_exporting)
else:
    st.button("Restart process" , on_click=restart_process)

    with open("NO-TDL.csv", "r", encoding="utf-8") as file:
        data = file.read()
        st.download_button(
            label="Download NO-TDL.csv",
            data = data,
            file_name="NO-TDL.csv",
            mime="text/csv"
        )
    with open("WITH-TDL.csv", "r", encoding="utf-8") as file:
        data = file.read()
        st.download_button(
            label="Download WITH-TDL.csv",
            data=data,
            file_name="WITH-TDL.csv",
            mime="text/csv"
        )

