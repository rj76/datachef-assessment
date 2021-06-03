import pytest

from apps.banner.batch import Batch
from apps.banner import models


@pytest.mark.django_db
class TestImport:
    def test_import(self):
        batch = Batch()
        batch.import_impressions(1)
        batch.import_clicks(1)
        batch.import_conversions(1)

        assert models.Impression.objects.count() == 20040
        assert models.Click.objects.count() == 50000
        assert models.Conversion.objects.count() == 6000
