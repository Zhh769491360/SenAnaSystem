import itertools
import json
import os
import pickle
import random
import re
import subprocess
import time

import jieba
import requests
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from lxml import etree
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.linear_model import LogisticRegression

# 改变时间输出格式
def changeTimeFormat(num):
    h = num // 3600
    m = (num - 3600 * h) // 60
    s = num - 3600 * h - 60 * m

    if h > 0:
        return str(h) + "h " + str(m) + "m " + str(s) + "s"
    elif m > 0:
        return str(m) + "m " + str(s) + "s"
    else:
        return str(s) + "s"


# 删除停用词
def deleteStopWords(stopwords, l):
    l_2 = []
    for i in range(len(l)):
        l_3 = []
        for j in range(len(l[i])):
            if l[i][j] not in stopwords:
                l_3.append(l[i][j])
        if len(l_3) > 0:
            l_2.append(l_3)

    return l_2


# 时间
class myThreadTime(QThread):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

    # 处理业务逻辑
    def run(self):
        self.alive = True
        while self.alive:
            try:
                data = QDateTime.currentDateTime()
                nowTime = data.toString("yyyy-MM-dd hh:mm:ss")
                self.update_date.emit(str(nowTime))  # 通过sleep(1),每秒发射一个信号
                time.sleep(1)
            except:
                continue


# 爬取时间
class myThreadSpiderTime(QThread):
    update_date = pyqtSignal(str)
    num = 0

    def run(self):
        self.alive = True
        while self.alive:
            try:
                self.num += 1
                self.update_date.emit(str(changeTimeFormat(int(self.num))))
                time.sleep(1)
            except:
                continue


# 爬取数据时的小人动图
class myThreadImg(QThread):
    update_img = pyqtSignal(str)
    num = 0

    def run(self):
        self.alive = True  # 控制该线程的存活
        while self.alive:
            try:
                self.num = (self.num + 1) % 6
                self.update_img.emit(str(self.num))
                time.sleep(0.1)
            except:
                continue


# 获取代理ip
class myThreadSpiderIP(QThread):
    update_str = pyqtSignal(str)
    update_int = pyqtSignal(int)
    alive = True
    num = 0

    def get_all_proxy(self):
        url = 'http://www.xicidaili.com/nn/1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.text)
        ip = html.xpath('//table[@id="ip_list"]/tr/td[2]/text()')
        port = html.xpath('//table[@id="ip_list"]/tr/td[3]/text()')
        proxy_list = []
        if len(ip) == 0:
            self.update_str.emit("请联网后再进行爬取！")
        else:
            self.update_str.emit("即将尝试" + str(len(ip)) + "个ip")
        for i in range(0, len(ip)):
            proxy_str = 'https://' + ip[i] + ':' + port[i]
            proxy_list.append(proxy_str)
        return proxy_list

    def check_all_proxy(self, proxy_list):
        valid_proxy_list = []
        for proxy in proxy_list:
            url = 'https://www.baidu.com/'
            proxy_dict = {
                'https': proxy
            }
            try:
                start_time = time.time()
                response = requests.get(url, proxies=proxy_dict, timeout=5)
                if self.alive == False:
                    break
                if response.status_code == 200:
                    end_time = time.time()
                    self.update_str.emit('代理可用：' + proxy)
                    # time.sleep(0.1)
                    self.update_str.emit('耗时:{:.4f} s'.format(end_time - start_time))
                    if end_time - start_time < 1:
                        valid_proxy_list.append("{#ip#:#" + proxy + "#}")
                else:
                    self.update_str.emit('代理超时')

            except:
                if self.alive == False:
                    break
                self.update_str.emit('代理不可用-------->' + proxy)

            finally:
                self.num += 1
                self.update_int.emit(self.num)
                if self.alive == False:
                    break

        return valid_proxy_list

    def run(self):
        while self.alive:
            try:
                proxy_list = self.get_all_proxy()
                valid_proxy_list = self.check_all_proxy(proxy_list)
                if self.alive:
                    result = str(valid_proxy_list).replace("'", "").replace("#", '"')
                    self.update_str.emit('--' * 25)
                    self.update_str.emit('爬取完成!')
                    self.update_str.emit("已添加代理ip:" + result)
                    f = open("./SenAnaSystem/json/ip.json", "w", encoding="utf-8")
                    f.write(result)
                    f.close()
                    self.alive = False
                    self.num = 0
            except Exception as e:
                print(e)
            finally:
                self.num = 0


