"""
用来自动化生成latex文档，将代码文件写入latex文档，批量生成图像代码等
"""
import os
import re

print('正在将代码文件写入tex文档')
content = '打开代码文件出错，请检查'
with open('./DisparityMap.py', 'r') as f:
    content = f.read()

with open('../doc/code.tex', 'w') as f:
    f.writelines([
        '\\begin{lstlisting}[language=Python]',
        content,
        '\n\\end{lstlisting}'
    ])

print('写入成功')

print('正在批量生成图片代码')
result_dir = './result/'
subfigs = []

def f2int(str):
    return [int(s) for s in str.replace('.png', '').split('_')]

def cmp_fn(key1):
    [n1, b1] = f2int(key1)
    return (n1 * 1000 + b1)

dirs = filter(lambda x: re.match(r'\d+_\d+\.png', x), os.listdir(result_dir))
dirs = [[f, cmp_fn(f)] for f in dirs]
dirs = sorted(dirs, key=lambda x: x[1])

for f in dirs:
    f = f[0]
    # 过滤掉不符合条件的数据
    [n, b] = f2int(f)
    subfigure = '\n'.join([
        '\\subfigure[$N_d=%d, S_b=%d$] {'%(n, b),
        '    \\centering',
        '    \\includegraphics[width=3.2cm]{../code/result/%s}'%f,
        '}'
    ])
    subfigs.append(subfigure)


print('正在将图片生成代码写入文件')

with open('../doc/image.tex', 'w') as f:
    f.writelines([
        '\\begin{figure}\centering',
        '\n'.join(subfigs),
        '\caption{不同参数对结果的影响}',
        '\label{bigfig}',
        '\\end{figure}'
    ])

print('完成')
