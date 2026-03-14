searchApp.factory("SearchService", function ($window, $q, HttpService, SearchParams) {
    return {
        search: function (data) {
            Notifications.persist("Performing search...");
            SearchParams.setParams(data);

            return HttpService.post({
                url: "?" + encodeURIComponent(SearchParams.asQueryString()),
            }).then(
                function (results) {
                    $window.SearchApi.currentSearch.groupBy = _.isUndefined(data.groupBy) ? "" : data.groupBy;
                    $window.SearchApi.currentSearch.buildResults(results);

                    return results;
                },
                function (err) {
                    $window.SearchApi.currentSearch.buildResults([]);

                    return $q.reject(err);
                }
            ).finally(function () {
                Notifications.closeLoading();
            });
        }
    };
});
