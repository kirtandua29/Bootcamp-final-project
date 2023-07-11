from kubernetes import client, config

# Load kubernetes configuration
config.load_kube_config()

#create k8s API client
api_client = client.ApiClient()# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="mynotes"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "mynotes"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "mynotes"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-notes-container",
                        image="",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-notes-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "mynotes"},
        ports=[client.V1ServicePort(port=8000)]
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)


