def SmallToBig_engine(textnodes):
    try:
        from llama_index.llama_pack import download_llama_pack
        
        RecursiveRetrieverSmallToBigPack = download_llama_pack(
            "RecursiveRetrieverSmallToBigPack",
            "./recursive_retriever_stb_pack",
            )
        return RecursiveRetrieverSmallToBigPack(textnodes)
        
    except Exception as e:
        raise ImportError(f"Error in importing RecursiveRetrieverSmallToBigPack from llama_index: {e}")
