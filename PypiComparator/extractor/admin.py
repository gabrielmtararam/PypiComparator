from django.contrib import admin
from extractor import models as mod
from extractor import forms as forms
from djangoql.admin import DjangoQLSearchMixin
from simple_history.admin import SimpleHistoryAdmin

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