/**
 * Sends requests to the server, and handles the responses.
 * This class has only one useful method, postFetch.
 * @param {OutputHandler} _ohInstance - The output handler this request handler will use to throw errors.
 * @constructor
 */
let RequestHandler = function (_ohInstance = null) {
    let _THIS = this;

    _THIS.defaultOnSuccess = function (text) {
        if (_ohInstance) _ohInstance.print('XHRResponse::' + text);
        else console.log('XHRResponse::' + text);
    };

    _THIS.defaultOnFailure = function (error) {
        if (_ohInstance) _ohInstance.error('XHRError::' + error);
        else console.log('XHRResponse::' + text);
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
                    if (text && onSuccess && onSuccess.call) onSuccess(text);
                } else {
                    if (onError && onError.call) onError(text ? text : response.statusText);
                }
            });
        }).catch(function (error) {
            if (onError && onError.call) onError(error.message);
        });
    };
};
