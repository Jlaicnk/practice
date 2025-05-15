from KnGraph.back.RAG.vector_store import VectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain


class RagSearch:
    def __init__(self):
        vec_db = VectorStore()
        self.vector_store = vec_db.init_vector_db()
        self.template = """使用以下上下文来回答最后的问题。
        如果你不知道答案，就说你不知道，不要试图编造答案。
        不用回复“根据您提供的上下文信息“字样
        
        rag信息为:
        {context}

        """
        self.llm = ChatZhipuAI(zhipuai_api_key='ed23925e82274091b878af5bb092c261.Bno6aFYOCMhIy1si',model_name="glm-4")

    def get_relevant_context(self,question,top_k=5):
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": top_k})

        retrieved_docs = retriever.invoke(question)

        context = [d.page_content for d in retrieved_docs]

        return context

    def rag_res(self,question,top_k=3):
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": top_k})
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        response = rag_chain.invoke({"input": question})

        return response["answer"]


if __name__ == "__main__":
    rag = RagSearch()
    res = rag.rag_res("常量是什么")
    print(rag.get_relevant_context("常量是什么"))
    print(res)

