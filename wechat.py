import numpy as np
import time
from uiautomation import WindowControl
import yagmail

# 注册和连接SMTP
yag = yagmail.SMTP(
    user='sender_email',      # 发件人邮箱
    password='password',      # QQ邮箱授权码
    host='smtp.qq.com',       # SMTP服务器地址
    port=465,                 # SMTP SSL端口
    smtp_ssl=True             # 启用SSL
)

# 获取微信窗口
wx = WindowControl(Name='微信')
print(wx)
wx.SwitchToThisWindow()

hw = wx.ListControl(Name='会话')
print('寻找会话控制件绑定', hw)

target_chat_name = ''  # 发送消息的目标聊天框名称

while True:
    we = hw.TextControl(searchDepth=3)
    while not we.Exists(0):
        time.sleep(1)  # 延时1秒，避免快速轮询

    # 如果存在未读消息
    if we.Exists(0) and we.Name:
        we.Click(simulateMove=False)
        print()
        msg_controls = wx.ListControl(Name='消息').GetChildren()
        send_name = we.GetParentControl().GetParentControl().Name

        if msg_controls:  # 检查是否有消息控件
            last_msg = msg_controls[-1]
            send_content = f'收到了一条来自{send_name}的消息，内容为: {last_msg.Name}'

            if send_name == 'xxxxxxxx' : # 收到xxxxxxx的消息作为邮件发送条件
                '''
                邮箱发送
                '''
                yag.send(
                    to='xjcee@outlook.com',  # 收件人
                    subject='subject',  # 邮件主题
                    contents=send_content  # 邮件正文
                )
                '''
                直接使用微信聊天转发消息内容（好像微信存在检测，有风险）
                '''
                # # 查找目标聊天框是否存在
                # target_chat = next((child for child in hw.GetChildren() if child.Name == target_chat_name), None)
                # 
                # if target_chat:
                #     target_chat.Click(simulateMove=False)
                #     # 格式化要发送的内容
                #     # 发送消息
                #     wx.SendKeys(send_content.replace('{br}', '{Shift}{Enter}'), waitTime=0)
                #     wx.SendKeys('{Enter}', waitTime=0)
                # else:
                #     print(f"没有找到目标聊天框: {target_chat_name}")
        else:
            print("没有找到消息控件")
    else:
        print("没有找到未读消息控件")

    # 稍微延时，避免过于频繁的循环
    time.sleep(8)
