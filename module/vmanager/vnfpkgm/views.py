# coding=utf-8
import logging
import os

import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response
from vnfpkgm.models import OnapVnfPackage
from vnfpkgm.models import PkgmSubscriptionRequest

logger = logging.getLogger(__name__)


class VnfdInVnfPackage(APIView):
    def get(self, request, vnf_pkg_id):
        """
        VNFM访问的接口，获取在NFVO中已经on-boarded的vnfd

        :param request: 框架参数
        :param vnf_pkg_id: vnf package id，在通知中出现
        :return: 成功时返回一个vnfd，失败时返回相应的详情
        """
        # 前置条件: vnf package 在 nfvo 已经 on-boarded
        # 根据vnf_pkg_id找到对应的onap的csar文件中的vnfd
        try:
            dir_mano_package = 'vnfpkgm/mano_packages/'
            package_record = OnapVnfPackage.objects.filter(id=vnf_pkg_id)
            dir_mano_package += package_record[0].csar_id
            csar_name = 'MainServiceTemplate--sol001--ver05.01.yaml'
            path_to_vnfd = dir_mano_package + '/vm-all-1/vm-all-1/Definitions/' + csar_name
            logger.debug('VnfdInVnfPackage-get-path_to_vnfd = %s' % path_to_vnfd)
            with open(path_to_vnfd, 'rb') as file:
                # 将vnfd文件写入response中返回
                response = HttpResponse(file, content_type='text/html')
                response['Content-Disposition'] = 'attachment; filename=%s' % csar_name
                response['vnfdUuid'] = package_record[0].csar_id
                response['filename'] = csar_name
                # 409 Conflict，资源状态冲突，通常是vnf package没有处于"ONBOARDED"状态，目前不存在这种
                return response
        except Exception as e:
            logger.error('VnfdInVnfPackage-get-获取指定id的包异常')
            logger.exception('VnfdInVnfPackage-get-Exception is %s' % e)
            data = {
                'detail': 'VnfdInVnfPackage-get-获取指定id的vnfd异常',
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VnfPackageContent(APIView):
    def get(self, request, vnf_pkg_id):
        """
        VNFM访问的接口，获取在NFVO中已经on-boarded的vnf package

        :param request: 框架参数
        :param vnf_pkg_id: vnf package id，在通知中出现
        :return: 成功时返回一个vnf package，失败时返回相应的详情
        """
        # 前置条件: vnf package 在 nfvo 已经 on-boarded
        # 根据vnf_pkg_id找到对应的onap的csar文件
        try:
            dir_mano_package = 'vnfpkgm/mano_packages/'
            dir_mano_package += vnf_pkg_id
            csar_name = [x for x in os.listdir(dir_mano_package) if x.endswith('.csar')]
            path_to_csar = dir_mano_package + '/' + csar_name[0]
            logger.debug('VnfPackageContent-get-path_to_csar = %s' % path_to_csar)
            with open(path_to_csar, 'rb') as file:
                # 将csar文件写入response中返回
                response = HttpResponse(file, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename=%s' % csar_name[0]
                # 409 Conflict，资源状态冲突，通常是vnf package没有处于"ONBOARDED"状态，目前不存在这种
                return response
        except Exception as e:
            logger.error('VnfPackageContent-get-获取指定id的包异常')
            logger.exception('VnfPackageContent-get-Exception is %s' % e)
            data = {
                'detail': 'VnfPackageContent-get-获取指定id的包异常',
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Subscriptions(APIView):
    def post(self, pkgm_subscription_request):
        """
        VNFM向NFVO订阅vnf包管理的通知

        :param pkgm_subscription_request: PkgmSubscriptionRequest结构，authentication未实现
        :return: 是否成功订阅及详情
        """
        # 接受PkgmSubscriptionRequest结构的request body，包含过滤信息，后面NFVO会将符合条件的通知发送到请求体中指定的url
        # That data structure contains filtering criteria and a client side URI to which the VNFM will subsequently send
        # notifications about events that match the filter.
        # 怀疑此处文档描述有误，VNFM应该是NFVO才符合逻辑（2018年9月的文档，V2.5.1中这个描述依旧没变）
        logger.debug('enter subscriptions post method')
        logger.debug('subscriptions-pkgm_subscription_request = %s' % pkgm_subscription_request.data)
        filter_json = pkgm_subscription_request.data.get('filter')
        callback_uri_str = pkgm_subscription_request.data.get('callbackUri')
        data = dict()
        data['status'] = status.HTTP_400_BAD_REQUEST
        # 如果有filter结构有内容，校验
        if filter_json != {}:
            flag, data['detail'] = check_pkgm_subscription_request(filter_json)
            if not flag:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        # 发送请求到body中的url，测试notification point是否有效，无效则返回详情 todo df 修改成NotificationEndpoint
        # response = Response()
        # try:
        #    response = requests.get(callback_uri_str)
        #    logger.debug('subscriptions-response = %s' % response.content)
        #except Exception as e:
        #    logger.exception('subscriptions-Exception = %s' % e)
        #    if response.status_code != status.HTTP_204_NO_CONTENT:
        #        data['status'] = status.HTTP_404_NOT_FOUND
        #        data['detail'] = '尝试访问callbackUri异常'
        #        return Response(data, status=status.HTTP_404_NOT_FOUND)
        # 根据filter与callback_url查询相关记录
        # 这里直接使用json作为查询条件，文档中10.5.3.4有相关描述，可以认为此json是有序的
        # All attributes shall match in order for the filter to match
        pkgm_subscription_request = PkgmSubscriptionRequest.objects.filter(filter=filter_json,
                                                                           callback_url=callback_uri_str)
        # 10.4.7.3.1中提到重复订阅，这里取第2种做法，即如果重复，不新建订阅，返回303
        logger.debug('subscriptions-pkgm_subscription_request = %s' % pkgm_subscription_request)
        if len(pkgm_subscription_request) != 0:
            return Response(status=status.HTTP_303_SEE_OTHER)
        # nfvo创建一个新的订阅
        pkgm_subscription_request = PkgmSubscriptionRequest(filter=filter_json, callback_url=callback_uri_str)
        # 保存订阅信息，之后可以通过其内容发送相关通知到vnfm
        pkgm_subscription_request.save()
        pkgm_subscription = dict()
        # 刚刚生成的记录id
        pkgm_subscription['id'] = pkgm_subscription_request.pk
        if filter_json is not None:
            pkgm_subscription['filter'] = filter_json
        pkgm_subscription['callback_uri'] = callback_uri_str
        headers = {'Location': 'todo/vnfpkgm/v1/subscriptions/todo'}  # todo df
        return Response(pkgm_subscription, status=status.HTTP_201_CREATED, headers=headers)

    def get(self):
        return Response('read_subscriptions')


class IndividualSubscription(APIView):
    def get(self):
        return Response('IndividualSubscription-get')

    def delete(self, subscription_id):
        PkgmSubscriptionRequest.objects.filter(id=subscription_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def check_pkgm_subscription_request(filter_json):
    """
    校验PkgmNotificationsFilter结构

    :param filter_json: 定义在sol003，10.5.3.4中的结构
    :return: 校验结果及详情
    """
    logger.debug('enter check_pkgm_subscription_request method')
    flag = False
    detail = ''
    count = 0
    try:
        type_list = filter_json.get('notificationTypes')
        if type_list is not None:
            if not isinstance(type_list, list):
                detail = '请求体-notificationTypes非数组结构'
            for content in type_list:
                if not isinstance(content, str):
                    detail = '请求体-notificationTypes，其值非string'
                if content not in ['VnfPackageOnboardingNotification', 'VnfPackageChangeNotification']:
                    detail = '请求体-notificationTypes不在指定枚举范围内'
        providers_list = filter_json.get('vnfProductsFromProviders')
        if providers_list is not None:
            count += 1
            if not isinstance(providers_list, list):
                detail = '请求体-vnfProductsFromProviders非数组结构'
            for provider_json in providers_list:
                if provider_json.get('vnfProvider') is None:
                    detail = '请求体-缺少vnfProvider'
                if provider_json.get('vnfProducts') is not None:
                    products_list = provider_json.get('vnfProducts')
                    if products_list is not None:
                        if not isinstance(products_list, list):
                            detail = '请求体-vnfProducts非数组结构'
                        for product_json in products_list:
                            if product_json.get('vnfProductName') is None:
                                detail = '请求体-缺少vnfProductName'
                            versions_list = product_json.get('versions')
                            if versions_list is not None:
                                if not isinstance(versions_list, list):
                                    detail = '请求体-versions非数组结构'
                                for version_json in versions_list:
                                    if version_json.get('vnfSoftwareVersion') is None:
                                        detail = '请求体-缺少vnfSoftwareVersion'
                                    vnfd_versions_list = version_json.get('vnfdVersions')
                                    if vnfd_versions_list is not None:
                                        if not isinstance(vnfd_versions_list, list):
                                            detail = '请求体-vnfdVersions非数组结构'
                                        for vnfd_version in vnfd_versions_list:
                                            if not isinstance(vnfd_version, str):
                                                detail = '请求体-vnfdVersions，其值非string'
        vnfd_id_list = filter_json.get('vnfdId')
        if vnfd_id_list is not None:
            count += 1
            if not isinstance(vnfd_id_list, list):
                detail = '请求体-vnfdId非数组结构'
        vnfd_pkg_id_list = filter_json.get('vnfPkgId')
        if vnfd_pkg_id_list is not None:
            count += 1
            if not isinstance(vnfd_pkg_id_list, list):
                detail = '请求体-vnfPkgId非数组结构'
        operational_state_list = filter_json.get('operationalState')
        if operational_state_list is not None:
            if not isinstance(operational_state_list, list):
                detail = '请求体-operationalState非数组结构'
            for state in operational_state_list:
                if state not in ['ENABLED', 'DISABLED']:
                    detail = '请求体-operationalState不在指定枚举范围内'
        usage_state_list = filter_json.get('usageState')
        if usage_state_list is not None:
            if not isinstance(usage_state_list, list):
                detail = '请求体-usageState非数组结构'
            for state in usage_state_list:
                if state not in ['IN_USE', 'NOT_IN_USE']:
                    detail = '请求体-usageState不在指定枚举范围内'
        # 要求vnfProductsFromProviders, vnfdId, vnfPkgId在一次请求中三个出现一个
        if count != 1:
            detail = "请求体-要求['vnfProductsFromProviders', 'vnfdId', 'vnfPkgId']三者出现一个"
        logger.debug('check_pkgm_subscription_request-detail = %s' % detail)
        logger.debug('check_pkgm_subscription_request-flag = %s' % flag)
    except Exception as e:
        logger.exception('check_pkgm_subscription_request-Exception = %s' % e)
        detail = '请求体-结构异常'
    flag = True
    return flag, detail
