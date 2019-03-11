# 不使用PyYAML模块，因为dump出来的文件，顺序乱了，PyYAML不觉得这是个问题，当前版本为4.2b4
import shutil

import requests
from ruamel.yaml import YAML

yaml = YAML()

onap_base_url = 'http://192.168.10.212:80'
ns_package_id = '86b9664c-a1eb-4413-b3ca-00b2a8e4ebe8'
timeout = 10

# 获取onap的csar文件下载地址
onap_csar_address_url = '{onap_base_url}/api/catalog/v1/nspackages/{ns_package_id}' \
    .format(onap_base_url=onap_base_url, ns_package_id=ns_package_id)
response = requests.get(onap_csar_address_url, timeout=timeout)
response.raise_for_status()
onap_csar_url = response.json()['packageInfo']['downloadUrl']

# 下载onap的csar文件
response = requests.get(onap_csar_url, timeout=timeout)
response.raise_for_status()
with open('onap.csar', 'wb') as onap_csar:
    onap_csar.write(response.content)

# 解压onap的csar
shutil.unpack_archive('onap.csar', './onap', 'zip')

# 解析onap的yaml文件，获取待转换属性
with open(r'D:\Desktop\2018-11-19_CertusNet_dev\2019-01-09_需求_onapYamlToMano\MainServiceTemplate.yaml',
          'r') as onap_yaml_file:
    res_onap = yaml.load(onap_yaml_file)
    node_templates = res_onap['topology_template']['node_templates']
    virtual_compute = node_templates['vcpe']['capabilities']['virtual_compute']
    # cpu
    num_virtual_cpu = virtual_compute['properties']['virtual_cpu']['num_virtual_cpu']
    # mem
    virtual_mem_size = virtual_compute['properties']['virtual_memory']['virtual_mem_size']
    # disk
    size_of_storage = node_templates['vcpeDataVolume']['properties']['size_of_storage']

# 解压mano的csar
shutil.unpack_archive('cp_c_cu_1123PM.csar', './cp_c_cu_1123PM', 'zip')

# 解析mano的yaml文件到res_mano
text_str = ''
with open(r'cp_c_cu_1123PM/cp_c_cu_1123PM/Definitions/MainServiceTemplate--sol001--ver05.02.yaml',
          'r') as mano_yaml_file:
    for line in mano_yaml_file.readlines():
        # 去除yaml文件中不应该出现的tab，避免转换出现问题
        no_tab_line = line.replace('\t', '')
        text_str += no_tab_line
    res_mano = yaml.load(text_str)

# 转换，在res_mano合适的位置写入属性
# res_mano['test_node']['cpu'] = num_virtual_cpu
# res_mano['test_node']['mem'] = virtual_mem_size
# res_mano['test_node']['storage'] = size_of_storage

# 从修改的res_mano覆盖原文件
with open(r'cp_c_cu_1123PM/cp_c_cu_1123PM/Definitions/MainServiceTemplate--sol001--ver05.02.yaml',
          'w') as result_yaml_file:
    # 使用mano的yaml格式
    yaml.default_flow_style = False
    yaml.dump(res_mano, result_yaml_file)
