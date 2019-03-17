const DEBUG_GAMEPAD_HANDLER = false;
const GAMEPAD_CHECK_TIME = 25;

const GamepadHandler = function () {
    let _THIS = this;

    _THIS.B1 = 0;
    _THIS.B2 = 1;
    _THIS.B3 = 2;
    _THIS.B4 = 3;
    _THIS.L1 = 4;
    _THIS.R1 = 5;
    _THIS.L2 = 6;
    _THIS.R2 = 7;
    _THIS.B9 = 8;
    _THIS.B10 = 9;
    _THIS.L3 = 10;
    _THIS.R3 = 11;
    _THIS.RU = 0;
    _THIS.RR = 1;
    _THIS.RD = 2;
    _THIS.RL = 3;
    _THIS.TURBO = 8;
    _THIS.CLEAR = 9;

    _THIS.gpIndex = null;
    _THIS.listener = null;
    _THIS.previousState = {
        axes : [],
        buttons: [],
    };

    _THIS.initializeGamepadIndex = function () {
        window.addEventListener("gamepadconnected", function(e) {
            _THIS.gpIndex = e.gamepad.index;
            if (DEBUG_GAMEPAD_HANDLER) console.log('Gamepad connected.');
        });
    };

    _THIS.fillPreviousState = function (gamepadObject) {
            gamepadObject.buttons.forEach(function (button, index) {
                _THIS.previousState.buttons[index] = button.pressed;
            });
            gamepadObject.axes.forEach(function (axis, index) {
                _THIS.previousState.axes[index] = axis;
            });
    };

    _THIS.initializeGamepadListener = function (onButtonChange, onAxesChange) {
        if (_THIS.hasListener()) return;
        _THIS.listener = window.setInterval(function () {
            let gp = navigator.getGamepads()[_THIS.gpIndex];
            if (!gp) return;
            if (!_THIS.previousState.buttons.length && !_THIS.previousState.axes.length) {
                if (DEBUG_GAMEPAD_HANDLER) console.log('Previous is empty.');
                _THIS.fillPreviousState(gp);
            }
            gp.buttons.forEach(function (button, index) {
                if (button.pressed !== _THIS.previousState.buttons[index]) {
                    let type = button.pressed ? 'press' : 'release';
                    if (onButtonChange && onButtonChange.call) onButtonChange(index, type);
                }
            });
            gp.axes.forEach(function (axis, index) {
                if (Math.abs(axis - _THIS.previousState.axes[index]) > 0.5) {
                    axis = Math.round(axis);
                    if (onAxesChange && onAxesChange.call) onAxesChange(index, axis);
                }
            });
            _THIS.fillPreviousState(gp);
        }, GAMEPAD_CHECK_TIME);
    };

    _THIS.destroyGamepadListener = function () {
        if (!_THIS.hasListener()) return;
        window.clearInterval(_THIS.listener);
        _THIS.listener = null;
    };

    _THIS.hasListener = function () {
        return _THIS.listener !== null;
    };
};
