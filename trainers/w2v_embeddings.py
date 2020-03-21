# -*-coding:utf-8 -*-

'''
@File       : w2v_embeddings.py
@Author      : TY Liu
@Date       : 2020/2/17
@Desc       :
'''

import gensim
from gensim.models import word2vec
import pandas as pd
import loguru


class Word2Vec:
    '''
    w2v词向量
    '''

    def __init__(self):
        '''
        初始化Word2Vec
        '''
        self.w2v_model = None

    def train(self, data, size=100, window=10, min_count=5, workers=4):
        '''
        训练词向量
        ----------
        data: 数据或路径，传入路径时需要对应数据中各词按空格分隔
        size: 词向量长度（默认100）
        window: 上下文窗口大小（默认5）
        min_count: 忽略出现次数小于min_count的词语（默认5）
        workers: 训练使用线程数（默认3）
        '''
        # 判断data是否是路径
        if isinstance(data, str):
            # 读取数据
            data = word2vec.LineSentence(data)
        # 训练模型
        logger.info("词向量训练开始...")
        logger.info("参数[size:{},windows:{},min_count:{},workers:{}]".format(size, window, min_count, workers))
        self.w2v_model = word2vec.Word2Vec(data,size=size,window=window,min_count=min_count,workers=workers)
        logger.info("训练完毕")

    def save_model(self, path):
        '''
        保存已训练好的词向量
        --------------------
        path: 保存模型的路径
        '''
        if self.w2v_model:
            self.w2v_model.save(path)
            logger.info("'{}'保存成功！".format(path))
        else:
            logger.info("词向量未训练！")

    def load_model(self, path):
        '''
        获取预先训练的词向量模型
        --------------------
        path: 保存模型的路径
        '''
        self.w2v_model = word2vec.Word2Vec.load(path)

    def get_similar(self, word):
        '''
        获取"近义词most_similar"
        ----------
        word: 目标词语
        '''
        if not self.w2v_model:
            logger.info("w2v模型不存在！")
        if word not in self.w2v_model.wv:
            logger.info("'{}' 不在词库中！".format(word))
        return self.w2v_model.wv.most_similar(word)

    def get_vec(self, words):
        '''
        获取词语对应向量
        ----------------
        words: 目标词列表
        '''
        if not self.w2v_model:
            logger.info("w2v模型不存在！")
        for word in words:
            # TODO 处理不在词库中的词语，返回全零或特定向量
            if word not in self.w2v_model.wv:
                logger.info("'{}' 不在词库中！".format(word))
                return None
        return self.w2v_model.wv[words]

    def evaluate_model(self, path, test_words):
        """
        评估不同参数下w2v_model的表现情况
        :return:
        """
        self.load_model(path)
        for word in test_words:
            try:
                logger.info(word + ": " + str(self.get_similar(word)))
            except Exception as e:
                pass


def function():

    # 1/ 不同参数的训练模型
    paras = [(100, 5), (100, 10), (200, 5), (200, 10), (300, 5), (300, 10)]
    data_path = "../data/combined_preprocess_data(re_stopwords).csv"
    for (size, window) in paras:
        w2v.train(data_path, size, window)
        logger.info(w2v.get_similar("向量"))
        model_path = "../outputs/word_vectors_s%d_w%d" % (size, window)
        w2v.save_model(model_path)

    # 2/ 评估不同模型的表现情况
    paras = [(100, 5), (100, 10), (200, 5), (200, 10), (300, 5), (300, 10)]
    test_words = ["北京", "华为", "自然语言处理", "神经网络", "孙杨", "感受视野", "噌吰", "新冠疫情", "向量", "矩阵"]
    logger.info("test words: " + str(test_words))
    logger.info("----------------------------")
    for (size, window) in paras:
        logger.info("model parameter: size={}, window={}".format(size, window))
        model_path = "../outputs/word_vectors_s%d_w%d" % (size, window)
        w2v.evaluate_model(model_path, test_words)
        logger.info("----------------------------")

    # 3/ 外部word2vec模型的测试结果
    test_words = ["北京", "华为", "自然语言处理", "神经网络", "孙杨", "感受视野", "噌吰", "新冠疫情", "向量", "矩阵"]
    logger.info("test words: " + str(test_words))
    logger.info("----------------------------")
    # model_path = "../outputs/word2Vec(combined_embedding300).bin"
    model_path = "../outputs/w2v(news_12g_baidubaike_20g_novel_90g_embedding_64).bin"

    # 加载bin格式的模型
    word2Vec_model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    for word in test_words:
        try:
            logger.info(word + ": " + str(word2Vec_model.most_similar(word)))
        except Exception as e:
            logger.info(e)


if __name__ == '__main__':

    # 设置日志输出
    logger = loguru.logger
    logger.add("../log/w2v/w2v_model_eveluation_{time}.log", encoding='utf-8')

    w2v = Word2Vec()

    function()

