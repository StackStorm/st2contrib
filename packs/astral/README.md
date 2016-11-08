# Astral Pack 

This pack provides a sensor with four triggers for initiating workflows based
on sun position for a geo lat/long coordinates:

### Configuration file:

Copy and edit the astral.yaml.example into the /opt/stackstorm/configs directory.

### Triggers:

```text
astral.dawn
astral.sunrise
astral.sunset
astral.dusk
```

### Actions:

#### get_dawn

Returns the time in the morning when the sun is a specific number of degrees below the horizon in UTC for the current day.

#### get_sunrise

Returns the time in the morning when the top of the sun breaks the horizon in UTC for the current day

#### get_sunset

Returns the time in the evening when the sun is about to disappear below the horizon in UTC for the current day

#### get_dusk

Returns the time in the evening when the sun is a specific number of degrees below the horizon in UTC for the current day.
