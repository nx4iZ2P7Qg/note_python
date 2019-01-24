# 不使用PyYAML模块，因为dump出来的文件，顺序乱了，PyYAML不觉得这是个问题，当前版本为4.2b4
import http.client
import shutil
import urllib.request
import urllib.parse
import os
import http.client
import json
import pymysql.cursors
import requests
import re
from ruamel.yaml import YAML

yaml = YAML()

# 下载onap的csar文件
onap_csar_url = 'http://192.168.10.212:8806/static/catalog/86b9664c-a1eb-4413-b3ca-00b2a8e4ebe8/xiey-ns-1207.csar'
with urllib.request.urlopen(onap_csar_url) as onap_csar_response, open('onap.csar', 'wb') as onap_csar:
    shutil.copyfileobj(onap_csar_response, onap_csar)

# 解压onap的csar
shutil.unpack_archive('onap.csar', './onap', 'zip')

# 解析onap的yaml文件，获取待转换属性
with open(r'D:\Desktop\2018-11-19_CertusNet_dev\2019-01-09_需求_onapYamlToMano\MainServiceTemplate.yaml', 'r') as onap_yaml_file:
    res_onap = yaml.load(onap_yaml_file)
    node_templates = res_onap['topology_template']['node_templates']
    virtual_compute = node_templates['vcpe']['capabilities']['virtual_compute']
    # cpu
    num_virtual_cpu = virtual_compute['properties']['virtual_cpu']['num_virtual_cpu']
    # mem
    virtual_mem_size = virtual_compute['properties']['virtual_memory']['virtual_mem_size']
    # disk
    size_of_storage = node_templates['vcpeDataVolume']['properties']['size_of_storage']

# 登陆mano，拿到mano的jsessionid
conn = http.client.HTTPConnection(host='192.168.2.120', port=8080)
login_body = "user_name=admin&user_password=21e19a17737c694224da126d5cee8f74"
headers = {
    'Content-Type': "application/x-www-form-urlencoded"
}
conn.request(method="POST", url="/mano/login", body=login_body, headers=headers)
res = conn.getresponse()
jsessionid_string = res.getheader('Set-Cookie')

# 下载mano的csar文件
mano_csar_url = 'http://192.168.2.120:8080/mano/vnfPackageAction/downloadVnfPackage.action'
opener = urllib.request.build_opener()
headers = ('Cookie', jsessionid_string)
opener.addheaders = [headers]
# 待下载的模板名
mano_csar_body = urllib.parse.urlencode({'vnfPackageName': 'cp_c_cu_1123PM'}).encode('utf-8')
# 不改变模板名
with opener.open(mano_csar_url, mano_csar_body) as mano_csar_response, open('cp_c_cu_1123PM.csar', 'wb') as mano_csar:
    data = mano_csar_response.read()
    mano_csar.write(data)

# 解压mano的csar
shutil.unpack_archive('cp_c_cu_1123PM.csar', './cp_c_cu_1123PM', 'zip')

# 解析mano的yaml文件到res_mano
text_str = ''
with open(r'cp_c_cu_1123PM/cp_c_cu_1123PM/Definitions/MainServiceTemplate--sol001--ver05.02.yaml', 'r') as mano_yaml_file:
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
with open(r'cp_c_cu_1123PM/cp_c_cu_1123PM/Definitions/MainServiceTemplate--sol001--ver05.02.yaml', 'w') as result_yaml_file:
    # 使用mano的yaml格式
    yaml.default_flow_style = False
    yaml.dump(res_mano, result_yaml_file)

# 准备好待上传的mano的csar文件
# 打包mano的csar成zip
shutil.make_archive('cp_c_cu_1123PM', 'zip', 'cp_c_cu_1123PM')
# 删除旧mano的csar
os.remove('cp_c_cu_1123PM.csar')
# 变更文件后缀
os.rename('cp_c_cu_1123PM.zip', 'cp_c_cu_1123PM.csar')

connection = pymysql.connect(host='localhost', user='root', password='123456', db='nfv_nfvo')
# 下载nsd模板，默认获取第一条
with connection.cursor() as cursor:
    sql = 'select nsd_identifier, nsd_name from nfv_nfvo.so_nsd'
    cursor.execute(sql)
    nsd_identifier, nsd_name = cursor.fetchone()
