INSERT INTO public.device (device_id,gateway_id,type_id,serial_number,name,description) VALUES
	 ('16737593-2431-4390-af71-d23a88848d11'::uuid,'16737593-2431-4390-af71-d23a88848d11'::uuid,'e0902405-9a96-497a-8fab-2deb007d8a0f'::uuid,'ENVGTW00','Environment gateway','Environment gateway testing'),
	 ('e8e9ada1-1840-4011-879e-3551c33db2d2'::uuid,'16737593-2431-4390-af71-d23a88848d11'::uuid,'0647b5e6-cc72-42b3-90f5-0824ff608fa5'::uuid,'ENVIRO00','Environment sensor testing','Environment sensor testing device');
INSERT INTO public.device_config (device_id,name,value,"type",category) VALUES
	 ('e8e9ada1-1840-4011-879e-3551c33db2d2'::uuid,'smbus_id',decode('00000002','hex'),3,'COMMUNICATION'),
	 ('e8e9ada1-1840-4011-879e-3551c33db2d2'::uuid,'smbus_address',decode('00000076','hex'),3,'COMMUNICATION');
