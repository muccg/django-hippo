from pkg_resources import resource_filename
from optparse import make_option
from django.core.management.base import BaseCommand
from ...ontology import load_hp_owl, Phenotype
import hippo
import os


class Command(BaseCommand):
    help = 'Imports the HP in OWL format'

    option_list = BaseCommand.option_list + (
        make_option(
            '--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Clear existing records before importing'),)

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Removing %d objects" % Phenotype.objects.count())
            Phenotype.objects.all().delete()

        filename = os.path.join(hippo.__path__[0], resource_filename('hippo', 'contrib/HPO/hp.owl'))
        load_hp_owl(filename)
