import pdfplumber
import re
import glob
import os
import hashlib

def get_file_hash(file_path):
    """计算文件的哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_duplicate_files(folder_path):
    """查找重复文件"""
    file_hash_dict = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            if file_hash in file_hash_dict:
                file_hash_dict[file_hash].append(file_path)
            else:
                file_hash_dict[file_hash] = [file_path]
    
    duplicates = [file_list for file_list in file_hash_dict.values() if len(file_list) > 1]
    return duplicates

def extract_amount_from_invoice(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # 使用正则表达式查找金额
            amounts = re.findall(r'\b\d+\.\d{2}\b', text)
            # print(amounts)
            if amounts:
                # 假设发票中只有一个金额，返回最后一个找到的金额
                return amounts[-1]
    return None
    
def collect_invoice_class(pdf_files, keywords):
    keyword_counts = {keyword: 0 for keyword in keywords}
    
    for pdf_file in pdf_files:
        with pdfplumber.open(pdf_file) as pdf:
            text = pdf.pages[0].extract_text()
            flag = False
            for keyword in keywords:
                if keyword in text:
                    keyword_counts[keyword] += 1
                    flag = True
                    break
            if flag is False:
                print(f"New class: {pdf_file}")

    return keyword_counts

# 发票路径
folder_path = './'

# 发票金额字典
invoice_amounts = {}

# 要统计的多个关键词
keywords = ["汽油", "柴油", "餐饮", "运输服务", "通信设备"]


def main():
    # 先检查发票有没有重复的，有的话不计算，需要先去重
    duplicate_files = find_duplicate_files(folder_path)
    if duplicate_files:
        print("发现重复的发票文件:")
        for files in duplicate_files:
            print("重复文件组:")
            for file in files:
                print(file)
    else:
        print("没有发现重复的发票文件\n")
        
        # PDF文件列表
        pdf_files = glob.glob("./*.pdf")
        # print(pdf_files, len(pdf_files))
        for item in pdf_files:
            # 计算金额
            amount = extract_amount_from_invoice(item)                  
            if amount:
                invoice_amounts[item] = float(amount)
                # print(f"{item}: {amount}\n")
            else:
                print(f"未找到金额: {item}\n")
        # 按金额排序输出
        sorted_invoices = sorted(invoice_amounts.items(), key=lambda item: item[1], reverse=True)    
        for invoice, amount in sorted_invoices:
            print(f"{invoice}: {amount}")
            
        # 计算明细
        print("分类明细如下：")
        class_result = collect_invoice_class(pdf_files, keywords)
        for key, value in class_result.items():
            print(f"{key}类: {value}")
        print("分类合计:", sum(class_result.values()))
            
        print(f"当前发票数量为：{len(pdf_files)}，总金额为： {sum(invoice_amounts.values())}元")
        
    input("Press Enter to exit...")
 
 
if __name__ == "__main__":
    main()