# 获取电影id
class myThreadSpiderGetId(QThread):
    moviename = ""
    alive = True

    def setMovieName(self, movieName):
        self.moviename = movieName

    def run(self):
        while self.alive:
            try:
                print(self.moviename)
                self.p = subprocess.Popen("scrapy crawl get_movie_id_spider -a movieName=" + self.moviename)
                self.p.wait()
                print("close id")
                self.returncode = self.p.returncode
                print(self.returncode)
                self.p.kill()
                self.alive = False
                print(self.alive)
            except Exception as e:
                print(e)


# 获取电影长评
class myThreadSpiderLong(QThread):
    alive = True

    def run(self):
        while self.alive:
            try:
                self.p = subprocess.Popen("scrapy crawl comment_long_spider")
                self.p.wait()
                print("close long")
                self.returncode = self.p.returncode
                print(self.returncode)
                self.p.kill()
                self.alive = False
                print(self.alive)
            except Exception as e:
                print(e)


# 获取电影短评
class myThreadSpiderShort(QThread):
    alive = True

    def run(self):
        while self.alive:
            try:
                self.p = subprocess.Popen("scrapy crawl comment_short_spider")
                self.p.wait()
                print("close short")
                self.returncode = self.p.returncode
                print(self.returncode)
                self.p.kill()
                self.alive = False
                print(self.alive)
            except Exception as e:
                print(e)


# 控制电影评论数据的爬取
class myThreadSpiders(QThread):
    update_str = pyqtSignal(str)
    moviename = ""
    alive = True
    data = ""
    getId = myThreadSpiderGetId()
    getCommentLong = myThreadSpiderLong()
    getCommentShort = myThreadSpiderShort()

    def setMovieName(self, movieName):
        self.moviename = movieName

    def run(self):

        while self.alive:
            try:
                self.getId.setMovieName(self.moviename)
                self.getId.alive = True
                self.getId.start()
                self.num = 0
                while self.getId.alive:
                    self.num += 1
                    time.sleep(1)
                    if self.num > 300:  # 30s后还没获取到电影id，说明ip异常
                        self.alive = False

                    try:
                        if self.alive == False:
                            if self.getId.alive:
                                self.getId.p.kill()
                            break
                        else:
                            continue
                    except Exception as e:
                        print(e)
                        break

                if self.alive:
                    f = open("SenAnaSystem/json/movie_id.json", "r", encoding="utf-8")
                    self.data = f.read()
                    f.close()
                    print("main:" + self.data)

                    if self.data != "":
                        self.update_str.emit("成功获取电影id!")
                        self.update_str.emit("正在爬取影评内容......请耐心等待")
                        if not os.path.exists("./SenAnaSystem/json//" + self.moviename + "//"):
                            os.mkdir("./SenAnaSystem/json//" + self.moviename + "//")

                        f = open("SenAnaSystem/json/movie_name.json", "w", encoding="utf-8")
                        content = json.dumps(dict({"movieName": self.moviename}), ensure_ascii=False)
                        f.write(content)
                        f.close()

                        self.getCommentLong.alive = True
                        self.getCommentLong.start()
                        self.getCommentShort.alive = True
                        self.getCommentShort.start()

                        while self.getCommentLong.alive or self.getCommentShort.alive:
                            try:
                                if self.alive == False:
                                    print("False")
                                    if self.getCommentLong.alive:
                                        self.getCommentLong.p.kill()
                                    if self.getCommentShort.alive:
                                        self.getCommentShort.p.kill()
                                    break
                                else:
                                    continue
                            except Exception as e:
                                print(e)
                                break
                        print("跳出while")
                        self.update_str.emit("{}电影评论爬取完毕！".format(self.moviename))
                        self.update_str.emit("success")
                    else:
                        self.update_str.emit("error")
                else:
                    self.update_str.emit("error")

            except Exception as e:
                self.update_str.emit("{}电影评论爬取完毕！".format(self.moviename))
                self.update_str.emit("success")

            finally:
                self.alive = False
                self.moviename = ""
                self.data = ""


