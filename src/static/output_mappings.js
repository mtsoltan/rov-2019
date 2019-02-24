function mapString(str, outputHandler) {
            console.log(str);
    let letter = str[0];
    switch (letter) {
        case 'M':
            if(parseInt(str.substr(1))) {
                $('#sensor_metal').addClass('active').text('Metal');
            } else {
                $('#sensor_metal').removeClass('active').text('Not Metal');
            }
            break;
        case 'E':
            outputHandler.print(str.substr(1));
            break;
    }
}