#!/bin/sh

# 导入配置文件，只能使用绝对路径
. ~/script/aria2/base.conf

# 如果种子文件夹有内容
#
# 不要使用以下方式，空目录会处理一个*
# for i in "${seeds_dir}"/*;
#
# 不要使用以下方式，空格问题无法处理
# for i in $(ls "${seeds_dir}")
#
# 正确的处理方式
ls "${seeds_dir}" | while read i
do
    # 将种子移动到工作种子目录
    mv "${seeds_dir}"/"${i}" "${seeds_work_dir}"

    # 开始下载
    # onComplete.sh 下载完成后事件处理
    # onError.sh 下载异常事件处理，未实现
    # onStart.sh 下载开始事件处理，未实现
    # 
    # 手动指定日志文件
    /usr/bin/aria2c --conf-path="${conf_dir}"/aria2.conf --on-download-complete "${script_dir}"/onComplete.sh --on-download-error "${script_dir}"/onError.sh -d "${download_dir}" "${seeds_work_dir}"/"${i}" > "${log_dir}"/"${i}".log 2>&1 &
done

# 如果批量磁力文件有磁力地址
# cat /home/dexter/script/aria2/batchMagnetLinkFile | while read i
# do
#     /usr/bin/aria2c --conf-path="${conf_dir}"/aria2.conf -d "${download_complete}" "${i}" > "${log_dir}"/"${i%%/*}".log 2>&1 &
# done

# 批量磁力链接文件
magnetFile="${script_dir}"/batchMagnetLinkFile
if [ -f "${magnetFile}" ];
then
    /usr/bin/aria2c --conf-path="${conf_dir}"/aria2.conf --dir "${download_dir}" --input-file="${magnetFile}" > "${log_dir}"/batchMagnet.log 2>&1 &
#    mv "${magnetFile}" "${magnetFile}"_working
fi
