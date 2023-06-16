import jsonlines
import pandas as pd
import json

# 讀取第一個 JSONL 檔案
data = []

folder_path = './'

df_source = pd.read_json(folder_path+'/public_private_submission_template.jsonl', lines=True)
df_private = pd.read_json(folder_path+'/test.jsonl', lines=True)
df_public = pd.read_json(folder_path+'/test_public.jsonl', lines=True)
print(df_source)
print(df_private)
print(df_public)

#https://blog.csdn.net/weixin_43509263/article/details/90203694
for index_source, row_source in df_source.iterrows():
    #row_index = index_source
    for index, row in df_public.iterrows():
        if (row_source['id'] == row['id']):
           df_source.at[index_source,'predicted_label'] = row['predicted_label']
           df_source.at[index_source,'predicted_evidence'] = row['predicted_evidence']

    for index_2, row_2 in df_private.iterrows():
        if (row_source['id'] == row_2['id']):
           df_source.at[index_source,'predicted_label'] = row_2['predicted_label']
           df_source.at[index_source,'predicted_evidence'] = row_2['predicted_evidence']

#data_dict = df_source.to_dict()

df_source.to_json(folder_path+"/out.jsonl", orient='records', lines=True, force_ascii=False)
#with open(folder_path+"/out.jsonl", "w", encoding='utf-8') as f:
#     f.write(json.dumps(data_dict, ensure_ascii=False))
