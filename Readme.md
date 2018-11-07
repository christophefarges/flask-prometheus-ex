# Collecting a python application telemetry with prometheus, prometheus-operator on openshift

## Summary

This repository contains the source files for a demo application showcasing the usage of the [https://github.com/prometheus/client_python
](prometheus_client) library to export python and applicative metrics data for prometheus to collect.



## Prerequesites

1. [git](https://git-scm.com/downloads)
2. [oc](https://github.com/openshift/origin/releases)
3. [odo](https://github.com/redhat-developer/odo/releases)
4. Access to an openshift instance with a prometheus deployed through the prometheus-operator
5. An empty python virtualenv with python 3.6.3 ([pyenv](https://github.com/pyenv/pyenv) && [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) )

6. A basic knowledge of prometheus, prometheus-operator and openshift is necessary to follow this documentation

## Methodology

1. Log into Openshift on an empty project

2. Initialize the python virtualenv

```sh
pip install -r requirements.txt
```

2. Create the application and the python component with odo

```sh
odo app create python-test

odo create python
```

3. Push the application and create the url

```sh

odo push

odo url create

```

Then check the application is running by opening the given url

4. Update the service in the application project

The service should be called "python-python-test"

Add a label as shown in the openshift/service.yml file

5. Create a new ServiceMonitor

Create a new ressource of type ServiceMonitor in the project containing the prometheus installation as shown in openshift/servicemonitor.yml

Be careful to replace the "<python-namespace>" by the namespace where you created the python application.

6. Collect the telemetry

You can query the metrics "python_*" or "ws_srv_*" metrics in the prometheus interface

The metric "ws_srv_func_now_count" will show you how many times the index of the application has been requested.

* Troubleshooting

If the metrics are not displayed in prometheus, you can check the following

- the prometheus service account needs a special permission to scrape data from other namespaces, you can use the following oc adm command:

oc adm policy add-scc-to-user privileged system:serviceaccount:<namespace>:prometheus-k8s

Don't forget to replace the <namespace> part by the actual namespace holding the prometheus application

- Check the prometheus configuration and ensure that there is a job named "<namespace>/python-scrapper/0" in the "scrape_configs" section of the prometheus configuration.

The configuration update after creating the ServiceMonitor ressource can take several minutes depending on the performance of your openshift cluster