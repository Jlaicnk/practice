import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class VectorStore:
    def __init__(self):
        self.VECTORSTORE_DIR = r'E:\临时资源\大创\大创a\vue_django_KnGraph\KnGraph\back\RAG\vector_db\db2'
        self.DOC_DIR = r'E:\临时资源\大创\大创a\vue_django_KnGraph\KnGraph\back\RAG\knowledge_doc'
        self.embeddings = OllamaEmbeddings(
            model="quentinz/bge-large-zh-v1.5:latest",
        )

    def init_vector_db(self):
        vector_db_dir = os.path.join(self.VECTORSTORE_DIR)
        # print('向量数据库地址:', vector_db_dir)

        # 如果持久化地址存在
        if os.path.exists(vector_db_dir):
            # 从本地持久化文件中加载
            print("从本地向量加载数据...")
            # 使用 Chroma 加载持久化的向量数据
            vector_store = Chroma(persist_directory=vector_db_dir, embedding_function=self.embeddings)

        # 如果持久化地址不存在
        else:
            print("生成向量数据库")
            # 加载知识文档
            documents = self.load_docs()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=100,  # 每个片段的最大字符数
                chunk_overlap=20  # 前后片段之间重叠的字符数
            )
            split_docs = text_splitter.split_documents(documents)

            print(split_docs)

            # 使用 Chroma 从文档中创建向量存储
            vector_store = Chroma.from_documents(documents=split_docs,
                                                 embedding=self.embeddings,
                                                 persist_directory=vector_db_dir)
            # vector_store.persist()  # 持久化向量存储

        return vector_store

    def load_docs(self):
        documents = []

        for root, _, files in os.walk(self.DOC_DIR, topdown=False):
            for file in files:
                filename = os.path.join(root, file)  # 获取文件的完整路径
                docs = self._load_file(filename)  # 加载文件中的文档

                new_docs = []  # 初始化一个空列表来存储新文档
                for doc in docs:
                    doc.metadata = {"source": doc.metadata["source"].replace(self.DOC_DIR, "")}
                    new_docs.append(doc)  # 将文档添加到新文档列表

                documents += new_docs

        return documents  # 返回所有文档的列表

    @staticmethod
    def _load_file(filename):
        file_extension = os.path.splitext(filename)[1]
        if file_extension == '.txt':
            loader = TextLoader(filename,encoding='utf-8')
        elif file_extension == '.pdf':
            loader = PyMuPDFLoader(filename)

        docs = loader.load()

        return docs


if __name__ == "__main__":
    v = VectorStore()
    v.init_vector_db()