class PandasQuery:
    
    def __init__(self, df) -> None:

        self.df = df
        self.query_engine = self.create_query_engine(df)
        self.responses = []
        self.use_counts = 0

    @staticmethod
    def create_query_engine(df):
        try: 
            from llama_index.query_engine import PandasQueryEngine
        except Exception as e:
            raise ImportError(f"Error in importing PandasQueryEngine from llama_index: {e}")
        
        return PandasQueryEngine(df=df, verbose=False)
        
    def reset_engine(self, df=None):
        df = df or self.df
        self.query_engine = self.create_query_engine(df)

    def query(self, query: str):
        try:
            response = self.query_engine.query(query)
            self.responses.append(response)
            self.use_counts += 1
            return str(response)
        
        except Exception as e:
            raise ValueError(f"Error occured during querying: {e}")

    def get_responses(self):
        return self.responses
    
    def get_source_nodes(self):
        return [i.source_nodes for i in self.responses]
    