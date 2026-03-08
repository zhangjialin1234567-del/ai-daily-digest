import paramiko
import os

# 配置信息（建议通过 GitHub Secrets 传入）
HOST = os.getenv('VPS_HOST') # 45.78.77.134
PASSWORD = os.getenv('VPS_PASSWORD')
REMOTE_PATH = '/opt/1panel/apps/openresty/openresty/www/sites/cleantengflight.com/index/index.html'

def update_html(news_content):
    # 这里定义你的 HTML 模板，把资讯嵌入进去
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head><title>CleanTENG AI Daily</title></head>
    <body style="background:#000; color:#0f0; font-family: monospace;">
        <h1>[System Update: AI News Received]</h1>
        <pre>{news_content}</pre>
        <hr>
        <p>Last Updated: {os.popen('date').read()}</p>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

def upload_to_vps():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=22, username='root', password=PASSWORD)
    
    sftp = ssh.open_sftp()
    sftp.put('index.html', REMOTE_PATH) # 覆盖服务器上的 index.html
    sftp.close()
    ssh.close()

# 假设这里是你抓取到的 AI 资讯
latest_ai_news = "1. GPT-5 灰度测试开启...\n2. NVIDIA 发布新一代 GPU..." 
update_html(latest_ai_news)
upload_to_vps()
