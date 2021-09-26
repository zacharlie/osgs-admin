import docker

client = docker.from_env()

admin_network_name = "osgs-admin_default"


def get_network_container_list(client, network_name):
    for network in client.networks.list():
        if network.name == network_name:
            network_client = network.client
            # containers = [container.name for container in network_client.containers.list()]
            return network_client.containers.list()


"""
#Client attributes
['client', 'collection', 'attrs', '__module__', '__doc__', 'name', 'image', 'labels', 'status', 'ports', 'attach', 'attach_socket', 'commit', 'diff', 'exec_run', 'export', 'get_archive', 'kill', 'logs', 'pause', 'put_archive', 'remove', 'rename', 'resize', 'restart', 'start', 'stats', 'stop', 'top', 'unpause', 'update', 'wait', 'id_attribute', '__init__', '__repr__', '__eq__', '__hash__', 'id', 'short_id', 'reload', '__dict__', '__weakref__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']

# Network attributes
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'attrs', 'client', 'collection', 'connect', 'containers', 'disconnect', 'id', 'id_attribute', 'name', 'reload', 'remove', 'short_id']
"""
