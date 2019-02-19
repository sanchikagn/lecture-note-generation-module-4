import pandas as pd
from itertools import islice


class TitleDuration:
    @classmethod
    def converting_to_topic_classes(cls, lecture_titles):
        print('Title Duration')
        # lecture_titles = titles
        title_duration = pd.DataFrame(columns=['start', 'end', 'text'])

        start_time = lecture_titles['start'].iloc[0]
        topic = lecture_titles['text'].iloc[0]
        # start time in seconds
        start = int(start_time)
        # print(start)
        for index, column in islice(lecture_titles.iterrows(), 1, None):
            # time in seconds
            time = (int(column[0]))
            end = time - 1
            # creating topic categories
            title_duration = title_duration.append({'start': start, 'end': end, 'text': topic}, ignore_index=True)
            topic = column[2]
            start = time
        last_topic = lecture_titles['text'].iloc[-1]
        title = last_topic
        title_duration = title_duration.append({'start': start, 'end': str(start+100000), 'text': title}, ignore_index=True)
        title_duration_sorted = title_duration.sort_values(by=['start'])
        # title_duration_sorted.to_csv('resources/title_duration.csv', header=None)
        return title_duration_sorted
