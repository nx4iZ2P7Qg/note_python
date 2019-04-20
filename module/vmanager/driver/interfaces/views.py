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

import inspect
import json
import logging
import time
import traceback
import ruamel.yaml

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from driver.pub.exceptions import CertusvmanagerdriverException
from driver.pub.utils import restcall
from driver.pub.utils.restcall import req_by_msb
from driver.pub.config.config import CERTUS_RESOURCE_URL

logger = logging.getLogger(__name__)

mano_vnfm_auth_url = None


@api_view(http_method_names=['POST'])
def instantiate_vnf(request, *args, **kwargs):
    try:
        logger.debug("instantiate_vnf--post::> %s" % request.data)
        logger.debug("instantiate_vnf-kwargs = %s" % kwargs)
        logger.debug("Create vnf begin!")
        vnfd_descriptor_id, vnfd_df_flavour_id = get_parameter_from_vnfd(ignorcase_get(request.data, "vnfPackageId"))
        logger.debug('vnfd_descriptor_id = %s' % vnfd_descriptor_id)
        logger.debug('vnfd_df_flavour_id = %s' % vnfd_df_flavour_id)

        vnfm_id = ignorcase_get(kwargs, "vnfmid")

        ret = req_by_msb("api/aai-esr-server/v1/vnfms/%s" % vnfm_id, "GET")
        logger.debug("instantiate_vnf-req_by_msb response=%s", ret)
        if ret[0] != 0:
            logger.error('Status code is %s, detail is %s.', ret[2], ret[1])
            raise CertusvmanagerdriverException("Failed to query vnfm(%s) from nslcm." % vnfm_id)
        global mano_vnfm_auth_url
        mano_vnfm_auth_url = json.JSONDecoder().decode(ret[1])['certificateUrl']
    
        logger.debug('instantiate_vnf-mano_vnfm_auth_url = %s' % mano_vnfm_auth_url)

        input_data = {
            "vnfdId": vnfd_descriptor_id,
            "vnfInstanceName": ignorcase_get(request.data, "vnfInstanceName"),
            "vnfInstanceDescription": ignorcase_get(request.data, "vnfInstanceDescription")
        }
        logger.debug("do_createvnf: request data=[%s],input_data=[%s],vnfm_id=[%s]", request.data, input_data, vnfm_id)

        #        vnf_package_id = ignorcase_get(request.data, "vnfPackageId")
        #        ret = vnfpackage_get(vnf_package_id)

        #        if ret[0] != 0:
        #            return Response(data={'error': ret[1]}, status=ret[2])
        #        vnf_package_info = json.JSONDecoder().decode(ret[1])
        #        packageInfo = ignorcase_get(vnf_package_info, "packageInfo")
        #        logger.debug("[%s] packageInfo=%s", fun_name(), packageInfo)

        #        vnfPkg_params = {
        #            "vnfdId": ignorcase_get(packageInfo, "vnfdId"),
        #            "vnfPkgId": ignorcase_get(packageInfo, "vnfPackageId"),
        #            "vnfPackageUri": ignorcase_get(packageInfo, "downloadUrl")
        #        }
        #        ret = svnfm_download_vnf_package(vnfm_id, vnfPkg_params)
        #        if ret[0] != 0:
        #            return Response(data={'error': ret[1]}, status=ret[2])

        resp = do_createvnf(vnfm_id, input_data)
        logger.debug("do_createvnf: response data=[%s]", resp)
        logger.debug("Create vnf end!")

        logger.debug("Instantiate vnf start!")
        vnfInstanceId = resp["id"]
        vim_uuid = ignorcase_get(ignorcase_get(request.data, "additionalParam"), "vimId")
        vim_connection_info = {
            "vimId": vim_uuid
        }
        input_data = {
            "flavourId": vnfd_df_flavour_id,
            # "extVirtualLinks": ignorcase_get(request.data, "extVirtualLink"),
            # 根据sol003，指定实例化的vim信息
            "vimConnectionInfo": vim_connection_info,
            "additionalParams": ignorcase_get(request.data, "additionalParam")
        }
        logger.debug("do_instvnf: vnfInstanceId=[%s], vnfm_id=[%s], input_data=[%s]",
                     vnfInstanceId, vnfm_id, input_data)
        resp = do_instvnf(vnfInstanceId, vnfm_id, input_data)
        logger.debug("do_instvnf: response data=[%s]", resp)
        resp_data = {
            "vnfInstanceId": vnfInstanceId,
            "jobId": ignorcase_get(resp, "vnfLcmOpOccId")
        }
        logger.debug("Instantiate vnf end!")
        return Response(data=resp_data, status=status.HTTP_201_CREATED)
    except CertusvmanagerdriverException as e:
        logger.error('instantiate vnf failed, detail message: %s' % e.message)
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['POST'])
def terminate_vnf(request, *args, **kwargs):
    logger.debug("terminate_vnf--post::> %s" % request.data)
    logger.debug("Terminate vnf begin!")
    vnfm_id = ignorcase_get(kwargs, "vnfmid")
    vnfInstanceId = ignorcase_get(kwargs, "vnfInstanceId")
    try:
        input_data = {
            "terminationType": ignorcase_get(request.data, "terminationType"),
            "gracefulTerminationTimeout": ignorcase_get(request.data, "gracefulTerminationTimeout")
        }
        logger.debug("do_terminatevnf: vnfm_id=[%s],vnfInstanceId=[%s],input_data=[%s]",
                     vnfm_id, vnfInstanceId, input_data)
        resp = do_terminatevnf(vnfm_id, vnfInstanceId, input_data)
        logger.debug("terminate_vnf: response data=[%s]", resp)

        jobId = ignorcase_get(resp, "vnfLcmOpOccId")
        gracefulTerminationTimeout = ignorcase_get(request.data, "gracefulTerminationTimeout")
        logger.debug("wait4job: vnfm_id=[%s],jobId=[%s],gracefulTerminationTimeout=[%s]",
                     vnfm_id, jobId, gracefulTerminationTimeout)
        resp = wait4job(vnfm_id, jobId, gracefulTerminationTimeout)
        logger.debug("[wait4job] response=[%s]", resp)

        logger.debug("Delete vnf start!")
        logger.debug("do_deletevnf: vnfm_id=[%s],vnfInstanceId=[%s],request data=[%s]",
                     vnfm_id, vnfInstanceId, request.data)
        resp = do_deletevnf(vnfm_id, vnfInstanceId, request.data)
        respData = {
            "jobId": ignorcase_get(resp, "vnfLcmOpOccId")
        }
        logger.debug("do_deletevnf: response data=[%s]", resp)
        logger.debug("Delete vnf end!")

        return Response(data=respData, status=status.HTTP_204_NO_CONTENT)
    except CertusvmanagerdriverException as e:
        logger.error('Terminate vnf failed, detail message: %s' % e.message)
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['GET'])
def query_vnf(request, *args, **kwargs):
    logger.debug("query_vnf--post::> %s" % request.data)
    vnfm_id = ignorcase_get(kwargs, "vnfmid")
    vnfInstanceId = ignorcase_get(kwargs, "vnfInstanceId")
    try:
        logger.debug("[%s] request.data=%s", fun_name(), request.data)
        resp = do_queryvnf(request, vnfm_id, vnfInstanceId)
        query_vnf_resp_mapping = {
            "vnfInstanceId": "",
            "vnfInstanceName": "",
            "vnfInstanceDescription": "",
            "vnfdId": "",
            "vnfPackageId": "",
            "version": "",
            "vnfProvider": "",
            "vnfType": "",
            "vnfStatus": ""
            #"extensions": ""
        }
        resp_response_data = mapping_conv(query_vnf_resp_mapping, ignorcase_get(resp, "ResponseInfo"))
        resp_data = {
            "vnfInfo": resp_response_data
        }
        resp_data["vnfInfo"]["version"] = ignorcase_get(resp, "version")
        resp_data["vnfInfo"]["vnfStatus"] = "INACTIVE"
        if ignorcase_get(resp, "instantiationState") == "INSTANTIATED":
            resp_data["vnfInfo"]["vnfStatus"] = "ACTIVE"
        resp_data["vnfInfo"]["vnfInstanceId"] = ignorcase_get(resp, "id")
        resp_data["vnfInfo"]["vnfdId"] = ignorcase_get(resp, "vnfdId")
        resp_data["vnfInfo"]["vnfType"] = ignorcase_get(resp, "vnfType")
        resp_data["vnfInfo"]["vnfInstanceDescription"] = ignorcase_get(resp, "vnfInstanceDescription")
        resp_data["vnfInfo"]["vnfInstanceName"] = ignorcase_get(resp, "vnfInstanceName")
        resp_data["vnfInfo"]["vnfProvider"] = ignorcase_get(resp, "vnfProvider")
        #resp_data["vnfInfo"]["extensions"] = ignorcase_get(resp, "extensions")
        logger.debug("[%s]resp_data=%s", fun_name(), resp_data)
        return Response(data=resp_data, status=status.HTTP_200_OK)
    except CertusvmanagerdriverException as e:
        logger.error('Query vnf failed, detail message: %s' % e.message)
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['GET'])
def operation_status(request, *args, **kwargs):
    logger.debug("operation_status--post::> %s" % request.data)
    try:
        logger.debug("[%s] request.data=%s", fun_name(), request.data)
        vnfm_id = ignorcase_get(kwargs, "vnfmid")
        jobId = ignorcase_get(kwargs, "jobId")
        responseId = ignorcase_get(kwargs, "responseId")
        logger.debug("[operation_status] vnfm_id=%s", vnfm_id)
        vnfm_info = get_vnfminfo_from_nslcm(vnfm_id)
        logger.debug("[operation_status] vnfm_info=[%s]", vnfm_info)

        ret = call_vnfm("lcm/v1/vnf_lc_ops/%s?responseId=%s" % (jobId, responseId), "GET", vnfm_info)
        if ret[0] != 0:
            logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
            raise CertusvmanagerdriverException('Failed to query vnf operation status.')
        resp_data = json.JSONDecoder().decode(ret[1])
        logger.debug("[%s]resp_data=%s", fun_name(), resp_data)
        query_operation_resp_mapping = {
            "progress": "",
            "status": "",
            "statusDescription": "",
            "errorCode": "",
            "responseId": "",
        }
        responseDescriptor = mapping_conv(query_operation_resp_mapping, ignorcase_get(resp_data, "ResponseInfo"))
        ResponseInfo = []
        resp_desc = ignorcase_get(resp_data, "responseDescriptor")
        if ignorcase_get(resp_desc, "lcmOperationStatus") == "COMPLETED":
            responseDescriptor["status"] = "finished"
        elif ignorcase_get(resp_desc, "lcmOperationStatus") == "FAILED_TEMP":
            responseDescriptor["status"] = "error"
        elif ignorcase_get(resp_desc, "lcmOperationStatus") == "FAILED":
            responseDescriptor["status"] = "error"
        elif ignorcase_get(resp_desc, "lcmOperationStatus") == "PROCESSING":
            responseDescriptor["status"] = "processing"
        else:
            responseDescriptor["status"] = ignorcase_get(resp_desc, "lcmOperationStatus")
        responseDescriptor["progress"] = ignorcase_get(resp_desc, "progress")
        responseDescriptor["responseId"] = ignorcase_get(resp_desc, "responseId")
        responseDescriptor["statusDescription"] = ignorcase_get(resp_desc, "statusDescription")
        responseDescriptor["errorCode"] = ignorcase_get(resp_desc, "errorCode")
        responseHistory = resp_desc["responseHistoryList"]
        for index, item in enumerate(responseHistory):
            history_dict = {}
            history_dict["responseId"] = ignorcase_get(item, "responseId")
            history_dict["progress"] = ignorcase_get(item, "progress")
            if ignorcase_get(item, "lcmOperationStatus") == "COMPLETED":
                history_dict["status"] = "finished"
            elif ignorcase_get(item, "lcmOperationStatus") == "FAILED_TEMP":
                history_dict["status"] = "error"
            elif ignorcase_get(item, "lcmOperationStatus") == "FAILED":
                history_dict["status"] = "error"
            elif ignorcase_get(item, "lcmOperationStatus") == "PROCESSING":
                history_dict["status"] = "processing"
            else:
                history_dict["status"] = ignorcase_get(item, "lcmOperationStatus")
            history_dict["statusDescription"] = ignorcase_get(item, "statusDescription")
            history_dict["errorCode"] = ignorcase_get(item, "errorCode")
            ResponseInfo.append(history_dict)
        responseDescriptor["responseHistoryList"] = ResponseInfo
        operation_data = {
            "jobId": ignorcase_get(resp_data, "vnfLcOpId"),
            "responseDescriptor": responseDescriptor
        }
        logger.debug("[%s]operation_data=%s", fun_name(), operation_data)
        return Response(data=operation_data, status=status.HTTP_200_OK)
    except CertusvmanagerdriverException as e:
        logger.error('Query vnf failed, detail message: %s' % e.message)
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['POST'])
def grantvnf(request, *args, **kwargs):
    try:
        logger.debug("[grant_vnf] req_data = %s", request.data)
        # ret = req_by_msb('api/nslcm/v1/grantvnf', "POST", content=json.JSONEncoder().encode(request.data))
        # logger.debug("ret = %s", ret)
        # if ret[0] != 0:
        #    logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        #    raise CertusvmanagerdriverException('Failed to grant vnf.')
        # resp = json.JSONDecoder().decode(ret[1])
        # vim_info = resp['vim']
        # accessinfo = ignorcase_get(resp['vim'], 'accessinfo')
        # resp_data = {
        #    'vimid': ignorcase_get(vim_info, 'vimid'),
        #    'tenant': ignorcase_get(accessinfo, 'tenant')
        # }
        # logger.debug("[%s]resp_data=%s", fun_name(), resp_data)
        # return Response(data=resp_data, status=ret[2])
        resp = do_checkavailable(json.JSONEncoder().encode(request.data))
        logger.debug("[%s]resp_data=%s", fun_name(), resp)
        return Response(data=resp, status=status.HTTP_200_OK)
    except CertusvmanagerdriverException as e:
        logger.error('Grant vnf failed, detail message: %s' % e.message)
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['POST'])
def notify(request, *args, **kwargs):
    try:
        logger.debug("[%s]req_data = %s", fun_name(), request.data)
        vnfinstanceid = ignorcase_get(request.data, 'vnfinstanceid')
        ret = req_by_msb("api/nslcm/v1/vnfs/%s/Notify" % vnfinstanceid, "POST", json.JSONEncoder().encode(request.data))
        logger.debug("[%s]data = %s", fun_name(), ret)
        if ret[0] != 0:
            logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
            raise CertusvmanagerdriverException('Failed to notify vnf.')
        return Response(data=None, status=ret[2])
    except CertusvmanagerdriverException as e:
        logger.error('Grant vnf failed, detail message: %s' % e.message)
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['GET'])
def get_vnfpkgs(request, *args, **kwargs):
    try:
        logger.debug("Enter %s", fun_name())
        ret = req_by_msb("api/nslcm/v1/vnfpackage", "GET")
        if ret[0] != 0:
            logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
            raise CertusvmanagerdriverException('Failed to get vnfpkgs.')
        resp = json.JSONDecoder().decode(ret[1])
        return Response(data=resp, status=status.HTTP_200_OK)
    except CertusvmanagerdriverException as e:
        logger.error('Get vnfpkgs failed, detail message: %s' % e.message)
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['POST'])
def scale_vnf(request, *args, **kwargs):
    logger.debug("scale_vnf--post::> %s" % request.data)
    logger.debug("scale vnf begin!")
    vnfm_id = ignorcase_get(kwargs, "vnfmid")
    vnfInstanceId = ignorcase_get(kwargs, "vnfInstanceId")
    try:
        input_data = {
            "type": ignorcase_get(request.data, "type"),
            "aspectId": ignorcase_get(request.data, "aspectId"),
            "numberOfSteps": ignorcase_get(request.data, "numberOfSteps"),
            "additionalParam": ignorcase_get(request.data, "additionalParam")
        }
        logger.debug("do_scalevnf: vnfm_id=[%s],vnfInstanceId=[%s],input_data=[%s]", vnfm_id, vnfInstanceId, input_data)
        resp = do_scalevnf(vnfm_id, vnfInstanceId, input_data)
        logger.debug("scale_vnf: response data=[%s]", resp)

        jobId = ignorcase_get(resp, "vnfLcmOpOccId")
        respData = {"jobid", jobId, "vnfInstanceId", vnfInstanceId}
        return Response(data=respData, status=status.HTTP_200_OK)
    except CertusvmanagerdriverException as e:
        logger.error('scale failed, detail message: %s' % e.message)
        return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def call_vnfm(resource, method, vnfm_info, data=""):
    ret = restcall.call_req(
        base_url=ignorcase_get(vnfm_info, "url"),
        user=ignorcase_get(vnfm_info, "userName"),
        passwd=ignorcase_get(vnfm_info, "password"),
        auth_type=restcall.rest_no_auth,
        resource=resource,
        method=method,
        content=json.JSONEncoder().encode(data),
        get_auth_token_url=mano_vnfm_auth_url,
    )
    return ret


