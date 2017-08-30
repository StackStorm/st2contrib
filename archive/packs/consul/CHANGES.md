# Change Log

## 0.3.0

 - Added consul.list action to get a list of Keys from consul under a given <root> key
 - Added Recursive lookup for consul.get action.
 - Both list and get use the same python runner with additional `recurse`, and `keys`
   parameters with appropriate defaults.

## 0.2.0

 - Added ability to register and deregister a remote service with consul
 - Added ports parameter to consul.query_service. When true, include ports in node list <ip:port>.

## 0.1.0

 - Initial Release
