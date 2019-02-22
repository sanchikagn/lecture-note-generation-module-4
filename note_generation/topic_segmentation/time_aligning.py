import pandas as pd
from note_generation.topic_segmentation.title_duration import TitleDuration
# from .input_time_align import ExtractTopics
from note_generation.topic_segmentation.input_time_align import ExtractTopics


class ContentAlignment:
    @classmethod
    def aligning_content(cls, text_path):
        print('Time Aligning Content')
        extracting_data = ExtractTopics()
        extracting_data.text_to_csv('data/' + text_path + '/slidedata.txt')
        lecture_titles_pre = pd.read_csv('pptskills.csv', sep=',', header=None, names=['type', 'title'])
        lecture_titles_pre = lecture_titles_pre.apply(lambda point: extracting_data.extract_details(point[0], point[1]),
                                                      axis=1)
        # Topic extraction
        extracting_data.topics_labeled()
        lecture_duration = TitleDuration()

        # Titles from the lecture with their duration
        titles = lecture_duration.converting_to_topic_classes(extracting_data.topics_typed)

        # Inspecting data
        audio_transcript = pd.read_csv('data/'+ text_path + '/voice_text.csv', sep=';', header=None,
                                       names=['start', 'text'], converters={'label': str, 'text': str})
        audio_transcript['label'] = 'audio'

        # Image extraction
        lecture_images = extracting_data.sort_images(text_path)

        # Text extraction
        lecture_text = extracting_data.text_typed.sort_values(by=['start'])

        # Acquiring the entire audio transcript
        # lecture_text = ''
        # for index, column in audio_transcript.iterrows():
        #     # start = column[1]
        #     text = column[2]
        #     lecture_text = lecture_text + ' ' + text
        all_lecture_content_sorted = cls.entire_lecture(audio_transcript, lecture_images, lecture_text)
        lecture = cls.topic_segmentation(titles, all_lecture_content_sorted)
        return lecture

    # Aligning images to audio transcript
    @classmethod
    def entire_lecture(cls, audio_transcript, lecture_images, lecture_text):
        all_lecture_content = audio_transcript.merge(lecture_images, how='outer', on=['start', 'label', 'text'])
        all_lecture_content = all_lecture_content.merge(lecture_text, how='outer', on=['start', 'label', 'text'])
        df = pd.DataFrame(all_lecture_content)
        all_lecture_content_sorted = df.sort_values(by=['start'])
        # all_lecture_content_sorted.to_csv('resources/all_content.csv', header=None)
        return all_lecture_content_sorted

    # General method for topic segmentation
    @classmethod
    def topic_segmentation(cls, lecture_titles, all_lecture_content_sorted):
        lecture = pd.DataFrame(columns=['start', 'end', 'topic', 'content', 'text', 'images'])
        for index, row in lecture_titles.iterrows():
            start = int(row[0])
            end = int(row[1])
            topic = row[2]
            topic_content = ''
            image_path = ''
            text = ''
            for index_content, row_content in all_lecture_content_sorted.iterrows():
                label = row_content[2]
                # align_all_content(label)
                time = int(row_content[0])
                if label == 'audio':
                    if time == end:
                        topic_content = topic_content + row_content[1] + ' '
                        # Considering end of strings
                        # if re.match('[.?!](?=$)', topic_content):
                        #     # ^ [A - Z][ ^?!.]*[?.!]$
                        #     print(topic)
                        #     # print('\n\n')
                        # else:
                        #     pre_topic = topic_content
                        #     print(pre_topic)
                        #     print('\n\n')
                        break
                    elif start <= time < end:
                        topic_content = topic_content + row_content[1] + ' '
                    else:
                        continue
                elif label == 'text':
                    if time == end:
                        text = text + ',' + row_content[1]
                        break
                    elif start <= time < end:
                        text = text + ',' + row_content[1]
                    else:
                        continue
                elif label == 'image':
                    if time == end:
                        image_name = str(row_content[1])
                        image_path = image_path + image_name
                        break
                    elif start <= time < end:
                        image_name = str(row_content[1])
                        image_path = image_path + ',' + image_name
                    else:
                        continue

            # Adding to lecture df
            lecture = lecture.append({'start': start, 'end': end, 'topic': topic, 'content': topic_content, 'text': text,
                                      'images': image_path}, ignore_index=True)

            print(topic)
            print(topic_content) if topic_content != '' else print('')
            print('TEXT: ' + text)
            print(image_path)
            print('\n')
        return lecture
