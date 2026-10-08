from pathlib import Path

from tutor import hooks


PLUGIN_ROOT = Path(__file__).resolve().parent
TEMPLATE_ROOT = PLUGIN_ROOT / "zz_kkux_certificates_templates"


hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(str(TEMPLATE_ROOT))

# Renders:
# templates/openedx/... → $(tutor config printroot)/env/build/openedx/...
hooks.Filters.ENV_TEMPLATE_TARGETS.add_item(
    ("openedx", "build")
)


CERTIFICATE_SETTINGS = """
FEATURES["CERTIFICATES_HTML_VIEW"] = True
FEATURES["CUSTOM_CERTIFICATE_TEMPLATES_ENABLED"] = True
"""


hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "openedx-lms-common-settings",
            CERTIFICATE_SETTINGS,
        ),
        (
            "openedx-cms-common-settings",
            CERTIFICATE_SETTINGS,
        ),
        (
            "openedx-dockerfile-pre-assets",
            r"""
# KKU certificate customization layered on top of Indigo.
USER root

RUN mkdir -p \
    /openedx/themes/indigo/lms/templates/certificates \
    /openedx/themes/indigo/lms/static/certificates/images \
    /tmp/certificates

COPY --chown=app:app \
    ./kkux-certificates/valid.html \
    /openedx/themes/indigo/lms/templates/certificates/valid.html

COPY --chown=app:app \
    ./kkux-certificates/kkux_cert_background.png.b64 \
    /tmp/kkux_cert_background.png.b64

RUN base64 -d \
      /tmp/kkux_cert_background.png.b64 \
      > /openedx/themes/indigo/lms/static/certificates/images/kkux_cert_background.png \
    && rm /tmp/kkux_cert_background.png.b64 \
    && chown -R app:app \
         /openedx/themes/indigo/lms/templates/certificates \
         /openedx/themes/indigo/lms/static/certificates \
         /tmp/certificates

USER app
""",
        ),
    ]
)