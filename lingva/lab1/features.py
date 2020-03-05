PATH = 'example_patents/patents/*.xml'

from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import IDF
from pyspark.ml.feature import Word2Vec
from lxml import etree
import re
import string
from pprint import pprint

def get_patent_name(patent_data):
    """
    Получение названия патента
    """
    root = etree.fromstring(patent_data.encode('utf-8'))
    doc_numers = root.findall(".//doc-number")
    countries = root.findall(".//country")
    patent_name = countries[0].text + doc_numers[0].text
    return patent_name


def get_claims(patent_data):
    """
    Проверка claim'ов патента
    """
    root = etree.fromstring(patent_data.encode('utf-8'))
    claims = root.findall(".//claim")
    if (claims):
        claims_without_tags = [''.join(claim.itertext()) for claim in claims]
        return ''.join(claims_without_tags)

    return ''


def remove_punctuation(text):
    """
    Удаление пунктуации из текста
    """
    return text.translate(str.maketrans('', '', string.punctuation))


def remove_linebreaks(text):
    """
    Удаление разрыва строк из текста
    """
    return text.strip()


def get_only_words(tokens):
    """
    Получение списка токенов, содержащих только слова
    """
    return list(filter(lambda x: re.match('[a-zA-Z]+', x), tokens))

spark = SparkSession \
    .builder \
    .appName("SimpleApplication") \
    .getOrCreate()

print("Загружаем данные...")
input_data = spark.sparkContext.wholeTextFiles(PATH)

print("Готовим данные...")
prepared_data = input_data.map(lambda x: (get_patent_name(x[1]), get_claims(x[1]))) \
    .map(lambda x: (x[0], remove_punctuation(x[1]))) \
    .map(lambda x: (x[0], remove_linebreaks(x[1])))

prepared_df = prepared_data.toDF().selectExpr('_1 as patent_name', '_2 as patent_claims')

print("Разбиваем текст на токены...")
tokenizer = Tokenizer(inputCol="patent_claims", outputCol="words")
words_data = tokenizer.transform(prepared_df)

print("Фильтруем токены...")
filtered_words_data = words_data.rdd.map(lambda x: (x[0], x[1], get_only_words(x[2])))
filtered_df = filtered_words_data.toDF().selectExpr('_1 as patent_name', '_2 as patent_claims', '_3 as words')

print("Удаляем стоп-слова...")
remover = StopWordsRemover(inputCol='words', outputCol='filtered')
filtered = remover.transform(filtered_df)

print("Считаем признаки...")
vectorizer = CountVectorizer(inputCol='filtered', outputCol='raw_features').fit(filtered)
featurized_data = vectorizer.transform(filtered)
featurized_data.cache()

print("Считаем относительные частоты признаков...")
idf = IDF(inputCol='raw_features', outputCol='features')
idf_model = idf.fit(featurized_data)
rescaled_data = idf_model.transform(featurized_data)

res = rescaled_data.select("features", "patent_name").collect()
#features_table = '\n'.join(list(map(lambda x:str(x), res)))
#features_table = list(map(lambda x:str(x), res))

print("Таблица значимых признаков:")
pprint({i:vectorizer.vocabulary[i] for i in range(len(vectorizer.vocabulary))})
print("Таблица значимых признаков для каждого из патентов:")
pprint(res)

spark.stop()