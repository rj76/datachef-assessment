import pytest

from apps.banner.batch import Batch
from apps.banner import models


@pytest.mark.django_db
class TestImport:
    def test_import(self):
        batch = Batch()
        batch.import_all(test=True)

        assert models.Impression.objects.count() == 9
        assert models.Click.objects.count() == 9
        assert models.Conversion.objects.count() == 9

        # run batch again and the counts should be the same
        # except impressions, they should be doubled
        batch.import_all(test=True)
        assert models.Impression.objects.count() == 18
        assert models.Click.objects.count() == 9
        assert models.Conversion.objects.count() == 9