def call_certus_resource(resource, method):
    ret = restcall.call_req(
        base_url=CERTUS_RESOURCE_URL,
        # user=ignorcase_get(vnfm_info, "userName"),
        user='a',
        # passwd=ignorcase_get(vnfm_info, "password"),
        passwd='b',
        auth_type=restcall.rest_no_auth,
        resource=resource,
        method=method,
        # content=json.JSONEncoder().encode(data))
        content='')
    return ret


def mapping_conv(keyword_map, rest_return):
    resp_data = {}
    for param in keyword_map:
        if keyword_map[param]:
            if isinstance(keyword_map[param], dict):
                resp_data[param] = mapping_conv(keyword_map[param], ignorcase_get(rest_return, param))
            else:
                resp_data[param] = ignorcase_get(rest_return, param)
    return resp_data


def fun_name():
    return "=========%s=========" % inspect.stack()[1][3]


def ignorcase_get(args, key):
    if not key:
        return ""
    if not args:
        return ""
    if key in args:
        return args[key]
    for old_key in args:
        if old_key.upper() == key.upper():
            return args[old_key]
    return ""


def get_vnfminfo_from_nslcm(vnfm_id):
    logger.debug("[get_vnfminfo_from_nslcm] vnfm_id=[%s]", vnfm_id)
    ret = req_by_msb("api/aai-esr-server/v1/vnfms/%s" % vnfm_id, "GET")
    logger.debug("[get_vnfminfo_from_nslcm] response=%s", ret)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CertusvmanagerdriverException("Failed to query vnfm(%s) from nslcm." % vnfm_id)
    return json.JSONDecoder().decode(ret[1])


