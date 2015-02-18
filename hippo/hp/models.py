from django.db import models


class Phenotype(models.Model):
    """
    Phenotypic abnormality
    """
    code = models.CharField(max_length=50, db_index=True, unique=True)
    label = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return " ".join((self.code, self.label))


class PhenotypeSubclass(models.Model):
    """
    This models phenotype class heirachy -- rdfs:subClassOf
    """
    parent = models.ForeignKey(Phenotype, related_name="subclasses")
    child = models.ForeignKey(Phenotype, related_name="superclasses")

    class Meta:
        unique_together = (("parent", "child"),)
        index_together = (("parent", "child"),)

    def __unicode__(self):
        return "%s > %s" % (self.parent.code, self.child.code)


class PhenotypeSynonym(models.Model):
    """
    This models the following relations of oboInOwl
     - hasNarrowSynonym
     - hasRelatedSynonym
     - hasExactSynonym
    """
    phenotype = models.ForeignKey(Phenotype, related_name="synonyms")
    synonym = models.CharField(max_length=200)
    SYNONYM_TYPES = ((1, "Exact"), (2, "Narrow"), (3, "Related"))
    type = models.PositiveSmallIntegerField(choices=SYNONYM_TYPES, default=1)

    # class Meta:
    #     unique_together = (("phenotype", "synonym"),)


class AlternativeId(models.Model):
    phenotype = models.ForeignKey(Phenotype)
    code = models.CharField(max_length=50)

