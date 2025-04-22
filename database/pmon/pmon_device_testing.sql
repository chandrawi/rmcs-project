INSERT INTO public.device (device_id,gateway_id,type_id,serial_number,name,description) VALUES
	 ('f7d0408d-9edb-4306-bbb5-908389af592e'::uuid,'f7d0408d-9edb-4306-bbb5-908389af592e'::uuid,'601bda88-9279-4ba5-a6ea-6222fb92ce6a'::uuid,'PWRMON00','Power monitor testing','Power monitor testing device');
INSERT INTO public.device_config (device_id,name,value,"type",category) VALUES
	 ('f7d0408d-9edb-4306-bbb5-908389af592e'::uuid,'smbus_id',decode('00000002','hex'),3,'COMMUNICATION'),
	 ('f7d0408d-9edb-4306-bbb5-908389af592e'::uuid,'smbus_address',decode('00000040','hex'),3,'COMMUNICATION'),
	 ('f7d0408d-9edb-4306-bbb5-908389af592e'::uuid,'resistor_0',decode('3F747AE147AE147B','hex'),13,'HARDWARE'),
	 ('f7d0408d-9edb-4306-bbb5-908389af592e'::uuid,'resistor_1',decode('3F747AE147AE147B','hex'),13,'HARDWARE'),
	 ('f7d0408d-9edb-4306-bbb5-908389af592e'::uuid,'resistor_2',decode('3F747AE147AE147B','hex'),13,'HARDWARE'),
	 ('f7d0408d-9edb-4306-bbb5-908389af592e'::uuid,'conversion_average',decode('00000007','hex'),3,'SETTING'),
	 ('f7d0408d-9edb-4306-bbb5-908389af592e'::uuid,'conversion_time',decode('00000004','hex'),3,'SETTING');
