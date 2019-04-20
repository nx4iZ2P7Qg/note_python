# coding=utf-8
import datetime
import logging
import os
import threading
import time
import zipfile

import requests
import ruamel.yaml
from vnfpkgm.models import Notification
from vnfpkgm.models import OnapVnfPackage
from vnfpkgm.models import PkgmSubscriptionRequest
from driver.pub.config.config import MSB_SERVICE_IP, MSB_SERVICE_PORT

from django.db import transaction

onap_multi_service_address = 'http://%s:%s' % (MSB_SERVICE_IP, MSB_SERVICE_PORT)
dir_onap_package = 'vnfpkgm/onap_packages/'
dir_mano_package = 'vnfpkgm/mano_packages/'

logger = logging.getLogger(__name__)


def job():
    logger.debug('================== timer task start ==================')
    response = requests.get(onap_multi_service_address + '/api/catalog/v1/vnfpackages')
    response.raise_for_status()
    vnf_packages = response.json()
    driver_vnf_packages = OnapVnfPackage.objects.all()
    # 目前不需要使用的更新列表，后期可能需要更新
    to_update_list = []
    to_insert_list = []
    for vnf_package in vnf_packages:
        onap_vnf_package = OnapVnfPackage(csar_id=vnf_package['csarId'],
                                          vnfd_id=vnf_package['packageInfo']['vnfdId'],
                                          vnf_pkg_id=vnf_package['packageInfo']['vnfPackageId'],
                                          vnfd_provider=vnf_package['packageInfo']['vnfdProvider'],
                                          vnfd_version=vnf_package['packageInfo']['vnfdVersion'],
                                          vnf_version=vnf_package['packageInfo']['vnfVersion'],
                                          download_url=vnf_package['packageInfo']['downloadUrl']
                                          )
        for driver_vnf_package in driver_vnf_packages:
            # 在driver_vnf_package中找到对应的vnf_package_id，认为是之前就保存的package
            if onap_vnf_package.vnf_pkg_id == driver_vnf_package.vnf_pkg_id:
                to_update_list.append(onap_vnf_package)
                break
        # 在driver_vnf_package中没有找到对应的vnf_package_id，认为是新的package
        else:
            to_insert_list.append(onap_vnf_package)
        # driver这边的csar包不删除，故不需要考虑onap中没有，driver中有的情况
    logger.debug('=============== to_update_list ==================')
    for x in to_update_list:
        logger.debug(x.vnf_pkg_id)
    logger.debug('=============== to_insert_list ==================')
    for y in to_insert_list:
        logger.debug(y.vnf_pkg_id)
    # 下载新的vnf package到driver本地
    for vnf_package in to_insert_list:
        logger.debug('=============== individual package start ===============')
        file_name = vnf_package.download_url[vnf_package.download_url.rindex('/') + 1:]
        response = requests.get(vnf_package.download_url)
        response.raise_for_status()
        dir_individual_package = dir_onap_package + vnf_package.vnf_pkg_id
        if not os.path.exists(dir_individual_package):
            os.makedirs(dir_individual_package)
        # 包路径为vnfpkgm/onap_packages/{vnf_pkg_id}/{vnf_pkg_name}
        path_onap_package_file = dir_individual_package + '/' + file_name
        with open(path_onap_package_file, 'wb') as onap_csar:
            onap_csar.write(response.content)
            logger.debug('onap package downloaded, package name = %s' % file_name)
        # 解压onap包
        dir_onap_package_unzip = dir_individual_package + '/' + file_name[:file_name.rindex('.')]
        if not os.path.exists(dir_onap_package_unzip):
            os.makedirs(dir_onap_package_unzip)
        with zipfile.ZipFile(path_onap_package_file, 'r') as onap_csar:
            onap_csar.extractall(dir_onap_package_unzip)
            logger.debug("unpack onap csar success")
        # 保存新的vnf package信息到数据库
        transaction.set_autocommit(False)
        vnf_package.save()
        try:
            translate_yaml(dir_onap_package_unzip, vnf_package.vnf_pkg_id, vnf_package.vnfd_id, vnf_package.pk)
        except Exception as e:
            logger.error('translate_yaml exception')
            transaction.rollback()
            logger.debug('manually transaction rollback')
            logger.exception(e)
            continue
        else:
            logger.debug('translate_yaml success')
            transaction.commit()
            logger.debug('manually transaction commit')
        transaction.set_autocommit(True)
        # 检查订阅
        subscriptions = PkgmSubscriptionRequest.objects.all()
        # for sub in subscriptions:
        # 过滤相应的订阅，暂不实现 todo df
        # 保存通知
        if len(subscriptions) == 0:
            raise Exception('no subscription found')
        notification = Notification(notification_type='VnfPackageOnboardingNotification',
                                    # subscription_id=,
                                    timestamp=datetime.datetime.now(),
                                    vnf_pkg_id=vnf_package.vnf_pkg_id,
                                    vnfd_id=vnf_package.vnfd_id
                                    )
        notification.save()
        logger.debug('send notification to mano-vnfm')
        on_boarding_notification = {
            'id': notification.pk,
            'notificationType': notification.notification_type,
            'subscriptionId': 0,
            # 'timeStamp': notification.timestamp,
            'onboardedVnfPkgId': vnf_package.pk,
            'vnfdId': vnf_package.pk,
        }
        try:
            response = requests.post(subscriptions[0].callback_url, json=on_boarding_notification)
            response.raise_for_status()
        except Exception as e:
            logger.debug('send notification fail')
            logger.exception(e)
        logger.debug('=============== individual package end ===============')
    logger.debug('================== timer task end ==================')


