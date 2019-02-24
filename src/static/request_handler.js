let RequestHandler = function (_ohInstance) {
    let _THIS = this;

    _THIS.defaultOnSuccess = function (text) {
        if (_ohInstance) _ohInstance.print('XHRResponse::' + text);
    };
    _THIS.defaultOnFailure = function (error) {
        if (_ohInstance) _ohInstance.error('XHRError::' + error);
    };

    _THIS.postFetch = function (url, body, onSuccess = _THIS.defaultOnSuccess, onError = _THIS.defaultOnFailure) {
        let headers = new Headers();
        headers.append('X-Requested-With', 'XMLHttpRequest');
        fetch(url, {
            method: 'POST',
            headers: headers,
            body: body,
        }).then(function (response) {
            response.text().then(function (text) {
                if (response.status === 200) {
                    if (text) {
                        if (onSuccess && onSuccess.call) onSuccess(text)
                    }
                } else {
                    if (text) {
                        if (onError && onError.call) onError(text);
                    } else {
                        if (onError && onError.call) onError(response.statusText);
                    }
                }
            });
        }).catch(function (error) {
            if (onError && onError.call) onError(error.message);
        });
    }
};
