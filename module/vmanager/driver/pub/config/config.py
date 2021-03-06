# Copyright 2016-2017 certus Corporation.
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

# [AAI]
AAI_SERVICE_IP = '127.0.0.1'
AAI_SERVICE_PORT = '8443'
AAI_BASE_URL = "https://%s:%s/aai/v8" % (AAI_SERVICE_IP, AAI_SERVICE_PORT)
AAI_USER = "AAI"
AAI_PASSWORD = "AAI"
CLOUD_OWNER = "11"
CLOUD_REGION_ID = ""
TENANT_ID = ""

# [MSB]
MSB_SERVICE_IP = '10.0.14.1'
MSB_SERVICE_PORT = '80'

# [register]
REG_TO_MSB_WHEN_START = True
REG_TO_MSB_REG_URL = "/api/microservices/v1/services"
REG_TO_MSB_REG_PARAM = {
    "serviceName": "certusvmanagerdriver",
    "version": "v1",
    "url": "/api/certusvmanagerdriver/v1",
    "protocol": "REST",
    "visualRange": "1",
    "nodes": [{
        "ip": "10.0.14.1",
        # "ip": "127.0.0.1",
        "port": "8510",
        "ttl": 0
    }]
}

# [certus-resource]
CERTUS_RESOURCE_URL="http://192.168.2.120:8080/mano-resource/rest/"
