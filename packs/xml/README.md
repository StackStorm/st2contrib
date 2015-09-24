# XML Integration pack

Pack containing various actions for working with XML documents / data.

## Actions

### parse

Parse the provided XML string and return a JSON object (dictionary).

#### Example

Input:

```xml
<note>
<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note>
```

Output (result):

```json
{
    "note": {
        "to": "Tove",
        "from": "Jani",
        "heading": "Reminder",
        "body": "Don't forget me this weekend"
    }
}
```
