import list_loader.list_loader as list_loader
import table_parsing.table_parser as table_parser_module
from csv import writer

def create_file_with_tables(table_parsers_list: list, names_list: list):
    # Open both files using a single with statement
    with open("WITH-TDL.csv", "w", encoding="utf-8", newline='') as with_tdl_file, \
         open("NO-TDL.csv", "w", encoding="utf-8", newline='') as no_tdl_file:

        with_tdl_file_writer = writer(with_tdl_file)
        no_tdl_file_writer = writer(no_tdl_file)

        # Write the header using the first parser's header list
        if table_parsers_list:
            header_list = table_parser_module.header_list
            with_tdl_file_writer.writerows(header_list)
            no_tdl_file_writer.writerows(header_list)

        # Loop through each parser and process the data
        for parser in table_parsers_list:
            swiss_names_dataframe = parser.parse_table()
            swiss_names_on_list, swiss_names_not_on_list = parser.filter_table_with_names_that_are_on_list(
                names_list, swiss_names_dataframe)

            # Write data to the appropriate files
            swiss_names_on_list.to_csv(with_tdl_file, index=False, header=False)
            swiss_names_not_on_list.to_csv(no_tdl_file, index=False, header=False)
