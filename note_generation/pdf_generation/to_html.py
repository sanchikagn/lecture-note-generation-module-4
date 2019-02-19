# Write to html
f = open('lecture.html','w')


def add_lesson_name(heading1):
    heading = """<h1 align="center">""" + heading1 + """</h1>"""
    return heading


def add_subtopic(topic):
    title = """<br/><br/><h3 class="break-before" align="center">""" + topic + """</h3>"""
    return title


def add_paragraph(paragraph):
    section = """<p>""" + paragraph + """</p>"""
    return section


def add_off_topic_content(content):
    section = """<p style = "background-color:powderblue;">""" + content + """</p>"""
    return section


def add_image(image_path):
    path = """<br/><div style="display: flex; justify-content: center;"><img src = '""" + image_path \
           + """' alt = "lecture image"></div><br/>"""
    # Add caption
    return path


def add_list(items):
    un_list = """<ul>""" + items + """</ul>"""
    return un_list


def add_list_item(item):
    list_item = """<li>""" + item + """</li>"""
    return list_item


def add_related_knowledge_points(content):
    k_points = """<br/><h5>Facts from Related Lessons: </h5><p>""" + content + """</p>"""
    return k_points


def create_html(all_elements):
    print('Creating Document')
    last = """</body></html>"""
    message = """<html><head><style>.break-before {page-break-before: always;}</style></head><body>""" + all_elements \
              + last
    f.write(message)
    f.close()
