class PandasQuery:
    
    def __init__(self, df) -> None:
        try: 
            from llama_index.query_engine import PandasQueryEngine
        except Exception as e:
            raise ImportError(f"Error in importing PandasQueryEngine from llama_index: {e}")
        
        self.df = df
        self.query_engine = PandasQueryEngine(df=df, verbose=False)
        self.responses = []
        self.use_counts = 0
            
    def set_df(self, df):
        self.df = df
        
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
