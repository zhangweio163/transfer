import requests


def test_upload():
    print("开始测试，接口响应慢，请耐心等待")
    # baseUrl = "http://www.lovezdy.com:8000"
    baseUrl = "http://127.0.0.1:8000"
    urI = "/upload_and_translate/"
    files = {'file': ('sample.pdf', open('/htmlDemo/斯坦福小镇：生成式人类行为交互模拟体.pdf', 'rb'), 'application/pdf')}
    headers = {'Authorization': 'Bearer 1437213b-6ea4-4007-bce1-c8c91fa1c317'}
    response = requests.post(baseUrl + urI, params={"start": 0, "end": 1}, files=files, headers=headers)
    if response.status_code == 200:
        with open('downloaded_file.pdf', 'wb') as f:
            f.write(response.content)
        f.close()
        print("File downloaded successfully.")
    else:
        print("Error:", response.json())


if __name__ == "__main__":
    test_upload()
