import html


# Numeric Character Reference 数字实体引用
def convert(normal_text):
    return html.escape(normal_text, quote=False)
