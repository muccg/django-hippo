# load HPO category information sourced from Phenotips

from pkg_resources import resource_filename
from optparse import make_option
from django.core.management.base import BaseCommand
from ...ontology import load_phenotips_categories


class Command(BaseCommand):
    help = 'Imports the HP in OWL format'

    def handle(self, *args, **options):
        filename = resource_filename('hippo', 'contrib/PhenoTips/Generic phenotype configuration.xml')
        load_phenotips_categories(filename)
