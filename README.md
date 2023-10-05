* /cloud/project/{serviceName}/instance
  * flavor (id)
  * image (id -> non exploitable)
  * planCode: "s1-2.monthly.postpaid"
* /cloud/project/{serviceName}/instance/{instanceId}
  * flavor: ram, disk, vcpus, inbound, outbound
  * image.name: Debian 11 - UEFI - deprecated - 2023-03-17
* /cloud/project/{serviceName}/instance/{instanceId}/monitoring
  * lastday
  * cpu:max cpu:used mem:max mem:used net:rx net:tx
  * slow
* /cloud/project/{serviceName}/region
  * liste des régions
* /cloud/project/{serviceName}/region/{regionName}/storage
  * S3 storage
  * region mandatory
* /cloud/project/{serviceName}/snapshot
* /cloud/project/{serviceName}/storage
  * swift container
  * public/private (containerType)
  * storedObjects
  * stotedBytes
* /cloud/project/{serviceName}/usage/current
  * storage: volume, outgoingBandwidth, incomingBandwidth, stored + prices, all storages by type by region
  * volume: GiBh + price, by type by region
  * instance: total by type by region + detail
  * period + last update
* /cloud/project/{serviceName}/usage/forecast
  * same format -> forecast
* /cloud/project/{serviceName}/volume
* /cloud/project/{serviceName}/volume/snapshot
* /cloud/project/{serviceName}/sshkey