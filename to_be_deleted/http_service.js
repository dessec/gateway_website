angular.module("core").factory("HttpService", function ($http, $q) {
    var resolving = false;

    var get = function (config) {
        return buildRequestPromise(config);
    };

    var post = function (config) {
        config.method = "POST";
        return buildRequestPromise(config);
    };

    var put = function (config) {
        config.method = "PUT";
        return buildRequestPromise(config);
    };

    var doDelete = function (config) {
        config.method = "DELETE";
        return buildRequestPromise(config);
    };

    var isZsMessagesUndefined = function () {
        return typeof zeMessages === "undefined";
    };

    var buildRequestPromise = function (config) {
        config = normaliseConfig(config);

        if (window.logger) {
            logger.dismissActionMessages();
        }

        if (config.loader.show && !resolving && window.Communications !== undefined && Communications.getServiceType) {
            Communications[Communications.getServiceType(config.loader.type)](config.loader.message);
        }

        var deferred = $q.defer();
        $http(config).then(
            function (results) {
                deferred.resolve(results.data);
            },
            function (err) {
                if (window.logger) {
                    logger.notifyError(err.data);
                }

                if (!isZsMessagesUndefined()) {
                    zsMessages[config.loader.type](false);
                }

                deferred.reject(err.data);
            }
        ).finally(function () {
            if (!isZsMessagesUndefined() && config.loader.show && !resolving) {
                zsMessages.loading(false);
            }
        });

        return deferred.promise;
    };

    var normaliseConfig = function (config) {
        var defaultConfig = {
            method: "GET",
            url: "",
            cache: false,
            loader: {
                show: true,
                type: "loading",
                message: "Loading..."
            }
        };

        config.loader = _.defaults(config.loader || {}, defaultConfig.loader);

        return _.defaults(config, defaultConfig);
    };

    var setResolving = function (val) {
        resolving = val;
    };

    return {
        get: get,
        post: post,
        put: put,
        delete: doDelete,
        setResolving: setResolving
    };
});
