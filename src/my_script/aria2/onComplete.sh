#!/bin/sh

# 导入配置
. ~/script/aria2/base.conf

echo "${custom_log} onComplete.sh start"

echo "${custom_log} GID=${1}"

# "${3}"是事件回调函数的第3个参数
# 是第一个下载文件的位置
# 去掉前面的下载目录，拿到文件名
newFileOrFolder="${3##"${download_dir}"/}"
echo "${custom_log} newFildOrFolder=${newFileOrFolder}"

# 路径是否包含斜线/
if (( "$(expr index "${newFileOrFolder}" "/")" > 0 ));
then
    # 是目录
    folderFlag=true
else
    # 不是目录
    folderFlag=false
fi

# 如果是目录
if [ "${folderFlag}" == true ];
then
    # 移动整个目录
    toMovedItem="${newFileOrFolder%%/*}"
# 如果是文件
else
    # 移动文件
    toMovedItem="${newFileOrFolder}"
fi
echo "${custom_log} toMovedItem=${toMovedItem}"

# 事件回调函数的第1个参数，是唯一的GID，取前6位，准备在日志里匹配
grep_str=#"${1:0:6}"
echo "${custom_log} grep_str=${grep_str}"

# 比较关键的步骤，通过GID拿到种子文件名，-H即使是只有一个文件，也列出文件全名
echo "${custom_log} grep loop start"
# 重试次数
retryCount=0
while :
do
    # grep结果条目去重，可能是多行
    grepEntries="$(grep -H "${grep_str}" "${log_dir}"/* | cut -d ':' -f 1 | sort -u)"
    echo "${custom_log} grepEntries=${grepEntries}"

    # grep结果去重条目数
    grepResultCount="$(echo ${grepEntries} | wc | awk '{print $1}')"
    echo "${custom_log} grepResultCount=${grepResultCount}"

    # 如果条目数不为1
    if [ "${grepResultCount}" -ne 1 ];
    then
        let "retryCount += 1"
        echo "${custom_log} grep retry ${retryCount}" times
        if (( "${retryCount}" > 30 ));
        then
            exit
        else
            sleep 1m
        fi
    else
        # 取条目值
        torrentFile="${grepEntries}"
        echo "${custom_log} torrentFile=${torrentFile}"
        break
    fi
done
echo "${custom_log} grep loop end"

# 去掉.log后缀，得到.torrent
# 
# 有时torrentFile会被识别为binary文件，比较奇怪
# 这种情况下，grep后，在正常路径的前面有Binary file，后面有 matches
# 通过下面的最长匹配路径前后端删除可以处理
torrentFile="${torrentFile%%.log*}"
echo "${custom_log} deleted max .log* torrentFile=${torrentFile}"

# 去掉目录路径，得到种子文件名
torrentName="${torrentFile##*/}"
echo "${custom_log} deleted max */ torrentName=${torrentName}"

if [ "${torrentName}" != "" ];
then
    # 删除.aria2文件
    echo "${custom_log} rm ${download_dir}/${toMovedItem}.aria2"
    rm "${download_dir}"/"${toMovedItem}".aria2

    # 移动且重命名.torrent
    echo "${custom_log} mv ${seeds_work_dir}/${torrentName} ${download_complete}/${toMovedItem}.torrent"
    mv "${seeds_work_dir}"/"${torrentName}" "${download_complete}"/"${toMovedItem}".torrent
    if [ "${?}" != 0 ];
    then
        echo "${custom_log} move and rename .torrent error"
    else
        echo "${custom_log} move and rename .torrent success"
    fi

    # 移动完成的下载
    echo "${custom_log} mv ${download_dir}/${toMovedItem} ${download_complete}"
    mv "${download_dir}"/"${toMovedItem}" "${download_complete}"
    if [ "${?}" != 0 ];
    then
        echo "${custom_log} move and rename video error"
    else
        echo "${custom_log} move and rename video success"
    fi

    # 移动且重命名.log
    echo "${custom_log} mv ${log_dir}/${torrentName}.log ${download_complete}/${toMovedItem}.log"
    mv "${log_dir}"/"${torrentName}".log "${download_complete}"/"${toMovedItem}".log
    if [ "${?}" != 0 ];
    then
        echo "${custom_log} move and rename .log error"
    else
        echo "${custom_log} move and rename log success"
    fi
else
    echo "${custom_log} get torrentName failed"
fi

echo "${custom_log} onComplete.sh end"
