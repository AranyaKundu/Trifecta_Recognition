import re, json, pandas as pd
from datetime import datetime

def data_prep(data):
    temp_data1 = data.split("},")
    
    # prepare data for 1st dictionary
    temp_data2 = temp_data1[0][1:] + "}" # Add "}" at the end to make the dictionaries
    my_dict = json.loads(temp_data2) # Transform string to dictionary
    date_time = datetime.utcfromtimestamp(my_dict['created_at']) # convert timestamp from number to date time format
    created_at = date_time.strftime("%Y-%m-%d %H:%M:%S")
    my_dict['created_at'] = created_at
    cols = ['Timestamp', 'Name', 'Message', 'Attachments']
    final_df = pd.DataFrame(columns = cols)
    final_df.loc[len(final_df)] = [date_time, my_dict['name'], my_dict['text'], my_dict['attachments']!=[]]

    # Prepare data for 2nd to last dictionaries
    for i in range(1, len(temp_data1)):
        string = temp_data1[i] + "}"
        try:
            dict_str = json.loads(string)

            # 'created_at' is not presnt for a group notification
            if 'created_at' in dict_str:
                date_time = datetime.utcfromtimestamp(dict_str['created_at'])
                created_at = date_time.strftime("%Y-%m-%d %H:%M:%S")
                final_df.loc[len(final_df)] = [date_time, dict_str['name'], dict_str['text'], dict_str['attachments']!=[]]
            else: continue
        except json.decoder.JSONDecodeError:
            continue

        # divide timestamp into its components
    final_df['year'] = final_df['Timestamp'].dt.year
    final_df['month'] =final_df['Timestamp'].dt.month_name()
    final_df['date'] = final_df['Timestamp'].dt.day
    final_df['hour'] = final_df['Timestamp'].dt.hour
    final_df['minute'] = final_df['Timestamp'].dt.minute

    return final_df