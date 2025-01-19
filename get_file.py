import os
import shutil

def collect_word_files(source_dir, target_dir):
    # 确保目标文件夹存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    total_files = 0
    copied_files = 0

    # 遍历源文件夹及其子文件夹
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.docx') or file.endswith('.doc'):
                total_files += 1
                # 构建源文件和目标文件的完整路径
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)
                print(f"Processing: {source_file}......")

                # 如果目标文件已存在，修改文件名
                base, extension = os.path.splitext(target_file)
                counter = 1
                while os.path.exists(target_file):
                    target_file = f"{base}_{counter}{extension}"
                    counter += 1
                
                # 复制文件到目标文件夹
                shutil.copy2(source_file, target_file)
                copied_files += 1
                print(f"Copied: {source_file} to {target_file}")

    print(f"Total Word documents found: {total_files}")
    print(f"Total Word documents copied: {copied_files}")

# 使用示例
source_directory = './'
target_directory = '../汇总'
collect_word_files(source_directory, target_directory)