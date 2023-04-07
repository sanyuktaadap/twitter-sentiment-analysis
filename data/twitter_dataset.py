import argparse
import snscrape.modules.twitter as sntwitter
import pandas as pd

from tqdm import tqdm

def write_twitter_dataset(queries, count, file_path):
    df = pd.DataFrame(columns=['Date','URL', 'Keyword', 'Tweet'])

    for query in queries:
        print(f'Keyword - {query}')
        tweets = sntwitter.TwitterSearchScraper(query).get_items()

        # Tweets is a generator that fetches tweets from the net on the fly
        # Thus, its length is unknown and indexing it is not possible (i.e. tweets[i] not poss)
        for index, tweet in tqdm(enumerate(tweets)):
            if index == count:
                break
            URL = f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
            df2 = {'Date': tweet.date, 'URL': URL, 'Tweet': tweet.rawContent, 'Keyword': query}
            df = pd.concat([df, pd.DataFrame.from_records([df2])])
            
    # Converting time zone from UTC to EST
    # df['Date'] = df['Date'].dt.tz_convert('US/Eastern')
    df.index = list(range(len(df)))
    print(df.head())

    df.to_csv(file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-k', 
        '--keywords-list', 
        nargs='+', 
        default=[
            'anterior knee pain syndrome arthroplasties', 
            'knee replacement arthroplasties', 
            'arthroplasty',
            'arthroplasties',
            'anterior knee pain syndrome',
            'total knee arthroplasty',
            'knee arthroplasty', 
            'knee replacement arthroplasty',
            # 'replacement', 
            # 'replacement', 
            # 'knee'
        ],
        help="List of keywords")
    parser.add_argument(
        "-c",
        "--count", 
        type=int,
        default=100,
        help="Count of tweets per keyword")
    parser.add_argument(
        "-f",
        "--file_path", 
        type=str,
        default='tweets.csv',
        help="Dataset output file path.")
    args = parser.parse_args()
    
    write_twitter_dataset(args.keywords_list, args.count, args.file_path)