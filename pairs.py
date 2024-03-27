from transformers import pipeline
import alpaca_trade_api as tradeapi
import yfinance as yf
import warnings

warnings.simplefilter('ignore')


def header(pairs):
    

    model_id = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
    classify = pipeline('sentiment-analysis', model=model_id)
    yftickers = []
    for ticker in pairs:
        yftickers.append(yf.Ticker(ticker))

    newsA = [news.get('title') for news in yftickers[0].get_news()]
    newsB = [news.get('title') for news in yftickers[1].get_news()]
    print('----NEWS FOR KO US----')
    print(newsA)
    print('----------------------')
    print()
    print('----NEWS FOR PEP US----')
    print(newsB)
    

    sentimentsA = []
    sentimentsB = []

        
    for titleA, titleB in zip(newsA, newsB):
        sentimentA = classify(titleA)
        sentimentB = classify(titleB)
        sentimentsA.append(sentimentA)
        sentimentsB.append(sentimentB)

    scores_to_avg_A = []
    scores_to_avg_B = []
    for sentA, sentB in zip(sentimentsA, sentimentsB):
        posmultiplier = 1
        negmultiplier = -1
        if sentA[0].get('label') == "negative":
            scoreA = sentA[0].get('score') * negmultiplier
        elif sentA[0].get('label') == 'positive':
            scoreA = sentA[0].get('score') * posmultiplier
        elif sentA[0].get('label') == "neutral":
            scoreA = 0

        if sentB[0].get('label') == "negative":
            scoreB = sentB[0].get('score') * negmultiplier
        elif sentB[0].get('label') == 'positive':
            scoreB = sentB[0].get('score') * posmultiplier
        elif sentB[0].get('label') == "neutral":
            scoreB = 0

        scores_to_avg_A.append(scoreA)
        scores_to_avg_B.append(scoreB)
        
    sample_sizeA = len(scores_to_avg_A)
    sample_sizeB = len(scores_to_avg_B)    
    
    average_score_A = round(sum(scores_to_avg_A)/sample_sizeA, 2)
    average_score_B = round(sum(scores_to_avg_B)/sample_sizeB, 2)
    sentiment_spread = round(abs(average_score_A-average_score_B), 2)
    print(average_score_A, average_score_B, sentiment_spread)
    indicator_A = ""
    indicator_B = ""
    if -0.1 <= average_score_A <= 0.1:
        indicator_A = 'neutral'
    elif average_score_A < -0.1:
        indicator_A = 'sell'
    elif average_score_A > 0.1:
        indicator_A = 'long'

    if -0.1 <= average_score_B <= 0.1:
        indicator_B = 'neutral'
    
    elif average_score_B < -0.1:
        indicator_B = 'sell'
    
    elif average_score_B > 0.1:
        indicator_B = 'long'
    
    
    return indicator_A, indicator_B, average_score_A, average_score_B


def spread_adjuster(a, b, scoreA, scoreB):
    alpaca_api_key = 'PKS466BHZVEWMMMHINY9'
    alpaca_secret_key = 'OpeByWSTZkkMRQPAcc3Vjvebfm1t4K5Gu2Plm3Jn'
    base_url = 'https://paper-api.alpaca.markets'
    api = tradeapi.REST(alpaca_api_key,
                        alpaca_secret_key,
                        base_url,
                        api_version='v2')
    if a == 'long':
        api.submit_order(
                    symbol='KO',  
                    qty=abs(scoreA)*100,  
                    side='buy',  
                    type='market', 
                    time_in_force='gtc'
                )
    elif a == 'sell':
        api.submit_order(
            symbol='KO',  
            qty=abs(scoreA)*100,  
            side='sell',  
            type='market',  
            time_in_force='gtc'
        )

    if b =='long':
        api.submit_order(
            symbol='PEP',  
            qty=abs(scoreB)*100,  
            side='buy',  
            type='market',  
            time_in_force='gtc'
        )
    elif b == 'sell':
        api.submit_order(
            symbol='PEP',  
            qty=abs(scoreB)*100,  
            side='sell',  
            type='market',  
            time_in_force='gtc'
        )

