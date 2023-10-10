import os
import re
from utils import traverse_directory, search_dirs, exclude_dirs, base_dir
import logging

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    filename='output/rename_symbols.log',  # Specify the log file name
    filemode='w'  # Use 'w' to overwrite the file or 'a' to append
)

# Create a logger instance
logger = logging.getLogger(__name__)

def increment_name(name):
    result = []
    for char in name:
        if 'a' <= char <= 'z':
            if char == 'z':
                result.append('a')
            else:
                result.append(chr(ord(char) + 1))
        elif 'A' <= char <= 'Z':
            if char == 'Z':
                result.append('A')
            else:
                result.append(chr(ord(char) + 1))
        else:
            result.append(char)
    return ''.join(result)

def rename_class(file_path, old_class_name, new_class_name):
    f_in = open(file_path, 'r', encoding='utf-8', errors='ignore')
    lines = f_in.readlines()
    f_in.close()

    flag = False
    out_lines = []
    logger.info(f'{file_path}')
    pattern = r'(?:(?<=[^\w])|(?<=^))' + re.escape(old_class_name) + r'(?:(?=$)|(?=[^\w]))'
    for line in lines:
        if line.startswith('#include') or line.startswith('#import'):
            result = line
        else:
            result = re.sub(pattern, new_class_name, line)
            if result != line:
                flag = True
                logger.info(f'{line} ---- {result}')
        out_lines.append(result)
    
    if flag:
        f_out = open(file_path, 'w', encoding='utf-8')
        for line in out_lines:
            f_out.write(line)
        f_out.close()


def rename_function(file_path, old_function_name, new_function_name):
    if old_function_name.startswith('set') or old_function_name.startswith('get') or\
        old_function_name.startswith('Set') or old_function_name.startswith('Get'):
        return
    # 构建正则表达式，查找需要替换的函数名
    pattern = r'(?:(?<=[^\w])|(?<=^))' + re.escape(old_function_name) + r'(?:($)|(?=[^\w]))'
    
    # 使用正则表达式查找并替换函数名
    f_in = open(file_path, 'r', encoding='utf-8', errors='ignore')
    lines = f_in.readlines()
    f_in.close()

    logger.info(f'{file_path}')
    out_lines = []
    flag = False
    for line in lines:
        if line.startswith('#include') or line.startswith('#import'):
            result = line
        else:
            result = re.sub(pattern, new_function_name, line)
            if result != line:
                flag = True
                logger.info(f'{line} ---- {result}')
        out_lines.append(result)
    if flag:
        f_out = open(file_path, 'w', encoding='utf-8')
        for line in out_lines:
            f_out.write(line)
        f_out.close()


def read_symbols(file_path, output_set):
    f = open(file_path, 'r')
    for line in f:
        infos = line.split(' ')
        output_set.add(infos[1])
    f.close()


if __name__ == '__main__':
    class_set = set()
    read_symbols('output/class_symbols.txt', class_set)

    func_set = set()
    read_symbols('output/func_symbols.txt', func_set)

    valid_class_set = class_set - func_set
    valid_func_set = func_set - class_set

    sorted(valid_class_set, reverse=True)
    sorted(valid_func_set, reverse=True)
    
    print('rename class...')
    for cn in valid_class_set:
        logger.info(f'rename class {cn}')
        visit_rename = lambda file_path: rename_class(file_path, cn, increment_name(cn))
        for dir in search_dirs:
            traverse_directory(logger, base_dir + dir, ['.h', '.hpp', '.cpp', '.cc', '.mm', '.m'], visit_rename, '')
    print('rename function...')
    for fn in valid_func_set:
        logger.info(f'rename function {fn}')
        visit_rename = lambda file_path: rename_function(file_path, fn, increment_name(fn))
        for dir in search_dirs:
            traverse_directory(logger, base_dir + dir, ['.h', '.hpp', '.cpp', '.cc', '.mm', '.m'], visit_rename, '')        