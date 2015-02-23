from lxml import etree as etree
from rdflib import Graph
from rdflib.term import URIRef
from django.db import transaction
import json

from .models import Phenotype, PhenotypeSubclass, PhenotypeSynonym, \
        PhenotypeCategoryGrouping, PhenotypeCategory, PhenotypeCategoryMember

import logging
logger = logging.getLogger(__name__)


@transaction.atomic
def load_hp_owl(filename):
    if Phenotype.objects.count() > 0:
        logger.debug("Skipping load of %s, phenotypes already loaded in DB." % (filename))
        return
    logger.debug("Loading %s" % filename)
    g = Graph()
    g.parse(filename, format="xml")
    # HP:0000118 is the phenotypic abnormality
    base = URIRef(u'http://purl.obolibrary.org/obo/HP_0000118')

    id_mapping = {}

    def add_phenotype(id, label):
        # logger.debug("  adding %s %s" % (id, label))
        ph, _ = Phenotype.objects.get_or_create(code=id, label=label)
        id_mapping[ph.code] = ph.id

    logger.debug("Querying base")
    result = g.query(
        """SELECT ?id ?label
           WHERE {
               ?base rdfs:label ?label ;
                     oboInOwl:id ?id .
        }""", initBindings={"base": base})

    for row in result:
        add_phenotype(*row)

    logger.debug("Querying classes")
    result = g.query("""
SELECT ?id ?label
   WHERE {
      ?cls a owl:Class ;
           rdfs:subClassOf+ ?base ;
           rdfs:label ?label ;
           oboInOwl:id ?id .
   }""", initBindings={"base": base})

    for row in result:
        add_phenotype(*row)

    logger.debug("Querying relationships")
    result = g.query("""
SELECT DISTINCT ?clsId ?subClsId
  WHERE {
    ?cls a owl:Class .
    ?subCls rdfs:subClassOf ?cls .
    ?cls oboInOwl:id ?clsId .
    ?subCls oboInOwl:id ?subClsId .
  }""")

    for (cls_id, subcls_id) in result:
        if cls_id in id_mapping and subcls_id in id_mapping:
            # logger.debug("  adding subclass %s of %s" % (subcls_id, cls_id))
            PhenotypeSubclass.objects.get_or_create(parent_id=id_mapping[cls_id], child_id=id_mapping[subcls_id])

    logger.debug("Synonyms")
    result = g.query("""
SELECT ?id ?rel ?syn
  WHERE {
    ?subCls rdfs:subClassOf [
        a owl:Class ;
        oboInOwl:id ?id ;
        ?rel ?syn ] .
    FILTER (?rel in (oboInOwl:hasExactSynonym, oboInOwl:hasNarrowSynonym, oboInOwl:hasRelatedSynonym))
  }""")

    def typenum(rel):
        name = rel.split("#")[1]
        names = ["hasExactSynonym", "hasNarrowSynonym", "hasRelatedSynonym"]
        return names.index(name) + 1

    for (id, rel, syn) in result:
        if id in id_mapping:
            # logger.debug("  adding synonym for %s: %s" % (id, syn[:25]))
            PhenotypeSynonym.objects.get_or_create(phenotype_id=id_mapping[id], synonym=syn, type=typenum(rel))


@transaction.atomic
def load_phenotips_categories(filename):
    def add_grouping(name):
        obj, _ = PhenotypeCategoryGrouping.objects.get_or_create(name=name)
        return obj

    def add_category(grp, name, parent_id):
        obj, _ = PhenotypeCategory.objects.get_or_create(name=name, grouping=grp, parent=parent_id)
        return obj

    def add_root_category(grp, obj):
        assert(obj['type'] == 'section')
        name = obj['title']
        member_terms = obj['categories']
        category = add_category(grp, name, None)
        print(category)

    with open(filename, 'rU') as fd:
        et = etree.parse(fd)
        text = et.xpath('//content/text()')[0]
    groupings = json.loads(text)
    for name in groupings:
         grp = add_grouping(name)
         for category in groupings[name]:
             add_root_category(grp, category)