data = {
    "nsd_name": nsd_name,
    "nsd_uuid": nsd_identifier,
}
headers = {
    'Cookie': jsessionid_string[0:43],
}
response = requests.post('http://localhost:8080/mano/templateAction/downloadNsdTemplate.action', data=data, headers=headers)
with open("../package_demo/nsd_old.yaml", 'w') as nsd_old:
    nsd_old.write(response.content.decode('utf-8'))

# 获取待删除的批量nsd_id，此操作会获取所有数据，请根据需要过滤
nsd_id_list = []
with connection.cursor() as cursor:
    sql = "select nsd_identifier from nfv_nfvo.so_nsd"
    cursor.execute(sql)
    result = cursor.fetchall()
    for nsd_tuple in result:
        nsd_id_list.append(list(nsd_tuple)[0])
nsd_id_join = ','.join(nsd_id_list)

# 删除mano系统中现存nsd模板
delete_mano_nsd_url = 'http://localhost:8080/mano/templateAction/deleteSoNsdTemplate.action?nsdIdentifierArray=%s' % nsd_id_join
opener = urllib.request.build_opener()
headers = ('Cookie', jsessionid_string)
opener.addheaders = [headers]
opener.open(delete_mano_nsd_url)

# 获取待删除的vnf_package_curr_id，默认只删除第一个
with connection.cursor() as cursor:
    sql = "select vnf_package_curr_id from nfv_nfvo.vnf_package"
    cursor.execute(sql)
    result = cursor.fetchone()
    vnf_package_curr_id = list(result)[0]

# 删除mano系统中现存vnfd模板
delete_mano_vnf_package_url = 'http://localhost:8080/mano/vnfPackageAction/deleteVnfPackageCurr.action?id=%s' % vnf_package_curr_id
opener = urllib.request.build_opener()
headers = ('Cookie', jsessionid_string)
opener.addheaders = [headers]
opener.open(delete_mano_vnf_package_url)

# 上传新的vnf_package到mano
# 拿到token
upload_mano_vnf_package_token = 'http://localhost:8080/mano/pck_tk' \
                                '?name=cp_c_cu_1123PM.csar' \
                                '&type=&size=4561' \
                                '&modified=Mon+Dec+10+2018+13%3A39%3A53+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)' \
                                '&50184'
opener = urllib.request.build_opener()
# headers = ('Cookie', jsessionid_string)
# opener.addheaders = [headers]
response = opener.open(upload_mano_vnf_package_token)
token = json.loads(response.read().decode('utf-8'))['token']
# 第二个请求，get方式，验证文件，准备上传文件，文件名为token，大小为0
upload_mano_vnf_package_second = 'http://localhost:8080/mano/pck_upload' \
                                 '?token=%s' \
                                 '&client=html5' \
                                 '&name=cp_c_cu_1123PM.csar' \
                                 '&size=4561' \
                                 '&50187' % token
opener = urllib.request.build_opener()
response = opener.open(upload_mano_vnf_package_second)
# 第三个请求，post方式，写入上传文件内容并重命名为csar
upload_mano_vnf_package_csar = 'http://localhost:8080/mano/pck_upload' \
                               '?token=%s' \
                               '&client=html5' \
                               '&name=cp_c_cu_1123PM.csar' \
                               '&size=4561' % token
mano_csar_files = {'file': open('../package_demo/cp_c_cu_1123PM.csar', 'rb')}
headers = {
    # 'Cookie': jsessionid_string,
    'Content-Range': 'bytes 0-4716/4716'
}
response = requests.post(upload_mano_vnf_package_csar, files=mano_csar_files, headers=headers)
# 这里因为使用了非标准http上传方式，要对生成的csar文件处理
# 能用，但感觉还有问题的代码，在解压时MANO中_zipFile.getEntries()为9，正常为5
os.rename('D:/IdeaProjects/MANO/uploadpath/pck/cp_c_cu_1123PM.csar', 'D:/IdeaProjects/MANO/uploadpath/pck/old')
with open('D:/IdeaProjects/MANO/uploadpath/pck/old', 'rb') as old:
    with open('D:/IdeaProjects/MANO/uploadpath/pck/cp_c_cu_1123PM.csar', 'wb') as new:
        line = old.readline()
        new.writelines(old.readlines()[2:-1])
