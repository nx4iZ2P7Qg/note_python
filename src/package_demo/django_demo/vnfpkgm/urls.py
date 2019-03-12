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

# 定时任务方法，每10秒取一次onap的vnf包
job = schedule.every(10).seconds.do(vnfpkgm.schedule_task.job)
# 将任务添加到 定时任务的实例
default_scheduler = vnfpkgm.schedule_task.Scheduler(job)
# 开启异步定时任务
default_scheduler.run_continuously()
