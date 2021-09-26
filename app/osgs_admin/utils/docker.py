import docker

client = docker.from_env()

admin_network_name = "osgs-admin_default"

stack_network_name = "osgs_default"


def get_network_container_list(client, network_name):
    for network in client.networks.list():
        if network.name == network_name:
            network_client = network.client
            # containers = [container.name for container in network_client.containers.list()]
            return network_client.containers.list()
