# coding=utf-8


def sha1_check_rsms_pdf_rar_archive():
    """
    诗人沙加Ultimania, BradyGames攻略书的pdf压缩文档sha1校验

    :return:
    """
    # 本地沙加u本1-4.rar文件sha1
    sha1_local_u_1 = '0BDA3CB971809D630765F9CD1AEB6E86F92AADA2'
    sha1_local_u_2 = '4E8DEDDA4D813A633ADE5016BB7D4081973433DA'
    sha1_local_u_3 = '32419C553D83657B08CD57E9CE50F8FC38E5C912'
    sha1_local_u_4 = '83881BBB8051E382EC6DE5F6D139697905FF1B58'

    # 远程对应文件sha1
    sha1_remote_u_1 = ''
    sha1_remote_u_2 = ''
    sha1_remote_u_3 = ''
    sha1_remote_u_4 = ''

    # 验证结果
    print(sha1_local_u_1.lower() == sha1_remote_u_1)
    print(sha1_local_u_2.lower() == sha1_remote_u_2)
    print(sha1_local_u_3.lower() == sha1_remote_u_3)
    print(sha1_local_u_4.lower() == sha1_remote_u_4)

    # 本地沙加b本1-5.rar文件sha1
    sha1_local_b_1 = '2C8612605FFB7E0EBD6011CE9A0144EA79778400'
    sha1_local_b_2 = '3884C8A4721B8F6D9ADDAE45C5D4A8CC2F9573D3'
    sha1_local_b_3 = '6ECE5410E6C7B6AFED0B0EC08D1A63153D84D661'
    sha1_local_b_4 = '4EC874025E2262A249647F3B3CC3BD8208552AA3'
    sha1_local_b_5 = 'CBD0AEB5BB1C29F20DA02A3973D85C0BC01164F1'

    # 远程对应文件sha1
    sha1_remote_b_1 = ''
    sha1_remote_b_2 = ''
    sha1_remote_b_3 = ''
    sha1_remote_b_4 = ''
    sha1_remote_b_5 = ''

    # 验证结果
    print(sha1_local_b_1.lower() == sha1_remote_b_1)
    print(sha1_local_b_2.lower() == sha1_remote_b_2)
    print(sha1_local_b_3.lower() == sha1_remote_b_3)
    print(sha1_local_b_4.lower() == sha1_remote_b_4)
    print(sha1_local_b_5.lower() == sha1_remote_b_5)