def wait4job(vnfm_id, job_id, gracefulTerminationTimeout=1200, retry_count=60, interval_second=3):
    logger.debug("[wait4job] vnfm_id=[%s],jobId=[%s],gracefulTerminationTimeout=[%s]",
                 vnfm_id, job_id, gracefulTerminationTimeout)
    count = 0
    job_end_normal, job_timeout = False, True
    vnfm_info = get_vnfminfo_from_nslcm(vnfm_id)

    logger.debug("[do_terminatevnf] vnfm_info=[%s]", vnfm_info)
    while count < retry_count:
        count = count + 1
        time.sleep(interval_second)
        # ret = call_vnfm("api/vnflcm/v1/vnf_lc_ops/%s?responseId=%s" % (job_id, response_id), "GET", vnfm_info)
        ret = call_vnfm("vnflcm/v1/vnf_lcm_op_occs/%s" % (job_id), "GET", vnfm_info)
        if ret[0] != 0:
            logger.error("Failed to query job: %s:%s", ret[2], ret[1])
            continue
        job_result = json.JSONDecoder().decode(ret[1])
        if "operationState" not in job_result:
            logger.error("Job(%s) does not exist.", job_id)
            continue
        operationState = job_result["operationState"]
        job_desc = job_result["operation"]
        logger.info("Job(%s)  status:(%s),job_operation.", job_id, operationState, job_desc)

        if operationState == "PROCESSING":
            logger.error("Job(%s) processing: %s", job_id, job_desc)
            continue
        elif operationState == "FAILED_TEMP":
            job_timeout = False
            logger.info("Job(%s) failed: %s", job_id, job_desc)
            break
        elif operationState == "COMPLETED":
            job_end_normal, job_timeout = True, False
            logger.debug("Job(%s) ended normally,job_end_normal=[%s],job_timeout=[%s]",
                         job_id, job_end_normal, job_timeout)
            return {"success": "success"}
    if job_timeout:
        logger.error("Job(%s) timeout", job_id)
    raise CertusvmanagerdriverException("Fail to get job status!")


