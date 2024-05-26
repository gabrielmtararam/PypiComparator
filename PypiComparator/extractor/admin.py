from django.contrib import admin
from extractor import models as mod
from extractor import forms as forms
from djangoql.admin import DjangoQLSearchMixin
from simple_history.admin import SimpleHistoryAdmin
# flapy_link = None and similar_flapy_link = None 
# ignorei links em chines o indiano ou russo que ou tudo estava sem traduzir ou vi que era uma biblioteca, ignorei bibliotecas de auxilio de sql, mas mantive bancos de dados
# ignorei link com nome e documento inapropriado The Fuck app, ignorei bibliotecas de analise e conversao de audio
# deixei como não outras listas
# deixei como unknow os n sdks, scripts de tradução, engines, n CPython (variações como ironpython), sistema de auto complete, comandos de detecção (ex nude.py), servidor, gerador de documentação, linha de comando para acessar servidor da amazon,
# deixei como unknow dh-virtualenv, py spy e memory_profiler que roda e analisa outros arquivos python, python-hunter debugger, analisador de processos manhole
# deixei como unknow bibliotecas de conversão de texto, que funcionam por si só, mantive tb auto complete, mantive linters, mantive cms
# deixei como sim ferramentas com interface grafica
# plugins fui vendo se era só algo que facilitava a criação de uma classe, ou criava um componente visual, ou algo mais complexo, maioria no unknow
# mantenho projetos depreciados



# testar django-remote-forms
# testar https://github.com/pallets/markupsafe
# pode ter algo util aqui Awesome Sphinx (Python Documentation Generator)
# virtualenv alternativo
# psutil (process and system utilities) system utilization (CPU, memory, disks, network, sensors) in Python
# pyinfra automates infrastructure using Python
# 	https://github.com/dcramer/django-devserver
# verificar que funções um processo está executando u/lptrace
# 	https://github.com/scottrogowski/code2flow graficos de codigo
#  PyPattyrn is a python package aiming to make it easier and faster to implement design patterns into your own projects.

# ./flapy.sh run --out-dir example_results flapy_input_example.csv 1
# ./flapy.sh parse ResultsDirCollection --path example_results get_tests_overview _df to_csv --index=false | visidata --filetype=csv
#
#
class AdvancedQueryAdmin(DjangoQLSearchMixin):
    """
    Added advanced query to admin.

    Use this class on the first place on all admin extensions.

    This admin add the DjangoQLSearchMixin class, this class implements
    a SQL like query on all admins. That reduced the query time on big tables
    to 10 minutes to 8 seconds.
    """

    djangoql_completion_enabled_by_default = True
    suggest_options = True


# Register your models here.
@admin.register(mod.PypiSimpleIndexLinks)
class PypiSimpleIndexLinksAdmin(SimpleHistoryAdmin, DjangoQLSearchMixin):
    """StationCodeType model admin."""

    form = forms.PypiSimpleIndexLinksForm
    # list_display = (
    #     "station",
    #     "code_type",
    #     "code",
    # )
    # autocomplete_fields = (
    #     "code_type",
    #     "station",
    # )
    # list_filter = ("code_type", "station__organization")

@admin.register(mod.PypiProcessedLink)
class PypiProcessedLinkAdmin(SimpleHistoryAdmin, DjangoQLSearchMixin):
    """StationCodeType model admin."""

    form = forms.PypiProcessedLinkForm
    # list_display = (
    #     "station",
    #     "code_type",
    #     "code",
    # )
    # autocomplete_fields = (
    #     "code_type",
    #     "station",
    # )
    # list_filter = ("code_type", "station__organization")


@admin.register(mod.GlobalProcessorParameters)
class GlobalProcessorParametersAdmin(SimpleHistoryAdmin, DjangoQLSearchMixin):
    """StationCodeType model admin."""

    form = forms.GlobalProcessorParametersForm
    # list_display = (
    #     "station",
    #     "code_type",
    #     "code",
    # )
    # autocomplete_fields = (
    #     "code_type",
    #     "station",
    # )
    # list_filter = ("code_type", "station__organization")


@admin.register(mod.PyPiFlapyIndexLinks)
class PyPiFlapyIndexLinksAdmin(SimpleHistoryAdmin, DjangoQLSearchMixin):
    """StationCodeType model admin."""

    form = forms.PyPiFlapyIndexLinksForm
    # list_display = (
    #     "station",
    #     "code_type",
    #     "code",
    # )
    # autocomplete_fields = (
    #     "code_type",
    #     "station",
    # )
    # list_filter = ("code_type", "station__organization")


@admin.register(mod.ALIndexLinks)
class ALIndexLinksAdmin(DjangoQLSearchMixin, SimpleHistoryAdmin):
    """StationCodeType model admin."""

    form = forms.ALIndexLinksForm
    list_display = (
        "pk",
        "flapy_link",
        "similar_flapy_link",
        "url",
        "is_a_project",
        "processed_by_flapy_message",
        "processed_by_flapy",
        "short_description",
        "can_run_flapy",
    )
    list_editable = ['is_a_project', 'short_description', 'can_run_flapy']
    # autocomplete_fields = (
    #     "code_type",
    #     "station",
    # )
    # list_filter = ("code_type", "station__organization")

@admin.register(mod.ALIndexLinksAnalysis)
class ALIndexLinksAnalysisAdmin(DjangoQLSearchMixin, SimpleHistoryAdmin):
    """StationCodeType model admin."""

    form = forms.ALIndexLinksAnalysisForm
    list_display = (
        "pk",
        "flapy_link",
        "similar_flapy_link",
        "url",
        "is_a_project",
        "processed_by_flapy_message",
        "processed_by_flapy",
        "short_description",
        "can_run_flapy",
        "processed_by_flapy_400",
    )
    list_editable = ['is_a_project', 'short_description', 'processed_by_flapy_400', 'can_run_flapy', 'processed_by_flapy']
    # autocomplete_fields = (
    #     "code_type",
    #     "station",
    # )
    # list_filter = ("code_type", "station__organization")