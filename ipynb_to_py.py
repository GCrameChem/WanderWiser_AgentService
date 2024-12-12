# 将ipynb转为python文件，调用此函数即可
# convert_ipynb_to_py('your_notebook.ipynb', 'your_notebook.py')

import json

def convert_ipynb_to_py(ipynb_file, py_file):
    with open(ipynb_file, 'r',encoding='utf-8') as f:
        notebook = json.load(f)

    with open(py_file, 'w',encoding='utf-8') as f:
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                f.write(''.join(cell['source']) + '\n\n')


convert_ipynb_to_py('agent1.ipynb', 'CenterAgent_main.py')