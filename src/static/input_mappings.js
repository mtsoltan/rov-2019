/**
 * Array of all allowed keys.
 * Speed control and other complex controls have different basis.
 * Uses capital letters for release.
 *
 *   r         t
 *   e         y
 *   w         u
 * a   d f g h   k
 *   s         j
 */
const allowed_keys = [
    'r', 't', 'w', 'a', 's', 'd',
    'e', 'y', 'u', 'h', 'j', 'k',
    'f', 'g', 'c',
];

/**
 * Forward mapping of keys/buttons to their sent letters.
 * @type {Object}
 */
let pressMapping = {};
/**
 * Forward mapping of axes to their sent letters.
 * @type {Object}
 */
let axesMapping = {};
/**
 * Inverse mapping of keys back to their GUI classes.
 * @type {Object}
 */
let viewMapping = {};

/**
 * Fills the variables in this file using keys in the
 * argument GamepadHandler.
 * @param {GamepadHandler} gamepadHandler
 */
function fillMappings (gamepadHandler) {
    pressMapping[gamepadHandler.B1] = 'u'; // Go Up
    pressMapping[gamepadHandler.B2] = 'k'; // Rotate Right
    pressMapping[gamepadHandler.B3] = 'j'; // Go Down
    pressMapping[gamepadHandler.B4] = 'h'; // Rotate Left
    pressMapping[gamepadHandler.L1] = 'e'; // Gripper 1
    pressMapping[gamepadHandler.L2] = 'r'; // Gripper 1
    pressMapping[gamepadHandler.R1] = 'y'; // Gripper 2
    pressMapping[gamepadHandler.R2] = 't'; // Gripper 2
    pressMapping[gamepadHandler.B9] = 'f'; // Broken Light
    pressMapping[gamepadHandler.B10] = 'g'; // Working Light
    pressMapping[gamepadHandler.L3] = 'v';
    pressMapping[gamepadHandler.R3] = 'b';
    pressMapping['f'] = 'w'; // Forward
    pressMapping['b'] = 's'; // Backward
    pressMapping['l'] = 'a'; // Left
    pressMapping['r'] = 'd'; // Right
    pressMapping['u'] = 'u';
    pressMapping['d'] = 'j';
    pressMapping['e'] = 'c'; // EMERGENCY_STOP

    axesMapping[0] = ['a', 'd']; // -1, 1
    axesMapping[1] = ['w', 's'];

    viewMapping['w'] = 'f';
    viewMapping['s'] = 'b';
    viewMapping['a'] = 'l';
    viewMapping['d'] = 'r';
    viewMapping['u'] = 'u';
    viewMapping['j'] = 'd';
    viewMapping['c'] = 'e';
}