class Scheduler(object):
    def __init__(self, jobs):
        self.jobs = [jobs]

    def run_pending(self):
        """Run all jobs that are scheduled to run.
        Please note that it is *intended behavior that tick() does not
        run missed jobs*. For example, if you've registered a job that
        should run every minute and you only call tick() in one hour
        increments then your job won't be run 60 times in between but
        only once.
        """
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            job.run()

    def run_continuously(self, interval=1):
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run


def translate_yaml(path_onap_package_file, vnf_pkg_id, vnfd_id, id):
    logger.debug('enter method translate_yaml')
    logger.debug('path_onap_package_file = %s' % path_onap_package_file)
    logger.debug('vnf_pkg_id = %s' % vnf_pkg_id)
    logger.debug('vnfd_id = %s' % vnfd_id)
    logger.debug('id = %s' % id)
    
    logger.debug('analyze onap yaml')
    with open(path_onap_package_file + '/Definitions/resource-ZengfStage1Vf-template.yml', 'r') as onap_yaml_file:
        res_onap = ruamel.yaml.YAML().load(onap_yaml_file)
        node_templates = res_onap['topology_template']['node_templates']
        virtual_compute = node_templates['vcpe']['capabilities']['virtual_compute']
        num_virtual_cpu = virtual_compute['properties']['virtual_cpu']['num_virtual_cpu']
        virtual_mem_size = virtual_compute['properties']['virtual_memory']['virtual_mem_size']
        size_of_storage = res_onap['topology_template']['inputs']['vcpedatavolume_size_of_storage']['default']
        logger.debug('cpu=%s, men=%s, storage=%s' % (num_virtual_cpu, virtual_mem_size, size_of_storage))
    logger.debug('unpack mano csar')
    dir_mano_package_unzip = dir_mano_package + vnf_pkg_id
    if not os.path.exists(dir_mano_package_unzip):
        os.makedirs(dir_mano_package_unzip)
    with zipfile.ZipFile(dir_mano_package + 'vm-all-1.csar', 'r') as mano_csar:
        mano_csar.extractall(dir_mano_package_unzip + '/vm-all-1')
        logger.debug("unpack mano csar success")
    logger.debug('load mano yaml to memory and format')
    text_str = ''
    with open(dir_mano_package_unzip + '/vm-all-1/vm-all-1/Definitions/MainServiceTemplate--sol001--ver05.01.yaml',
              'r') as mano_yaml_file:
        for line in mano_yaml_file.readlines():
            # 去除yaml文件中不应该出现的tab，避免转换出现问题
            no_tab_line = line.replace('\t', '')
            text_str += no_tab_line
        res_mano = ruamel.yaml.YAML().load(text_str)
    logger.debug('update mano yaml values')
    node_templates = res_mano['topology_template']['node_templates']
    virtual_compute = node_templates['dp_vdu']['capabilities']['virtual_compute']
    virtual_compute['properties']['virtual_cpu']['num_virtual_cpu'] = num_virtual_cpu
    virtual_compute['properties']['virtual_memory']['virtual_mem_size'] = int(virtual_mem_size[: -2]) // 1024
    node_templates['dp_storage']['properties']['size_of_storage'] = int(size_of_storage[:-2])
    logger.debug('overwrite mano yaml')
    with open(dir_mano_package_unzip + '/vm-all-1/vm-all-1/Definitions/MainServiceTemplate--sol001--ver05.01.yaml',
              'w') as result_yaml_file:
        # 使用mano的yaml格式
        ruamel.yaml.YAML().default_flow_style = False
        ruamel.yaml.YAML().dump(res_mano, result_yaml_file)
        logger.debug('overwrite mano yaml success')
    logger.debug('repack mano to zip')
    folder_path = dir_mano_package_unzip + '/vm-all-1/vm-all-1'
    parent_folder = os.path.dirname(folder_path)
    contents = os.walk(folder_path)
    with zipfile.ZipFile(dir_mano_package_unzip + '/vm-all-1.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '/', '')
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '/', '')
                zip_file.write(absolute_path, relative_path)
    logger.debug('repack mano zip success')
    if os.path.exists(dir_mano_package_unzip + '/vm-all-1.csar'):
        os.remove(dir_mano_package_unzip + '/vm-all-1.csar')
    os.rename(dir_mano_package_unzip + '/vm-all-1.zip', dir_mano_package_unzip + '/vm-all-1.csar')

