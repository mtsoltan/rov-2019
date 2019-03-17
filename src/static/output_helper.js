function mapString(str, outputHandler) {
    let letter = str[0];
    switch (letter) {
        case 'M':
            if(parseInt(str.substr(1))) {
                $('#sensor_metal').addClass('active').find('span').text('Metal');
            } else {
                $('#sensor_metal').removeClass('active').find('span').text('Not Metal');
            }
            break;
        case 'E':
            outputHandler.print(str.substr(1));
            break;
    }
}