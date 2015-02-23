# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhenotypeCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhenotypeCategoryGrouping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhenotypeCategoryMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='hp.PhenotypeCategory')),
                ('phenotype', models.ForeignKey(to='hp.Phenotype')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='phenotypecategory',
            name='grouping',
            field=models.ForeignKey(to='hp.PhenotypeCategoryGrouping'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phenotypecategory',
            name='parent',
            field=models.ForeignKey(to='hp.PhenotypeCategory', null=True),
            preserve_default=True,
        ),
    ]
