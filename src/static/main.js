const WATER_DENSITY = 1000; // kilogram / meter^3
const WATER_DRAG_COEFFICIENT = 1.2; // unitless
const GRAVITATIONAL_ACCELERATION = 9.81; // meter / second^2

const ROV_MAX_FORCE = 58; // newton
const ROV_WEIGHT_IN_WATER = 9.8; // newton
const ROV_DRAG_FORCE = 0; // newton

const REFRESH_TIME = 1000;

let oh = new OutputHandler();
let rh = new RequestHandler(oh);
let gh = new GamepadHandler();

fillMappings(gh);
gh.initializeGamepadIndex();

$(function () {
    setupGamepadMain();
    $('.control-box button').prop('disabled', 'disabled'); // Direction buttons cannot be used.
    rh.postFetch('/get_mode', '', function (result) {
        $('#' + result).addClass('active');
    });

    window.setInterval(function () {
        if ($('#refresh_auto')[0].checked) {
            rh.postFetch('/flush_buffer', '', function (response) {
                mapString(response, oh);
            });
        }
    }, REFRESH_TIME);
    $('#refresh_once').click(function () {
        rh.postFetch('/flush_buffer', '');
    });

    $('.mode').click(function () {
        $('.mode').removeClass('active');
        $(this).addClass('active');
    });
    $('#mode_free').click(function () {
        rh.postFetch('/mode_free', '', function() {});
    });
    $('#mode_line').click(function () {
        rh.postFetch('/mode_line', '', function() {});
    });
    $('#mode_micro').click(function () {
        rh.postFetch('/mode_micro', '', function() {});
    });

    $('#cannon_calc').submit(function () {
        let l = parseFloat(this.cannon_l.value);
        let r1 = parseFloat(this.cannon_r1.value);
        let r2 = parseFloat(this.cannon_r2.value);
        let r3 = parseFloat(this.cannon_r3.value);
        let p = parseFloat(this.cannon_p.value);
        if (!(r3 > r1 && r3 > r2)) {
            oh.error('R3 has to be biggest radius.');
            return false;
        }
        if (!(r2 < r1 && r2 < r3)) {
            oh.error('R2 has to be the smallest radius.');
            return false;
        }
        if (!(l > 0)) {
            oh.error('Length has to be a positive number.');
            return false;
        }
        if (!(p > WATER_DENSITY)) {
            oh.error(`Cannon density has to be higher than water density (whcih is ${WATER_DENSITY}).`);
            return false;
        }
        let volume_cannon = (((r1 * l / (r3 - r1) + l) * r3**2 - r1**3 * l / (r3 - r1)) / 3 - r2**2 * l) * Math.PI;
        let f_weight_cannon = (p - WATER_DENSITY) * volume_cannon * GRAVITATIONAL_ACCELERATION;
        let f_drag_cannon_velocity_coefficient = 0.5 * WATER_DENSITY * WATER_DRAG_COEFFICIENT * l * (r1 + r3) / 2;
        let f_drag_Cannon = ROV_MAX_FORCE - ROV_DRAG_FORCE - ROV_WEIGHT_IN_WATER - f_weight_cannon;
        let rov_velocity =  f_drag_Cannon / f_drag_cannon_velocity_coefficient;

        oh.print(
            `Cannon has volume ${volume_cannon} m<sup>3</sup>\n` +
            `and needs force ${f_weight_cannon} N to lift its weight.\n` +
            `The drag force of the cannon is ${f_drag_cannon} N so the ROV\n` +
            `can at most run with a velocity of ${rov_velocity} while attempting\n` +
            `to lift this cannon.`
        );
        return false;
    });
});