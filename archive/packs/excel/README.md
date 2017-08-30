# Microsoft Excel Pack 

This pack is for reading and writing to Excel Spreadsheets as a information store.

This can come in handy when you want to grab data for workflows and/or store
results from workflows in a format that is easily editable and formatable.

## Configuration File

Copy and edit the excel.yaml.example into the /opt/stackstorm/configs directory.

## Important Notes about the Excel File

If the excel file does not exist, a new spreadsheet will be created with
a single sheet named 'Sheet'

The key_column and variable_name_row are normally 1, but can be altered
if you have an existing spreadsheet that includes information above and to the
left of the data.

The end of keys and variables is signified by an empty row or column, so keys
and variables (columns) must be continuous.  If you plan on adding variables
and/or keys, ensure there is no additional information to the right or below the data.

## Actions

There are five actions:

```text
- get_sheets
- get_keys_for_columns
- get_keys_for_rows
- get_variables
- set_variables
```

####get_sheets

Returns an array of all the sheet names in the excel file

####get_keys_for_columns

Returns all the column keys (aka variable names) in the specified sheet in the excel file

####get_keys_for_rows

Returns all the row keys in the specified sheet in the excel file

####get_variables

For a key (row name) in a given Excel Sheet, returns the variables in JSON format.
Variable names are the column headers. An optional list of variables names (in 
array format) will retrieve only those variables that match the array.

Examples:
```
# Gets all variables for key '123'
st2 run excel.get_varibles key='123' sheet='Accounts'

# Gets only the last_name and first_name variables for key '123'
st2 run excel.get_variables key='123' sheet='Accounts' \
       variables='[last_name,first_name]'
```

####set_variables

For a key (row name) in a given Excel Sheet, set the variables provided. If the 
key does not exist, a new row is created.  If the sheet or variables do not
exist, a new sheet or column will be created unless "strict" mode is enable.

When calling this action, the excel file will be locked during the process. If 
another instance has locked the file, then it will retry by default three times 
waiting a second between attempts. You can adjust these values in the configuration.

Example:
```
# Sets values for key '123'
st2 run excel.set_variables sheet='Accounts' key='123' \
       variables='{"last_name":"Braly","first_name":"Tim"}' \
       strict=False
```
