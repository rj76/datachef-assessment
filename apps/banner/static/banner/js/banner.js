var viewModel = {
    campaignId: ko.observable(),
    numBanners: ko.observable(),
    scenario: ko.observable(),
    error: ko.observable(),
    hasError: ko.observable(false),
    hasBanners: ko.observable(false),
    banners: ko.observableArray(),
    submitCapaign: function() {
        var self = this;
        var url = '/campaign/' + self.campaignId() + '/';
        $.getJSON(url, function(data) {
            self.banners(data.banners);
            self.scenario(data.scenario);
            self.numBanners(data.num_banners);
            self.hasError(false);
            self.hasBanners(data.banners.length > 0);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            if (jqXHR.status === 404) {
                self.error('Campaign not found');
                self.hasError(true);
                self.banners([]);
            }
        });
    }

};

ko.applyBindings(viewModel, document.getElementById('container'));
