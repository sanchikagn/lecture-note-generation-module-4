import pandas as pd

from note_generation import ContentAlignment
from note_generation import preprocessing_acontent, preprocessing_topic
from note_generation import Course
from note_generation import word_net_similarity
from note_generation import add_lesson_name, converting_pdf, add_subtopic, open_note, create_html, add_off_topic_content\
    , add_paragraph, add_image, add_related_knowledge_points, add_list_item, add_list

content_aligned = ContentAlignment()

# Time-aligned lecture
lecture = content_aligned.aligning_content('input_1')

# Obtaining ontology
print('Retrieving Ontology')
acquire_ontology = Course()


# Entities from ontology
def get_classes(topics):
    topic_words = str(topics).split()
    facts = pd.DataFrame()
    facts_kp = pd.DataFrame()
    for word in topic_words:
        fact = acquire_ontology.search_features(word)
        fact_kp = acquire_ontology.search_kps(word)
        facts = facts.append(fact)
        facts_kp = facts_kp.append(fact_kp)
        # Removing duplicates from entities
        facts = facts.drop_duplicates({'facts'}, keep='last')
        facts_kp = facts_kp.drop_duplicates({'facts'}, keep='last')
    return facts, facts_kp


# Highlight off-topic
def pdf_content_cat(topic_content, label):
    item = ''
    if label == 'off':
        item = item + add_off_topic_content(topic_content)
    else:
        item = item + add_paragraph(topic_content)
    return item


# Creating lecture note
def generating_lecture(lecture_pd):
    # Heading for PDF
    element1 = add_lesson_name(lecture_pd['topic'].iloc[0])
    lesson = lecture['topic'].iloc[0]
    doc = element1
    related_kps = pd.DataFrame()
    related_kp = pd.DataFrame()
    for index, column in lecture_pd.iterrows():
        doc_element = ''

        # Sub-topic for PDF
        if column[2] is not lesson:
            doc_element = add_subtopic(column[2])

        topic = column[2]
        # Pre-processing topics to search on ontology
        keywords = preprocessing_topic(topic)
        unique_topic_content, related_kps = get_classes(keywords)
        unique_topic_content = unique_topic_content.dropna()
        related_kps = related_kps.dropna()
        related_kp = related_kp.append(related_kps)

        content = column[3]
        # Find similarity
        if content and not unique_topic_content.empty:
            preprocessed_content = preprocessing_acontent(content)
            labeled_content = word_net_similarity(preprocessed_content, unique_topic_content['facts'])
            # labeled_content.groupby(labeled_content['sentence'])
            for index_content, row_content in labeled_content.iterrows():
                doc_element = doc_element + pdf_content_cat(row_content['sentence'], row_content['label'])
            # labeled_content.to_csv('compare.csv', header=None)
        elif content:
            doc_element = doc_element + add_paragraph(content)

        # Text for PDF
        text = column[4]
        un_list = ''
        if text:
            result = [x.strip() for x in text.split(',')]
            for x in result[1:]:
                un_item = add_list_item(x)
                un_list = un_list + un_item
            doc_element = doc_element + add_list(un_list)
        doc = doc + doc_element

        # Add images to previous topic
        image = column[5]
        if image:
            result = [x.strip() for x in image.split(',')]
            for x in result[1:]:
                doc = doc + add_image(x)

    if not related_kp.empty:
        related_kp = related_kp.drop_duplicates({'entity'}, keep='last')
        # print(related_kps)
        doc = doc + add_related_knowledge_points(related_kp)
    return doc, lesson


pdf_content, lesson_name = generating_lecture(lecture)
# Create PDF content
create_html(pdf_content)
converting_pdf(lesson_name)
open_note(lesson_name + '.pdf')
