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
  name: "StackStorm",
  namespace: "st2",
  author: "James Fryman",
  description: "StackStorm integration with SmartThings",
  category: "SmartThings Labs",
  iconUrl: "https://cloud.githubusercontent.com/assets/20028/6063021/ccfde732-ad19-11e4-99f6-08e55e42cf28.jpeg",
  iconX2Url: "https://cloud.githubusercontent.com/assets/20028/6063021/ccfde732-ad19-11e4-99f6-08e55e42cf28.jpeg",
  iconX3Url: "https://cloud.githubusercontent.com/assets/20028/6063021/ccfde732-ad19-11e4-99f6-08e55e42cf28.jpeg",
  oauth: [displayName: "SmartThings / StackStorm Integration", displayLink: ""]
)

// SmartApp Preferences
preferences {
  section("Allow StackStorm to manage these devices:") {
    // https://graph.api.smartthings.com/ide/doc/capabilities

    input "devicesAcceleration", "capability.accelerationSensor", title: "Acceleration Sensor", multiple: true, required: false
    input "devicesAlarm", "capability.alarm", title: "Alarms", multiple: true, required: false
    input "devicesCO2", "capability.carbonMonoxideDetector", title: "CO2 Detectors", multiple: true, required: false
    input "devicesEnergy", "capability.energyMeter", title: "Energy Meters", multiple: true, required: false
    input "deviceImageCapture", "capability.imageCapture", title: "Image Capture Devices", multiple: true, required: false
    input "devicesLock", "capability.lock", title: "Locks", multiple: true, required: false
    input "devicesMusic", "capabilitiy.musicPlayer", title: "Music Players", multiple: true, required: false
    input "devicesPower", "capability.powerMeter", title: "Power Measurement Devices", multiple: true, required: false
    input "devicesPresence", "capability.presenceSensor", title: "Presence Sensors", multiple: true, required: false
    input "devicesHumidity", "capability.relativeHumidityMeasurement", title: "Humidity Sensors", multiple: true, required: false
    input "devicesRelay", "capability.relaySwitch", title: "Relays", multiple: true, required: false
    input "devicesSleep", "capability.sleepSensor", title: "Sleep Sensors", multiple: true, required: false
    input "devicesSmoke", "capability.smokeDetector", title: "Smoke Detectors", multiple: true, required: false
    input "devicesSpeech", "capability.speechSynthesis", title: "Speech Synthesis Devices", multiple: true, required: false
    input "devicesStep", "capability.stepSensor", title: "Step Sensors", multiple: true, required: false
    input "devicesSwitch", "capability.switch", title: "Switches", multiple: true, required: false
    input "devicesThermostat", "capability.thermostat", title: "Thermostats", multiple: true, required: false
    input "devicesTouch", "capability.touchSensor", title: "Touch Sensors", multiple: true, required: false
    input "devicesValve", "capability.valve", title: "Valves", multiple: true, required: false
    input "devicesWater", "capability.waterSensor", title: "Water Sensors", multiple: true, required: false
  }
  section("StackStorm Installation Configuration") {
    input "st2ApiUri", "text", title: "StackStorm API URI", required: false
    input "st2AuthUri", "text", title: "Stackstorm Auth URI", required: false
    input "st2Auth", "boolean", title: "Enable StackStorm Authentication", default: true, required: false
    input "st2Username", "text", title: "StackStorm Auth Username", required: false
    input "st2Password", "password", title: "StackStorm Auth Password", required: false
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

  subscribe(devicesAlarm, "alarm", eventHandler)
  subscribe(devicesBattery, "battery", eventHandler)
  subscribe(devicesButton, "button", eventHandler)
  subscribe(devicesCO2, "co2", eventHandler)
  subscribe(devicesContact, "contact", eventHandler)
  subscribe(devicesImageCapture, "image", eventHandler)
  subscribe(devicesLock, "lock", eventHandler)
  subscribe(devicesMotion, "motion", eventHandler)
  subscribe(devicesPresence, "presence", eventHandler)
  subscribe(devicesHumidity, "humidity", eventHandler)
  subscribe(devicesSleep, "sleep", eventHandler)
  subscribe(devicesSmoke, "smoke", eventHandler)
  subscribe(devicesSwitch, "switch", eventHandler)
  subscribe(devicesTemperature, "temperature", eventHandler)
  subscribe(devicesThermostat, "thermostat", eventHandler)
  subscribe(devicesValve, "valve", eventHandler)
  subscribe(devicesWater, "water", eventHandler)
}

def eventHandler(event) {
  log.debug "[eventHandler]: Received event: ${event}"

  sendEventToStackStorm(event)
}

def getAuthToken() {
  // Check to see if token is in keystore
  // if it exists, check the token expiry date
  //   if it's still valid, return that
  //   otherwise, go and get a new token
  // if not, go and get a new token
  //
  // http://docs.stackstorm.com/authentication.html#usage
  def token = "yermom"

  return token
}

/* sendEventToStackStorm
 *   Takes Event object and forwards to StackStorm WebHook Endpoint
 */
def sendEventToStackStorm(event) {
  log.debug "[sendEventToStackStorm] Sending event to StackStorm ${event}"

  def uri = "${st2ApiUri}/v1/webhooks/smartthings/event"
  def headers = [:]

  if (st2Auth) {
    headers["X-Auth-Token"] = getAuthToken()
  }

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

// API Commands
def apiListDevices() {
  log.debug "[apiLisdDevices]: Received API list devices with params ${params}"

  def type = params.type
  if (!type) { httpTypeMissing() }

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

  if (!type) { httpTypeMissing() }
  if (!command) { httpCommandMissing() }

  switch(type) {
    case ['light', 'switch']:
      def device = getDevice(device, type)
      return commandLight(device, command, value)
    case 'lock':
      def device = getDevice(device, type)
      return commandLock(device, command, value)
    case 'mode':
      return commandMode(value)
    case 'thermostat':
      def device = getDevice(device, type)
      return commandThermostat(device, command, value, mode)
    default:
      return httpCommandInvalid()
      break
  }
}

def apiDeviceInfo() {
  log.debug "[apiDeviceInfo]: Received API device info with params ${params}"

  def device = getDevice(params.id, params.type)
  if (!device) { httpDeviceNotFound() }
  else { devicePayload(device, type) }
}

// Meta
def deviceMap() {
  [
    alarm: devicesAlarm,
    battery: devicesBattery,
    button: devicesButton,
    co2: devicesCO2,
    contact: devicesContact,
    image: devicesImageCapture,
    lock: devicesLock,
    motion: devicesMotion,
    power: devicesPower,
    presence: devicesPresence,
    humidity: devicesHumidity,
    sleep: devicesSleep,
    step: devicesStep,
    switch: devicesSwitch,
    thermostat: devicesThermostat,
    valve: deviceValve,
    water: deviceWater
  ]
}

def listDevices(type) {
  return deviceMap[type]
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

  switch(type) {
    case "acceleration":
      state = device.currentState("acceleration")
      payload["acceleration"] = state.value == "active"
    case "battery":
      state = device.currentState("battery")
      payload["battery"] = state.value.toFloat()
      break
    case "contact":
      state = device.currentState("contact")
      payload["contact"] = state.value == "closed"
      break
    case "motion":
      state = device.currentState("motion")
      payload["motion"] == s.value == "active"
      break
    case "presence":
      state = device.currentState("presence")
      payload["presence"] = state.value == "present"
      break
    case "switch":
      state = device.currentState("switch")
      payload["switch"] = s.value == "on"
      break
    case "temperature":
      state = device.currentState("temperature")
      payload["temperature"] = state.value.toFloat()
      break
    case "threeAxis":
      state = device.currentState("threeAxis")
      payload["x"] = state.xyzValue.x
      payload["y"] = state.xyzValue.y
      payload["z"] = state.xyzValue.z
      break
    default:
      break
  }
  // Make sure to also add the timestamp of value
  payload["timestamp"] = state.isoDate

  return payload
}

// Commands
def commandLight(device, command, value) {
  log.debug "[commandLight]: Executing ${command} (value: ${value}) on ${device}"

  switch(command) {
    case "toggle":
      if (device.currentValue("switch") == "on") {
        device.off()
      } else {
        device.on()
      }
      break
    case "on":
      device.on()
      break
    case "off":
      device.off()
      break
    default:
      break
  }

  return [status:"ok"]
}

def commandMode(mode) {
  log.debug "[commandMode]: Changing mode to ${mode}"

  setLocationMode(mode)
  return [status:"ok"]
}

def commandLock(device, command, value) {
  log.debug "[commandLock]: executing ${command} (value: ${value} on ${device}"

  switch(command) {
    case "toggle":
      if (device.currentValue("lock") == "locked") {
        device.unlock()
      } else {
        device.lock()
      }
      break
    case "unlock":
      device.unlock()
      break
    case "lock":
      device.lock()
      break
    default:
      break
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
def httpDeviceNotFound() { httpError(404, "Device not found") }
def httpCommandInvalid() { httpError(406, "Invalid command") }
def httpTypeMissing() { httpError(406, "Invalid type") }
