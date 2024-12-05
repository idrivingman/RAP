import os
import json
import pandas as pd

def process_files_to_excel(directory, output_excel):
    # 获取文件夹中的所有 .txt 文件
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    data = []

    for file_name in sorted(txt_files):  # 按文件名排序
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                # 解析 JSON 数据
                file_data = json.load(file)
                entry = file_data[-1]
                query = entry.get('query', '')
                traj = entry.get('traj', [])
                traj_all = "\n**********".join(traj)  # traj 的全部内容
                traj_last = traj[-1] if traj else ""  # traj 的最后一个元素
                data.append({'query': query, 'traj_all': traj_all, 'traj_last': traj_last})
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {file_name}: {e}")

    # 转换为 DataFrame
    df = pd.DataFrame(data, columns=['query', 'traj_all', 'traj_last'])

    # 写入到 Excel 文件
    df.to_excel(output_excel, index=False, engine='openpyxl')
    print(f"Data saved to {output_excel}")

# 示例用法
directory = "/Users/bytedance/o1_rap/RAP/logs/prontoqa_mcts_13B/2024-1204-1324"
output_excel = "/Users/bytedance/o1_rap/RAP/utils_lzq/processed_results.xlsx"
process_files_to_excel(directory, output_excel)
