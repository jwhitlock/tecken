# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.

from django.urls import register_converter, path
from django.conf import settings

from . import views


class _Converter:
    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class MixedCaseHexConverter(_Converter):
    regex = "[0-9A-Fa-f]+"


class LegacyProductPrefixesConverter(_Converter):
    """This is a relic from the past when the symbols were prefixed by
    the products we had at the time.
    To be safe (Jan 2018), let's just keep this around as a valid URL.
    """

    regex = "({})".format("|".join(settings.DOWNLOAD_LEGACY_PRODUCTS_PREFIXES))


register_converter(MixedCaseHexConverter, "hex")
register_converter(LegacyProductPrefixesConverter, "legacyproduct")


app_name = "download"

urlpatterns = [
    path("missingsymbols.csv", views.missing_symbols_csv, name="missing_symbols_csv"),
    path(
        "try/<str:symbol>/<hex:debugid>/<str:filename>",
        views.download_symbol_try,
        name="download_symbol_try",
    ),
    path(
        "<legacyproduct>/<str:symbol>/<hex:debugid>/<str:filename>",
        views.download_symbol_legacy,
        name="download_symbol_legacy",
    ),
    path(
        "<str:symbol>/<hex:debugid>/<str:filename>",
        views.download_symbol,
        name="download_symbol",
    ),
]
