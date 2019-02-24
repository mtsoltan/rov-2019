/**
 *   r         t
 *   e         y
 *   w         u
 * a   d f g h   k
 *   s         j
 */

const MOVE_HALT = 0xff; // Could be any value that isn't a real button.
const GRIPPER_HALT = 0xfe; // Could be any value that isn't a real button.

let buttonMapping = {};
let axesMapping = {};
let guiButtonMapping = {};
let movementButtons = [];

function fillMappings(gameHandler) {
    buttonMapping[gameHandler.B1] = 'u'; // Go Up
    buttonMapping[gameHandler.B2] = 'k'; // Rotate Right
    buttonMapping[gameHandler.B3] = 'j'; // Go Down
    buttonMapping[gameHandler.B4] = 'h'; // Rotate Left
    buttonMapping[gameHandler.L1] = 'e'; // Gripper 1
    buttonMapping[gameHandler.L2] = 'r'; // Gripper 1
    buttonMapping[gameHandler.R1] = 'y'; // Gripper 2
    buttonMapping[gameHandler.R2] = 't'; // Gripper 2
    buttonMapping[gameHandler.B9] = 'f'; // Broken Light
    buttonMapping[gameHandler.B10] = 'g'; // Working Light
    buttonMapping[gameHandler.L3] = 'v';
    buttonMapping[gameHandler.R3] = 'b';
    buttonMapping['f'] = 'w'; // Forward
    buttonMapping['b'] = 's'; // Backward
    buttonMapping['l'] = 'a'; // Left
    buttonMapping['r'] = 'd'; // Right
    buttonMapping['u'] = 'u';
    buttonMapping['d'] = 'j';
    buttonMapping[MOVE_HALT] = 'c'; // c is the SERIAL letter for stopping thrusters.
    buttonMapping[GRIPPER_HALT] = 'm'; // m is the SERIAL letter for stopping grippers.

    axesMapping[0] = ['a', 'd']; // -1, 1
    axesMapping[1] = ['w', 's'];

    guiButtonMapping['w'] = 'f';
    guiButtonMapping['s'] = 'b';
    guiButtonMapping['a'] = 'l';
    guiButtonMapping['d'] = 'r';
    guiButtonMapping['u'] = 'u';
    guiButtonMapping['j'] = 'd';

    movementButtons = ['w', 'a', 's', 'd', 'u', 'j'];

    gripperButtons = ['e', 'r', 't', 'y'];
}