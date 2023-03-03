from urllib.parse import urlparse


# 分辨URL和路径: 判断一个字符串是否为URL
def is_url(string):
    result = urlparse(string)
    return all([result.scheme, result.netloc])


# 分辨URL和路径: 判断一个字符串是否为路径
def is_path(string):
    result = urlparse(string)
    return not all([result.scheme, result.netloc])
