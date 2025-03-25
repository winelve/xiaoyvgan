import requests
from lxml import html
import os

def fetch_image_url(url, xpath):
    """从指定URL和XPath提取图片URL"""
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.pixiv.net/'
    }
    
    try:
        # 发送请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析HTML
        tree = html.fromstring(response.content)
        
        # 使用XPath提取图片元素
        img_elements = tree.xpath(xpath)
        
        if not img_elements:
            print("未找到匹配的图片元素")
            return None
        
        # 获取图片的src属性
        img_url = img_elements[0].get('src')
        return img_url
        
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except Exception as e:
        print(f"解析错误: {e}")
        return None

def download_image(img_url, save_dir='./cmds/pixiv/download'):
    """下载图片"""
    if not img_url:
        return
    
    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.pixiv.net/'
    }
    
    try:
        # 下载图片
        response = requests.get(img_url, headers=headers)
        response.raise_for_status()
        
        # 从URL提取文件名
        filename = img_url.split('/')[-1]
        filepath = os.path.join(save_dir, filename)
        
        # 保存图片
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"成功下载: {filename}")
        
    except requests.RequestException as e:
        print(f"下载失败: {e}")

def main():
    # 目标网页URL（需要替换为实际URL）
    target_url = 'https://www.pixiv.net/artworks/128470225'  # 示例URL
    
    # 指定的XPath
    xpath = '/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/main/section/div[1]/div/figure/div[1]/div[1]/div'
    # 获取图片URL
    img_url = fetch_image_url(target_url, xpath)
    
    if img_url:
        # 下载图片
        download_image(img_url)

if __name__ == '__main__':
    main()