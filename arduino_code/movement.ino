void Move (char* dir) {
  switch (dir[0]) {
    case 'w':
      Esc0.writeMicroseconds(ESC_STOP - _speed);
      Esc1.writeMicroseconds(ESC_STOP + _speed);
      Esc2.writeMicroseconds(ESC_STOP + _speed);
      Esc3.writeMicroseconds(ESC_STOP - _speed);
      break;
    case 's':
      Esc0.writeMicroseconds(ESC_STOP + _speed);
      Esc1.writeMicroseconds(ESC_STOP - _speed);
      Esc2.writeMicroseconds(ESC_STOP - _speed);
      Esc3.writeMicroseconds(ESC_STOP + _speed);
      break;
    case 'd':
      Esc0.writeMicroseconds(ESC_STOP - _speed);
      Esc1.writeMicroseconds(ESC_STOP + _speed);
      Esc2.writeMicroseconds(ESC_STOP - _speed);
      Esc3.writeMicroseconds(ESC_STOP + _speed);
      break;
    case 'a':
      Esc0.writeMicroseconds(ESC_STOP + _speed);
      Esc1.writeMicroseconds(ESC_STOP - _speed);
      Esc2.writeMicroseconds(ESC_STOP + _speed);
      Esc3.writeMicroseconds(ESC_STOP - _speed);
      break;
    case 'h':
      Esc0.writeMicroseconds(ESC_STOP - _speed);
      Esc1.writeMicroseconds(ESC_STOP - _speed);
      Esc2.writeMicroseconds(ESC_STOP + _speed);
      Esc3.writeMicroseconds(ESC_STOP + _speed);
      break;
    case 'k':
      Esc0.writeMicroseconds(ESC_STOP + _speed);
      Esc1.writeMicroseconds(ESC_STOP + _speed);
      Esc2.writeMicroseconds(ESC_STOP - _speed);
      Esc3.writeMicroseconds(ESC_STOP - _speed);
      break;
    case 'u':
      liftEsc_1.writeMicroseconds(ESC_STOP + _speed);
      liftEsc_2.writeMicroseconds(ESC_STOP + _speed);
      break;   
    case 'j':
      liftEsc_1.writeMicroseconds(ESC_STOP - _speed);
      liftEsc_2.writeMicroseconds(ESC_STOP - _speed);
      break;
    case 'e':
      analogWrite(GRIPPER1_PWM_PIN, GRIPPER_SPEED);
      digitalWrite(GRIPPER1_DIR_PIN, GRIPPER_OPEN_STATE);
      break;
    case 'r':
      analogWrite(GRIPPER1_PWM_PIN, GRIPPER_SPEED);
      digitalWrite(GRIPPER1_DIR_PIN, GRIPPER_CLOSE_STATE);
      break;
    case 'y':
      analogWrite(GRIPPER2_PWM_PIN, GRIPPER_SPEED);
      digitalWrite(GRIPPER2_DIR_PIN, GRIPPER_OPEN_STATE);
      break;
    case 't':
      analogWrite(GRIPPER2_PWM_PIN, GRIPPER_SPEED);
      digitalWrite(GRIPPER2_DIR_PIN, GRIPPER_CLOSE_STATE);
      break;
    case 'f':
      flash1State = !flash1State;
      digitalWrite(LED1,flash1State);
      break;
    case 'g':
      flash2State = !flash2State;
      digitalWrite(LED2,flash2State);
      break;
    case 'c':
      Esc0.writeMicroseconds(ESC_STOP);
      Esc1.writeMicroseconds(ESC_STOP);
      Esc2.writeMicroseconds(ESC_STOP);
      Esc3.writeMicroseconds(ESC_STOP);
      liftEsc_1.writeMicroseconds(ESC_STOP);
      liftEsc_2.writeMicroseconds(ESC_STOP);
      break;
    case 'm':
      analogWrite(GRIPPER1_PWM_PIN, GRIPPER_STOP);
      analogWrite(GRIPPER2_PWM_PIN, GRIPPER_STOP);
      break;
    case 'n':
      if (dir[1] > '9' || dir[1] < '0') break;
      _speed = (uint16_t)atoi(dir + 1);
      _speed = _speed < ESC_SPEED_LIMIT ? _speed : ESC_SPEED_LIMIT;
      _speed = _speed > 0 ? _speed : 0;
      break;
  }
}

