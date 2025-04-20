INSERT INTO public.device (device_id,gateway_id,type_id,serial_number,name,description) VALUES
	 ('426a016d-c384-4ed7-b74d-b3dbc5e21029'::uuid,'426a016d-c384-4ed7-b74d-b3dbc5e21029'::uuid,'e0902405-9a96-497a-8fab-2deb007d8a0f'::uuid,'TESTGW00','Power monitor gateway','Gateway for power monitoring'),
	 ('9585a648-d9e5-442b-b192-0f758cab89ff'::uuid,'426a016d-c384-4ed7-b74d-b3dbc5e21029'::uuid,'601bda88-9279-4ba5-a6ea-6222fb92ce6a'::uuid,'PWRMON00','Power monitor testing','Power monitor testing device');
INSERT INTO public.device_config (device_id,name,value,"type",category) VALUES
	 ('9585a648-d9e5-442b-b192-0f758cab89ff'::uuid,'smbus_id',decode('00000002','hex'),3,'COMMUNICATION'),
	 ('9585a648-d9e5-442b-b192-0f758cab89ff'::uuid,'smbus_address',decode('00000040','hex'),3,'COMMUNICATION'),
	 ('9585a648-d9e5-442b-b192-0f758cab89ff'::uuid,'resistor_0',decode('3F747AE147AE147B','hex'),13,'HARDWARE'),
	 ('9585a648-d9e5-442b-b192-0f758cab89ff'::uuid,'resistor_1',decode('3F747AE147AE147B','hex'),13,'HARDWARE'),
	 ('9585a648-d9e5-442b-b192-0f758cab89ff'::uuid,'resistor_2',decode('3F747AE147AE147B','hex'),13,'HARDWARE'),
	 ('9585a648-d9e5-442b-b192-0f758cab89ff'::uuid,'conversion_average',decode('00000007','hex'),3,'SETTING'),
	 ('9585a648-d9e5-442b-b192-0f758cab89ff'::uuid,'conversion_time',decode('00000004','hex'),3,'SETTING');
