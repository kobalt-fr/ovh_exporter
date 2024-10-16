"""OVH Collector."""

from __future__ import annotations

import typing

from prometheus_client.core import GaugeMetricFamily

from ovh_exporter import ovh_client
from ovh_exporter.logger import log

if typing.TYPE_CHECKING:
    import ovh

    from ovh_exporter.config import Service


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Metrics:
    """Metrics wrapper."""

    # pylint: disable=too-many-statements
    def __init__(self, labelnames):
        # Storage
        storage_usage_labels = ["service_id", "region", "flavor", "storage_name"]
        self.ovh_usage_storage_gb_hours = GaugeMetricFamily(
            "ovh_usage_storage_gb_hours",
            "Storage usage in gb x hours",
            labels=labelnames + storage_usage_labels,
        )
        self.ovh_usage_storage_price = GaugeMetricFamily(
            "ovh_usage_storage_price",
            "Storage usage price",
            labels=labelnames + storage_usage_labels,
        )
        self.ovh_usage_storage_bandwidth_external_outgoing_gb = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_outgoing_gb",
            "Storage usage external outgoing bandwidth in gb",
            labels=labelnames + storage_usage_labels,
        )
        self.ovh_usage_storage_bandwidth_external_outgoing_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_outgoing_price",
            "Storage usage external outgoing bandwidth price",
            labels=labelnames + storage_usage_labels,
        )
        self.ovh_usage_storage_bandwidth_internal_outgoing_gb = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_outgoing_gb",
            "Storage usage external outgoing bandwidth in gb",
            labels=labelnames + storage_usage_labels,
        )
        self.ovh_usage_storage_bandwidth_internal_outgoing_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_outgoing_price",
            "Storage usage external outgoing bandwidth price",
            labels=labelnames + storage_usage_labels,
        )
        self.ovh_usage_storage_bandwidth_external_incoming_gb = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_incoming_gb",
            "Storage usage external incoming bandwidth in gb",
            labels=labelnames + storage_usage_labels,
        )
        self.ovh_usage_storage_bandwidth_external_incoming_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_external_incoming_price",
            "Storage usage external incoming bandwidth price",
            labels=labelnames + storage_usage_labels,
        )
        self.ovh_usage_storage_bandwidth_internal_incoming_gb = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_incoming_gb",
            "Storage usage external incoming bandwidth in gb",
            labels=labelnames + storage_usage_labels,
        )
        self.ovh_usage_storage_bandwidth_internal_incoming_price = GaugeMetricFamily(
            "ovh_usage_storage_bandwidth_internal_incoming_price",
            "Storage usage external incoming bandwidth price",
            labels=labelnames + storage_usage_labels,
        )

        # Volumes
        volume_labels = ["service_id", "volume_id", "name", "region", "type"]
        self.ovh_volume_size_gb = GaugeMetricFamily(
            "ovh_volume_size_gb", "Volume size in Gb", labels=labelnames + volume_labels
        )

        # Volumes quota
        volume_quota_labels = ["service_id", "region"]
        self.ovh_quota_volume_gb = GaugeMetricFamily(
            "ovh_quota_volume_gb", "Volume gigabytes", labels=labelnames + volume_quota_labels
        )
        self.ovh_quota_volume_max_gb = GaugeMetricFamily(
            "ovh_quota_volume_max_gb",
            "Volume max gigabytes",
            labels=labelnames + volume_quota_labels,
        )
        self.ovh_quota_volume_backup_gb = GaugeMetricFamily(
            "ovh_quota_volume_backup_gb",
            "Volume backup gigabytes",
            labels=labelnames + volume_quota_labels,
        )
        self.ovh_quota_volume_backup_max_gb = GaugeMetricFamily(
            "ovh_quota_volume_backup_max_gb",
            "Volume backup max gigabytes",
            labels=labelnames + volume_quota_labels,
        )
        self.ovh_quota_volume_count = GaugeMetricFamily(
            "ovh_quota_volume_count", "Volume count", labels=labelnames + volume_quota_labels
        )
        self.ovh_quota_volume_max_count = GaugeMetricFamily(
            "ovh_quota_volume_max_count", "Volume max count", labels=labelnames + volume_quota_labels
        )
        self.ovh_quota_volume_backup_count = GaugeMetricFamily(
            "ovh_quota_volume_backup_count", "Volume count", labels=labelnames + volume_quota_labels
        )
        self.ovh_quota_volume_backup_max_count = GaugeMetricFamily(
            "ovh_quota_volume_backup_max_count",
            "Volume max count",
            labels=labelnames + volume_quota_labels,
        )

        # Instances
        instance_labels = ["service_id", "region"]
        self.ovh_quota_instance_count = GaugeMetricFamily(
            "ovh_quota_instance_count", "Instance count", labels=labelnames + instance_labels
        )
        self.ovh_quota_instance_max_count = GaugeMetricFamily(
            "ovh_quota_instance_max_count", "Instance max count", labels=labelnames + instance_labels
        )
        self.ovh_quota_cpu_count = GaugeMetricFamily(
            "ovh_quota_cpu_count", "CPU count", labels=labelnames + instance_labels
        )
        self.ovh_quota_cpu_max_count = GaugeMetricFamily(
            "ovh_quota_cpu_max_count", "CPU max count", labels=labelnames + instance_labels
        )
        self.ovh_quota_ram_gb = GaugeMetricFamily("ovh_quota_ram_gb", "RAM count", labels=labelnames + instance_labels)
        self.ovh_quota_ram_max_gb = GaugeMetricFamily(
            "ovh_quota_ram_max_gb", "RAM max count", labels=labelnames + instance_labels
        )

        # Network quota
        network_quota_labels = ["service_id", "region"]
        self.ovh_quota_network_count = GaugeMetricFamily(
            "ovh_quota_network_count", "Network count", labels=labelnames + network_quota_labels
        )
        self.ovh_quota_network_max_count = GaugeMetricFamily(
            "ovh_quota_network_max_count",
            "Network max count",
            labels=labelnames + network_quota_labels,
        )
        self.ovh_quota_network_subnet_count = GaugeMetricFamily(
            "ovh_quota_network_subnet_count",
            "Network subnet count",
            labels=labelnames + network_quota_labels,
        )
        self.ovh_quota_network_subnet_max_count = GaugeMetricFamily(
            "ovh_quota_network_subnet_max_count",
            "Network subnet max count",
            labels=labelnames + network_quota_labels,
        )
        self.ovh_quota_network_floating_ip_count = GaugeMetricFamily(
            "ovh_quota_network_floating_ip_count",
            "Network floating IP count",
            labels=labelnames + network_quota_labels,
        )
        self.ovh_quota_network_floating_ip_max_count = GaugeMetricFamily(
            "ovh_quota_network_floating_ip_max_count",
            "Network floating IP max count",
            labels=labelnames + network_quota_labels,
        )
        self.ovh_quota_network_gateway_count = GaugeMetricFamily(
            "ovh_quota_network_gateway_count",
            "Network gateway count",
            labels=labelnames + network_quota_labels,
        )
        self.ovh_quota_network_gateway_max_count = GaugeMetricFamily(
            "ovh_quota_network_gateway_max_count",
            "Network gateway max count",
            labels=labelnames + network_quota_labels,
        )

        # load balancer quota
        load_balancer_quota_labels = ["service_id", "region"]
        self.ovh_quota_load_balancer_count = GaugeMetricFamily(
            "ovh_quota_load_balancer_count",
            "Load balancer count",
            labels=labelnames + load_balancer_quota_labels,
        )
        self.ovh_quota_load_balancer_max_count = GaugeMetricFamily(
            "ovh_quota_load_balancer_max_count",
            "Load balancer max count",
            labels=labelnames + load_balancer_quota_labels,
        )

        # keymanager quota
        keymanager_labels = ["service_id", "region"]
        self.ovh_quota_keymanager_secret_count = GaugeMetricFamily(
            "ovh_quota_keymanager_secret_count",
            "Key manager count",
            labels=labelnames + keymanager_labels,
        )
        self.ovh_quota_keymanager_secret_max_count = GaugeMetricFamily(
            "ovh_quota_keymanager_secret_max_count",
            "Key manager max count",
            labels=labelnames + keymanager_labels,
        )

        # storage
        storage_labels = [
            "service_id",
            "region",
            "storage_id",
            "storage_name",
            "storage_type",
        ]
        self.ovh_storage_size_bytes = GaugeMetricFamily(
            "ovh_storage_size_bytes", "Storage size in bytes", labels=labelnames + storage_labels
        )
        self.ovh_storage_object_count = GaugeMetricFamily(
            "ovh_storage_object_count", "Storage object count", labels=labelnames + storage_labels
        )

        # instance usage
        instance_usage_labels = [
            "service_id",
            "region",
            "instance_id",
            "type",
            "flavor",
        ]
        self.ovh_usage_instance_hours = GaugeMetricFamily(
            "ovh_usage_instance_hours",
            "Instance usage in hours",
            labels=labelnames + instance_usage_labels,
        )
        self.ovh_usage_instance_price = GaugeMetricFamily(
            "ovh_usage_instance_price",
            "Instance usage price",
            labels=labelnames + instance_usage_labels,
        )

        # volume usage
        volume_usage_labels = ["service_id", "region", "volume_id", "flavor"]
        self.ovh_usage_volume_gb_hours = GaugeMetricFamily(
            "ovh_usage_volume_gb_hours",
            "Volume usage in gb x hours",
            labels=labelnames + volume_usage_labels,
        )
        self.ovh_usage_volume_price = GaugeMetricFamily(
            "ovh_usage_volume_price", "Volume usage price", labels=labelnames + volume_usage_labels
        )

    # pylint: disable=too-many-statements
    def do_yield(self):
        """Perform all yields."""
        yield self.ovh_quota_instance_count
        yield self.ovh_quota_instance_max_count
        yield self.ovh_quota_cpu_count
        yield self.ovh_quota_cpu_max_count
        yield self.ovh_quota_ram_gb
        yield self.ovh_quota_ram_max_gb

        yield self.ovh_quota_volume_gb
        yield self.ovh_quota_volume_max_gb
        yield self.ovh_quota_volume_count
        yield self.ovh_quota_volume_max_count
        yield self.ovh_quota_volume_backup_gb
        yield self.ovh_quota_volume_backup_max_gb
        yield self.ovh_quota_volume_backup_count
        yield self.ovh_quota_volume_backup_max_count

        yield self.ovh_quota_network_count
        yield self.ovh_quota_network_max_count
        yield self.ovh_quota_network_subnet_count
        yield self.ovh_quota_network_subnet_max_count
        yield self.ovh_quota_network_floating_ip_count
        yield self.ovh_quota_network_floating_ip_max_count
        yield self.ovh_quota_network_gateway_count
        yield self.ovh_quota_network_gateway_max_count

        yield self.ovh_quota_load_balancer_count
        yield self.ovh_quota_load_balancer_max_count

        yield self.ovh_quota_keymanager_secret_count
        yield self.ovh_quota_keymanager_secret_max_count

        yield self.ovh_storage_object_count
        yield self.ovh_storage_size_bytes

        yield self.ovh_usage_instance_hours
        yield self.ovh_usage_instance_price

        yield self.ovh_usage_volume_gb_hours
        yield self.ovh_usage_volume_price

        yield self.ovh_usage_storage_price
        yield self.ovh_usage_storage_gb_hours
        yield self.ovh_usage_storage_bandwidth_internal_outgoing_price
        yield self.ovh_usage_storage_bandwidth_internal_outgoing_gb
        yield self.ovh_usage_storage_bandwidth_internal_incoming_price
        yield self.ovh_usage_storage_bandwidth_internal_incoming_gb
        yield self.ovh_usage_storage_bandwidth_external_outgoing_price
        yield self.ovh_usage_storage_bandwidth_external_outgoing_gb
        yield self.ovh_usage_storage_bandwidth_external_incoming_price
        yield self.ovh_usage_storage_bandwidth_external_incoming_gb


