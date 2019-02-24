let OutputHandler = function () {
    let _THIS = this;
    _THIS.DEFAULT_PROPERTY_COLOR = '#1b3f80';
    _THIS.DEFAULT_STRING_COLOR = '#075037';
    _THIS.DEFAULT_NUMBER_COLOR = '#460a9c';
    _THIS.DEFAULT_BOOLEAN_COLOR = '#9c4a00';
    _THIS.DEFAULT_ERROR_COLOR = '#500000';

    _THIS.color = function (data, color) {
        return `<span style="color: ${color}">${data}</span>`;
    };

    _THIS.pad = function (length) {
        let rv = '';
        for(let j = 0; j < length; j++) rv += '    ';
        return rv;
    };

    _THIS.stringify = function (arr, level) {
        let dumped_text = '';
        if(!level) level = 0;
        let level_padding = _THIS.pad(level + 1);
        if(typeof(arr) == 'object') {
            if(level === 0) dumped_text += '{\n';
            for(let item in arr) {
                let value = arr[item];
                if(typeof(value) == 'object') {
                    dumped_text += level_padding + _THIS.color('"' + item + '"', _THIS.DEFAULT_PROPERTY_COLOR) + ' : {';
                    let next_stringify = _THIS.stringify(value,level+1);
                    if (next_stringify) dumped_text += '\n' + next_stringify;
                    else dumped_text += '}\n';
                } else if (typeof(value) != 'function') {
                    dumped_text += level_padding + _THIS.color('"' + item + '"', _THIS.DEFAULT_PROPERTY_COLOR) + ' : ' + _THIS.stringify(value) + '\n';
                }
            }
            if (dumped_text) dumped_text += _THIS.pad(level) + '}\n';
            else return '';
        } else {
            let type = typeof(arr);
            if (type === 'boolean') {
                arr = arr ? 'true' : 'false';
                arr = _THIS.color(arr, _THIS.DEFAULT_BOOLEAN_COLOR);
            } else if (type === 'string') {
                arr = _THIS.color('"' + arr + '"', _THIS.DEFAULT_STRING_COLOR);
            } else if (type === 'number') {
                arr = _THIS.color(arr, _THIS.DEFAULT_NUMBER_COLOR);
            }
            dumped_text = type + "(" + arr + ")";
        }
        return dumped_text;
    };

    _THIS.print = function (data, color = '') {
        if (typeof(data) === 'object') data = _THIS.stringify(data);
        if (typeof(data) === 'boolean') data = data ? 'true' : 'false';
        if (color !== '') data = _THIS.color(data, color);
        $('#stdout').append(new Date().getTime() + '\n' + data + '<hr>');
        return true;
    };

    _THIS.error = function (data) {
        return _THIS.print(data, _THIS.DEFAULT_ERROR_COLOR);
    };
};
