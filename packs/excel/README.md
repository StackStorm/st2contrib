# Microsoft Excel Pack 

This pack is for reading and writing to Excel Spreadsheets as a information store.

This can come in handy when you want to grab data for workflows and/or store
results from workflows in a format that is easily editable and formatable.

Edit the config.yaml file to specify the spreadsheet to use.

There are two actions:

```text
- get_variables
- set_variables
```

####get_variables

For a key (row name) in a given Excel Sheet, returns the variables in JSON format.
Variable names are the column headers. An optional list of variables names (in 
array format) will retrieve only those variables that match the array.

Examples:
```
# Gets all variables for key '123'
st2 run excel.get_varibles key='123' sheet='Accounts'

# Gets only the last_name and first_name variables for key '123'
st2 run excel.get_variables key='123' sheet='Accounts' variables='[last_name,first_name]'
```

####set_variables

For a key (row name) in a given Excel Sheet, set the variables provided. If the 
key does not exist, a new row is created.  If the variables do not exist, a new 
column will be created unless "strict" mode is enable, and then an Error will be 
raised 

When calling this action, the excel file will be locked during the process. If 
another instance has locked the file, then it will retry by default three times 
waiting a second between attempts. You can adjust these values in the config.yaml

