INSERT INTO public.device (device_id,gateway_id,type_id,serial_number,"name",description) VALUES
	 ('39682460-6af2-4b36-89ff-9d54e98cbbb5','39682460-6af2-4b36-89ff-9d54e98cbbb5','e0902405-9a96-497a-8fab-2deb007d8a0f','GATE01','Gateway_1',''),
	 ('5e7c4ea6-b6f3-4198-ae14-9888bf437cf1','39682460-6af2-4b36-89ff-9d54e98cbbb5','eea82bb2-d427-4081-890d-c7c4795fd6f7','TESTACC01','Accelerometer_1','soil inclinometer 1 testing'),
	 ('b76a8ef4-52cf-4c18-9d6b-abcff383d822','39682460-6af2-4b36-89ff-9d54e98cbbb5','eea82bb2-d427-4081-890d-c7c4795fd6f7','TESTACC02','Accelerometer_2','soil inclinometer 2 testing'),
	 ('45cb6c63-d895-4382-bc62-ad113ae0dd24','39682460-6af2-4b36-89ff-9d54e98cbbb5','eea82bb2-d427-4081-890d-c7c4795fd6f7','TESTACC03','Accelerometer_3','soil inclinometer 3 testing'),
	 ('4dd2c477-b2f3-4565-8403-29093127b202','39682460-6af2-4b36-89ff-9d54e98cbbb5','eea82bb2-d427-4081-890d-c7c4795fd6f7','TESTACC04','Accelerometer_4','soil inclinometer 4 testing'),
	 ('3676235b-195d-4c63-bfc4-f9abb1590d77','39682460-6af2-4b36-89ff-9d54e98cbbb5','eea82bb2-d427-4081-890d-c7c4795fd6f7','TESTACC05','Accelerometer_5','soil inclinometer 5 testing'),
	 ('d86ab73a-9b02-4117-9bb9-8e900c859396','39682460-6af2-4b36-89ff-9d54e98cbbb5','3b48c722-766a-4cc4-8fe9-cf7d8a3cff69','TESTPIE01','Piezometer_1','piezometer testing'),
	 ('ff38c507-73ea-49bd-8093-51f5f052cb72','39682460-6af2-4b36-89ff-9d54e98cbbb5','24709a09-0cf3-47e4-9080-efa7cd2860be','TESTRAG01','Rain_Gauge_1','rain gauge testing'),
	 ('2ec7f527-2377-4a10-ae57-c590eafd07f1','39682460-6af2-4b36-89ff-9d54e98cbbb5','99f387e1-e082-4e52-9f03-f2a6fa3f3e35','TESTENV01','Environment_Sensor_1','environment sensor testing');
