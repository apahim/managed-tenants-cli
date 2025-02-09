import pytest

from managedtenants.core.addons_loader.addon import Addon
from tests.testutils.addon_helpers import addon_with_imageset  # noqa: F401
from tests.testutils.addon_helpers import (  # noqa: F401
    addon_with_deadmanssnitch,
    addon_with_indeximage,
    addon_with_indeximage_path,
    addon_with_pagerduty,
    addon_with_secrets_path,
)


@pytest.mark.parametrize(
    "addon_str",
    [
        "addon_with_indeximage",
        "addon_with_imageset",
        "addon_with_deadmanssnitch",
        "addon_with_pagerduty",
    ],
)
def test_addon_sss_object(addon_str, request):
    """Test that addon metadata is loaded."""
    addon = request.getfixturevalue(addon_str)
    sss_walker = addon.sss.walker()
    catalogue_src_obj = sss_walker["sss_deploy"]["spec"]["resources"][
        "CatalogSource"
    ]
    assert len(catalogue_src_obj) == 1
    name, data = catalogue_src_obj[0]
    assert name is not None
    assert data is not None
    assert data["spec"]["image"] is not None
    assert data["spec"].get("secrets") is None


def test_additional_catalog_srcs():
    addon = Addon(addon_with_indeximage_path(), "integration")
    sss_walker = addon.sss.walker()
    catalogue_src_objs = sss_walker["sss_deploy"]["spec"]["resources"][
        "CatalogSource"
    ]
    assert len(catalogue_src_objs) == 2
    for catalog_obj in catalogue_src_objs:
        name, data = catalog_obj
        assert name is not None
        assert data is not None
        assert data["spec"]["image"] is not None


def test_pull_secret_injection():
    addon = Addon(addon_with_secrets_path(), "stage")
    sss_walker = addon.sss.walker()
    catalogue_src_objs = sss_walker["sss_deploy"]["spec"]["resources"][
        "CatalogSource"
    ]
    assert len(catalogue_src_objs) == 2
    for catalog_obj in catalogue_src_objs:
        name, data = catalog_obj
        assert name is not None
        assert data is not None
        assert data["spec"]["image"] is not None
        assert len(data["spec"]["secrets"]) == 1
        assert data["spec"]["secrets"][0] == addon.metadata["pullSecretName"]

    # Addon with legacy pull secret attribute
    addon = Addon(addon_with_indeximage_path(), "integration")
    sss_walker = addon.sss.walker()
    catalogue_src_objs = sss_walker["sss_deploy"]["spec"]["resources"][
        "CatalogSource"
    ]
    assert len(catalogue_src_objs) == 2
    for catalog_obj in catalogue_src_objs:
        name, data = catalog_obj
        assert name is not None
        assert data is not None
        assert data["spec"]["image"] is not None
        assert len(data["spec"]["secrets"]) == 1
        # Ensure name is the hardcoded value in the SSS.
        assert data["spec"]["secrets"][0] == "addon-pullsecret"
