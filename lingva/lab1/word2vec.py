PATH = 'example_patents/patents_massive/*.xml'


from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import IDF
from pyspark.ml.feature import Word2Vec
from lxml import etree
import re
import string
import datetime

def get_patent_name(patent_data):
    """
    Получение названия патента
    """
    try:
        root = etree.fromstring(patent_data.encode('utf-8'))
        doc_numers = root.findall(".//doc-number")
        countries = root.findall(".//country")
        patent_name = countries[0].text + doc_numers[0].text
        return patent_name
    except BaseException:
        return ''

def get_claims(patent_data):
    """
    Проверка claim'ов патента
    """
    try:
        root = etree.fromstring(patent_data.encode('utf-8'))
        claims = root.findall(".//claim")
        if (claims):
            claims_without_tags = [''.join(claim.itertext()) for claim in claims]
            return ''.join(claims_without_tags)
        return ''
    except:
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


input_file = spark.sparkContext.wholeTextFiles(PATH)

print("""

Подготовка данных (1)...

""")
prepared_data = input_file.map(lambda x: (get_patent_name(x[1]), get_claims(x[1]))) \
    .map(lambda x: (x[0], remove_punctuation(x[1]))) \
    .map(lambda x: (x[0], remove_linebreaks(x[1])))

print("""

Подготовка данных (2)...

""")
df = prepared_data.toDF()

print("""

Подготовка данных (3)...

""")
prepared_df = df.selectExpr('_2 as text')

print("""

Разбитие на токены...

""")
tokenizer = Tokenizer(inputCol='text', outputCol='words')
words = tokenizer.transform(prepared_df)
#words.show()

print("""

Очистка от стоп-слов...

""")
stop_words = StopWordsRemover.loadDefaultStopWords('english')
remover = StopWordsRemover(inputCol="words", outputCol="filtered", stopWords=stop_words)
filtered = remover.transform(words)
#filtered.show()


print("""

Построение модели...

""")
word2Vec = Word2Vec(inputCol='words', outputCol='result')
model = word2Vec.fit(words)
w2v_df = model.transform(words)
#w2v_df.show()

print("""

Сохранение модели...

""")
today = datetime.datetime.today()
model_name = today.strftime("/home/vagrant/models/w2v_%Y-%m-%d-%H.%M.%S")
print("""

Model  """ + model_name + """  saved

""")
model.save(model_name)
# model.findSynonyms('shown', 5).show()

spark.stop()