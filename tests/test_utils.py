from app.operations.utils import prepare_bundle


def test_prepare_bundle():
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "/QuestionnaireResponse?subject={{%CurrentAppointmentId}}",
        }
    }

    assert prepare_bundle(bundle_entry, {}) == {
        "request": {
            "method": "GET",
            "url": "/QuestionnaireResponse?subject=",
        }
    }


def test_multuple_var_in_one_line():
    # Ref https://github.com/beda-software/aidbox-sdc/issues/1
    bundle_entry = {
        "request": {
            "method": "GET",
            "url": "Slot?specialty={{%specialty}}&start={{%start}}&status=free",
        }
    }

    env = {
        "specialty": "394586005",  # Gynecology
        "start": "2021-01-01",
    }
    assert prepare_bundle(bundle_entry, env) == {
        "request": {
            "method": "GET",
            "url": "Slot?specialty=394586005&start=2021-01-01&status=free",
        }
    }
