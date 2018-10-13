"""
用来自动化生成latex文档，将代码文件写入latex文档，批量生成图像代码等
"""

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
