def get_huggingface_classifier(
    model='mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis'
    ):
    try: 
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

        model_name = 'mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis'
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        return pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
        
    except Exception as e:
        raise ImportError(f"Error in importing AutoModelForSequenceClassification from transformers: {e}")
    