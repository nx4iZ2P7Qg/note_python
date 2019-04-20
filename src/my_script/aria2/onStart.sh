#!/bin/sh

source base.conf

echo "${custom_log}" $1

echo "${custom_log}" onStart.sh start

newFileOrFolder=${3##"${download_dir}"/}
echo "${custom_log}" newFildOrFolder is "${newFileOrFolder}"

grep_str=#${1:0:6}
echo ${custom_log} grep_str="${grep_str}"

torrentFile=$(grep -n "${grep_str}" "${log_dir}" | cut -d ':' -f 1 | sort -u)
echo "${custom_log}" torrentFile="${torrentFile}"
