import pandas as pd, re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from transformers import pipeline

# function to display total messages
def tot_msgs(user_choice, data):
    if user_choice == 'OverAll':
        return data.shape[0]
    else:
        return data[data['Name'] == user_choice].shape[0]

# function to display total number of words
def tot_words(user_choice, data):
    word_count = 0
    if user_choice == 'OverAll':
        messages = data['Message'].str.split()
    else:
        messages = data[data['Name'] == user_choice]['Message'].str.split()
    for message in messages:
            try:
                word_count += len(message)
            except TypeError: continue
    return word_count

# function to compute total attachments
def tot_attachments(user_choice, data):
    if user_choice == 'OverAll':
        att_count = data['Attachments'].sum()
    else:
        att_count = data[data['Name'] == user_choice]['Attachments'].sum()
    return att_count

# function to display total urls
def total_urls(user_choice, data):
    if user_choice == 'OverAll':
        texts = data['Message']
    else:
        texts = data[data['Name'] == user_choice]['Message']
    cnt = 0
    for text in texts:
        try:
            urls = re.findall(r"https:?\/\/[^\s]+", text)
            cnt += len(urls)
        except TypeError: continue
    return cnt

# function to display most active users
def active_users_bar(data):
    new_series = data['Name'].value_counts().head()
    name = new_series.index
    count = new_series.values
    fig, ax = plt.subplots()
    ax = plt.bar(name, count)
    plt.autoscale(tight = True)
    plt.xticks(rotation = 45, ha = 'right')
    new_dataframe = round(data['Name'].value_counts() / len(data) * 100, 2).reset_index().rename(columns = {
        'index':'Name', 'Name':'Percent'
    })
    return fig, new_dataframe

# function to create a wordcloud
def create_wc(choice_user, data):
    if choice_user == 'OverAll':
        wc_data = data['Message']
    else:
        wc_data = data[data['Name'] == choice_user]['Message']
    
    wc_object = WordCloud(height = 500, width = 500, background_color = '#ffffff', min_font_size = 12)
    
    final_wc = wc_object.generate(wc_data.str.cat(sep = " "))
    
    fig, ax = plt.subplots()
    ax.imshow(final_wc)
    return fig

# function to create top most used words after removing stopwords
def user_sentiment(choice_user, data):
    classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
    # temp_df = pd.DataFrame()
    # if choice_user == 'OverAll':
    texts = data['Message'].tolist()
    # else:
    #     texts = data[data['Name'] == choice_user]['Message'].tolist()
    
    new_texts = [text if text is not None else "NA" for text in texts]
    # Initialize empty lists for positive, negative, and neutral scores
    pos_scores = []
    neg_scores = []
    neu_scores = []

    # Loop over each message and classify its sentiment
    for message in new_texts:
        result = classifier(message)[0]  # Get the first (and only) result from the pipeline
        score = result['score']
        label = result['label']
        
        # Add the score to the appropriate list based on the sentiment label
        if label == 'POSITIVE':
            pos_scores.append(score)
            neg_scores.append(0)  # Add a 0 for negative and neutral scores to maintain shape
            neu_scores.append(0)
        elif label == 'NEGATIVE':
            pos_scores.append(0)
            neg_scores.append(score)
            neu_scores.append(0)
        else:
            pos_scores.append(0)
            neg_scores.append(0)
            neu_scores.append(score)
    
    # Add the new columns to the dataframe
    data['pos_score'] = pos_scores
    data['neg_score'] = neg_scores
    data['neu_score'] = neu_scores
    return data[['Name', 'Message', 'Attachments', 'pos_score', 'neg_score', 'neu_score']]