# 数据训练、测试
class myThreadTrainTest(QThread):
    update_str = pyqtSignal(str)
    key = -1

    folder = ""
    file1 = ""
    file2 = ""
    pos_num = 0
    neg_num = 0
    classifier_name = ""
    movie_list = []
    pos_review = []  # 积极数据
    neg_review = []  # 消极数据
    best_words = []
    # best_pos = []
    # best_neg = []
    test = []  # 测试集
    word_scores_pos = {}
    word_scores_neg = {}
    feature_num = 2000
    bigram_num = 3000
    test_features = []
    cla = 0

    # 1.载入训练数据集
    def load_data(self):

        f = open(self.folder + "/Pos.pkl", "rb")
        self.pos_review = pickle.load(f)
        f.close()

        f = open(self.folder + "/Neg.pkl", "rb")
        self.neg_review = pickle.load(f)
        f.close()

        self.update_str.emit("Tip:积极评论[" + str(len(self.pos_review))
                             + "]条  消极评论["
                             + str(len(self.neg_review)) + "]条")

    # 2.1.2 计算整个语料里面每个词和双词搭配的信息量
    def create_word_bigram_scores(self):
        posdata = self.pos_review  # [['我','是个']]
        negdata = self.neg_review

        posWords = list(itertools.chain(*posdata))  # ['我','是个'] 单词
        negWords = list(itertools.chain(*negdata))

        # print(posWords)
        # print(negWords)
        # time.sleep(100)
        bigram_finder = BigramCollocationFinder.from_words(posWords)  # 把词列表变为双词搭配
        posBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, self.bigram_num)  # 双词
        bigram_finder = BigramCollocationFinder.from_words(negWords)
        negBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, self.bigram_num)

        # 词和双词搭配
        pos = posWords + posBigrams
        neg = negWords + negBigrams

        word_fd = FreqDist()
        cond_word_fd = ConditionalFreqDist()

        for word in pos:
            word_fd[word] += 1
            cond_word_fd["pos"][word] += 1
        for word in neg:
            word_fd[word] += 1
            cond_word_fd["neg"][word] += 1

        pos_word_count = cond_word_fd['pos'].N()
        neg_word_count = cond_word_fd['neg'].N()
        print(pos_word_count)
        print(neg_word_count)

        total_word_count = pos_word_count + neg_word_count

        for word, freq in word_fd.items():  # freq表示数量
            pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count),
                                                   total_word_count)  # 计算积极词的卡方统计量
            neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count),
                                                   total_word_count)
            # word_scores[word] = pos_score + neg_score
            self.word_scores_pos[word] = pos_score
            self.word_scores_neg[word] = neg_score

        # word + 值   {'a':100,('b','c'):200}

    # 2.2 根据信息量进行倒序排序，选择排名靠前的信息量的词
    def find_best_words(self):

        # best_vals = sorted(word_scores.items(), key=lambda w_s: w_s[1], reverse=True)[:number]  # 把词按信息量倒序排序。number是特征的维度，是可以不断调整直至最优的
        best_vals_pos = sorted(self.word_scores_pos.items(), key=lambda w_s: w_s[1], reverse=True)[
                        :int(self.feature_num)]
        best_vals_neg = sorted(self.word_scores_neg.items(), key=lambda w_s: w_s[1], reverse=True)[
                        :int(self.feature_num)]
        best_vals = best_vals_pos + best_vals_neg
        # print(best_vals)       #[('a', 100), ('b', 200)]
        # for i in range(len(best_vals)):
        #     print(best_vals[i])
        self.best_words = set([w for w, s in best_vals])

    # 2.3 把选出的这些词作为特征（这就是选择了信息量丰富的特征）
    def best_word_features(self, words, bestWords):
        return dict([(word, True) for word in words if word in bestWords])

    # 3.3 赋予类标签
    # 3.3.1 积极
    def pos_features(self):
        posFeatures = []
        for i in self.pos_review:
            posWords = [self.best_word_features(i, self.best_words), 'pos']  # 为积极文本赋予"pos"
            posFeatures.append(posWords)
        return posFeatures

    # 3.3.2 消极
    def neg_features(self):

        negFeatures = []
        for j in self.neg_review:
            negWords = [self.best_word_features(j, self.best_words), 'neg']  # 为消极文本赋予"neg"
            negFeatures.append(negWords)
        return negFeatures

    # 5.3 把分类器存储下来（存储分类器和前面没有区别，只是使用了更多的训练数据以便分类器更为准确）
    def store_classifier(self):
        self.pos_review = self.pos_review[:self.pos_num]
        self.neg_review = self.neg_review[:self.neg_num]
        self.create_word_bigram_scores()
        if self.key == 0:
            return
        self.find_best_words()
        if self.key == 0:
            return
        posFeatures = self.pos_features()  # 将训练集中符合best_words的词赋予标签
        negFeatures = self.neg_features()
        trainSet = posFeatures + negFeatures
        if self.key == 0:
            return

        if self.cla == 0:
            choice_classifier = SklearnClassifier(BernoulliNB())
        elif self.cla == 1:
            choice_classifier = SklearnClassifier(MultinomialNB())
        elif self.cla == 2:
            choice_classifier = SklearnClassifier(LogisticRegression())
        elif self.cla == 3:
            choice_classifier = SklearnClassifier(SVC())
        elif self.cla == 4:
            choice_classifier = SklearnClassifier(LinearSVC())
        elif self.cla == 5:
            choice_classifier = SklearnClassifier(NuSVC())

        choice_classifier.train(trainSet)

        if self.classifier_name != "":
            output = open('classifiers/' + self.classifier_name + '.pkl', 'wb')
            pickle.dump(choice_classifier, output)  # 存储训练结果
            output.close()
            f = open("classifiers/" + self.classifier_name + "_bestWords.text", "w", encoding="utf_8")
            f.write(str(self.best_words))
            f.close()
        else:
            t = time.localtime(int(time.time()))
            name = time.strftime("%Y%m%d%H%M%S", t)
            output = open('classifiers/' + name + '.pkl', 'wb')
            pickle.dump(choice_classifier, output)  # 存储训练结果
            output.close()
            f = open("classifiers/" + name + "_bestWords.text", "w", encoding="utf_8")
            f.write(str(self.best_words))
            f.close()

    # 6 使用分类器进行分类，并给出概率值
    # 6.1 把文本变为特征表示的形式
    def transfer_text(self):
        f = open(self.file1, "rb")
        self.test = pickle.load(f)
        f.close()

        f = open("classifiers/" + self.file2.split("/")[-1].split(".")[0] + "_bestWords.text", "r", encoding="utf_8")
        bestWords = f.read()
        f.close()

        def extract_features(data):
            feat = []
            for j in data:
                feat.append(self.best_word_features(j, bestWords))
            return feat

        self.test_features = extract_features(self.test)  # 把文本转化为特征表示的形式
        if len(self.test_features) == 0:
            self.key = 0

    # 6.2 对文本进行分类，给出概率值
    def comment_test(self):
        if self.key == 0:
            return
        output = open(self.file2, 'rb')
        clf = pickle.load(output)  # 载入分类器
        output.close()
        pred = clf.prob_classify_many(self.test_features)  # 该方法是计算分类概率值的
        t = time.localtime(int(time.time()))
        name = time.strftime("%Y%m%d%H%M%S", t)
        p_file = open('result/test_result_' + name + '.txt', 'w')  # 把结果写入文档
        self.update_str.emit("result&" + name)

        pos_Num = 0
        neg_Num = 0

        for i in pred:
            if self.key == 0:
                return
            if i.prob('pos') > i.prob('neg'):
                pos_Num += 1
                p_file.write(str(pos_Num + neg_Num) + '|' + str(int(round(i.prob('pos') * 100))) + '|' + str(
                    int(round(i.prob('neg') * 100))) + '|' + 'Pos' + '\n')
            else:
                neg_Num += 1
                p_file.write(str(pos_Num + neg_Num) + '|' + str(int(round(i.prob('pos') * 100))) + '|' + str(
                    int(round(i.prob('neg') * 100))) + '|' + 'Neg' + '\n')
        p_file.close()
        total = pos_Num + neg_Num
        self.update_str.emit(
            "所测试的评论中，积极评论占{:.2f}%  消极评论占{:.2f}%".format((pos_Num * 100 / total), (neg_Num * 100 / total)))

    def run(self):
        self.alive = True
        while self.alive:
            try:
                if self.key == 1:
                    self.pos_review = []
                    self.neg_review = []
                    start = time.perf_counter()
                    self.load_data()
                    end = time.perf_counter()
                    self.update_str.emit("载入完成! 用时{:.2f}s".format(end - start))
                    self.key = 0
                elif self.key == 2:
                    start = time.perf_counter()
                    self.store_classifier()
                    end = time.perf_counter()
                    self.folder = ""
                    self.pos_num = 0
                    self.neg_num = 0
                    self.classifier_name = ""
                    self.movie_list = []
                    self.pos_review = []
                    self.neg_review = []
                    self.best_words = []
                    self.word_scores_pos = {}
                    self.word_scores_neg = {}
                    self.feature_num = 1500
                    self.bigram_num = 3000
                    if self.key == 2:
                        self.key = 0
                        self.update_str.emit("训练完成！ 用时{:.2f}s".format(end - start))
                    else:
                        self.key = 0
                        self.update_str.emit("训练已停止!")

                elif self.key == 3:
                    start = time.perf_counter()
                    self.transfer_text()
                    if self.key == 3:
                        self.comment_test()
                    end = time.perf_counter()
                    self.test = []
                    self.file1 = ""
                    self.file2 = ""
                    self.moto_features = []

                    if self.key == 3:
                        self.key = 0
                        self.update_str.emit("测试完成！ 用时{:.2f}s".format(end - start))
                    else:
                        self.key = 0
                        self.update_str.emit("测试已停止!")
                else:
                    continue

            except Exception as e:
                self.update_str.emit("出错:" + e + " 请重新选择文件或者相关配置参数!")


