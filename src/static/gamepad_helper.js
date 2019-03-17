/**
 * Key state constant for clarity.
 * @type {boolean}
 */
const ON = true;

/**
 * Key state constant for clarity.
 * @type {boolean}
 */
const OFF = false;

/**
 * Selector to be used for keys.
 * Distinguishing letter is appended to this.
 * @type {string}
 */
const KEY_SELECTOR = '.control-box button#';

/**
 * ID of the checkbox that allows free keys.
 * @type {string}
 */
const FREE_KEYS_ID = 'free_keys';

/**
 * URL at which keys are sent.
 * @type {string}
 */
const KEY_URL = '/move_free_drive';

/**
 * The last sent character.
 * Used to make sure it doesn't get sent again.
 * @type {string}
 */
let last_sent = '';

/**
 * Allows keyboard to control the robot if set.
 * @type {boolean}
 */
let free_keys = false;

/**
 * Activates a GUI button.
 * @param {string} key - A 1-letter string.
 */
function activate (key) {
    if (viewMapping[key]) $(KEY_SELECTOR + viewMapping[key]).addClass('active');
}

/**
 * Deactivates a GUI button.
 * @param {string} key - A 1-letter string.
 */
function deactivate (key) {
    if (viewMapping[key]) $(KEY_SELECTOR + viewMapping[key]).removeClass('active');
}

/**
 * Sends a key to the server, and activates/deactivates the corresponding GUI button.
 * @param {string} key - A 1-letter string.
 * @param {boolean} state - Whether to send that key lowercase, or uppercase.
 */
function sendKey (key, state = ON) {
    key = state ? key.toLowerCase() : key.toUpperCase();
    if (last_sent === key) return;
    rh.postFetch(KEY_URL, key, null);
    state ? activate(key) : deactivate(key);
    last_sent = key;
}

/**
 * Include this function in main to set up all the key stuff.
 */
function setupGamepadMain () {
    gh.initializeGamepadListener(function (button, type) {
        let key = pressMapping[button];
        if (type === 'press') {
            sendKey(key);
        } else {
            sendKey(key, OFF);
        }
    }, function (axis, value) {
        let key = axesMapping[axis][~~(value > 0)];
        if (Math.abs(value - 0) > 0.5) {
            sendKey(key);
        } else {
            axesMapping[axis].forEach(function (key) {
                sendKey(key, OFF);
            });
        }
    });

    $(window).on('keydown', function (ev) {
        let key = ev.key.toLowerCase();
        if (free_keys) {
            if (!allowed_keys.includes(key)) return;
            sendKey(key);
        }
    });

    $(window).on('keyup', function (ev) {
        let key = ev.key.toLowerCase();
        if (free_keys) {
            if (!allowed_keys.includes(key)) return;
            sendKey(key, OFF);
        }
    });

    $('#' + FREE_KEYS_ID).change(function () {
        free_keys = this.checked;
    }).change();
}