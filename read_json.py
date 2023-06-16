import jsonlines
import pandas as pd

# 讀取第一個 JSONL 檔案
data1 = []
with open('file1.jsonl', 'r') as f1:
    for line in jsonlines.Reader(f1):
        data1.append(line)

# 讀取第二個 JSONL 檔案
data2 = []
with open('file2.jsonl', 'r') as f2:
    for line in jsonlines.Reader(f2):
        data2.append(line)

# 合併兩個資料列表
merged_data = data1 + data2

# 將合併的資料轉換為 DataFrame
df = pd.DataFrame(merged_data)
