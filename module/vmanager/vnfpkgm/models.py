from django.db import models

# Create your models here.


# # filter start
# class VnfdId(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_vnfd_id'
#     vnfd_id = models.CharField(max_length=100)
#     pkgm_notifications_filter_id = models.IntegerField(null=False)
#
#
# class VnfPkgId(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_vnf_pkg_id'
#     vnf_pkg_id =models.CharField(max_length=100)
#     pkgm_notifications_filter_id = models.IntegerField(null=False)
#
#
# class OperationalState(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_operational_state'
#     operational_state = models.CharField(max_length=10)
#     pkgm_notifications_filter_id = models.IntegerField(null=False)
#
#
# class UsageState(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_usage_state'
#     usage_state = models.CharField(max_length=10)
#     pkgm_notifications_filter_id = models.IntegerField(null=False)
#
#
# class VnfdVersion(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_vnfd_version'
#     vnfd_versions = models.CharField(max_length=100)
#     versions_id = models.IntegerField(null=False)
#
#
# class Versions(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_versions'
#     vnf_software_version = models.CharField(max_length=100)
#     vnf_products_id = models.IntegerField(null=False)
#
#
# class VnfProducts(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_vnf_products'
#     vnf_product_name = models.CharField(max_length=100)
#     vnf_products_from_providers_id = models.IntegerField(null=False)
#
#
# class VnfProductsFromProviders(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_vnf_products_from_providers'
#     vnf_provider = models.CharField(max_length=100)
#     pkgm_notifications_filter_id = models.IntegerField(null=False)
#
#
# class NotificationTypes(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_notification_types'
#     notification_types = models.CharField(max_length=100)
#     pkgm_notifications_filter_id = models.IntegerField(null=False)
#
#
# class PkgmNotificationsFilter(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_pkgm_notifications_filter'
#     pkgm_subscription_request_id = models.IntegerField(null=False)
# # filter end
#
#
# # authentication start
# # not implement
# # authentication end
#
#
# # request
# class PkgmSubscriptionRequest(models.Model):
#     class Meta:
#         db_table = 'vnfpkgm_pkgm_subscription_request'
#     callback_url = models.CharField(max_length=300)

class PkgmSubscriptionRequest(models.Model):
    class Meta:
        db_table = 'vnfpkgm_pkgm_subscription_request'
    filter = models.TextField(max_length=20000, blank=True)
    callback_url = models.CharField(max_length=300)


class Notification(models.Model):
    class Meta:
        db_table = 'vnfpkgm_notification'
    notification_type = models.CharField(max_length=32)
    subscription_id = models.IntegerField(null=True)
    timestamp = models.DateTimeField()
    vnf_pkg_id = models.CharField(max_length=100)
    vnfd_id = models.CharField(max_length=100)
    change_type = models.CharField(max_length=15)
    operational_state = models.CharField(max_length=8)


class OnapVnfPackage(models.Model):
    class Meta:
        db_table = 'vnfpkgm_onap_vnf_package'
    csar_id = models.CharField(max_length=36)
    vnfd_id = models.CharField(max_length=36)
    vnf_pkg_id = models.CharField(max_length=36)
    vnfd_provider = models.CharField(max_length=100)
    vnfd_version = models.CharField(max_length=30)
    vnf_version = models.CharField(max_length=30)
    download_url = models.TextField(max_length=20000)
