# 不使用PyYAML模块，因为dump出来的文件，顺序乱了，PyYAML不觉得这是个问题，当前版本为4.2b4
from ruamel.yaml import YAML

yaml = YAML()

# onap的yaml文件
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

# mano的yaml文件
text_str = ''
with open(r'D:\Desktop\2018-11-19_CertusNet_dev\2019-01-09_需求_onapYamlToMano\MainServiceTemplate_mano.yaml',
          'r') as mano_yaml_file:
    for line in mano_yaml_file.readlines():
        # 去除yaml文件中不应该出现的tab，避免转换出现问题
        no_tab_line = line.replace('\t', '')
        text_str += no_tab_line
    res_mano = yaml.load(text_str)

# 转换
res_mano['topology_template']['substitution_mappings']['capability']['deployment_flavour']['vnfdf_vcpe_1'] \
    ['properties']['vdu_profile']['vduProfile_dp1']['attributes']['tosca_name'] = 'abc'

# 输出文件
with open(
        r'D:\Desktop\2018-11-19_CertusNet_dev\2019-01-09_需求_onapYamlToMano\MainServiceTemplate--sol001--ver05.01.yaml',
        'w') as result_yaml_file:
    yaml.default_flow_style = False
    yaml.dump(res_mano, result_yaml_file)