def do_createvnf(vnfm_id, data):
    logger.debug("[%s] request.data=%s", fun_name(), data)
    vnfm_info = get_vnfminfo_from_nslcm(vnfm_id)
    logger.debug("[do_createvnf] vnfm_info=[%s]", vnfm_info)
    ret = call_vnfm("vnflcm/v1/vnf_instances", "POST", vnfm_info, data)
    logger.debug("[%s] call_req ret=%s", fun_name(), ret)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CertusvmanagerdriverException('Failed to create vnf.')
    return json.JSONDecoder().decode(ret[1])


def do_instvnf(vnfInstanceId, vnfm_id, data):
    logger.debug("[%s] request.data=%s", fun_name(), data)
    vnfm_info = get_vnfminfo_from_nslcm(vnfm_id)
    logger.debug("[do_instvnf] vnfm_info=[%s]", vnfm_info)
    ret = call_vnfm("vnflcm/v1/vnf_instances/%s/instantiate" % vnfInstanceId, "POST", vnfm_info, data)
    logger.debug("[%s] call_req ret=%s", fun_name(), ret)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CertusvmanagerdriverException('Failed to inst vnf.')
    return json.JSONDecoder().decode(ret[1])


def do_terminatevnf(vnfm_id, vnfInstanceId, data):
    logger.debug("[%s] request.data=%s", fun_name(), data)
    vnfm_info = get_vnfminfo_from_nslcm(vnfm_id)
    logger.debug("[do_terminatevnf] vnfm_info=[%s]", vnfm_info)
    ret = call_vnfm("vnflcm/v1/vnf_instances/%s/terminate" % vnfInstanceId, "POST", vnfm_info, data)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CertusvmanagerdriverException('Failed to terminate vnf.')
    return json.JSONDecoder().decode(ret[1])


