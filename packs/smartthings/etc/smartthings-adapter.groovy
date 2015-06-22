/**
 *  StackStorm Integration
 *
 *  Copyright 2015 James Fryman
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
definition(
  name: "StackStorm.bridge",
  namespace: "StackStorm",
  author: "James Fryman",
  description: "SmartThings integration with StackStorm",
  category: "SmartThings Labs",
  iconUrl: "https://cloud.githubusercontent.com/assets/20028/6063021/ccfde732-ad19-11e4-99f6-08e55e42cf28.jpeg",
  iconX2Url: "https://cloud.githubusercontent.com/assets/20028/6063021/ccfde732-ad19-11e4-99f6-08e55e42cf28.jpeg",
  iconX3Url: "https://cloud.githubusercontent.com/assets/20028/6063021/ccfde732-ad19-11e4-99f6-08e55e42cf28.jpeg",
  oauth: [displayName: "StackStorm / SmartThings Integration", displayLink: ""]
)

// SmartApp Preferences
preferences {
  section("Allow API access to manage these devices:") {
    // https://graph.api.smartthings.com/ide/doc/capabilities
    input "devicesSwitch", "capability.switch", title: "Switches", multiple: true, required: false
    input "devicesMotion", "capability.motionSensor", title: "Motion Sensors", multiple: true, required: false
    input "devicesTemperature", "capability.temperatureMeasurement", title: "Temperature", multiple: true, required: false
    input "devicesContact", "capability.contactSensor", title: "Contact Sensors", multiple: true, required: false
    input "devicesPresence", "capability.presenceSensor", title: "Presence Sensors", multiple: true, required: false
    input "devicesLock", "capability.lock", title: "Locks", multiple: true, required: false
  }
  section("StackStorm Server Configuration") {
    input "st2Server", "text", title: "FQDN to StackStorm Server", required: false
    input "st2ApiKey", "text", title: "StackStorm / SmartThings API Key", required: false
  }
}

// API Mappings from StackStorm
mappings {
  path("/:type") {
    action: [
      GET: "apiListDevices"
    ]
  }
  path("/:type/:id") {
    action: [
      GET: "apiDeviceInfo",
      PUT: "apiDeviceCommand"
    ]
  }
}

// SmartApp Management
def installed() {
  log.debug "[installed]: Installed with settings: ${settings}"
  eventSubscribe()
}

def updated() {
  log.debug "[updated]: Updated with settings: ${settings}"
  unsubscribe()
  eventSubscribe()
}

// Main Subscription Function
def eventSubscribe() {
  log.debug "[eventSubscribe]: Entered eventSubscribe()"

  subscribe(devicesSwitch, "switch", eventHandler)
  subscribe(devicesMotion, "motion", eventHandler)
  subscribe(devicesTemperature, "temperature", eventHandler)
  subscribe(devicesContact, "contact", eventHandler)
  subscribe(devicesPresence, "presence", eventHandler)
  subscribe(devicesLock, "lock", eventHandler)
}

def eventHandler(event) {
  log.debug "[eventHandler]: Received event: ${event}"

  sendEventToStackStorm(event)
}

// API Commands
def apiListDevices() {
  log.debug "[apiListDevices]: Received API list devices with params ${params}"

  def type = params.type
  listDevices(type).collect { devicePayload(it, type) }
}

// Entry point for commands sent to devices
// Core controller logic from API
def apiDeviceCommand() {
  log.debug "[apiDeviceCommand]: Received API device command with params ${params}"

  def type    = params.type
  def command = params.command
  def value   = params.value
  def mode    = params.mode
  def id      = params.id

  if (!type) { httpErrorTypeMissing() }
  if (!command) { httpErrorCommandInvalid() }

  if (type == 'light' || type == 'switch') {
    def device = getDevice(id, type)
    return commandLight(device, command)
  } else if (type == 'lock') {
    def device = getDevice(id, type)
    return commandLock(device, command)
  } else if (type == 'mode') {
    return commandMode(value)
  } else if (type == 'thermostat') {
    def device = getDevice(id, type)
    return commandThermostat(device, command, value, mode)
  } else {
    return httpErrorCommandInvalid()
  }
}

def apiDeviceInfo() {
  log.debug "[apiDeviceInfo]: Received API device info with params ${params}"
  def type = params.type
  def id = params.id
  def device = getDevice(id, type)

  if (!device) { httpErrorDeviceNotFound() }
  else { devicePayload(device, type) }
}

def sendEventToStackStorm(event) {
  log.debug "[sendEventToStackStorm] Sending event to StackStorm ${event}"

  def uri = st2Server
  def headers = [
    "X-API-Key": st2ApiKey,
    "Content-Type": "application/json",
  ]

  def body = [
    "id": event.id,
    "name": event.name,
    "value": event.value,
    "device_id": event.deviceId,
    "hub_id": event.hubId,
    "location_id": event.locationId,
    "state_change": event.isStateChange(),
    "raw_description": event.description,
    "description": event.descriptionText,
    "date": event.date,
    "iso_date": event.isoDate,
  ]

  def payload = [
    uri: uri,
    headers: headers,
    body: body
  ]

  httpPutJson(payload) { log.debug "[sendEventToStackStorm]: payload=${payload} response=${response}" }
}

// Meta
def deviceMap() {
  [
    switch: devicesSwitch,
    motion: devicesMotion,
    temperature: devicesTemperature,
    contact: devicesContact,
    presence: devicesPresence,
    lock: devicesLock
  ]
}

def listDevices(type) {
  return deviceMap()[type]
}

def getDevice(id, type) {
  def devices = listDevices(type)
  def device = devices.find { it.id == id }

  if (!device) { return httpErrorDeviceNotFound() }

  return device
}

def devicePayload(device, type) {
  if (!device) { return }

  def state = ""
  def payload = [
    id: device.id,
    label: device.label,
    type: type,
  ]

  if (type == 'switch') {
    state = device.currentState("switch")
    payload["switch"] = state.value == "on"
  } else if (type == 'motion') {
    state = device.currentState("motion")
    payload["motion"] == state.value == "active"
  } else if (type == 'temperature') {
    state = device.currentState("temperature")
    payload["temperature"] = state.value.toFloat()
  } else if (type == 'contact') {
    state = device.currentState("contact")
    payload["contact"] = state.value == "closed"
  } else if (type == 'presence') {
    state = device.currentState("presence")
    payload["presence"] = state.value == "present"
  } else if (type == 'lock') {
    state = device.currentState("lock")
    payload["lock"] = state.value == "locked"
  }

  payload["timestamp"] = state.isoDate

  return payload
}

// Commands
def commandLight(device, command) {
  log.debug "[commandLight]: Executing ${command} (${device})"

  if (command == "toggle") {
    if (device.currentValue("switch") == "on") {
      device.off()
    } else {
      device.on()
    }
  } else if (command == "on") {
    device.on()
  } else if (command == "off") {
    device.off()
  }

  return [status:"ok"]
}

def commandMode(mode) {
  log.debug "[commandMode]: Changing mode to ${mode}"

  setLocationMode(mode)
  return [status:"ok"]
}

def commandLock(device, command) {
  log.debug "[commandLock]: executing ${command} (${device})"

  if (command == "toggle") {
    if (device.currentValue("lock") == "locked") {
      device.unlock()
    } else {
      device.lock()
    }
  } else if (command == "unlock") {
    device.unlock()
  } else if (command == "lock") {
    device.lock()
  }

  return [status:"ok"]
}

def commandThermostat(device, command, value, mode) {
  log.debug "[commandThermostat]: executing ${command} (value: ${value}/${mode}) on ${device}"
  value = value.toInteger()

  // Limit to thermostat min/max
  if (value < getMinTemp()) { value = getMinTemp() }
  else if (value > getMaxTemp()) { value = getMaxTemp() }

  if (mode == "heat") {
    device.setHeatingSetpoint(value)
  } else {
    device.setCoolingSetpoint(value)
  }

  return [status:"ok"]
}

// Helper Functions
def getMinTemp() {getTemperatureScale() == "F" ? 45 : 7}
def getMaxTemp() {getTemperatureScale() == "F" ? 90 : 30}
def httpErrorDeviceNotFound() { httpError(404, "Device not found") }
def httpErrorCommandInvalid() { httpError(406, "Invalid command") }
def httpErrorTypeMissing() { httpError(406, "Invalid type") }
