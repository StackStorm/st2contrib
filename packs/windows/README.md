# Windows Integration Pack

Pack which allows integration with Windows systems.

## Actions

### WMIQueryAction

Action which runs a provided WQL query on a specified host and returns the
result.

For this action to work, WMI client for Linux (wmic) needs to be installed on
the host where this action is running. Packages for Ubuntu and other systems
are available at [https://www.orvant.com/packages/](https://www.orvant.com/packages/).

#### Parameters

* ``host`` - Host of a Window machine to run the query on.
* ``username`` - Account username (defaults to ``Administrator``).
* ``password`` - Account password.
* ``query`` - WQL query to run.

For information on how to enable and configure WMI, please see the following
page - [Enable WMI (Windows Management Instrumentation)](http://www.poweradmin.com/help/enablewmi.aspx).

#### Sample Queries

1. Retrieve process id for all the running processes

```sql
Select ProcessId from Win32_Process Where CommandLine like '%java.exe%'
```

2. Retrieve all the information for a particular process

```sql
Select * from Win32_Process Where CommandLine like '%java.exe%'
```

3. Retrieve information about Windows services

```sql
Select * From Win32_Service
```

4. Retrieve information about free memory

```sql
Select FreePhysicalMemory from Win32_OperatingSystem
```

For more examples, see [WMI Query Language by Example](http://www.codeproject.com/Articles/46390/WMI-Query-Language-by-Example).
