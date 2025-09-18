```
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "1"
  creationTimestamp: "2025-07-28T14:21:17Z"
  generation: 1
  labels:
    k8s-app: proxy-agent
    qcloud-app: proxy-agent
  managedFields:
  - apiVersion: apps/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:labels:
          .: {}
          f:k8s-app: {}
          f:qcloud-app: {}
      f:spec:
        f:progressDeadlineSeconds: {}
        f:replicas: {}
        f:revisionHistoryLimit: {}
        f:selector: {}
        f:strategy:
          f:rollingUpdate:
            .: {}
            f:maxSurge: {}
            f:maxUnavailable: {}
          f:type: {}
        f:template:
          f:metadata:
            f:labels:
              .: {}
              f:k8s-app: {}
              f:qcloud-app: {}
          f:spec:
            f:affinity:
              .: {}
              f:nodeAffinity:
                .: {}
                f:requiredDuringSchedulingIgnoredDuringExecution: {}
            f:containers:
              k:{"name":"proxy-agent"}:
                .: {}
                f:args: {}
                f:image: {}
                f:imagePullPolicy: {}
                f:name: {}
                f:resources:
                  .: {}
                  f:requests:
                    .: {}
                    f:cpu: {}
                    f:memory: {}
                f:terminationMessagePath: {}
                f:terminationMessagePolicy: {}
            f:dnsPolicy: {}
            f:restartPolicy: {}
            f:schedulerName: {}
            f:securityContext: {}
            f:terminationGracePeriodSeconds: {}
    manager: controller
    operation: Update
    time: "2025-07-28T14:21:17Z"
  - apiVersion: apps/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          .: {}
          f:deployment.kubernetes.io/revision: {}
      f:status:
        f:conditions:
          .: {}
          k:{"type":"Available"}:
            .: {}
            f:lastTransitionTime: {}
            f:lastUpdateTime: {}
            f:message: {}
            f:reason: {}
            f:status: {}
            f:type: {}
          k:{"type":"Progressing"}:
            .: {}
            f:lastTransitionTime: {}
            f:lastUpdateTime: {}
            f:message: {}
            f:reason: {}
            f:status: {}
            f:type: {}
        f:observedGeneration: {}
        f:replicas: {}
        f:unavailableReplicas: {}
        f:updatedReplicas: {}
    manager: kube-controller-manager
    operation: Update
    subresource: status
    time: "2025-07-28T14:31:18Z"
  name: proxy-agent
  namespace: prom-6r0uv7dm
  resourceVersion: "215959533"
  uid: f9658775-ac27-494a-ba03-522dd234433e
spec:
  progressDeadlineSeconds: 600
  replicas: 2
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      k8s-app: proxy-agent
      qcloud-app: proxy-agent
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        k8s-app: proxy-agent
        qcloud-app: proxy-agent
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node.kubernetes.io/instance-type
                operator: NotIn
                values:
                - external
      containers:
      - args:
        - agent
        - --id=cls-l9taan9w
        - --server-addr=10.206.0.3:8008
        - --token=JHfviCR!!WdtT5)hNXO7z1WA-8y
        image: ccr.ccs.tencentyun.com/cloudmonitor/multi-proxy:v1.0.12
        imagePullPolicy: Always
        name: proxy-agent
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  conditions:
  - lastTransitionTime: "2025-07-28T14:21:17Z"
    lastUpdateTime: "2025-07-28T14:21:17Z"
    message: Deployment does not have minimum availability.
    reason: MinimumReplicasUnavailable
    status: "False"
    type: Available
  - lastTransitionTime: "2025-07-28T14:31:18Z"
    lastUpdateTime: "2025-07-28T14:31:18Z"
    message: ReplicaSet "proxy-agent-6b6d9d866b" has timed out progressing.
    reason: ProgressDeadlineExceeded
    status: "False"
    type: Progressing
  observedGeneration: 1
  replicas: 2
  unavailableReplicas: 2
  updatedReplicas: 2
```

