import csv
import os

import pandas as pd
import re


class ExtractTopics:
    def __init__(self):
        self.topic_extraction = pd.DataFrame(columns=['type', 'text', 'start', 'end'])
        self.topics_typed = pd.DataFrame(columns=['start', 'end', 'text'])
        self.text_typed = pd.DataFrame(columns=['label', 'start', 'text'])

    @classmethod
    def text_to_csv(cls, file):
        with open(file, 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            with open('pptskills.csv', 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerows(lines)

    def extract_details(self, text_from_slides, title):
        details = str(text_from_slides)
        lesson_pattern = re.search(r'^1$', details)
        topic_pattern = re.search(r"[0-9]+_[0-9]_Topic", details)
        time_pattern = re.match(r"(\d+)_(\d+)", details)
        time = 0
        if time_pattern:
            # print(time_pattern.group(1) + ' ' + time_pattern.group(2))
            time = int(time_pattern.group(1))
        if lesson_pattern is not None:
            time = 1
            text_from_slides = 'lesson'
        elif topic_pattern is not None:
            text_from_slides = 'topic'
        else:
            text_from_slides = 'text'
        self.topic_extraction = self.topic_extraction.append({'type': text_from_slides, 'text': title,
                                                              'start': time, 'end': time}, ignore_index=True)

    def topics_labeled(self):
        self.topic_extraction = self.topic_extraction.drop_duplicates({'text'}, keep='first')
        for index, row in self.topic_extraction.iterrows():
            if row[0] == 'text':
                self.text_typed = self.text_typed.append({'label': 'text', 'start': row[2], 'text': row[1]},
                                                         ignore_index=True)
            else:
                self.topics_typed = self.topics_typed.append({'start': row[2], 'end': row[3], 'text': row[1]},
                                                             ignore_index=True)

    @classmethod
    def sort_images(cls, folder):
        images = os.listdir('data/' + folder + '/images')
        typed_images = pd.DataFrame(columns=['label', 'start', 'text'])
        path = 'data/' + folder + '/images'
        for item in images:
            time_pattern = re.match(r"(\d+)_(\d+).", str(item))
            main_pattern = re.match(r"^(\d+)\.", str(item))
            if time_pattern:
                time = int(time_pattern.group(1))
                image_path = path + '/' + str(item)
                typed_images = typed_images.append({'label': 'image', 'start': time, 'text': image_path}, ignore_index=True)
            elif main_pattern:
                time = int(main_pattern.group(1))
                image_path = path + '/' + str(item)
                typed_images = typed_images.append({'label': 'image', 'start': time, 'text': image_path}, ignore_index=True)
        # print(typed_images.sort_values(by=['start']))
        return typed_images.sort_values(by=['start'])


# extracting_data = ExtractTopics()
# extracting_data.text_to_csv('../../data/input_1/slidedata.txt')
# lecture_titles = pd.read_csv('pptskills.csv', sep=',', header=None, names=['type', 'title'])
# lecture_titles = lecture_titles.apply(lambda point: extracting_data.extract_details(point[0], point[1]), axis=1)
# extracting_data.topics_labeled()
# lecture_duration = TitleDuration()
# titles = lecture_duration.converting_to_topic_classes(extracting_data.topics_typed)
# print(titles)