os.remove('D:/IdeaProjects/MANO/uploadpath/pck/old')
# 第四个请求，解压上传文件并将模板提交到系统
upload_mano_vnf_package_on_board = 'http://localhost:8080/mano/vnfPackageAction/onBoard.action'
opener = urllib.request.build_opener()
headers = ('Cookie', jsessionid_string)
opener.addheaders = [headers]
upload_mano_csar_body = urllib.parse.urlencode({'fileName': 'cp_c_cu_1123PM.csar'}).encode('utf-8')
response = opener.open(upload_mano_vnf_package_on_board, upload_mano_csar_body)

# 从数据库查找模板各id
with connection.cursor() as cursor:
    # 找最新的一条
    sql = 'select id, descriptor_id from nfv_vnfm.so_vnfd order by id desc'
    cursor.execute(sql)
    id_database, vnfd_id_datebase = cursor.fetchone()
    sql = 'select tosca_name from nfv_vnfm.so_vnfd_ext_cpd where vnfd_id = %s' % id_database
    cursor.execute(sql)
    cpd_id_oam_database, cpd_id_master_database, cpd_id_slave_database = cursor.fetchall()
    cpd_id_oam_database = str(cpd_id_oam_database)
    cpd_id_master_database = str(cpd_id_master_database)
    cpd_id_slave_database = str(cpd_id_slave_database)

# 修改nsd模板内的vnfdId，cpdId
with open("../package_demo/nsd_old.yaml", 'r') as nsd_old:
    with open("../package_demo/nsd_new.yaml", 'w') as nsd_new:
        to_modify_content = nsd_old.read()
        # 修改vnfdId
        vnfd_id_list = re.findall('vnfdId: *([0-9a-zA-Z_-]{46})', to_modify_content)
        vnfd_id = vnfd_id_list[0]
        to_modify_content.replace(vnfd_id, vnfd_id_datebase)
        # 修改cpdId
        cpd_id_list = re.findall('cpdId:[ \t\n\r-]*([0-9a-zA-Z_-]{50,63})', to_modify_content)
        cpd_id_oam = None
        cpd_id_master = None
        cpd_id_slave = None
        for cpd_id in cpd_id_list:
            if 'oam' in cpd_id:
                cpd_id_oam = cpd_id
            elif 'master' in cpd_id:
                cpd_id_master = cpd_id
            elif 'slave' in cpd_id:
                cpd_id_slave = cpd_id
        to_modify_content.replace(cpd_id_oam, cpd_id_oam_database)
        to_modify_content.replace(cpd_id_master, cpd_id_master_database)
        to_modify_content.replace(cpd_id_slave, cpd_id_slave_database)
        nsd_new.write(to_modify_content)

# 上传nsd模板
# 拿到mano的token
# mano_token_url = 'http://192.168.2.120:8080/mano-nfvo/rest/auth/check/admin/21e19a17737c694224da126d5cee8f74'
# response = requests.get(mano_token_url)
# mano_token = json.loads(response.content.decode('utf-8'))['result']
mano_nsd_upload_url = 'http://localhost:8080/mano/templateAction/uploadImportFile.action;%s' % jsessionid_string[:43]
mano_nsd_files = {
    # 'Filename': (None, 'cp_c_cu_1123PM.yaml'),
    # 'token': (None, mano_token),
    # 消除请求中的filename=，让接口识别到请求中的名字，此名字是界面上传nsd模板时输入的名字
    'tplName': (None, '123'),
    # 'userId': (None, 'null'),
    'fileName': ('cp_c_cu_1123PM.yaml', open('D:/Desktop/2018-11-19_CertusNet_dev/2018-12-04_需求_FPGA网卡_指定计算节点/cp_c_cu_1123PM.yaml', 'r'), 'application/octet-stream'),
    # 'Upload': (None, 'Submit Query'),
}
headers = {
    'Cookie': jsessionid_string[0:43],
    # 'X-Requested-With': 'ShockwaveFlash/32.0.0.114',
    # 'Content-Range': 'bytes 0-4716/4716'
}
response = requests.post(mano_nsd_upload_url, files=mano_nsd_files, headers=headers)


connection.close()