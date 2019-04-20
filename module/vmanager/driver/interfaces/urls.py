# coding=utf-8
# Copyright 2017 certus Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls import url
from driver.interfaces import views

urlpatterns = [
    url(r'^api/(?P<vnfmtype>[0-9a-zA-Z\-\_]+)/v1/(?P<vnfmid>[0-9a-zA-Z\-\_]+)/vnfs$', views.instantiate_vnf,
        name='instantiate_vnf'),
    url(r'^api/(?P<vnfmtype>[0-9a-zA-Z\-\_]+)/v1/(?P<vnfmid>[0-9a-zA-Z\-\_]+)/vnfs/(?P<vnfInstanceId>'
        r'[0-9a-zA-Z\-\_]+)/terminate$', views.terminate_vnf, name='terminate_vnf'),
    url(r'^api/(?P<vnfmtype>[0-9a-zA-Z\-\_]+)/v1/(?P<vnfmid>[0-9a-zA-Z\-\_]+)/vnfs/(?P<vnfInstanceId>'
        r'[0-9a-zA-Z\-\_]+)$', views.query_vnf, name='query_vnf'),
    url(r'^api/(?P<vnfmtype>[0-9a-zA-Z\-\_]+)/v1/(?P<vnfmid>[0-9a-zA-Z\-\_]+)/jobs/(?P<jobid>[0-9a-zA-Z\-\_]+)$',
        views.operation_status, name='operation_status'),
    url(r'^api/(?P<vnfmtype>[0-9a-zA-Z\-\_]+)/v1/vnfpackages$', views.get_vnfpkgs, name='get_vnfpkgs'),
    url(r'^api/(?P<vnfmtype>[0-9a-zA-Z\-\_]+)/v1/resource/grant$', views.grantvnf, name='grantvnf'),
    url(r'^api/(?P<vnfmtype>[0-9a-zA-Z\-\_]+)/v1/vnfs/lifecyclechangesnotification$', views.notify, name='notify'),
    # (?P<vnfmtype>[0-9a-zA-Z\-\_]+)将匹配到的[0-9a-zA-Z\-\_]+取一个组名vnfmtype
    # 这个raw串不够清晰，是r''r''的形式，后面的r''没必要，可以写在一起，等测试后修改
    url(r'^api/(?P<vnfmtype>[0-9a-zA-Z\-\_]+)/v1/(?P<vnfmid>[0-9a-zA-Z\-\_]+)/vnfs/(?P<vnfInstanceId>'r'[0-9a-zA-Z\-\_]+)/scale',
        views.scale_vnf, name='scale_vnf')
]
