#include <Servo.h> 
// 动态变量
volatile float mind_n_my_float_variable;
// 创建对象
Servo servo_4;
Servo servo_5;
Servo servo_6;


// 主程序开始
void setup() {
	servo_4.attach(4);
	servo_5.attach(5);
	servo_6.attach(6);
	Serial.begin(9600);
	servo_4.write(abs(90));
	servo_5.write(abs(90));
	servo_5.write(abs(90));
}
void loop() {
	if ((Serial.available())) {
		mind_n_my_float_variable = Serial.parseInt();
	}
	if ((mind_n_my_float_variable==1)) {
		servo_4.write(abs(0));
		delay(1000);
		servo_4.write(abs(90));
		mind_n_my_float_variable = 0;
	}
	if ((mind_n_my_float_variable==2)) {
		servo_5.write(abs(180));
		delay(1000);
		servo_5.write(abs(90));
		mind_n_my_float_variable = 0;
	}
	if ((mind_n_my_float_variable==3)) {
		for (int index = 0; index < 3; index++) {
			servo_6.write(abs(0));
			delay(500);
			servo_6.write(abs(180));
			delay(500);
		}
		servo_6.write(abs(90));
		mind_n_my_float_variable = 0;
	}
}

