#9產生test_data_result
import jsonlines
import json
import pandas as pd
import os
from txtai.embeddings import Embeddings


#part1
folder_path = './wiki-pages-em'
df = pd.DataFrame()

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

#print(df.head(100))
print(df.count())

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
              new_text = columns[1].replace("|", "")
              new_data = {'id': row['id'], 'lineno': columns[0] , 'text': new_text}
              #print(new_data)
              answer_list.append(new_data) # 將欄添加到資料列表中

answer_data =[]

for item in answer_list:
    column_value = item['text']  # 假設欄位索引為 1
    answer_data.append(column_value)

#9產生test_data

# 資料夾路徑


# 儲存所有檔案資料的列表
test_df = pd.DataFrame()

# 讀取資料夾中的檔案
folder_path = './'

file_path = os.path.join(folder_path, "private_test_data.jsonl")

# 讀取 JSONL 檔案並存入 DataFrame
test_df = pd.read_json(file_path, lines=True)
        

#print(df.head(100))
print(test_df.count())


test_query_data = []

for index,row in test_df.iterrows():
  test_query_data.append(row['claim'])
#part2

embeddings = Embeddings()
embeddings.load("./index-014")

# Run an embeddings search for each query
#for query in ("天衛三軌道在天王星內部的磁層，以《 仲夏夜之夢 》作者緹坦妮雅命名。", "信天翁科的活動範圍位於北冰洋以及南太平洋，牠的翼展可達到3.7米，是世界上現存的翼展最大的鳥類。", "南京大學附屬中學，從中國江蘇省遷移南京大學附屬中學，從中國江蘇省遷移", "離開黑豹樂隊後，著名中國音樂人竇唯的音樂風格擺脫過往的流行搖滾。", "wildlife", "asia", "lucky", "dishonest junk"):

#把結果寫到file
from datetime import datetime
result = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")


fp = open("./test_result_1.csv", mode='w')

lines = ['test_query','|','answer_data[uid]','|','score','|','answer_id','|','answer_lineno','|','datetime','\n']
fp.writelines(lines)

for test_query in test_query_data:
#for query in query_data:
    # Extract uid of first result
    # search result format: (uid, score)
    #uid = embeddings.search(query, 2)[0][0]
    #score = embeddings.search(query, 2)[0][1]

    # Print text
    #print("%-60s %s  %s" % (query, text_data[uid], score))
    get_result = embeddings.search(test_query,3)
    
    for item  in get_result:
        uid = item[0]
        score = item[1]

        #印出answer_list[]的結果
        for item2 in answer_list:
          if item2['text'] == answer_data[uid]:
              answer_id = item2['id']
              answer_lineno = item2['lineno']
        
              #print("%-60s %s %s  %s %s %s" % (query, query_evidence, answer_data[uid], score, answer_id, answer_lineno))
              lines = [test_query, '|',answer_data[uid],'|', str(score),'|', answer_id, '|',str(answer_lineno),'|',result,'\n']
              #print(lines)
              fp.writelines(lines)

fp.close()

"""


#part2
#組成output file

folder_path = './'

# 儲存所有檔案資料的列表
test_df = pd.DataFrame()

# 讀取資料夾中的檔案
file_path = os.path.join(folder_path, "public_test_data.jsonl")
file_path2 = os.path.join(folder_path, "test_result.csv")
# 讀取 JSONL 檔案並存入 DataFrame
test_out_df = pd.read_json(file_path, lines=True)
test_out2_df = pd.read_csv(file_path2, sep='|')
#print(test_out2_df.dtypes)
#print(test_out_df.count())
#print(test_out2_df.count())


test_out_list = []
evidence_list = []
pred_label = "SUPPORTS"
#data.append({"id": 22334, "predicted_label": "SUPPORTS", "predicted_evidence": [["樂山大佛", 3]]})

for index, row in test_out_df.iterrows():
      sub_evidence = []
      evidence_list = []
      for index2, row2 in test_out2_df.iterrows():
          if (row['claim'] == row2['test_query']):
              if row2['score'] >=0.9:
                new_item = [row2['answer_id'],row2['answer_lineno']]
                if len(sub_evidence) >=1:
                  if (new_item not in [item[:2] for item in sub_evidence]) & (any(item[0] == row2['answer_id'] for item in sub_evidence)): 
                    sub_evidence.append([row2['answer_id'],row2['answer_lineno']])
                else:
                  sub_evidence.append([row2['answer_id'],row2['answer_lineno']])

      if len(sub_evidence) == 0:
        sub_evidence = None
        pred_label = "NOT ENOUGH INFO"
      else:
        pred_label = "SUPPORTS"
        
      evidence_list.append(sub_evidence)
      test_out_list.append({"id": row['id'], "predicted_label": pred_label, "predicted_evidence": evidence_list})

print (test_out_list)

with jsonlines.open(folder_path+'test.jsonl', mode="w") as writer:
    for item in test_out_list:
        writer.write(item)

"""