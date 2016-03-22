[![Microsoft SQL Server](https://c.s-microsoft.com/en-us/CMSImages/lrn-exam-sql-server-logo.png?version=ff7a32f0-a1ce-831c-cd76-2d50c77694ce)](http://www.microsoft.com/SQLServer)

# MSSQL Integration Pack

Pack which allows integration with Microsoft SQL Server.

## Configuration

This pack uses the `pymssql` which builds on [freetds](freetds.org). You'll need to install `freetds` on
the server where StackStorm actionrunners run. For example, in Ubuntu, you'd run:

    sudo apt-get install freetds-dev

### Connections

You will need to add at least one connection in `config.yaml`.

    production:
      server: "prod-sql"
      database: "employees"
      user: "corp-domain\\service-user"
      password: "service-password"

Each connection is named. If no `database` name is specified in the config or provided by the action,
the connection name will be used. The next example also connects to the `employees` database.

    employees:
      server: "prod-sql"
      user: "corp-domain\\service-user"
      password: "service-password"

This also allows you to create separate connections to the same database with different credentials.

    finance:
      server: "prod-sql"
      database: "employees"
      user: "corp-domain\\finance-user"
      password: "top-secret-password"

Lastly, you can include a default connection so it isn't required by the action.

    default: employees

### Query Result Cache

Some actions cache their query results on disk. This avoids the risk of destabilizing
the workflow engine by sending a large amount of data to downstream actions.

* ``output_csv.file_prefix`` - Prefix for query result file names. (default: `mssql-query.`).
* ``output_csv.file_suffix`` - Suffix for query result file names. (default: `.csv`).
* ``output_csv.directory`` - Directory in which query results are written. (default: `null` for [tempfile]
                             (https://docs.python.org/2/library/tempfile.html#tempfile.tempdir)).

## Actions

Action                      | Description                                     | Example or Use Case
----------------------------| ----------------------------------------------------------------------------------
**execute.scalar**          | Returns first column of first row from result.  | `SELECT COUNT(*) FROM employees`
**execute.row**             | Returns first row of data from result.          | `SELECT * FROM employees WHERE id=13`
**execute.insert**          | Returns newly inserted row identity.            | `INSERT INTO employees VALUES ('Cody', 'Ray')`
**execute.non_query**       | Returns number of affected rows.                | `INSERT`, `UPDATE`, `DELETE`, or DDL commands
**execute.query**           | Returns list of CSV files containing result.    | `SELECT` or `EXEC` stored procedures
**execute.query_and_email** | Emails all query results as attached files      | `SELECT` or `EXEC` stored procedures

### Query Parameters


You can use Python formatting in query strings and all values get properly quoted.
Parameter passing is flexible in accepting named or positional parameters.

```python
    query_string = "SELECT * FROM empl WHERE id=%d"
    params = 13
    
    query_string = "SELECT * FROM empl WHERE name=%s"
    params = "'John Doe'"
    
    query_string = "SELECT * FROM empl WHERE name LIKE %s"
    params = "'J%'"
    
    query_string = "SELECT * FROM empl WHERE name=%(name)s AND city=%(city)s"
    params = "{ 'name': 'John Doe', 'city': 'Nowhere' }"
    
    query_string = "SELECT * FROM cust WHERE salesrep=%s AND id IN (%s)"
    params = "('John Doe', (1, 2, 3)))"
```

With some versions of MSSQL, you may also pass multiple values for a single parameter.

```python
    query_string = "SELECT * FROM empl WHERE id IN (%s)"
    params = "((5, 6),)"
```

For more details, please see the  [pymmsql documentation](http://www.pymssql.org/en/latest/_mssql_examples.html).

### Stored Procedures

Stored procedures are executed using `mssql.execute.query`, with or without including `EXEC` keyword.

```bash
    st2 run mssql.execute.query query_string="spc_NightlyReport"

    st2 run mssql.execute.query database=employees query_string="EXEC spc_UpdatePTO"
```

Each result set returned by the stored procedure will be written to an independent CSV file.
The order of the returned CSV file paths match the order of the result sets.
