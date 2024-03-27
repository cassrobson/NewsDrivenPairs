from pairs import header, spread_adjuster

def main(pairs):
    sentiment_indicator_A, sentiment_indicator_B, scoreA, scoreB = header(pairs)
    print(sentiment_indicator_A)
    print(sentiment_indicator_B)
    print(scoreA*100)
    print(scoreB*100)
    spread_adjuster(sentiment_indicator_A, sentiment_indicator_B, scoreA, scoreB)


if __name__ == '__main__':
  main(['KO', 'PEP'])