# 数据分离
class myThreadSeparate(QThread):
    update_str = pyqtSignal(str)
    key = -1

    folder = ""
    train_pos_num = 0
    train_neg_num = 0
    test_pos_num = 0
    test_neg_num = 0
    movie_list = []
    pos_review = []  # 积极数据
    neg_review = []  # 消极数据

    # 1.载入训练数据集
    def load_data(self):
        jieba.del_word(" ")
        # print(self.movie_list)
        for j in self.movie_list:
            f = open(self.folder + j + "/comment_short_neg.json", "r", encoding="utf-8")
            content_short_neg = json.loads(f.read())
            f.close()
            f = open(self.folder + j + "/comment_long_neg.json", "r", encoding="utf-8")
            content_long_neg = json.loads(f.read())
            f.close()
            for i in range(len(content_short_neg)):
                self.neg_review.append(jieba.lcut(
                    re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",
                           content_short_neg[i]["commentNeg"])))
            for i in range(len(content_long_neg)):
                self.neg_review.append(jieba.lcut(
                    re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",
                           content_long_neg[i]["commentNeg"])))

            f = open(self.folder + j + "/comment_short_pos.json", "r", encoding="utf-8")
            content_short_pos = json.loads(f.read())
            f.close()
            f = open(self.folder + j + "/comment_long_pos.json", "r", encoding="utf-8")
            content_long_pos = json.loads(f.read())
            f.close()
            for i in range(len(content_short_pos)):
                self.pos_review.append(jieba.lcut(
                    re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",
                           content_short_pos[i]["commentPos"])))
            for i in range(len(content_long_pos)):
                self.pos_review.append(jieba.lcut(
                    re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",
                           content_long_pos[i]["commentPos"])))

        stopwords = []
        f = open("./stopwords/stopwords.txt", "r", encoding="utf-8")
        content = f.readline()
        while content != "":
            stopwords.append(content)
            content = f.readline()
        f.close()

        self.pos_review = deleteStopWords(stopwords, self.pos_review)
        self.neg_review = deleteStopWords(stopwords, self.neg_review)

        self.update_str.emit("Tip:积极评论[" + str(len(self.pos_review))
                             + "]条  消极评论["
                             + str(len(self.neg_review)) + "]条")

    def separate_data(self):
        name = self.folder.split("/")[-1]
        if name == "":
            name = self.folder.split("/")[-2]
        if not os.path.exists("./train//" + name + "//"):
            os.mkdir("./train//" + name + "//")
        if not os.path.exists("./test//" + name + "//"):
            os.mkdir("./test//" + name + "//")
        random.shuffle(self.pos_review)
        random.shuffle(self.neg_review)
        f = open("./train/" + name + "/Pos.pkl", "wb")
        pickle.dump(self.pos_review[:self.train_pos_num], f)
        f.close()

        f = open("./train/" + name + "/Neg.pkl", "wb")
        pickle.dump(self.neg_review[:self.train_neg_num], f)
        f.close()

        f = open("./test/" + name + "/Pos.pkl", "wb")
        pickle.dump(self.pos_review[self.train_pos_num:self.test_pos_num + self.train_pos_num], f)
        f.close()

        f = open("./test/" + name + "/Neg.pkl", "wb")
        pickle.dump(self.neg_review[self.train_neg_num:self.test_neg_num + self.train_neg_num], f)
        f.close()

    def run(self):
        self.alive = True
        while self.alive:
            try:
                if self.key == 1:
                    self.pos_review = []
                    self.neg_review = []
                    start = time.perf_counter()
                    self.load_data()
                    end = time.perf_counter()
                    self.update_str.emit("检测完成! 用时{:.2f}s".format(end - start))
                    self.key = 0
                elif self.key == 2:
                    start = time.perf_counter()
                    self.separate_data()
                    end = time.perf_counter()
                    self.update_str.emit("数据分离完成! 用时{:.2f}s".format(end - start))
                    self.key = 0
                else:
                    continue

            except Exception as e:
                self.update_str.emit("出错:" + e + " 请重新选择文件或者相关配置参数!")


