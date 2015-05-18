# Integrating with Logstash

Logstash is a log processor which basically passes log events through the pipeline: *receive -> filter -> output*.
Being a comprehensive processor it's able to output your log messages to SQL, Redis, RabbitMQ, ZeroMQ and many more.
While a specific StackStorm sensor can be developed to receive messages from Logstash there's actually no need to implement a new protocol inside this sensor. User can use an existing transport which satisfies his requirements, for example RabbitMQ.

Logstash also has webhook output, which can directly post messages into StackStorm. However this method is not encouraged to be used in production. But if the volume of messages is not high or wisely controlled by Logstash filtering it might even work for you, just using webhooks.

Let's have a look at the following example which allows you to transmit http metrics directly into StackStorm using a webhook.

## Logstash configuration

Here's a sample logstash config: 
```
filter {
  metrics {
    meter => [ "http.%{response}" ]
    add_tag => "http_metrics"
    flush_interval => 30 # metric event will be generated every 30 seconds.
  }
}

output {
  if "http_metrics" in [tags] {
    http {
      content_type => json
      http_method => post
      url => "http://_stackstorm_api_node:9101/v1/webhooks/logstash_http_metrics"
      workers => 4
    }
  }
}
```

Since the volume of events transmitted to StackStorm is considerably small there's no problems to use the given webhook approach.

## StackStorm webhook configuration

Just create a StackStorm webhook like below and place it in your pack. Every time when Logstash sends an http metric event webhook will trigger an action.

```
---
    name: "examples.logstash_http_metrics"
    description: "Logstash http metrics webhook."
    enabled: true

    trigger:
        type: "core.st2.webhook"
        parameters:
            url: "logstash_http_metrics"

    criteria:
        trigger.body.name:
            pattern: "st2"
            type: "equals"

    action:
        ref: "core.local"
        parameters:
            cmd: "echo \"{{trigger.body}}\" >> /tmp/st2.webhook_sample.out"
```

### Issues with dots  in trigger instance payload

Logstash generates metrics containing dots like *hits.rate_1m*. There's a known [bug](https://github.com/StackStorm/st2/pull/1465) in StackStorm which is known to be resolved, but not yet merged at the moment of writing of this example. As soon as it merged into a newer release the suggested example should work fine.
