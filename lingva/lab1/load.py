PATH1 = '/home/vagrant/models/w2v_2020-02-24-18.08.19'
PATH_TEST = '/home/vagrant/models/w2v_2020-02-24-19.20.18'

from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pyspark.ml.feature import Word2Vec
from pprint import pprint
import py4j

model = Word2VecModel.load(PATH1)

pprint(model.findSynonyms("claim", 5).collect())
#
# def printHelp():
#     print("""
# Команды:
# help - отобразить эту справку
# load - загрузить модель из списка доступных
# load_path - загрузить модель по указанному адресу
# syn - подобрать синоним к слову
# exit - завершить работу
#     """)
#
# def loadModel():
#     while True:
#         print("""
# Введите номер модели или exit для выхода
# Возможные модели:""" + str(PATHS.keys()))
#         num = input()
#         if 'exit' == num:
#             return 'invalid_model'
#         elif num in PATHS.keys():
#             return Word2VecModel.load(PATH1)
#         else:
#             print("Модель с указанным номером не найдена")
#
# def loadModelPath():
#     print("Введите путь к модели:")
#     path = input()
#     return Word2VecModel.load(path)
#
# def findSynonyms(model):
#     print("Введите слово, к которому нужно искать синонимы:")
#     word = input()
#     print("Введите число синонимов:")
#     num = int(input())
#     pprint(model.findSynonyms(word, num).collect())
#
# spark = SparkSession \
#     .builder \
#     .appName("SimpleApplication") \
#     .getOrCreate()
#
# printHelp()
# model = 'invalid_model'
#
# while True:
#
#
#     command = input()
#
#     if 'exit'==command:
#         break
#     elif 'help'==command:
#         printHelp()
#     elif 'load'==command:
#         model = loadModel()
#     elif 'load_path'==command:
#         model = loadModelPath()
#     elif 'syn'==command:
#         findSynonyms()
#     else:
#         print("Команда не распознана")
#
# spark.stop()