package jmxquery;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.Collection;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

import javax.management.MBeanInfo;
import javax.management.MBeanServerConnection;
import javax.management.MBeanAttributeInfo;
import javax.management.ObjectName;
import javax.management.ObjectInstance;
import javax.management.AttributeList;
import javax.management.Attribute;
import javax.management.openmbean.CompositeDataSupport;
import javax.management.openmbean.CompositeType;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;


/*                                                                                                                                                                            
 *  Copyright 2012 Rackspace
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 */


/**
 *
 * JMXQuery is used for local or remote request of JMX attributes
 * It requires JRE 1.5 to be used for compilation and execution.
 * Look method main for description how it can be invoked.
 *
 * This plugin was found on nagiosexchange.  It lacked a username/password/role system.
 *
 * @author unknown
 * @author Ryan Gravener (<a href="http://ryangravener.com/app/contact">rgravener</a>)
 *
 */
public class JMXQuery {

  private String url;
  private int verbatim;
  private JMXConnector connector;
  private MBeanServerConnection connection;
  private String attribute;
  private ArrayList<String> attributeKeys = new ArrayList<String>();;
  private String object;
  private String username, password;

  private static int maxMatchingObjects = 15;

  private Object checkData;

  private void connect() throws IOException
  {
    JMXServiceURL jmxUrl = new JMXServiceURL(url);

    if (username != null) {
      Map<String, String[]> m = new HashMap<String,String[]>();
      m.put(JMXConnector.CREDENTIALS,new String[] {username,password});
      connector = JMXConnectorFactory.connect(jmxUrl,m);
    }
    else {
      connector = JMXConnectorFactory.connect(jmxUrl);
    }

    connection = connector.getMBeanServerConnection();
  }


  private void disconnect() throws IOException
  {
    if (connector != null) {
      connector.close();
      connector = null;
    }
  }

  /**
   * @param args
   */
  public static void main(String[] args)
  {
    JMXQuery query = new JMXQuery();
    int status;
    try {
      query.parse(args);
      query.connect();
      query.execute();
      status = query.report(System.out);
    }
    catch(Exception ex) {
      status = query.report(ex, System.out);
    }
    finally {
      try {
        query.disconnect();
      }
      catch (IOException e) {
        status = query.report(e, System.out);
      }
    }

    System.exit(status);
  }

  private int report(Exception ex, PrintStream out)
  {
    if (ex instanceof ParseError) {
      reportException(ex, out);
      out.println("Usage: jmxquery.jar -help ");
      return 0;
    }
    else {
      reportException(ex, out);
      out.println();
      return 0;
    }
  }

  private void reportException(Exception ex, PrintStream out)
  {
    out.print("status err JMX: ");
    if (verbatim < 2) {
      out.print(rootCause(ex).getMessage());
    }
    else {
      out.print(ex.getMessage()+" connecting to "+object+" by URL "+url);
    }

    if (verbatim >= 3) {
      ex.printStackTrace(out);
    }
  }

  private static Throwable rootCause(Throwable ex)
  {
    if (ex.getCause()==null) {
      return ex;
    }

    return rootCause(ex.getCause());
  }

  private int report(PrintStream out)
  {
    int status;
    out.println("status ok JMX Check successful");

    if (checkData instanceof HashMap) {
      report(checkData, out);
    }
    else if (checkData instanceof CompositeDataSupport) {
      CompositeDataSupport cds = (CompositeDataSupport) checkData;
      report(null, cds, out);
    }
    else {
      reportrow(null, attribute, checkData, out);
    }

    return 0;
  }

  private String cleanName(String name) {
    name = name.replace(' ', '_').toLowerCase();

    return name;
  }

  private void reportrow(String prefix, String name, Object value, PrintStream out)
  {
    if (prefix != null) {
      name = String.format("%s.%s", prefix, name);
    }

    name = this.cleanName(name);

    if (value instanceof Number) {
      Number check = (Number)value;
      if (check.floatValue() != Math.floor(check.floatValue())) {
        out.println(String.format("metric %s float %f", name, check.floatValue()));
      }
      else {
        out.println(String.format("metric %s int %d", name, check.longValue()));
      }
    }

    if (value instanceof String) {
      out.println(String.format("metric %s string %s", name, value));
    }

    if (value instanceof Boolean) {
      out.println(String.format("metric %s string %s", name, value.toString()));
    }
  }

