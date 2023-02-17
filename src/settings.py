import platform

template_one = "template.html"

template_html_from = str()

if platform.system().lower() == 'windows':
    template_html_from = ".\\src\\static\\template\\" + template_one
elif platform.system().lower() == 'linux':
    template_html_from = "./src/static/template/" + template_one

