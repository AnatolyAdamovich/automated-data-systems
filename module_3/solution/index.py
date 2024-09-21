from nltk.tokenize import RegexpTokenizer
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
from bitarray import bitarray
from coding import EliasCoder

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.documents = {}
        self.tokenizer = RegexpTokenizer(r'[а-яёa-z0-9]+')
        self.stopwords_ru = stopwords.words("russian")
        self.morph = MorphAnalyzer()
        self.compress_method = None
        self.coder = EliasCoder()

    def get_index(self):
        '''
        Получить индекс, содержащий токены и ссылки на документы
        '''
        return self.index
    
    def add_document(self, document_id: int, text: str) -> None:
        '''
        Добавление документа и его токенов в индекс
        
        Parameters
        ----------
        document_id : int
            идентификатор документа
        text : str
            документ
        '''
        self.documents[document_id] = text
        
        # токенизация
        words = self._tokenize(text)
        # лемматизация и удаление стоп-слов
        words = self._lemmatize(words)
        
        self._update_index(document_id, words)

    def search(self, query: str) -> list[int]:
        '''
        Поиск документов в инвертированном индексе
        
        Parameters
        ----------
        query : str
            запрос в виде строки для поиска
        '''
        # токенизация
        words = self._tokenize(query)
        # лемматизация и удаление стоп-слов
        words = self._lemmatize(words)

        
        if self.compress_method == 'delta':
            list_of_documents = self.coder.decode_delta_string(self.index[words[0]].to01())
        elif self.compress_method == 'gamma':
            list_of_documents = self.coder.decode_gamma_string(self.index[words[0]].to01())
        else:
            list_of_documents = self.index[words[0]]
        
        # документы, содержащие первое слово запроса
        result_docs = set(doc_id for doc_id in list_of_documents)
        
        # пересекаем результаты для остальных слов запроса
        for word in words[1:]:
            if self.compress_method == 'delta':
                list_of_documents = self.coder.decode_delta_string(self.index[word].to01())
            elif self.compress_method == 'gamma':
                list_of_documents = self.coder.decode_gamma_string(self.index[word].to01())
            else:
                list_of_documents = self.index[word]

            result_docs &= set(doc_id for doc_id in list_of_documents)

        return list(result_docs)

    def get_document(self, document_id: int) -> str:
        '''
        Получения документа по его идентификатору

        Parameters
        ----------
        document_id : int
            идентификатор документа
        '''
        return self.documents.get(document_id)
    
    def compress_index(self, method: str) -> None:
        '''
        Сжатие данных за счет применения алгоритмов гамма и дельта кодирования Элиаса
        
        Parameters
        ----------
        method : str
            метод кодирования (gamma / delta)
        '''
        if method == 'gamma':
            for token in self.index.keys():
                compressed_documents_ids = bitarray("".join([self.coder.gamma_encoding(document_id) 
                                                             for document_id in self.index[token]]))
                self.index[token] = compressed_documents_ids
            self.compress_method = 'gamma'
        elif method == 'delta':
            for token in self.index.keys():
                compressed_documents_ids = bitarray("".join([self.coder.delta_encoding(document_id) 
                                                             for document_id in self.index[token]]))
                self.index[token] = compressed_documents_ids
            self.compress_method = 'delta'
        else:
            print('Параметр <method> указан неверно')
            return 
        
    def _update_index(self, document_id: int, words: list[str]) -> None:
        '''
        Обновление индекса при обработке нового документа

        Parameters
        ----------
        document_id : int
            идентификатор документа
        words : list[str]
            массив обработанных (лемматизация, удаление стоп-слов) токенов
        '''
        
        for word in words:
            self.index.setdefault(word, []).append(document_id)

    def _tokenize(self, text: str) -> list[str]:
        '''
        Вспомогательный метод для выделения токенов с помощью tokenizer

        Parameters
        ----------
        text : str
            текст, который требуется разбить на токены
        '''
        return self.tokenizer.tokenize(text.lower())
    
    def _lemmatize(self, tokens: list[str]) -> list[str]:
        '''
        Вспомогательный модуль для лемматизации токенов
        
        Parameters
        ----------
        tokens : list
            массив токенов
        '''

        words = []
        for token in tokens:
            token_in_normal_form = self.morph.normal_forms(token)[0]
            if token_in_normal_form not in self.stopwords_ru:
                words.append(token_in_normal_form)
        return words
    