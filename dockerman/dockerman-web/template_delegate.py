from jinja2 import Template
import shutil
import re


TMP = '/tmp/'
TEMPLATES = '../templates/'
JAVA_APP = 'java-app/'
PYTHON_APP = 'python-app/'

def new_image(id, type = PYTHON_APP):
    r = shutil.copytree(TEMPLATES + type, TMP + id, symlinks = False, ignore = None, ignore_dangling_symlinks = False, copy_function = shutil.copy2)
    return TMP + id

def _new_file(path, file):
    content = None
    with open(path + '/' + file, 'r') as f:
        content = f.read()
    return content


def template_file(path, file, **targets):
    print(f'templating {file} at {path} with {targets}')
    content = _new_file(path, file)
    t = Template(content)
    rendered_content = t.render(targets)
    with open(path + '/' + file, 'w') as f:
        f.write(rendered_content)

if __name__ == '__main__':
    print(template_file('/home/vlad/hambda/python-app/', 'app.py', endpoint = '/end', code = 'print(\"it works!\")\n    return None'))