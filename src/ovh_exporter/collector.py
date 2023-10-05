"""OVH Collector."""
import ovh
from prometheus_client.core import GaugeMetricFamily

from . import ovh_client
from .logger import log


# pylint: disable=too-few-public-methods
class OvhCollector:
    """OVH collector."""
    def __init__(self, client: ovh.Client, service_id: str):
        self._client = client
        self._service_id = service_id

    def collect(self):
        """Collector implementation."""
        response = ovh_client.fetch(self._client, self._service_id)
        yield self._collect_volumes(response.volumes)
        for item in self._collect_volume_quota(response.quotas):
            yield item
        for item in self._collect_instance_quota(response.quotas):
            yield item
        for item in self._collect_network_quota(response.quotas):
            yield item
        for item in self._collect_load_balancer_quota(response.quotas):
            yield item
        for item in self._collect_keymanager_quota(response.quotas):
            yield item
        for item in self._collect_storages(response.storages):
            yield item
        for item in self._collect_instance_usage(response.usage):
            yield item
        for item in self._collect_volume_usage(response.usage):
            yield item
        for item in self._collect_storage_usage(response.usage):
            yield item

    def _collect_volumes(self, volumes):
        """Collect volume information."""
        labels = ["service_id", "volume_id", "name", "region", "type"]
        volume_metric = GaugeMetricFamily(
            "ovh_volume_size_gb",
            "Volume size in Gb",
            labels=labels
        )
        for volume in volumes:
            try:
                gauge_value = int(volume["size"])
                volume_metric.add_metric(
                    [self._service_id,
                     volume["id"], volume["name"], volume["region"], volume["type"]],
                    gauge_value
                )
            except (TypeError, ValueError):
                log.warning("Volume %s ignored as size is missing", volume["id"])
        return volume_metric

    def _collect_instance_quota(self, quotas):
        """Collect instance quota information."""
        labels = ["service_id", "region"]
        instance_metric = GaugeMetricFamily(
            "ovh_quota_instance_count",
            "Instance count",
            labels=labels
        )
        instance_max_metric = GaugeMetricFamily(
            "ovh_quota_instance_max_count",
            "Instance max count",
            labels=labels
        )
        cpu_metric = GaugeMetricFamily(
            "ovh_quota_cpu_count",
            "CPU count",
            labels=labels
        )
        cpu_max_metric = GaugeMetricFamily(
            "ovh_quota_cpu_max_count",
            "CPU max count",
            labels=labels
        )
        ram_metric = GaugeMetricFamily(
            "ovh_quota_ram_gb",
            "RAM count",
            labels=labels
        )
        ram_max_metric = GaugeMetricFamily(
            "ovh_quota_ram_max_gb",
            "RAM max count",
            labels=labels
        )
        for quota in quotas:
            if "instance" in quota:
                instance_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["instance"]["usedInstances"]
                )
                instance_max_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["instance"]["maxInstances"]
                )
                cpu_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["instance"]["usedCores"]
                )
                cpu_max_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["instance"]["maxCores"]
                )
                ram_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["instance"]["usedRAM"]
                )
                ram_max_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["instance"]["maxRam"]
                )
        yield instance_metric
        yield instance_max_metric
        yield cpu_metric
        yield cpu_max_metric
        yield ram_metric
        yield ram_max_metric

    def _collect_volume_quota(self, quotas):
        """Collect volume quota information."""
        labels = ["service_id", "region"]
        volume_gb_metric = GaugeMetricFamily(
            "ovh_quota_volume_gb",
            "Volume gigabytes",
            labels=labels
        )
        volume_max_gb_metric = GaugeMetricFamily(
            "ovh_quota_volume_max_gb",
            "Volume max gigabytes",
            labels=labels
        )
        volume_backup_gb_metric = GaugeMetricFamily(
            "ovh_quota_volume_gb",
            "Volume gigabytes",
            labels=labels
        )
        volume_backup_max_gb_metric = GaugeMetricFamily(
            "ovh_quota_volume_max_gb",
            "Volume max gigabytes",
            labels=labels
        )
        volume_count_metric = GaugeMetricFamily(
            "ovh_quota_volume_count",
            "Volume count",
            labels=labels
        )
        volume_max_count_metric = GaugeMetricFamily(
            "ovh_quota_volume_max_count",
            "Volume max count",
            labels=labels
        )
        volume_backup_count_metric = GaugeMetricFamily(
            "ovh_quota_volume_backup_count",
            "Volume count",
            labels=labels
        )
        volume_backup_max_count_metric = GaugeMetricFamily(
            "ovh_quota_volume_backup_max_count",
            "Volume max count",
            labels=labels
        )
        for quota in quotas:
            if "volume" in quota:
                volume_gb_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["volume"]["usedGigabytes"]
                )
                volume_max_gb_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["volume"]["maxGigabytes"]
                )
                volume_backup_gb_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["volume"]["usedBackupGigabytes"]
                )
                volume_backup_max_gb_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["volume"]["maxBackupGigabytes"]
                )
                volume_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["volume"]["volumeCount"]
                )
                volume_max_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["volume"]["maxVolumeCount"]
                )
                volume_backup_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["volume"]["volumeBackupCount"]
                )
                volume_backup_max_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["volume"]["maxVolumeBackupCount"]
                )
        yield volume_gb_metric
        yield volume_max_gb_metric
        yield volume_count_metric
        yield volume_max_count_metric
        yield volume_backup_gb_metric
        yield volume_backup_max_gb_metric
        yield volume_backup_count_metric
        yield volume_backup_max_count_metric

    def _collect_network_quota(self, quotas):
        """Collect network quota information."""
        labels = ["service_id", "region"]
        network_count_metric = GaugeMetricFamily(
            "ovh_quota_network_count",
            "Network count",
            labels=labels
        )
        network_max_count_metric = GaugeMetricFamily(
            "ovh_quota_network_max_count",
            "Network max count",
            labels=labels
        )
        network_subnet_count_metric = GaugeMetricFamily(
            "ovh_quota_network_subnet_count",
            "Network subnet count",
            labels=labels
        )
        network_subnet_max_count_metric = GaugeMetricFamily(
            "ovh_quota_network_subnet_max_count",
            "Network subnet max count",
            labels=labels
        )
        network_floating_ip_count_metric = GaugeMetricFamily(
            "ovh_quota_network_floating_ip_count",
            "Network floating IP count",
            labels=labels
        )
        network_floating_ip_max_count_metric = GaugeMetricFamily(
            "ovh_quota_network_floating_ip_max_count",
            "Network floating IP max count",
            labels=labels
        )
        network_gateway_count_metric = GaugeMetricFamily(
            "ovh_quota_network_gateway_count",
            "Network gateway count",
            labels=labels
        )
        network_gateway_max_count_metric = GaugeMetricFamily(
            "ovh_quota_network_gateway_max_count",
            "Network gateway max count",
            labels=labels
        )
        for quota in quotas:
            if "network" in quota:
                network_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["network"]["usedNetworks"]
                )
                network_max_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["network"]["maxNetworks"]
                )
                network_subnet_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["network"]["usedSubnets"]
                )
                network_subnet_max_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["network"]["maxSubnets"]
                )
                network_floating_ip_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["network"]["usedFloatingIPs"]
                )
                network_floating_ip_max_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["network"]["maxFloatingIPs"]
                )
                network_gateway_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["network"]["usedGateways"]
                )
                network_gateway_max_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["network"]["maxGateways"]
                )
        yield network_count_metric
        yield network_max_count_metric
        yield network_subnet_count_metric
        yield network_subnet_max_count_metric
        yield network_floating_ip_count_metric
        yield network_floating_ip_max_count_metric
        yield network_gateway_count_metric
        yield network_gateway_max_count_metric

    def _collect_load_balancer_quota(self, quotas):
        """Collect load balancer quota information."""
        labels = ["service_id", "region"]
        load_balancer_count_metric = GaugeMetricFamily(
            "ovh_quota_load_balancer_count",
            "Load balancer count",
            labels=labels
        )
        load_balancer_max_count_metric = GaugeMetricFamily(
            "ovh_quota_load_balancer_max_count",
            "Load balancer max count",
            labels=labels
        )
        for quota in quotas:
            if "loadBalancer" in quota:
                load_balancer_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["loadBalancer"]["usedLoadBalancers"]
                )
                load_balancer_max_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["loadBalancer"]["maxLoadBalancers"]
                )
        yield load_balancer_count_metric
        yield load_balancer_max_count_metric

    def _collect_keymanager_quota(self, quotas):
        """Collect key manager quota information."""
        labels = ["service_id", "region"]
        keymanager_count_metric = GaugeMetricFamily(
            "ovh_quota_keymanager_secret_count",
            "Key manager count",
            labels=labels
        )
        keymanager_max_count_metric = GaugeMetricFamily(
            "ovh_quota_keymanager_secret_max_count",
            "Key manager max count",
            labels=labels
        )
        for quota in quotas:
            if "keymanager" in quota:
                keymanager_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["keymanager"]["usedSecrets"]
                )
                keymanager_max_count_metric.add_metric(
                    [self._service_id,
                    quota["region"]],
                    quota["keymanager"]["maxSecrets"]
                )
        yield keymanager_count_metric
        yield keymanager_max_count_metric

    def _collect_storages(self, storages):
        """Collect instance usage information."""
        labels = ["service_id", "region", "storage_id", "storage_name", "storage_type"]
        storage_size_bytes_metric = GaugeMetricFamily(
            "ovh_storage_size_bytes",
            "Storage size in bytes",
            labels=labels
        )
        storage_object_count_metric = GaugeMetricFamily(
            "ovh_storage_object_count",
            "Storage object count",
            labels=labels
        )
        for storage in storages:
            storage_size_bytes_metric.add_metric(
                [self._service_id,
                    storage["region"], storage["id"], storage["name"], storage["containerType"]],
                storage["storedBytes"]
            )
            storage_object_count_metric.add_metric(
                [self._service_id,
                    storage["region"], storage["id"], storage["name"], storage["containerType"]],
                storage["storedObjects"]
            )
        yield storage_object_count_metric
        yield storage_size_bytes_metric

    def _collect_instance_usage(self, usages):
        instance_labels = ["service_id", "region", "instance_id", "type", "flavor"]
        ovh_usage_instance_hours = GaugeMetricFamily(
            "ovh_usage_instance_hours",
            "Instance usage in hours",
            labels=instance_labels)
        ovh_usage_instance_price = GaugeMetricFamily(
            "ovh_usage_instance_price",
            "Instance usage price",
            labels=instance_labels)
        if "hourlyUsage" in usages:
            for group in usages["hourlyUsage"]["instance"]:
                flavor = group["reference"]
                region = group["region"]
                for instance in group["details"]:
                    hours = instance["quantity"]["value"]
                    price = instance["totalPrice"]
                    instance_id = instance["instanceId"]
                    ovh_usage_instance_hours.add_metric(
                        [self._service_id,
                            region, instance_id, "hourly", flavor],
                        hours
                    )
                    ovh_usage_instance_price.add_metric(
                        [self._service_id,
                            region, instance_id, "hourly", flavor],
                        price
                    )
        if "monthlyUsage" in usages:
            for group in usages["monthlyUsage"]["instance"]:
                flavor = group["reference"]
                region = group["region"]
                for instance in group["details"]:
                    hours = 720
                    price = instance["totalPrice"]
                    instance_id = instance["instanceId"]
                    ovh_usage_instance_hours.add_metric(
                        [self._service_id,
                            region, instance_id, "monthly", flavor],
                        hours
                    )
                    ovh_usage_instance_price.add_metric(
                        [self._service_id,
                            region, instance_id, "monthly", flavor],
                        price
                    )
        yield ovh_usage_instance_hours
        yield ovh_usage_instance_price

    def _collect_storages(self, storages):
        """Collect instance usage information."""
        labels = ["service_id", "region", "storage_id", "storage_name", "storage_type"]
        storage_size_bytes_metric = GaugeMetricFamily(
            "ovh_storage_size_bytes",
            "Storage size in bytes",
            labels=labels
        )
        storage_object_count_metric = GaugeMetricFamily(
            "ovh_storage_object_count",
            "Storage object count",
            labels=labels
        )
        for storage in storages:
            storage_size_bytes_metric.add_metric(
                [self._service_id,
                    storage["region"], storage["id"], storage["name"], storage["containerType"]],
                storage["storedBytes"]
            )
            storage_object_count_metric.add_metric(
                [self._service_id,
                    storage["region"], storage["id"], storage["name"], storage["containerType"]],
                storage["storedObjects"]
            )
        yield storage_object_count_metric
        yield storage_size_bytes_metric

    def _collect_volume_usage(self, usages):
        """Collect volume usage information."""
        volume_labels = ["service_id", "region", "volume_id", "flavor"]
        ovh_usage_volume_gb_hours = GaugeMetricFamily(
            "ovh_usage_volume_gb_hours",
            "Volume usage in gb x hours",
            labels=volume_labels)
        ovh_usage_volume_price = GaugeMetricFamily(
            "ovh_usage_volume_price",
            "Volume usage price",
            labels=volume_labels)
        if "hourlyUsage" in usages:
            for group in usages["hourlyUsage"]["volume"]:
                flavor = group["type"]
                region = group["region"]
                for volume in group["details"]:
                    hours = volume["quantity"]["value"]
                    price = volume["totalPrice"]
                    instance_id = volume["volumeId"]
                    ovh_usage_volume_gb_hours.add_metric(
                        [self._service_id,
                            region, instance_id, flavor],
                        hours
                    )
                    ovh_usage_volume_price.add_metric(
                        [self._service_id,
                            region, instance_id, flavor],
                        price
                    )
        yield ovh_usage_volume_gb_hours
        yield ovh_usage_volume_price

    # pylint: disable=too-many-locals,too-many-statements
    def _collect_storage_usage(self, usages):
        """Collect storage usage information."""
        storage_labels = ["service_id", "region", "flavor"]
        ovh_usage_storage_gb_hours = GaugeMetricFamily(
            "ovh_usage_volume_gb_hours",
            "Storage usage in gb x hours",
            labels=storage_labels)
        ovh_usage_storage_price = GaugeMetricFamily(
            "ovh_usage_volume_price",
            "Storage usage price",
            labels=storage_labels)
        ovh_usage_storage_bandwidth_external_outgoing_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_outgoing_gb_hours",
            "Storage usage external outgoing bandwidth in gb x hours",
            labels=storage_labels)
        ovh_usage_storage_bandwidth_external_outgoing_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_outgoing_price",
            "Storage usage external outgoing bandwidth price",
            labels=storage_labels)
        ovh_usage_storage_bandwidth_internal_outgoing_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_outgoing_gb_hours",
            "Storage usage external outgoing bandwidth in gb x hours",
            labels=storage_labels)
        ovh_usage_storage_bandwidth_internal_outgoing_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_outgoing_price",
            "Storage usage external outgoing bandwidth price",
            labels=storage_labels)
        ovh_usage_storage_bandwidth_external_incoming_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_incoming_gb_hours",
            "Storage usage external incoming bandwidth in gb x hours",
            labels=storage_labels)
        ovh_usage_storage_bandwidth_external_incoming_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_incoming_price",
            "Storage usage external incoming bandwidth price",
            labels=storage_labels)
        ovh_usage_storage_bandwidth_internal_incoming_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_incoming_gb_hours",
            "Storage usage external incoming bandwidth in gb x hours",
            labels=storage_labels)
        ovh_usage_storage_bandwidth_internal_incoming_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_incoming_price",
            "Storage usage external incoming bandwidth price",
            labels=storage_labels)
        if "hourlyUsage" in usages:
            for storage in usages["hourlyUsage"]["storage"]:
                if not storage["totalPrice"]:
                    continue
                flavor = storage["type"]
                region = storage["region"]
                hours = storage["stored"]["quantity"]["value"]
                price = storage["stored"]["totalPrice"]
                if storage.get("incomingBandwidth", None):
                    external_incoming_gb = storage["incomingBandwidth"]["quantity"]["value"]
                    external_incoming_price = storage["incomingBandwidth"]["totalPrice"]
                else:
                    external_incoming_gb = 0
                    external_incoming_price = 0
                if storage.get("outgoingBandwidth", None):
                    external_outgoing_gb = storage["outgoingBandwidth"]["quantity"]["value"]
                    external_outgoing_price = storage["outgoingBandwidth"]["totalPrice"]
                else:
                    external_outgoing_gb = 0
                    external_outgoing_price = 0
                if storage.get("incomingInternalBandwidth", None):
                    internal_incoming_gb = storage["incomingInternalBandwidth"]["quantity"]["value"]
                    internal_incoming_price = storage["incomingInternalBandwidth"]["totalPrice"]
                else:
                    internal_incoming_gb = 0
                    internal_incoming_price = 0
                if storage.get("outgoingInternalBandwidth", None):
                    internal_outgoing_gb = storage["outgoingInternalBandwidth"]["quantity"]["value"]
                    internal_outgoing_price = storage["outgoingInternalBandwidth"]["totalPrice"]
                else:
                    internal_outgoing_gb = 0
                    internal_outgoing_price = 0
                ovh_usage_storage_gb_hours.add_metric(
                    [self._service_id,
                        region, flavor],
                    hours
                )
                ovh_usage_storage_price.add_metric(
                    [self._service_id,
                        region, flavor],
                    price
                )
                ovh_usage_storage_bandwidth_external_incoming_gb_hours.add_metric(
                    [self._service_id,
                        region, flavor],
                    external_incoming_gb
                )
                ovh_usage_storage_bandwidth_external_incoming_price.add_metric(
                    [self._service_id,
                        region, flavor],
                    external_incoming_price
                )
                ovh_usage_storage_bandwidth_external_outgoing_gb_hours.add_metric(
                    [self._service_id,
                        region, flavor],
                    external_outgoing_gb
                )
                ovh_usage_storage_bandwidth_external_outgoing_price.add_metric(
                    [self._service_id,
                        region, flavor],
                    external_outgoing_price
                )
                ovh_usage_storage_bandwidth_internal_incoming_gb_hours.add_metric(
                    [self._service_id,
                        region, flavor],
                    internal_incoming_gb
                )
                ovh_usage_storage_bandwidth_internal_incoming_price.add_metric(
                    [self._service_id,
                        region, flavor],
                    internal_incoming_price
                )
                ovh_usage_storage_bandwidth_internal_outgoing_gb_hours.add_metric(
                    [self._service_id,
                        region, flavor],
                    internal_outgoing_gb
                )
                ovh_usage_storage_bandwidth_internal_outgoing_price.add_metric(
                    [self._service_id,
                        region, flavor],
                    internal_outgoing_price
                )
        yield ovh_usage_storage_price
        yield ovh_usage_storage_gb_hours
        yield ovh_usage_storage_bandwidth_internal_outgoing_price
        yield ovh_usage_storage_bandwidth_internal_outgoing_gb_hours
        yield ovh_usage_storage_bandwidth_internal_incoming_price
        yield ovh_usage_storage_bandwidth_internal_incoming_gb_hours
        yield ovh_usage_storage_bandwidth_external_outgoing_price
        yield ovh_usage_storage_bandwidth_external_outgoing_gb_hours
        yield ovh_usage_storage_bandwidth_external_incoming_price
        yield ovh_usage_storage_bandwidth_external_incoming_gb_hours
