import os
import subprocess

from src.my_script.aria2.aria2_batch_config import download_dir, log_dir, script_dir, seeds_dir, seeds_work_dir, \
    conf_dir

for torrent in [torrent for torrent in os.listdir(seeds_dir) if torrent[-8:].lower() == '.torrent']:
    # 移动种子到工作目录
    os.rename(os.path.join(seeds_dir, torrent), os.path.join(seeds_work_dir, torrent))
    # 准备路径
    conf_path = os.path.join(conf_dir, 'aria2.conf')
    on_download_complete = os.path.join(script_dir, 'onComplete.sh')
    on_download_error = os.path.join(script_dir, 'onError.sh')
    torrent_path = os.path.join(seeds_work_dir, torrent)
    log_path = os.path.join(log_dir, torrent) + str('.log')
    # 调用aria2c
    subprocess.run(f'/usr/bin/aria2c \
                    --check-integrity true \
                    --summary-interval 600 \
                    --conf-path={conf_path} \
                    --on-download-complete={on_download_complete} \
                    --on-download-error={on_download_error} \
                    --dir={download_dir} {torrent_path} > {log_path} 2>&1 &')
