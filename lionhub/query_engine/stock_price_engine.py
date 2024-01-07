from lionagi import lcall
from .query_pandas import PandasQuery


def stock_price_engine(stock_prices, symbols):
    try:
        from llama_index.schema import IndexNode
        from llama_index import VectorStoreIndex
        from llama_index.retrievers import RecursiveRetriever
        from llama_index.query_engine import RetrieverQueryEngine
        from llama_index.response_synthesizers import get_response_synthesizer
    except Exception as e:
        raise ImportError(f"Error importing llama_index: {e}")
    
    
    df_price_query_engines = [
        PandasQuery.create_query_engine(stock) for stock in stock_prices
    ]

    summaries = lcall(symbols, lambda x: f'{x} stock price history')

    df_price_nodes = [
        IndexNode(text=summary, index_id=f'pandas{idx}') 
        for idx, summary in enumerate(summaries)
    ]

    df_price_id_query_engine_mapping = {
        f'pandas{idx}': df_engine
        for idx, df_engine in enumerate(df_price_query_engines)
    }

    stock_price_vector_index = VectorStoreIndex(df_price_nodes)
    stock_price_vector_retriever = stock_price_vector_index.as_retriever(similarity_top_k=1)

    stock_price_recursive_retriever = RecursiveRetriever(
        "vector",
        retriever_dict={"vector": stock_price_vector_retriever},
        query_engine_dict=df_price_id_query_engine_mapping,
        verbose=True,
    )

    stock_price_response_synthesizer = get_response_synthesizer(
        # service_context=service_context,
        response_mode="compact"
    )

    stock_price_query_engine = RetrieverQueryEngine.from_args(
        stock_price_recursive_retriever, response_synthesizer=stock_price_response_synthesizer
    )
    
    return stock_price_query_engine
