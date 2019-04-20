import schedule
import vnfpkgm.schedule_task
from django.conf.urls import url
from vnfpkgm.views import IndividualSubscription
from vnfpkgm.views import Subscriptions
from vnfpkgm.views import VnfPackageContent
from vnfpkgm.views import VnfdInVnfPackage

urlpatterns = [
    url(r'^v1/vnf_packages/(?P<vnf_pkg_id>[0-9a-zA-Z\-\_]+)/vnfd$', VnfdInVnfPackage.as_view()),
    url(r'^v1/vnf_packages/(?P<vnf_pkg_id>[0-9a-zA-Z\-\_]+)/package_content$', VnfPackageContent.as_view()),
    url(r'^v1/subscriptions$', Subscriptions.as_view()),
    url(r'^v1/subscriptions/(?P<subscription_id>[0-9]+)$', IndividualSubscription.as_view()),
]

# timer, every 10 seconds run job
job = schedule.every(60).seconds.do(vnfpkgm.schedule_task.job)
# add job to instance
default_scheduler = vnfpkgm.schedule_task.Scheduler(job)
# start async job
default_scheduler.run_continuously()
