import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class ArticleClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
        self.categories = []
    
    def train(self, texts, labels):
        """
        训练分类模型
        :param texts: 文章文本列表
        :param labels: 对应标签列表
        """
        self.categories = sorted(list(set(labels)))
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
    
    def predict(self, text):
        """
        预测文章类别
        :param text: 文章文本
        :return: 预测类别
        """
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]
    
    def save_model(self, model_path):
        """保存模型到文件"""
        with open(model_path, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'model': self.model,
                'categories': self.categories
            }, f)
    
    def load_model(self, model_path):
        """从文件加载模型"""
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
            self.vectorizer = data['vectorizer']
            self.model = data['model']
            self.categories = data['categories']

# 示例分类体系
SAMPLE_CATEGORIES = {
    'AI': '人工智能',
    '5G': '5G通信',
    'CHIP': '半导体芯片',
    'EV': '电动汽车',
    'OTHER': '其他科技'
}