# CSV Integration pack

Pack containing various actions for working with CSV documents / data.

## Actions

### parse

Parse the provided csv string and return a JSON array.

#### Example

Input:

```csv
FirstName,LastName,Title,ReportsTo.Email,Birthdate,Description
Tom,Jones,Senior Director,buyer@salesforcesample.com,1940-06-07Z,"Self-described as ""the top"" branding guru on the West Coast"
Ian,Dury,Chief Imagineer,cto@salesforcesample.com,,"World-renowned expert in fuzzy logic design. 
Influential in technology purchases."
```

Output (result):

```json
[
    [
        "FirstName",
        "LastName",
        "Title",
        "ReportsTo.Email",
        "Birthdate",
        "Description"
    ],
    [
        "Tom",
        "Jones",
        "Senior Director",
        "buyer@salesforcesample.com",
        "1940-06-07Z",
        "Self-described as \"thetop\" branding guru on the West Coast"
    ],
    [
        "Ian",
        "Dury",
        "Chief Imagineer",
        "cto@salesforcesample.com",
        "",
        "World-renowned expert in fuzzy logic design.  Influential in technology purchases."
    ]
]
```

### format

Format a list of dictionary objects into a CSV string

#### Example


Input (object):

```json
[
    {
        "FirstName": "Tom",
        "LastName": "Jones",
        "Title": "Senior Director",
        "ReportsTo.Email": "buyer@salesforcesample.com",
        "Birthdate": "1940-06-07Z",
        "Description": "Self-described as \"thetop\" branding guru on the West Coast"
    },
    ...
]
```

Output

```csv
FirstName,LastName,Title,ReportsTo.Email,Birthdate,Description
Tom,Jones,Senior Director,buyer@salesforcesample.com,1940-06-07Z,"Self-described as ""the top"" branding guru on the West Coast"
Ian,Dury,Chief Imagineer,cto@salesforcesample.com,,"World-renowned expert in fuzzy logic design. 
Influential in technology purchases."
```