# 实际应用
class myThreadApplication(QThread):
    alive = True
    update_str = pyqtSignal(str)

    key = -1
    folder = ""
    movie_list = []
    pos_review = []
    neg_review = []
    all_review = []
    file = ""
    test_feature = []

    def best_word_features(self, words, bestWords):
        return dict([(word, True) for word in words if word in bestWords])

    def load_data(self):
        for j in self.movie_list:
            f = open(self.folder + j + "/comment_short_neg.json", "r", encoding="utf-8")
            content_short_neg = json.loads(f.read())
            f.close()
            f = open(self.folder + j + "/comment_long_neg.json", "r", encoding="utf-8")
            content_long_neg = json.loads(f.read())
            f.close()
            for i in range(len(content_short_neg)):
                self.neg_review.append(jieba.lcut(
                    re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",
                           content_short_neg[i]["commentNeg"])))
            for i in range(len(content_long_neg)):
                self.neg_review.append(jieba.lcut(
                    re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",
                           content_long_neg[i]["commentNeg"])))

            f = open(self.folder + j + "/comment_short_pos.json", "r", encoding="utf-8")
            content_short_pos = json.loads(f.read())
            f.close()
            f = open(self.folder + j + "/comment_long_pos.json", "r", encoding="utf-8")
            content_long_pos = json.loads(f.read())
            f.close()
            for i in range(len(content_short_pos)):
                self.pos_review.append(jieba.lcut(
                    re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",
                           content_short_pos[i]["commentPos"])))
            for i in range(len(content_long_pos)):
                self.pos_review.append(jieba.lcut(
                    re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",
                           content_long_pos[i]["commentPos"])))

        self.all_review = self.pos_review + self.neg_review

        stopwords = []
        f = open("./stopwords/stopwords.txt", "r", encoding="utf-8")
        content = f.readline()
        while content != "":
            stopwords.append(content)
            content = f.readline()
        f.close()

        self.all_review = deleteStopWords(stopwords, self.all_review)
        random.shuffle(self.all_review)

        if self.movie_list[0] == "":
            name = self.folder.split("/")[-1]
        else:
            name = self.folder.split("/")[-2]
        f = open("./test/" + name + ".pkl", "wb")
        pickle.dump(self.all_review, f)
        f.close()

        self.update_str.emit("分类评论共" + str(len(self.all_review)) + "条")

    def transfer_text(self):

        f = open("classifiers/" + self.file.split("/")[-1].split(".")[0] + "_bestWords.text", "r", encoding="utf_8")
        bestWords = f.read()
        f.close()

        def extract_features(data):
            feat = []
            for j in data:
                feat.append(self.best_word_features(j, bestWords))
            return feat

        self.test_features = extract_features(self.all_review)
        if len(self.test_features) == 0:
            self.key = 0

    def comment_test(self):

        if self.key == 0:
            return
        output = open(self.file, 'rb')
        clf = pickle.load(output)
        output.close()
        pred = clf.prob_classify_many(self.test_features)
        t = time.localtime(int(time.time()))
        name = time.strftime("%Y%m%d%H%M%S", t)
        p_file = open('result/test_result_' + name + '.txt', 'w')
        self.update_str.emit("result&" + name)

        pos_Num = 0
        neg_Num = 0

        for i in pred:
            if self.key == 0:
                return
            if i.prob('pos') > i.prob('neg'):
                pos_Num += 1
                p_file.write(str(pos_Num + neg_Num) + '|' + str(int(round(i.prob('pos') * 100))) + '|' + str(
                    int(round(i.prob('neg') * 100))) + '|' + 'Pos' + '\n')
            else:
                neg_Num += 1
                p_file.write(str(pos_Num + neg_Num) + '|' + str(int(round(i.prob('pos') * 100))) + '|' + str(
                    int(round(i.prob('neg') * 100))) + '|' + 'Neg' + '\n')
        p_file.close()
        total = pos_Num + neg_Num
        self.update_str.emit(
            "所分类的评论中，积极评论占{:.2f}%  消极评论占{:.2f}%".format((pos_Num * 100 / total), (neg_Num * 100 / total)))

    def run(self):
        while self.alive:
            try:
                if self.key == 1:
                    start = time.perf_counter()
                    self.load_data()
                    end = time.perf_counter()
                    self.update_str.emit("影评转换完成，用时{:.2f}s".format(end - start))
                    self.update_str.emit("开始进行影评分类......请耐心等待")
                    start = time.perf_counter()
                    self.transfer_text()
                    self.comment_test()
                    end = time.perf_counter()
                    self.update_str.emit("影评分类完成，用时{:.2f}s".format(end - start))
                    self.key = -1
                    self.pos_review = []
                    self.neg_review = []
                    self.all_review = []
                    self.test_feature = []
                    self.update_str.emit("end")
                else:
                    continue
            except Exception as e:
                print(e)


# 测试结果数据（表格形式）
class myThreadResultTable(QThread):
    alive = True
    name = ""
    commentAddress = ""
    condition = ""

    def run(self):
        while self.alive:
            try:
                self.p = subprocess.Popen(r"python myqttable.py " + self.name + " " + self.commentAddress + " " + self.condition)
                self.p.wait()
                self.p.kill()
                self.alive = False
            except Exception as e:
                print(e)


# 测试结果数据（图像形式）
class myThreadResultGraph(QThread):
    alive = True
    name = ""

    def run(self):
        while self.alive:
            try:
                self.p = subprocess.Popen(r"python mygraph.py " + self.name)
                self.p.wait()
                self.p.kill()
                self.alive = False
            except Exception as e:
                print(e)


