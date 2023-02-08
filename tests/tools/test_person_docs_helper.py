import pytest

from tools.person_docs_helper import mask_cpf, remove_mask_cpf, validate_cpf


def test_remove_mask_cpf():
    assert "67121228050" == remove_mask_cpf("671.212.280-50")


def test_mask_cpf():
    assert "671.212.280-50" == mask_cpf("67121228050")


@pytest.mark.parametrize("cpf_valid", ["671.212.280-50", "67121228050"])
def test_validate_valid_cpf(cpf_valid):
    assert validate_cpf(cpf_valid) is True


def test_validate_invalid_cpf():
    assert validate_cpf("123.456.789-00") is False
