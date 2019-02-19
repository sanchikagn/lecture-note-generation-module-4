import math

from owlready2 import *
import pandas as pd


class Course(Thing):
    namespace = None

    def __init__(self):
        self.course_world = World()
        self.course_world.get_ontology("resources/ontology/english.owl").load()
        # sync_reasoner()
        self.graph = self.course_world.as_rdflib_graph()
        # self.topic_entities = pd.DataFrame(columns=['topic', 'keywords', 'entity', 'facts'])
        self.related_kps = pd.DataFrame(columns=['topic', 'keywords', 'entity', 'facts'])

    # Searching for topics discussed in lecture
    def search_topics(self, topics, title_keywords):
        print('Searching Topics')
        query = """PREFIX my: <http://www.itfac.lk/kasumi/ontologies/english.owl#>
                                     PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                     SELECT DISTINCT ?iri ?fact
                                     WHERE{{
                                            ?iri ?p ?o.
                                            ?iri my:hasFact ?fact
                                            FILTER regex(str(?iri), '""" + title_keywords + """', 'i') }
                                     UNION{
                                           ?iri rdf:type ?s.
                                           ?iri my:hasFact ?fact.
                                           ?s rdf:type owl:Class.
                                           FILTER regex(str(?s), '""" + title_keywords + """', 'i')
                                           }}"""
        results = self.graph.query(query)
        for item in results:
            fact = str(item[1].toPython())
            # print(fact)
            class_entity = str(item['iri'].toPython())
            class_entity = re.sub(r'.*#', "", class_entity)
            self.topic_entities = self.topic_entities.append({'topic': topics, 'keywords': title_keywords,
                                                              'entity': class_entity,'facts': fact}, ignore_index=True)
            # print(self.topic_entities)
            # print(item)

    def search_features(self, title_keywords):
        print('Searching Topics')
        related_facts = pd.DataFrame(columns=['entity', 'facts'])
        query = """PREFIX my: <http://www.itfac.lk/kasumi/ontologies/english.owl#>
                                     PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                     SELECT DISTINCT ?iri ?fact
                                     WHERE{{
                                            ?iri ?p ?o.
                                            ?iri my:hasActivity ?activity.
                                            ?activity my:hasTask ?task.
                                            ?task my:hasFact ?fact.
                                            FILTER regex(str(?iri), '""" + title_keywords + """', 'i')
                                            FILTER regex(str(?r), '""" + title_keywords + """', 'i')}
                                     UNION{
                                           ?iri rdf:type ?s.
                                           ?iri my:hasFact ?fact.
                                           ?s rdf:type owl:Class.
                                            FILTER regex(str(?s), '""" + title_keywords + """', 'i') }
                                     UNION{
                                            ?iri rdf:type ?k.
                                                   ?k rdfs:subClassOf ?s.
                                                   ?iri my:hasFact ?fact.
                                                   ?s rdf:type owl:Class.
                                                   FILTER regex(str(?s), '""" + title_keywords + """', 'i') }
                                             UNION{
                                                   ?iri ?p ?o.
                                                    ?iri my:hasActivity ?activity.
                                                    ?activity my:hasTask ?task.
                                                    ?task my:hasFact ?fact.
                                                    FILTER regex(str(?fact), '""" + title_keywords + """', 'i')}
                                      }"""
        results = self.graph.query(query)
        for item in results:
            fact = str(item[1].toPython())
            # print(fact)
            class_entity = str(item['iri'].toPython())
            class_entity = re.sub(r'.*#', "", class_entity)
            if class_entity.isnumeric():
                continue
            else:
                related_facts = related_facts.append({'entity': class_entity, 'facts': fact}, ignore_index=True)
            # print(self.topic_entities)
            # print(item)
        return related_facts

    # Searching for related Knowledge Points
    def search_kps(self, topic, title_keywords):
        print('Searching Knowledge Points')
        query = """PREFIX my: <http://www.itfac.lk/kasumi/ontologies/english.owl#> 
                                             PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                             SELECT DISTINCT ?iri ?p ?o
                                             WHERE{
                                             ?iri ?p ?o.
                                             FILTER regex(str(?iri), '""" + title_keywords + """', 'i')
                                             }"""
        results = self.graph.query(query)
        for item in results:
            class_entity = str(item['iri'].toPython())
            class_entity = re.sub(r'.*#', "", class_entity)
            # print(class_entity)
            data = str(item['o'].toPython())
            # data = re.sub(r'.*#', "", data)
            self.related_kps = self.related_kps.append({'keyword': topic, 'keywords': title_keywords,
                                                        'entity': class_entity, 'facts': data}, ignore_index=True)
            # print(data)
