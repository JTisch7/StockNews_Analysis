# Stock_Price_Analysis
Analyzing absolute and directional stock price movement


API_DataPulls :  
newsfilteriioPull.py - script to pull historical news data from newsfilter.io's API  
polygonPull.py - script to pull historical stock price data from polygon.io's API  
redditDataPull.py - script to pull historical reddit submissions data from pushshift.io (an API with historical reddit data)
               
DataPrep_AND_Models :  
RNN_DataPrep.py - data preparation and models (RNNs, Conv1D, WaveNet)  
non_RNN_DataPrep.py - data preparation and models (all others)  
data - all data used for RNN_DataPrep.py and non_RNN_DataPrep.py  

Financial_Sentiment_Analyzers :  
Creating_A_FinBert - scripts that show how to fine-tune, save, and reload a BERT model for financial sentiment analysis (final model achieved over 96% accuracy on the Financial PhraseBank dataset)  
HuggingFace_PreTrained_FinBERT - a pretrained and ready-to-go model for financial sentiment analysis from Hugging Face Transformers  
(the output of either of these models can be used as inputs for both data prep/model files - RNN_DataPrep.py, non_RNN_DataPrep.py) 
