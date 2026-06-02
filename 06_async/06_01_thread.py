from concurrent.futures import ThreadPoolExecutor

def download(url):
    print(f"开始下载: {url}")
    # 模拟 IO 操作
    import time; time.sleep(1)
    print(f"下载完成: {url}")

urls = ["www.baidu.com", "www.jd.com", "www.taobao.com"]

# 使用线程池并发下载-写法1
with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(download, urls)
    print(results)


# 使用线程池并发下载-写法2
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(download, url) for url in urls]
    for future in futures:
        print(future.result())




