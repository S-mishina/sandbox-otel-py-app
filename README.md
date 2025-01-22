# introduction

A tool for simple verification of the connection of otel traces.

## attention (heed)

* This tool imports otel but does not have it as a package.
* When using this tool, it is assumed that the auto Integration function is used.[link](https://opentelemetry.io/docs/kubernetes/operator/automatic/)
* If auto-instrumentation is not available, the package must be installed using an init container or other means.

## sample

Here is a sample manifest using Kuberentes as an example.

```yaml:yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sandbox-app
  labels:
    app: sandbox-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sandbox-app
  template:
    metadata:
      labels:
        app: sandbox-app
        test: "1"
      annotations:
        instrumentation.opentelemetry.io/inject-python: "splunk/splunk-otel-collector"
        instrumentation.opentelemetry.io/container-names: "sandbox-app"
    spec:
      containers:
      - name: sandbox-app
        image: ghcr.io/s-mishina/test-otel-app:latest
        ports:
        - containerPort: 8080
        env:
        - name: HTTP_FLG
          value: "true"
        - name: API_URL
          value: "http://sandbox-app1:8081"
        - name: OTEL_LOG_LEVEL
          value: "DEBUG"
        command: ["python","main.py"]
---
apiVersion: v1
kind: Service
metadata:
  name: sandbox-app
  labels:
    app: sandbox-app
spec:
  selector:
    app: sandbox-app
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sandbox-app1
  labels:
    app: sandbox-app1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sandbox-app1
  template:
    metadata:
      labels:
        app: sandbox-app1
        test: "2"
      annotations:
        instrumentation.opentelemetry.io/inject-python: "splunk/splunk-otel-collector"
        instrumentation.opentelemetry.io/container-names: "sandbox-app1"
    spec:
      containers:
      - name: sandbox-app1
        image: ghcr.io/s-mishina/test-otel-app:latest
        ports:
        - containerPort: 8080
        env:
        - name: HTTP_FLG
          value: "false"
        - name: API_URL
          value: "dummy"
        - name: OTEL_LOG_LEVEL
          value: "DEBUG"
        command: ["python","main.py"]
---
apiVersion: v1
kind: Service
metadata:
  name: sandbox-app1
  labels:
    app: sandbox-app1
spec:
  selector:
    app: sandbox-app1
  ports:
    - protocol: TCP
      port: 8081
      targetPort: 8080
  type: ClusterIP
```

If you run this and send a request to sandbox-app, you can see the trace connection of sandbox-app -> sandbox-app1.

If the traces do not connect, you can check for possible problems in the collector configuration.

## At the time of use

TBU
