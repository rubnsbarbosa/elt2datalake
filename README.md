## ELT Data Pipeline with K8s CronJob, Azure Data Lake

In this first part I will show how to create an ELT. We'll extract data from a Public API called IntegraSUS regarding Covid-19 data, and load it on Azure Data Lake Storage. So, this ELT will be containerized on Azure Container Registry (ACR), and we will use Azure Kubernetes Service (AKS) to schedule our job on K8s cluster to run daily.

### build the docker image using docker build command

```
$ docker build -t el2datalakejob .
```

### run our ELT inside the container

```
$ docker run -it el2datalakejob:latest
```

### deploy our Kubernetes cron job

```
kubectl apply -f job.yml
```

### some details about the cron job

```
kubectl get cronjobs
```

### get pods

```
$ kubectl get pods
NAME                       READY   STATUS      RESTARTS   AGE
k8sjob-27513350--1-xnj8x   0/1     Completed   0          4m2s
```

### retrieve cron job logs from Kubernetes

```
$ kubectl logs k8sjob-27513350--1-xnj8x
```
