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
    input "lights", "capability.switch", title: "Lights", multiple: true, required: false
    input "locks", "capability.lock", title: "Locks", multiple: true, required: false
    input "doors", "capability.doorControl", title: "Doors", multiple: true, required: false
    input "motion", "capability.motionSensor", title: "Motion Sensors", multiple: true, required: false
    input "presence", "capability.presenceSensor", title: "Presence Sensors", multiple: true, required: false
    input "thermostats", "capability.thermostat", title: "Thermostats", multiple: true, required: false
  }
  section("StackStorm Installation Configuration") {
    input "server", "text", title: "StackStorm Server"
    input "port", "text", title: "StackStorm Port"
    input "HTTPS", "boolean", title: "HTTPS"
  }
}

// SmartApp Management
def installed() {
  log.debug "Installed with settings: ${settings}"
  eventSubscribe()
}

def updated() {
  log.debug "Updated with settings: ${settings}"
  unsubscribe()
  eventSubscribe()
}

// Main Subscription Function
def eventSubscribe() {
  subscribe(lights, "light", eventHandler)
  subscribe(locks, "lock", eventHandler)
  subscribe(doors, "door", eventHandler)
  subscribe(motion, "motion", eventHandler)
  subscribe(presence, "presence", eventHandler)
  subscribe(thermostats, "thermostat", eventHandler)
}

def eventHandler(event) {
  sendEventToStackStorm(event)
}

/* sendEventToStackStorm
 *   Takes Event object and forwards to StackStorm WebHook Endpoint
 */
def sendEventToStackStorm(event) {
  // candidate for config abstraction
  def uri = ""
  def headers = [:]
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

  httpPutJson(payload) { log.debug "[sendEventToStackStorm]: response=${response}" }
}

// Helper Functions

