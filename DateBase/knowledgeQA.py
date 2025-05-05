import json
import os

import pandas as pd
import numpy as np
import re
import random
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

from DeepSeekChat.deepseek_api import deepseek_chat

# data_path=r'jmu_data\output.json'
class KnowledgeQA:
    def __init__(self,
                 data_path: str = None,
                 model_name: str = 'uer/sbert-base-chinese-nli'):

        #自动定位默认路径
        if data_path is None:
            base_dir = os.path.dirname(__file__)
            data_path = os.path.join(base_dir, "jmu_data", "output.json")
        else:
            #若用户传入相对路径，转换成绝对路径
            data_path = os.path.abspath(data_path)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.df = self.load_data(data_path)
        self.category_vectors = self.build_category_vectors()

    #加载知识库
    def load_data(self, path: str):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        df = pd.DataFrame(data)
        df['encoded'] = df.apply(self.encode_content, axis=1)
        return df

    #去除HTML标签
    def clean_content(self, content: str):
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'http\S+', '', content)
        return content

    #对内容进行编码
    def encode_content(self, row):
        title = row['title']
        content = self.clean_content(row['content'])[:20]

        title_inputs = self.tokenizer(title, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
        content_inputs = self.tokenizer(content, return_tensors='pt', max_length=512, truncation=True, padding='max_length')

        with torch.no_grad():
            title_vec = self.model(**title_inputs).last_hidden_state.mean(dim=1).squeeze().numpy()
            content_vec = self.model(**content_inputs).last_hidden_state.mean(dim=1).squeeze().numpy()

        return 0.55 * title_vec + 0.45 * content_vec

    #构建标题分类向量字典
    def build_category_vectors(self):
        category_vectors = {}
        for category in self.df['title'].unique():
            vectors = self.df[self.df['title'] == category]['encoded'].tolist()
            category_vectors[category] = np.array(vectors)
        return category_vectors

    #构建用户问题向量字典
    def vectorize_question(self, question: str):
        inputs = self.tokenizer(question, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
        with torch.no_grad():
            return self.model(**inputs).last_hidden_state.mean(dim=1).squeeze().numpy()

    #从知识库检索内容
    def retrieve_background(self, question: str):
        question_vector = self.vectorize_question(question)
        scores = {
            cat: np.max(cosine_similarity([question_vector], vecs)[0])
            for cat, vecs in self.category_vectors.items()
        }
        top_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

        best_articles = []
        for cat, score in top_categories:
            if score > 0.5:
                idx = np.argmax(cosine_similarity([question_vector], self.category_vectors[cat])[0])
                best_article = self.df[self.df['title'] == cat].iloc[idx]['content']
                best_articles.append(best_article)

        return best_articles if best_articles else None

    #调用语言大模型
    def call_llm(self, question: str, background_list=None):
        if background_list:
            background = "\n\n".join(background_list)
            prompt = f'{question}，请你根据以下背景知识以及结合你的资料回答我的问题, 若背景知识不包含相关内容，则调用你自己的资料库，建议你的回答在100字以内,不需要用小括号标注回答字数：\n\n{background}'
        else:
            prompt = question
        return deepseek_chat(prompt)

    #传入用户问题
    def ask(self, question: str):
        background = self.retrieve_background(question)
        return self.call_llm(question, background)


if __name__ == "__main__":
    qa_bot = KnowledgeQA(data_path="jmu_data/output.json")

    question = "财务处电话是多少？"
    answer = qa_bot.ask(question)
    print("回答：", answer)
