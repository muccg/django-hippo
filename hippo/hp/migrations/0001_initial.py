# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativeId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phenotype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=50, db_index=True)),
                ('label', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhenotypeSubclass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('child', models.ForeignKey(related_name='superclasses', to='hp.Phenotype')),
                ('parent', models.ForeignKey(related_name='subclasses', to='hp.Phenotype')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhenotypeSynonym',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('synonym', models.CharField(max_length=200)),
                ('type', models.PositiveSmallIntegerField(default=1, choices=[(1, b'Exact'), (2, b'Narrow'), (3, b'Related')])),
                ('phenotype', models.ForeignKey(related_name='synonyms', to='hp.Phenotype')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='phenotypesubclass',
            unique_together=set([('parent', 'child')]),
        ),
        migrations.AlterIndexTogether(
            name='phenotypesubclass',
            index_together=set([('parent', 'child')]),
        ),
        migrations.AddField(
            model_name='alternativeid',
            name='phenotype',
            field=models.ForeignKey(to='hp.Phenotype'),
            preserve_default=True,
        ),
    ]
