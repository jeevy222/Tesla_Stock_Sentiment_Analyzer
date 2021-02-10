import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd

sia = SIA()


def perform_sentimental_analysis():
    """perform sentimental analysis on processed/clean data using SentimentIntensityAnalyzer."""

    # Initialize variables
    results = []
    positive_sentiments_count = 0
    negative_sentiments_count = 0
    neutral_sentiments_count = 0

    tesla_processed_content_df = pd.read_csv('tesla_processed_content.csv')
    print(tesla_processed_content_df)

    # Compute compound polarity scores
    for line in tesla_processed_content_df.processed_content:

        pol_score = sia.polarity_scores(line)
        pol_score['text'] = line

        results.append(pol_score)


    # Read dataframe and setup compound score based on polarity scores
    results_df = pd.DataFrame.from_records(results)
    results_df.head()
    results_df['score'] = 0
    results_df.loc[results_df['compound'] > 0, 'score'] = 1
    results_df.loc[results_df['compound'] < -0.2, 'score'] = -1
    results_df.head()
    df2 = results_df[['text', 'score', 'compound']]
    print(df2)
    df2.to_csv('tesla_sentiment_analysis.csv', mode='a', encoding='utf-8', index=False)

    # Compute count of positive, negative and neutral sentiments
    df_positive = results_df[results_df.score == 1]
    positive_sentiments_count = positive_sentiments_count + df_positive.score.count()

    df_neutral = results_df[results_df.score == 0]
    neutral_sentiments_count = neutral_sentiments_count + df_neutral.score.count()

    df_negative = results_df[results_df.score == -1]
    negative_sentiments_count = negative_sentiments_count + df_negative.score.count()

    print("Positive Sentiments Count: ", positive_sentiments_count)
    print("Neutral Sentiments Count: ", neutral_sentiments_count)
    print("Negative Sentiments Count: ", negative_sentiments_count)

    input_content_count = positive_sentiments_count + negative_sentiments_count + neutral_sentiments_count

    # Compute percentage of positive, negative and neutral sentiments
    positive_sentiments_percentage = (positive_sentiments_count / input_content_count) * 100
    negative_sentiments_percentage = (negative_sentiments_count / input_content_count) * 100
    neutral_sentiments_percentage = (neutral_sentiments_count / input_content_count) * 100
    print("Positive Sentiments Percentage: ", round(positive_sentiments_percentage, 2))
    print("Neutral Sentiments Percentage: ", round(neutral_sentiments_percentage, 2))
    print("Negative Sentiments Percentage: ", round(negative_sentiments_percentage, 2))

    # Conclude Results
    if positive_sentiments_percentage > negative_sentiments_percentage:
        print(
            'Positive sentiments percentage is more than Negative sentiments percentage based on the content analysed '
            'on cnbc, so one should buy (i.e. invest) stocks of Tesla')
    else:
        print(
            'Negative sentiments percentage is more than Positive sentiments percentage based on the content analysed '
            'on cnbc, so one should sell (i.e. not invest) stocks of Tesla')


if __name__ == '__main__':
    print('---Perform sentiment analysis---')
    perform_sentimental_analysis()