def do_deletevnf(vnfm_id, vnfInstanceId, data):
    logger.debug("[%s] request.data=%s", fun_name(), data)
    vnfm_info = get_vnfminfo_from_nslcm(vnfm_id)
    logger.debug("[do_deletevnf] vnfm_info=[%s]", vnfm_info)
    ret = call_vnfm("vnflcm/v1/vnf_instances/%s" % vnfInstanceId, "DELETE", vnfm_info)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CertusvmanagerdriverException('Failed to delete vnf.')
    #     return json.JSONDecoder().decode(ret[1])
    return


def do_queryvnf(data, vnfm_id, vnfInstanceId):
    logger.debug("[%s] request.data=%s", fun_name(), data)
    vnfm_info = get_vnfminfo_from_nslcm(vnfm_id)
    logger.debug("[do_queryvnf] vnfm_info=[%s]", vnfm_info)
    ret = call_vnfm("vnflcm/v1/vnf_instances/%s" % vnfInstanceId, "GET", vnfm_info)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CertusvmanagerdriverException('Failed to query vnf.')
    return json.JSONDecoder().decode(ret[1])


# special vnfm(certus-vnfm) download vnf package ,and analysize the vnfd.
def svnfm_download_vnf_package(vnfm_id, data):
    logger.debug("[%s] request.data=%s", fun_name(), data)
    vnfm_info = get_vnfminfo_from_nslcm(vnfm_id)
    logger.debug("[do_createvnf] vnfm_info=[%s]", vnfm_info)
    ret = call_vnfm("vnfpkgm/v1/vnfd/save", "POST", vnfm_info, data)
    logger.debug("[%s] call_req ret=%s", fun_name(), ret)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CertusvmanagerdriverException('Failed to save vnfd.')
    return json.JSONDecoder().decode(ret[1])