INSERT INTO public.device_config (device_id,"name",value,"type",category) VALUES
	 ('5e7c4ea6-b6f3-4198-ae14-9888bf437cf1','slave_id',decode('0000000000000001','hex'),1,'COMMUNICATION'),
	 ('5e7c4ea6-b6f3-4198-ae14-9888bf437cf1','offset-X',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('5e7c4ea6-b6f3-4198-ae14-9888bf437cf1','offset-Y',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('5e7c4ea6-b6f3-4198-ae14-9888bf437cf1','offset-Z',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('5e7c4ea6-b6f3-4198-ae14-9888bf437cf1','space',decode('00000000000003E8','hex'),1,'ANALYSIS'),
	 ('5e7c4ea6-b6f3-4198-ae14-9888bf437cf1','position',decode('0000000000000001','hex'),1,'ANALYSIS'),
	 ('b76a8ef4-52cf-4c18-9d6b-abcff383d822','slave_id',decode('0000000000000002','hex'),1,'COMMUNICATION'),
	 ('b76a8ef4-52cf-4c18-9d6b-abcff383d822','offset-X',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('b76a8ef4-52cf-4c18-9d6b-abcff383d822','offset-Y',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('b76a8ef4-52cf-4c18-9d6b-abcff383d822','offset-Z',decode('0000000000000000','hex'),1,'OFFSET');
INSERT INTO public.device_config (device_id,"name",value,"type",category) VALUES
	 ('b76a8ef4-52cf-4c18-9d6b-abcff383d822','space',decode('00000000000003E8','hex'),1,'ANALYSIS'),
	 ('b76a8ef4-52cf-4c18-9d6b-abcff383d822','position',decode('0000000000000002','hex'),1,'ANALYSIS'),
	 ('45cb6c63-d895-4382-bc62-ad113ae0dd24','slave_id',decode('0000000000000003','hex'),1,'COMMUNICATION'),
	 ('45cb6c63-d895-4382-bc62-ad113ae0dd24','offset-X',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('45cb6c63-d895-4382-bc62-ad113ae0dd24','offset-Y',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('45cb6c63-d895-4382-bc62-ad113ae0dd24','offset-Z',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('45cb6c63-d895-4382-bc62-ad113ae0dd24','space',decode('00000000000003E8','hex'),1,'ANALYSIS'),
	 ('45cb6c63-d895-4382-bc62-ad113ae0dd24','position',decode('0000000000000003','hex'),1,'ANALYSIS'),
	 ('4dd2c477-b2f3-4565-8403-29093127b202','slave_id',decode('0000000000000004','hex'),1,'COMMUNICATION'),
	 ('4dd2c477-b2f3-4565-8403-29093127b202','offset-X',decode('0000000000000000','hex'),1,'OFFSET');
INSERT INTO public.device_config (device_id,"name",value,"type",category) VALUES
	 ('4dd2c477-b2f3-4565-8403-29093127b202','offset-Y',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('4dd2c477-b2f3-4565-8403-29093127b202','offset-Z',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('4dd2c477-b2f3-4565-8403-29093127b202','space',decode('00000000000003E8','hex'),1,'ANALYSIS'),
	 ('4dd2c477-b2f3-4565-8403-29093127b202','position',decode('0000000000000004','hex'),1,'ANALYSIS'),
	 ('3676235b-195d-4c63-bfc4-f9abb1590d77','slave_id',decode('0000000000000005','hex'),1,'COMMUNICATION'),
	 ('3676235b-195d-4c63-bfc4-f9abb1590d77','offset-X',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('3676235b-195d-4c63-bfc4-f9abb1590d77','offset-Y',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('3676235b-195d-4c63-bfc4-f9abb1590d77','offset-Z',decode('0000000000000000','hex'),1,'OFFSET'),
	 ('3676235b-195d-4c63-bfc4-f9abb1590d77','space',decode('00000000000003E8','hex'),1,'ANALYSIS'),
	 ('3676235b-195d-4c63-bfc4-f9abb1590d77','position',decode('0000000000000005','hex'),1,'ANALYSIS');
INSERT INTO public.device_config (device_id,"name",value,"type",category) VALUES
	 ('d86ab73a-9b02-4117-9bb9-8e900c859396','slave_id',decode('0000000000000080','hex'),1,'COMMUNICATION'),
	 ('d86ab73a-9b02-4117-9bb9-8e900c859396','offset-pressure',decode('FFFFFFFFFFFFFFF2','hex'),1,'OFFSET'),
	 ('d86ab73a-9b02-4117-9bb9-8e900c859396','offset-depth',decode('FFFFFFFFFFFFFFFF','hex'),1,'OFFSET'),
	 ('ff38c507-73ea-49bd-8093-51f5f052cb72','slave_id',decode('0000000000000090','hex'),1,'COMMUNICATION'),
	 ('ff38c507-73ea-49bd-8093-51f5f052cb72','coefficient',decode('3FB999999999999A','hex'),2,'ANALYSIS'),
	 ('2ec7f527-2377-4a10-ae57-c590eafd07f1','slave_id',decode('00000000000000A0','hex'),1,'COMMUNICATION');