  @SuppressWarnings("unchecked")
  private void report(String prefix, CompositeDataSupport data, PrintStream out)
  {
    CompositeType type = data.getCompositeType();
    for (Iterator it = type.keySet().iterator(); it.hasNext();)
    {
      String key = (String) it.next();

      if (this.attributeKeys.size() > 0 && this.attributeKeys.indexOf(key) == -1)
      {
        continue;
      }

      if (data.containsKey(key))
      {
        reportrow(prefix, key, data.get(key), out);
      }
    }
  }

  @SuppressWarnings("unchecked")
  private void report(Object values, PrintStream out)
  {
    HashMap<String, Object[]> valuesCasted = (HashMap<String, Object[]>)values;
    String key;
    Object value;

    for (Iterator it = valuesCasted.keySet().iterator(); it.hasNext();)
    {
      key = (String)it.next();

      if (valuesCasted.containsKey(key))
      {
        value = valuesCasted.get(key);
         if (value instanceof CompositeDataSupport) {
          CompositeDataSupport cds = (CompositeDataSupport)value;
          report(key, cds, out);
        }
        else
        {
          reportrow(key, attribute, value, out);
        }
      }
    }
  }

  private void execute() throws Exception
  {
    if (object.indexOf('*') != -1)
    {
      // Object name glob match
      if (object.indexOf('*') != object.lastIndexOf('*'))
      {
        throw new Exception("You can only use a single glob in an object name");
      }

      ArrayList<String> allObjectNames = getAllObjectNames();
      HashMap<String, Object> matchingObjects = new HashMap<String, Object>();
      Object attr;

      Pattern matchPattern = Pattern.compile("^" + object.replace("*", "(.*)") + "$");
      Matcher matcher;
      String globName;

      for (String objectName : allObjectNames)
      {
        matcher = matchPattern.matcher(objectName);
        if (matcher.find())
        {
          globName = matcher.group(1);

          attr = connection.getAttribute(new ObjectName(objectName), attribute);
          matchingObjects.put(globName, attr);

          if (matchingObjects.size() > maxMatchingObjects)
          {
            throw new Exception(String.format("More then %s matching objects found", maxMatchingObjects));
          }
        }
      }

      if (matchingObjects.size() == 0)
      {
        throw new Exception("No matching objects found");
      }

      checkData = matchingObjects;
    }
    else
    {
      Object attr = connection.getAttribute(new ObjectName(object), attribute);
      checkData = attr;
    }
  }

  private ArrayList<String> getAllObjectNames() throws Exception
  {
    ArrayList<String> objectNames = new ArrayList<String>();
    Set<ObjectInstance> mBeans = connection.queryMBeans(null, null);

    for (ObjectInstance instance : mBeans)
    {
      objectNames.add(instance.getObjectName().toString());
    }

    return objectNames;
  }

  private ArrayList<String> getAllAttributeNames(String objectName) throws Exception
  {
    ArrayList<String> attributeNames = new ArrayList<String>();
    MBeanInfo mBeanInfo = connection.getMBeanInfo(new ObjectName(objectName));
    MBeanAttributeInfo[] attributes = mBeanInfo.getAttributes();

    for (MBeanAttributeInfo attribute : attributes)
    {
      attributeNames.add(attribute.getName().toString());
    }

    return attributeNames;
  }

  private void parse(String[] args) throws ParseError
  {
    try {
      for(int i=0; i<args.length; i++) {
        String option = args[i];
        if (option.equals("-help")) {
          printHelp(System.out);
          System.exit(1);
        }
        else if (option.equals("-U")) {
          this.url = args[++i];
        }
        else if (option.equals("-O")) {
          this.object = args[++i];
        }
        else if(option.equals("-A")) {
          this.attribute = args[++i];
        }
        else if (option.equals("-K")) {
          this.attributeKeys = new ArrayList(Arrays.asList(args[++i].split(",")));
        }
        else if(option.startsWith("-v")) {
          this.verbatim = option.length()-1;
        }
        else if(option.equals("-username")) {
          this.username = args[++i];
        }
        else if(option.equals("-password")) {
          this.password = args[++i];
        }
      }

      if (url == null ||
          object==null ||
          attribute==null) {
        throw new Exception("Required options not specified");
      }
    }
    catch (Exception e) {
      throw new ParseError(e);
    }
  }

  private void printHelp(PrintStream out)
  {
    InputStream is = JMXQuery.class.getClassLoader().getResourceAsStream("jmxquery/HELP");
    BufferedReader reader = new BufferedReader(new InputStreamReader(is));

    try {
      while (true) {
        String s = reader.readLine();
        if (s == null) {
          break;
        }
        out.println(s);
      }
    }
    catch (IOException e) {
      out.println(e);
    }
    finally {
      try {
        reader.close();
      }
      catch (IOException e) {
        out.println(e);
      }
    }
  }

}