# Query vnfpackage_info from catalog
def vnfpackage_get(csarid):
    ret = req_by_msb("api/catalog/v1/vnfpackages/%s" % csarid, "GET")
    return ret


def do_checkavailable(data):
    logger.debug("[%s] request.data=%s", fun_name(), data)
    # ret = call_certus_resource("grant/v1/grants", "POST", VNFM_INFO, data)
    ret = call_certus_resource("grant/v1/grants", "POST")
    logger.debug("[%s] call_req ret=%s", fun_name(), ret)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CertusvmanagerdriverException('Failed to check available.')
    return json.JSONDecoder().decode(ret[1])


# request vnfm scale vnfr
def do_scalevnf(vnfm_id, vnfInstanceId, data):
    logger.debug("[%s] request.data=%s", fun_name(), data)
    vnfm_info = get_vnfminfo_from_nslcm(vnfm_id)
    logger.debug("[do_terminatevnf] vnfm_info=[%s]", vnfm_info)
    ret = call_vnfm("vnflcm/v1/vnf_instances/%s/scale" % vnfInstanceId, "POST", vnfm_info, data)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CertusvmanagerdriverException('Failed to terminate vnf.')
    return json.JSONDecoder().decode(ret[1])


def get_parameter_from_vnfd(vnf_package_id):
    logger.debug('enter into method get_parameter_from_vnfd')
    path_to_vnfd = "vnfpkgm/mano_packages/%s/vm-all-1/vm-all-1/Definitions/MainServiceTemplate--sol001--ver05.01.yaml" % vnf_package_id
    with open(path_to_vnfd, 'r') as vnfd:
        res_mano = ruamel.yaml.YAML().load(vnfd)
        vnf_df_id_list = []
        for k in res_mano['topology_template']['substitution_mappings']['capability']['deployment_flavour'].keys():
            vnf_df_id_list.append(k)
        logger.debug('vnf_df_id_list = %s' % vnf_df_id_list)
        # 暂时只使用到一个vnf df id，需要扩展再加
        return res_mano['topology_template']['substitution_mappings']['properties']['descriptor_id'], vnf_df_id_list[0]
