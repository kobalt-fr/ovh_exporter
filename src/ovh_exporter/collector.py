"""OVH Collector."""
from typing import List
import ovh
from prometheus_client.core import GaugeMetricFamily

from . import ovh_client
from .logger import log


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Metrics:
    """Metrics wrapper."""
    # pylint: disable=too-many-statements
    def __init__(self):
        # Storage
        storage_usage_labels = ["service_id", "region", "flavor"]
        self.ovh_usage_storage_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_gb_hours",
            "Storage usage in gb x hours",
            labels=storage_usage_labels)
        self.ovh_usage_storage_price = GaugeMetricFamily(
            "ovh_usage_storage_price",
            "Storage usage price",
            labels=storage_usage_labels)
        self.ovh_usage_storage_bandwidth_external_outgoing_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_outgoing_gb_hours",
            "Storage usage external outgoing bandwidth in gb x hours",
            labels=storage_usage_labels)
        self.ovh_usage_storage_bandwidth_external_outgoing_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_outgoing_price",
            "Storage usage external outgoing bandwidth price",
            labels=storage_usage_labels)
        self.ovh_usage_storage_bandwidth_internal_outgoing_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_outgoing_gb_hours",
            "Storage usage external outgoing bandwidth in gb x hours",
            labels=storage_usage_labels)
        self.ovh_usage_storage_bandwidth_internal_outgoing_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_outgoing_price",
            "Storage usage external outgoing bandwidth price",
            labels=storage_usage_labels)
        self.ovh_usage_storage_bandwidth_external_incoming_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_incoming_gb_hours",
            "Storage usage external incoming bandwidth in gb x hours",
            labels=storage_usage_labels)
        self.ovh_usage_storage_bandwidth_external_incoming_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_incoming_price",
            "Storage usage external incoming bandwidth price",
            labels=storage_usage_labels)
        self.ovh_usage_storage_bandwidth_internal_incoming_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_incoming_gb_hours",
            "Storage usage external incoming bandwidth in gb x hours",
            labels=storage_usage_labels)
        self.ovh_usage_storage_bandwidth_internal_incoming_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_incoming_price",
            "Storage usage external incoming bandwidth price",
            labels=storage_usage_labels)

        # Volumes
        volume_labels = ["service_id", "volume_id", "name", "region", "type"]
        self.volume_metric = GaugeMetricFamily(
            "ovh_volume_size_gb",
            "Volume size in Gb",
            labels=volume_labels
        )

        # Volumes quota
        volume_quota_labels = ["service_id", "region"]
        self.volume_gb_metric = GaugeMetricFamily(
            "ovh_quota_volume_gb",
            "Volume gigabytes",
            labels=volume_quota_labels
        )
        self.volume_max_gb_metric = GaugeMetricFamily(
            "ovh_quota_volume_max_gb",
            "Volume max gigabytes",
            labels=volume_quota_labels
        )
        self.volume_backup_gb_metric = GaugeMetricFamily(
            "ovh_quota_volume_gb",
            "Volume gigabytes",
            labels=volume_quota_labels
        )
        self.volume_backup_max_gb_metric = GaugeMetricFamily(
            "ovh_quota_volume_max_gb",
            "Volume max gigabytes",
            labels=volume_quota_labels
        )
        self.volume_count_metric = GaugeMetricFamily(
            "ovh_quota_volume_count",
            "Volume count",
            labels=volume_quota_labels
        )
        self.volume_max_count_metric = GaugeMetricFamily(
            "ovh_quota_volume_max_count",
            "Volume max count",
            labels=volume_quota_labels
        )
        self.volume_backup_count_metric = GaugeMetricFamily(
            "ovh_quota_volume_backup_count",
            "Volume count",
            labels=volume_quota_labels
        )
        self.volume_backup_max_count_metric = GaugeMetricFamily(
            "ovh_quota_volume_backup_max_count",
            "Volume max count",
            labels=volume_quota_labels
        )

        # Instances
        instance_labels = ["service_id", "region"]
        self.instance_metric = GaugeMetricFamily(
            "ovh_quota_instance_count",
            "Instance count",
            labels=instance_labels
        )
        self.instance_max_metric = GaugeMetricFamily(
            "ovh_quota_instance_max_count",
            "Instance max count",
            labels=instance_labels
        )
        self.cpu_metric = GaugeMetricFamily(
            "ovh_quota_cpu_count",
            "CPU count",
            labels=instance_labels
        )
        self.cpu_max_metric = GaugeMetricFamily(
            "ovh_quota_cpu_max_count",
            "CPU max count",
            labels=instance_labels
        )
        self.ram_metric = GaugeMetricFamily(
            "ovh_quota_ram_gb",
            "RAM count",
            labels=instance_labels
        )
        self.ram_max_metric = GaugeMetricFamily(
            "ovh_quota_ram_max_gb",
            "RAM max count",
            labels=instance_labels
        )

        # Network quota
        network_quota_labels = ["service_id", "region"]
        self.network_count_metric = GaugeMetricFamily(
            "ovh_quota_network_count",
            "Network count",
            labels=network_quota_labels
        )
        self.network_max_count_metric = GaugeMetricFamily(
            "ovh_quota_network_max_count",
            "Network max count",
            labels=network_quota_labels
        )
        self.network_subnet_count_metric = GaugeMetricFamily(
            "ovh_quota_network_subnet_count",
            "Network subnet count",
            labels=network_quota_labels
        )
        self.network_subnet_max_count_metric = GaugeMetricFamily(
            "ovh_quota_network_subnet_max_count",
            "Network subnet max count",
            labels=network_quota_labels
        )
        self.network_floating_ip_count_metric = GaugeMetricFamily(
            "ovh_quota_network_floating_ip_count",
            "Network floating IP count",
            labels=network_quota_labels
        )
        self.network_floating_ip_max_count_metric = GaugeMetricFamily(
            "ovh_quota_network_floating_ip_max_count",
            "Network floating IP max count",
            labels=network_quota_labels
        )
        self.network_gateway_count_metric = GaugeMetricFamily(
            "ovh_quota_network_gateway_count",
            "Network gateway count",
            labels=network_quota_labels
        )
        self.network_gateway_max_count_metric = GaugeMetricFamily(
            "ovh_quota_network_gateway_max_count",
            "Network gateway max count",
            labels=network_quota_labels
        )

        # load balancer quota
        load_balancer_quota_labels = ["service_id", "region"]
        self.load_balancer_count_metric = GaugeMetricFamily(
            "ovh_quota_load_balancer_count",
            "Load balancer count",
            labels=load_balancer_quota_labels
        )
        self.load_balancer_max_count_metric = GaugeMetricFamily(
            "ovh_quota_load_balancer_max_count",
            "Load balancer max count",
            labels=load_balancer_quota_labels
        )

        # keymanager quota
        keymanager_labels = ["service_id", "region"]
        self.keymanager_count_metric = GaugeMetricFamily(
            "ovh_quota_keymanager_secret_count",
            "Key manager count",
            labels=keymanager_labels
        )
        self.keymanager_max_count_metric = GaugeMetricFamily(
            "ovh_quota_keymanager_secret_max_count",
            "Key manager max count",
            labels=keymanager_labels
        )

        # storage
        storage_labels = ["service_id", "region", "storage_id", "storage_name", "storage_type"]
        self.storage_size_bytes_metric = GaugeMetricFamily(
            "ovh_storage_size_bytes",
            "Storage size in bytes",
            labels=storage_labels
        )
        self.storage_object_count_metric = GaugeMetricFamily(
            "ovh_storage_object_count",
            "Storage object count",
            labels=storage_labels
        )

        # instance usage
        instance_usage_labels = ["service_id", "region", "instance_id", "type", "flavor"]
        self.ovh_usage_instance_hours = GaugeMetricFamily(
            "ovh_usage_instance_hours",
            "Instance usage in hours",
            labels=instance_usage_labels)
        self.ovh_usage_instance_price = GaugeMetricFamily(
            "ovh_usage_instance_price",
            "Instance usage price",
            labels=instance_usage_labels)

        # volume usage
        volume_usage_labels = ["service_id", "region", "volume_id", "flavor"]
        self.ovh_usage_volume_gb_hours = GaugeMetricFamily(
            "ovh_usage_volume_gb_hours",
            "Volume usage in gb x hours",
            labels=volume_usage_labels)
        self.ovh_usage_volume_price = GaugeMetricFamily(
            "ovh_usage_volume_price",
            "Volume usage price",
            labels=volume_usage_labels)

    # pylint: disable=too-many-statements
    def do_yield(self, metrics):
        """Perform all yields."""
        yield metrics.instance_metric
        yield metrics.instance_max_metric
        yield metrics.cpu_metric
        yield metrics.cpu_max_metric
        yield metrics.ram_metric
        yield metrics.ram_max_metric

        yield metrics.volume_gb_metric
        yield metrics.volume_max_gb_metric
        yield metrics.volume_count_metric
        yield metrics.volume_max_count_metric
        yield metrics.volume_backup_gb_metric
        yield metrics.volume_backup_max_gb_metric
        yield metrics.volume_backup_count_metric
        yield metrics.volume_backup_max_count_metric

        yield metrics.network_count_metric
        yield metrics.network_max_count_metric
        yield metrics.network_subnet_count_metric
        yield metrics.network_subnet_max_count_metric
        yield metrics.network_floating_ip_count_metric
        yield metrics.network_floating_ip_max_count_metric
        yield metrics.network_gateway_count_metric
        yield metrics.network_gateway_max_count_metric

        yield metrics.load_balancer_count_metric
        yield metrics.load_balancer_max_count_metric

        yield metrics.keymanager_count_metric
        yield metrics.keymanager_max_count_metric

        yield metrics.storage_object_count_metric
        yield metrics.storage_size_bytes_metric

        yield metrics.ovh_usage_instance_hours
        yield metrics.ovh_usage_instance_price

        yield metrics.ovh_usage_volume_gb_hours
        yield metrics.ovh_usage_volume_price

        yield metrics.ovh_usage_storage_price
        yield metrics.ovh_usage_storage_gb_hours
        yield metrics.ovh_usage_storage_bandwidth_internal_outgoing_price
        yield metrics.ovh_usage_storage_bandwidth_internal_outgoing_gb_hours
        yield metrics.ovh_usage_storage_bandwidth_internal_incoming_price
        yield metrics.ovh_usage_storage_bandwidth_internal_incoming_gb_hours
        yield metrics.ovh_usage_storage_bandwidth_external_outgoing_price
        yield metrics.ovh_usage_storage_bandwidth_external_outgoing_gb_hours
        yield metrics.ovh_usage_storage_bandwidth_external_incoming_price
        yield metrics.ovh_usage_storage_bandwidth_external_incoming_gb_hours


