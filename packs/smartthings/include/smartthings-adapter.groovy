/**
 *  SmartThings StackStorm Adapter
 *
 *  Author: StackStorm
 */

definition(
    name: "StackStorm.bridge",
    namespace: "stackstorm",
    author: "James Fryman",
    description: "Bridge to/from StackStorm.",
    category: "My Apps",
    iconUrl: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience.png",
    iconX2Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience%402x.png",
    oauth: true)

preferences {
    section("Allow StackStorm to access and control...") {
      input "motionSensors", "capability.motionSensor", title: "Motion", multiple: true, required: true
    }
}

def installed() {

}

def updated() {

}

def initialize() {

}

