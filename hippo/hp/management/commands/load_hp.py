from optparse import make_option
from django.core.management.base import BaseCommand
from ...ontology import load_hp_owl, Phenotype
from ...hpo_download import download_owl


class Command(BaseCommand):
    args = 'hp.owl'
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

        if len(args) > 0:
            filename = args[0]
        else:
            fd = download_owl()
            filename = fd.name

        load_hp_owl(filename)
