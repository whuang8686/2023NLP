#1
#讀進wiki資料集
import json
import pandas as pd
import os

# 資料夾路徑
folder_path = './wiki-pages'
from txtai.embeddings import Embeddings

# Create embeddings model, backed by sentence-transformers & transformers
embeddings = Embeddings({"path": "sentence-transformers/nli-mpnet-base-v2"})
# 儲存所有檔案資料的列表
df = pd.DataFrame()

# 讀取資料夾中的檔案

for filename in os.listdir(folder_path):
    if filename.endswith('.jsonl'):
        file_path = os.path.join(folder_path, filename)
        #file_path = os.path.join(folder_path, "wiki-test.jsonl")

        # 讀取 JSONL 檔案並存入 DataFrame
        filename_df = pd.read_json(file_path, lines=True)
        
        # 在 DataFrame 中新增一列，存放檔案名稱
        filename_df['filename'] = os.path.splitext(filename)[0]

        # 將讀取的 DataFrame 與主 DataFrame 進行合併
        df = pd.concat([filename_df,df], ignore_index=True)

        print(df.count())

#2
        answer_list = []

        for index, row in df.iterrows():

          if isinstance(row['lines'], str):
                mlines = row['lines'].split('\n')  # 將文本根據換行符拆分為行
                for line in mlines:
                        if line:
                           columns = line.split('\t')  # 將每行根據制表符拆分為欄
                           if columns[1] != "":
            #if row['id'] == "南大附中" or row['id'] == "信天翁科" or row['id']=="竇唯":
              # 要添加的數據
                                new_data = {'id': row['id'], 'lineno': columns[0] , 'text': columns[1]}
              #print(new_data)
                                answer_list.append(new_data) # 將欄添加到資料列表中


        answer_data =[]

        for item in answer_list:
                column_value = item['text']  # 假設欄位索引為 1
                answer_data.append(column_value)


#for item in answer_data:
#    print(item)

        embeddings.index([(uid, text, None) for uid, text in enumerate(answer_data)])
        embeddings.save("index_"+filename)
