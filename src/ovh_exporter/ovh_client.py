"""OVH API client."""
import ovh

from .logger import log


# pylint: disable=too-few-public-methods
class Configuration:
    """Client configuration."""
    def __init__(self, endpoint: str, application_key: str, application_secret: str,
                 consumer_key: str):
        self.endpoint = endpoint
        self.application_key = application_key
        self.application_secret = application_secret
        self.consumer_key = consumer_key

    @staticmethod
    def load(config_dict):
        """Load configuration from a configuration dict."""
        return Configuration(
            config_dict["endpoint"],
            config_dict["application_key"],
            config_dict["application_secret"],
            config_dict["consumer_key"]
        )


class OvhApiResponse:
    """API fetch result."""
    # pylint: disable=too-many-arguments
    def __init__(self, projects, instances, storages, volumes, quotas, usage):
        self.projects = projects
        self.instances = instances
        self.storages = storages
        self.volumes = volumes
        self.quotas = quotas
        self.usage = usage


def build_client(config: Configuration):
    """Build a client from a Configuration."""
    return ovh.Client(config.endpoint,
               config.application_key,
               config.application_secret,
               config.consumer_key)


def fetch(client: ovh.Client, service_id: str) -> OvhApiResponse:
    """Test OVH API calls."""
    projects = _project(client, service_id)
    instances = _instances(client, service_id)
    volumes = _volumes(client, service_id)
    storages = _storages(client, service_id)
    quotas = _quota(client, service_id)
    usage = _usage(client, service_id)
    return OvhApiResponse(
        projects=projects,
        instances=instances,
        quotas=quotas,
        storages=storages,
        volumes=volumes,
        usage=usage
    )


def _project(client: ovh.Client, service_id: str):
    """Fetch project information."""
    proj = client.get(f"/cloud/project/{service_id}")
    log.info(proj)
    return proj


def _quota(client: ovh.Client, service_id: str):
    """Fetch quota information.

    region
    instance.maxCores
    instance.maxInstances
    instance.maxRam
    instance.usedCores
    instance.usedInstances
    instance.usedRAM
    keypair.maxCount
    volume.maxGigabytes
    volume.usedGigabytes
    volume.volumeCount
    volume.maxVolumeCount
    volume.maxBackupGigabytes
    volume.usedBackupGigabytes
    volume.volumeBackupCount
    volume.maxVolumeBackupCount
    network.maxNetworks
    network.usedNetworks
    network.maxSubnets
    network.usedSubnets
    network.maxFloatingIPs
    network.usedFloatingIPs
    network.maxGateways
    network.usedGateways
    loadbalancer.maxLoadbalancers
    loadbalancer.usedLoadbalancers
    keymanager.maxSecrets
    keymanager.usedSecrets
    """
    quota = client.get(f"/cloud/project/{service_id}/quota")
    log.info(quota)
    return quota


def _storages(client: ovh.Client, service_id: str):
    """Fetch storage information.
    
    id
    name
    archive: bool
    containerType: public/private
    region
    storedBytes
    storedObjects
    """
    storages = client.get(f"/cloud/project/{service_id}/storage", includeType=True)
    log.info(storages)
    return storages


def _usage(client: ovh.Client, service_id: str):
    """Fetch usage information.
    
    hourlyUsage.instance[].reference: d2-2, ...
    hourlyUsage.instance[].region
    hourlyUsage.instance[].quantity.unit: Hour
    hourlyUsage.instance[].quantity.value
    hourlyUsage.instance[].totalPrice
    hourlyUsage.instance[].details[].instanceId
    hourlyUsage.instance[].details[].quantity.unit
    hourlyUsage.instance[].details[].quantity.value
    hourlyUsage.instance[].details[].totalPrice
    hourlyUsage.instanceOption: []
    hourlyUsage.storage[].region
    hourlyUsage.storage[].type: storage-standard, pcs
    hourlyUsage.storage[].bucketName
    hourlyUsage.storage[].totalPrice
    hourlyUsage.storage[].outgoingBandwidth
    hourlyUsage.storage[].outgoingBandwidth.quantity.unit: GiB
    hourlyUsage.storage[].outgoingBandwidth.value
    hourlyUsage.storage[].outgoingBandwidth.totalPrice
    hourlyUsage.storage[].outgoingInternalBandwidth: ...
    hourlyUsage.storage[].incomingBandwidth: ...
    hourlyUsage.storage[].incomingInternalBandwidth: ...
    hourlyUsage.storage[].stored: ... (unit GiBh)
    hourlyUsage.volume[].type: classic, high-speed-gen2
    hourlyUsage.volume[].region
    hourlyUsage.volume[].quantity.unit: GiBh
    hourlyUsage.volume[].quantity.value
    hourlyUsage.volume[].totalPrice
    hourlyUsage.volume[].details[]
    hourlyUsage.volume[].details[].volumeId
    hourlyUsage.volume[].details[].quantity.unit: GiBh
    hourlyUsage.volume[].details[].quantity.value
    hourlyUsage.volume[].details[].totalPrice
    monthlyUsage.instance[].reference: d2-2, ...
    monthlyUsage.instance[].region
    monthlyUsage.instance[].totalPrice
    monthlyUsage.instance[].details[].instanceId
    monthlyUsage.instance[].details[].activation
    monthlyUsage.instance[].details[].totalPrice
    monthlyUsage.instanceOption
    monthlyUsage.certification
    resourcesUsage
    period.from
    period.to
    lastUpdate
    """
    usage = client.get(f"/cloud/project/{service_id}/usage/current")
    log.info(usage)
    return usage


def _volumes(client: ovh.Client, service_id: str):
    """Fetch volumes information.
    [].id
    [].attachedTo: [uuid]
    [].creationDate
    [].name
    [].description
    [].size: Gb
    [].status: in-use, ?
    [].region
    [].bootable
    [].planCode: volume.classic.consumption, volume.high-speed-gen2.consumption
    [].type: classic, high-speed-gen2
    """
    volumes = client.get(f"/cloud/project/{service_id}/volume")
    log.info(volumes)
    return volumes


def _instances(client: ovh.Client, service_id: str):
    """Fetch instances information."""
    instances = client.get(f"/cloud/project/{service_id}/instance")
    log.debug(instances)
    log.info([_instance(i) for i in instances])
    return instances


def _instance(instance):
    """Map instance information."""
    # ex: s1-2.monthly.postpaid
    plan = instance["planCode"].split(".")
    flavor = plan[0] # s1.2
    billing = plan[1] # monthly / hourly
    if not billing in ("monthly", "hourly"):
        log.warning("Unexpected value for billing: %s", billing)
    return {
        "id": instance["id"],
        "name": instance["name"],
        "flavor": flavor,
        "billing": billing,
        "region": instance["region"]
    }