# pylint: disable=too-few-public-methods
class OvhCollector:
    """OVH collector."""

    def __init__(self, client: ovh.Client, services: list[Service]):
        self._client: ovh.Client = client
        self._services: list[Service] = services
        self.labels: typing.Mapping[str, typing.Sequence[str]] = {}
        self.labelnames = []
        if services:
            labelset = set(services[0].labels.keys())
            self.labelnames = list(services[0].labels.keys())
            for service in services:
                service_labelset = set(service.labels.keys())
                if labelset != service_labelset:
                    raise RuntimeError("Service label names must be the same for all services")  # noqa: TRY003,EM101
                self.labels[service.id] = [service.labels[name] for name in self.labelnames]

    def _labels(self, service, labels):
        value = []
        value.extend(self.labels[service.id])
        value.extend(labels)
        return value

    def describe(self):
        """Describe metrics."""
        metrics = Metrics(self.labelnames)
        yield from metrics.do_yield()

    def collect(self):
        """Collect metrics."""
        metrics = Metrics(self.labelnames)
        for service in self._services:
            response = ovh_client.fetch(self._client, service.id)
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
        yield from metrics.do_yield()

    def _collect_volumes(self, metrics: Metrics, service, volumes):
        """Collect volume information."""
        for volume in volumes:
            try:
                gauge_value = int(volume["size"])
                metrics.ovh_volume_size_gb.add_metric(
                    self._labels(
                        service,
                        [
                            service.id,
                            volume["id"],
                            volume["name"],
                            volume["region"],
                            volume["type"],
                        ],
                    ),
                    gauge_value,
                )
            except (TypeError, ValueError):
                log.warning("Volume %s ignored as size is missing", volume["id"])

    def _collect_instance_quota(self, metrics: Metrics, service, quotas):
        """Collect instance quota information."""
        for quota in quotas:
            if "instance" not in quota:
                return
            metrics.ovh_quota_instance_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["instance"]["usedInstances"]
            )
            metrics.ovh_quota_instance_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["instance"]["maxInstances"]
            )
            metrics.ovh_quota_cpu_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["instance"]["usedCores"]
            )
            metrics.ovh_quota_cpu_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["instance"]["maxCores"]
            )
            metrics.ovh_quota_ram_gb.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["instance"]["usedRAM"]
            )
            metrics.ovh_quota_ram_max_gb.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["instance"]["maxRam"]
            )

    def _collect_volume_quota(self, metrics: Metrics, service, quotas):
        """Collect volume quota information."""
        for quota in quotas:
            if "volume" not in quota:
                return
            metrics.ovh_quota_volume_gb.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["volume"]["usedGigabytes"]
            )
            metrics.ovh_quota_volume_max_gb.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["volume"]["maxGigabytes"]
            )
            metrics.ovh_quota_volume_backup_gb.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["volume"]["usedBackupGigabytes"]
            )
            metrics.ovh_quota_volume_backup_max_gb.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["volume"]["maxBackupGigabytes"]
            )
            metrics.ovh_quota_volume_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["volume"]["volumeCount"]
            )
            metrics.ovh_quota_volume_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["volume"]["maxVolumeCount"]
            )
            metrics.ovh_quota_volume_backup_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["volume"]["volumeBackupCount"]
            )
            metrics.ovh_quota_volume_backup_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]),
                quota["volume"]["maxVolumeBackupCount"],
            )

    def _collect_network_quota(self, metrics: Metrics, service, quotas):
        """Collect network quota information."""
        for quota in quotas:
            if "network" not in quota:
                return
            metrics.ovh_quota_network_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["network"]["usedNetworks"]
            )
            metrics.ovh_quota_network_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["network"]["maxNetworks"]
            )
            metrics.ovh_quota_network_subnet_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["network"]["usedSubnets"]
            )
            metrics.ovh_quota_network_subnet_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["network"]["maxSubnets"]
            )
            metrics.ovh_quota_network_floating_ip_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["network"]["usedFloatingIPs"]
            )
            metrics.ovh_quota_network_floating_ip_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["network"]["maxFloatingIPs"]
            )
            metrics.ovh_quota_network_gateway_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["network"]["usedGateways"]
            )
            metrics.ovh_quota_network_gateway_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["network"]["maxGateways"]
            )

    def _collect_load_balancer_quota(self, metrics: Metrics, service, quotas):
        """Collect load balancer quota information."""
        for quota in quotas:
            if "loadBalancer" not in quota:
                return
            metrics.ovh_quota_load_balancer_count.add_metric(
                self._labels(service, [service.id, quota["region"]]),
                quota["loadBalancer"]["usedLoadBalancers"],
            )
            metrics.ovh_quota_load_balancer_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]),
                quota["loadBalancer"]["maxLoadBalancers"],
            )

    def _collect_keymanager_quota(self, metrics: Metrics, service, quotas):
        """Collect key manager quota information."""
        for quota in quotas:
            if "keymanager" not in quota:
                return
            metrics.ovh_quota_keymanager_secret_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["keymanager"]["usedSecrets"]
            )
            metrics.ovh_quota_keymanager_secret_max_count.add_metric(
                self._labels(service, [service.id, quota["region"]]), quota["keymanager"]["maxSecrets"]
            )

    def _collect_storages(self, metrics: Metrics, service, storages):
        """Collect storage usage information."""
        for storage in storages:
            metrics.ovh_storage_size_bytes.add_metric(
                self._labels(
                    service,
                    [
                        service.id,
                        storage["region"],
                        storage["id"],
                        storage["name"],
                        storage["containerType"],
                    ],
                ),
                storage["storedBytes"],
            )
            metrics.ovh_storage_object_count.add_metric(
                self._labels(
                    service,
                    [
                        service.id,
                        storage["region"],
                        storage["id"],
                        storage["name"],
                        storage["containerType"],
                    ],
                ),
                storage["storedObjects"],
            )

    def _collect_instance_usage(self, metrics: Metrics, service, usages):
        if "hourlyUsage" in usages:
            for group in usages["hourlyUsage"]["instance"]:
                flavor = group["reference"]
                region = group["region"]
                for instance in group["details"]:
                    hours = instance["quantity"]["value"]
                    price = instance["totalPrice"]
                    instance_id = instance["instanceId"]
                    metrics.ovh_usage_instance_hours.add_metric(
                        self._labels(service, [service.id, region, instance_id, "hourly", flavor]), hours
                    )
                    metrics.ovh_usage_instance_price.add_metric(
                        self._labels(service, [service.id, region, instance_id, "hourly", flavor]), price
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
                        self._labels(service, [service.id, region, instance_id, "monthly", flavor]), hours
                    )
                    metrics.ovh_usage_instance_price.add_metric(
                        self._labels(service, [service.id, region, instance_id, "monthly", flavor]), price
                    )

    def _collect_volume_usage(self, metrics: Metrics, service, usages):
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
                        self._labels(service, [service.id, region, instance_id, flavor]), hours
                    )
                    metrics.ovh_usage_volume_price.add_metric(
                        self._labels(service, [service.id, region, instance_id, flavor]), price
                    )

    # pylint: disable=too-many-locals,too-many-statements
    def _collect_storage_usage(self, metrics: Metrics, service, usages):
        """Collect storage usage information."""
        if "hourlyUsage" not in usages:
            return
        for storage in usages["hourlyUsage"]["storage"]:
            if not storage["totalPrice"]:
                continue
            flavor = storage["type"]
            region = storage["region"]
            hours = storage["stored"]["quantity"]["value"]
            price = storage["stored"]["totalPrice"]
            storage_name = "__all__" if flavor == "pcs" else storage["bucketName"]
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
                self._labels(service, [service.id, region, flavor, storage_name]), hours
            )
            metrics.ovh_usage_storage_price.add_metric(
                self._labels(service, [service.id, region, flavor, storage_name]), price
            )
            metrics.ovh_usage_storage_bandwidth_external_incoming_gb.add_metric(
                self._labels(service, [service.id, region, flavor, storage_name]), external_incoming_gb
            )
            metrics.ovh_usage_storage_bandwidth_external_incoming_price.add_metric(
                self._labels(service, [service.id, region, flavor, storage_name]), external_incoming_price
            )
            metrics.ovh_usage_storage_bandwidth_external_outgoing_gb.add_metric(
                self._labels(service, [service.id, region, flavor, storage_name]), external_outgoing_gb
            )
            metrics.ovh_usage_storage_bandwidth_external_outgoing_price.add_metric(
                self._labels(service, [service.id, region, flavor, storage_name]), external_outgoing_price
            )
            metrics.ovh_usage_storage_bandwidth_internal_incoming_gb.add_metric(
                self._labels(service, [service.id, region, flavor, storage_name]), internal_incoming_gb
            )
            metrics.ovh_usage_storage_bandwidth_internal_incoming_price.add_metric(
                self._labels(service, [service.id, region, flavor, storage_name]), internal_incoming_price
            )
            metrics.ovh_usage_storage_bandwidth_internal_outgoing_gb.add_metric(
                self._labels(service, [service.id, region, flavor, storage_name]), internal_outgoing_gb
            )
            metrics.ovh_usage_storage_bandwidth_internal_outgoing_price.add_metric(
                self._labels(service, [service.id, region, flavor, storage_name]), internal_outgoing_price
            )
