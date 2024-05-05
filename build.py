import subprocess
import shutil
import os


def run_command(command, cwd):
    subprocess.run(command, cwd=cwd, shell=True, check=True)


def move_files(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.move(source_dir, dest_dir)


# cd到ui文件夹并运行pnpm命令
ui_dir = './ui'
build_command = 'pnpm run build'
run_command(build_command, cwd=ui_dir)

# 移动build好的内容到目标文件夹
build_dir = './ui/dist'
css_dir = os.path.join(build_dir, 'css')
js_dir = os.path.join(build_dir, 'js')
index_html = os.path.join(build_dir, 'index.html')

static_dir = './meow/web/static'
templates_dir = './meow/web/templates'

# 删除旧的静态文件夹中的内容
old_css_dir = os.path.join(static_dir, 'css')
old_js_dir = os.path.join(static_dir, 'js')
if os.path.exists(old_css_dir):
    shutil.rmtree(old_css_dir)
if os.path.exists(old_js_dir):
    shutil.rmtree(old_js_dir)

# 移动新的静态文件和模板文件
move_files(css_dir, os.path.join(static_dir, 'css'))
move_files(js_dir, os.path.join(static_dir, 'js'))
shutil.move(index_html, os.path.join(templates_dir, 'index.html'))
