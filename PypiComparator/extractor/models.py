from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class BaseModel(models.Model):
    """Project Base model.

    Used to keep track of creation and update dates.

    This model doesn't need to have a screen in admin.
    """

    created_at = models.DateTimeField(_("data de criação"), help_text="", auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(_("data de atualização"), help_text="", auto_now=True, null=True, blank=True)

    class Meta:  # NOQA
        abstract = True


class GlobalProcessorParameters(BaseModel):
    """Project Base Parameter model.

    This model doesn't need to have a screen in admin.
    """

    total_links_to_process_per_chunck = models.IntegerField(_("total_links_to_process_per_chunck"), help_text=_("total_links_to_process_per_chunck"), default=5, null=True, blank=True)
    last_pypi_file_index_list_downloaded = models.DateTimeField(_("last_pypi_file_index_list_downloaded"), help_text="", null=True, blank=True)
    last_pypi_file_links_registered = models.BooleanField(_("last_pypi_file_links_registered"), default=False, help_text=_("last_pypi_file_links_registered"))
    last_pypi_file_links_processed = models.BooleanField(_("last_pypi_file_links_processed"), default=False, help_text=_("last_pypi_file_links_processed"))
    total_links_in_file = models.IntegerField(_("total_links_in_file"), help_text=_("total_links_in_file"), default=0, null=True, blank=True)
    total_links_processed = models.IntegerField(_("total_links_processed"), help_text=_("total_links_processed"), default=0, null=True, blank=True)


class PypiSimpleIndexLinks(BaseModel):
    """Project Base Parameter model.

    This model doesn't need to have a screen in admin.
    """

    href = models.CharField(_("href"), help_text=_("href"), max_length=512, blank=False)
    pypi_project_url = models.CharField(_("pypi_project_url"), help_text=_("pypi_project_url"), max_length=512, blank=True)
    processed_message = models.CharField(_("processed_message"), help_text=_("processed_message"), max_length=512, blank=True)
    processed = models.BooleanField(_("processed"), default=False, help_text=_("processed"))
    successful_processed = models.BooleanField(_("successful_processed"), default=False, help_text=_("successful_processed"))
    home_page_found = models.BooleanField(_("home_page_found"), default=False, help_text=_("home_page_found"))


class PypiProcessedLink(BaseModel):
    """Project Base Parameter model.

    This model doesn't need to have a screen in admin.
    """
    simple_index = models.ForeignKey(
        PypiSimpleIndexLinks,
        verbose_name=_("simple_index"),
        help_text=_("simple_index"),
        on_delete=models.DO_NOTHING,
    )
    homepage_link = models.CharField(_("homepage_link"), help_text=_("homepage_link"), max_length=512, blank=True, null=True)
    github_link = models.CharField(_("github_link"), help_text=_("github_link"), max_length=512, blank=True, null=True)



class PyPiFlapyIndexLinks(BaseModel):
    """Project Base Parameter model.

    This model doesn't need to have a screen in admin.
    """

    url = models.CharField(_("url"), help_text=_("url"), max_length=512, blank=False)
    name = models.CharField(_("name"), help_text=_("name"), max_length=512, blank=True)


class ALIndexLinks(BaseModel):
    """Project Base Parameter model.

    This model doesn't need to have a screen in admin.
    """
    flapy_link = models.ForeignKey(
        PyPiFlapyIndexLinks,
        verbose_name=_("flapy_link"),
        help_text=_("flapy_link"),
        on_delete=models.DO_NOTHING,
        related_name="al_link",
        blank=True,
        null=True
    )
    similar_flapy_link = models.ForeignKey(
        PyPiFlapyIndexLinks,
        verbose_name=_("similar_flapy_link"),
        help_text=_("similar_flapy_link"),
        on_delete=models.DO_NOTHING,
        related_name="similar_al_link",
        blank=True,
        null=True
    )
    url = models.CharField(_("url"), help_text=_("url"), max_length=512, blank=False)
    is_a_project = models.BooleanField(_("is_a_project"), default=False, help_text=_("is_a_project"), blank=True,
                                             null=True)
    can_run_flapy = models.BooleanField(_("can_run_flapy"), default=False, help_text=_("can_run_flapy"), blank=True,
                                             null=True)
    processed_by_flapy_message = models.CharField(_("processed_message"), help_text=_("processed_message"), max_length=512, blank=True, null=True)
    short_description = models.CharField(_("short_description"), help_text=_("short_description"), max_length=512, blank=True, null=True)
    processed_by_flapy = models.BooleanField(_("processed"), default=False, help_text=_("processed"), blank=True, null=True)