# pylint: disable=too-few-public-methods
class OvhCollector:
    """OVH collector."""
    def __init__(self, client: ovh.Client, services: List):
        self._client = client
        self._services = services

    def describe(self):
        """Describe metrics."""
        metrics = Metrics()
        yield from metrics.do_yield(metrics)

    def collect(self):
        """Collect metrics."""
        metrics = Metrics()
        for service in self._services:
            response = ovh_client.fetch(self._client, service["id"])
            self._collect_volumes(metrics, service, response.volumes)
            self._collect_volume_quota(metrics, service, response.quotas)
            self._collect_instance_quota(metrics, service, response.quotas)
            self._collect_network_quota(metrics, service, response.quotas)
            self._collect_load_balancer_quota(metrics, service, response.quotas)
            self._collect_keymanager_quota(metrics, service, response.quotas)
            self._collect_storages(metrics, service, response.storages)
            self._collect_instance_usage(metrics, service, response.usage)
            self._collect_volume_usage(metrics, service, response.usage)
            self._collect_storage_usage(metrics, service, response.usage)
        yield from metrics.do_yield(metrics)

    def _collect_volumes(self, metrics, service, volumes):
        """Collect volume information."""
        for volume in volumes:
            try:
                gauge_value = int(volume["size"])
                metrics.volume_metric.add_metric(
                    [service["id"],
                     volume["id"], volume["name"], volume["region"], volume["type"]],
                    gauge_value
                )
            except (TypeError, ValueError):
                log.warning("Volume %s ignored as size is missing", volume["id"])

    def _collect_instance_quota(self, metrics, service, quotas):
        """Collect instance quota information."""
        for quota in quotas:
            if not "instance" in quota:
                return
            metrics.instance_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["instance"]["usedInstances"]
            )
            metrics.instance_max_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["instance"]["maxInstances"]
            )
            metrics.cpu_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["instance"]["usedCores"]
            )
            metrics.cpu_max_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["instance"]["maxCores"]
            )
            metrics.ram_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["instance"]["usedRAM"]
            )
            metrics.ram_max_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["instance"]["maxRam"]
            )

    def _collect_volume_quota(self, metrics, service, quotas):
        """Collect volume quota information."""
        for quota in quotas:
            if not "volume" in quota:
                return
            metrics.volume_gb_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["volume"]["usedGigabytes"]
            )
            metrics.volume_max_gb_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["volume"]["maxGigabytes"]
            )
            metrics.volume_backup_gb_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["volume"]["usedBackupGigabytes"]
            )
            metrics.volume_backup_max_gb_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["volume"]["maxBackupGigabytes"]
            )
            metrics.volume_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["volume"]["volumeCount"]
            )
            metrics.volume_max_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["volume"]["maxVolumeCount"]
            )
            metrics.volume_backup_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["volume"]["volumeBackupCount"]
            )
            metrics.volume_backup_max_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["volume"]["maxVolumeBackupCount"]
            )

    def _collect_network_quota(self, metrics, service, quotas):
        """Collect network quota information."""
        for quota in quotas:
            if not "network" in quota:
                return
            metrics.network_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["network"]["usedNetworks"]
            )
            metrics.network_max_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["network"]["maxNetworks"]
            )
            metrics.network_subnet_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["network"]["usedSubnets"]
            )
            metrics.network_subnet_max_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["network"]["maxSubnets"]
            )
            metrics.network_floating_ip_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["network"]["usedFloatingIPs"]
            )
            metrics.network_floating_ip_max_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["network"]["maxFloatingIPs"]
            )
            metrics.network_gateway_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["network"]["usedGateways"]
            )
            metrics.network_gateway_max_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["network"]["maxGateways"]
            )

    def _collect_load_balancer_quota(self, metrics, service, quotas):
        """Collect load balancer quota information."""
        for quota in quotas:
            if not "loadBalancer" in quota:
                return
            metrics.load_balancer_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["loadBalancer"]["usedLoadBalancers"]
            )
            metrics.load_balancer_max_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["loadBalancer"]["maxLoadBalancers"]
            )

    def _collect_keymanager_quota(self, metrics, service, quotas):
        """Collect key manager quota information."""
        for quota in quotas:
            if not "keymanager" in quota:
                return
            metrics.keymanager_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["keymanager"]["usedSecrets"]
            )
            metrics.keymanager_max_count_metric.add_metric(
                [service["id"],
                quota["region"]],
                quota["keymanager"]["maxSecrets"]
            )

    def _collect_storages(self, metrics, service, storages):
        """Collect storage usage information."""
        for storage in storages:
            metrics.storage_size_bytes_metric.add_metric(
                [service["id"],
                    storage["region"], storage["id"], storage["name"], storage["containerType"]],
                storage["storedBytes"]
            )
            metrics.storage_object_count_metric.add_metric(
                [service["id"],
                    storage["region"], storage["id"], storage["name"], storage["containerType"]],
                storage["storedObjects"]
            )

    def _collect_instance_usage(self, metrics, service, usages):
        if "hourlyUsage" in usages:
            for group in usages["hourlyUsage"]["instance"]:
                flavor = group["reference"]
                region = group["region"]
                for instance in group["details"]:
                    hours = instance["quantity"]["value"]
                    price = instance["totalPrice"]
                    instance_id = instance["instanceId"]
                    metrics.ovh_usage_instance_hours.add_metric(
                        [service["id"],
                            region, instance_id, "hourly", flavor],
                        hours
                    )
                    metrics.ovh_usage_instance_price.add_metric(
                        [service["id"],
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
                    metrics.ovh_usage_instance_hours.add_metric(
                        [service["id"],
                            region, instance_id, "monthly", flavor],
                        hours
                    )
                    metrics.ovh_usage_instance_price.add_metric(
                        [service["id"],
                            region, instance_id, "monthly", flavor],
                        price
                    )

    def _collect_volume_usage(self, metrics, service, usages):
        """Collect volume usage information."""
        if "hourlyUsage" in usages:
            for group in usages["hourlyUsage"]["volume"]:
                flavor = group["type"]
                region = group["region"]
                for volume in group["details"]:
                    hours = volume["quantity"]["value"]
                    price = volume["totalPrice"]
                    instance_id = volume["volumeId"]
                    metrics.ovh_usage_volume_gb_hours.add_metric(
                        [service["id"],
                            region, instance_id, flavor],
                        hours
                    )
                    metrics.ovh_usage_volume_price.add_metric(
                        [service["id"],
                            region, instance_id, flavor],
                        price
                    )

    # pylint: disable=too-many-locals,too-many-statements
    def _collect_storage_usage(self, metrics, service, usages):
        """Collect storage usage information."""
        if not "hourlyUsage" in usages:
            return
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
            metrics.ovh_usage_storage_gb_hours.add_metric(
                [service["id"],
                    region, flavor],
                hours
            )
            metrics.ovh_usage_storage_price.add_metric(
                [service["id"],
                    region, flavor],
                price
            )
            metrics.ovh_usage_storage_bandwidth_external_incoming_gb_hours.add_metric(
                [service["id"],
                    region, flavor],
                external_incoming_gb
            )
            metrics.ovh_usage_storage_bandwidth_external_incoming_price.add_metric(
                [service["id"],
                    region, flavor],
                external_incoming_price
            )
            metrics.ovh_usage_storage_bandwidth_external_outgoing_gb_hours.add_metric(
                [service["id"],
                    region, flavor],
                external_outgoing_gb
            )
            metrics.ovh_usage_storage_bandwidth_external_outgoing_price.add_metric(
                [service["id"],
                    region, flavor],
                external_outgoing_price
            )
            metrics.ovh_usage_storage_bandwidth_internal_incoming_gb_hours.add_metric(
                [service["id"],
                    region, flavor],
                internal_incoming_gb
            )
            metrics.ovh_usage_storage_bandwidth_internal_incoming_price.add_metric(
                [service["id"],
                    region, flavor],
                internal_incoming_price
            )
            metrics.ovh_usage_storage_bandwidth_internal_outgoing_gb_hours.add_metric(
                [service["id"],
                    region, flavor],
                internal_outgoing_gb
            )
            metrics.ovh_usage_storage_bandwidth_internal_outgoing_price.add_metric(
                [service["id"],
                    region, flavor],
                internal_outgoing_price
            )
