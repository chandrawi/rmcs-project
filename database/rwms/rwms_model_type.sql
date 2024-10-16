INSERT INTO public.model (model_id,name,category,description,data_type) VALUES
	 ('2f85c046-6851-4b80-8e6e-3698e9e707db'::uuid,'3-axis 16-bit accelerometer','RAW','3 16-bit integer accelerometer output value',decode('070707','hex')),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,'XZ-axis inclinometer array','DATA','XZ-axis inclination and displacement, Y-axis parallel with gravity',decode('0D0D0D0D0D0D0D','hex'));
INSERT INTO public.model_config (model_id,"index","name",value,"type",category) VALUES
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,0,'scale',decode('616363656C65726174696F6E2D58','hex'),17,'SCALE'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,0,'unit',decode('67726176697479','hex'),17,'UNIT'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,0,'symbol',decode('67','hex'),17,'SYMBOL'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,1,'scale',decode('616363656C65726174696F6E2D59','hex'),17,'SCALE'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,1,'unit',decode('67726176697479','hex'),17,'UNIT'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,1,'symbol',decode('67','hex'),17,'SYMBOL'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,2,'scale',decode('616363656C65726174696F6E2D5A','hex'),17,'SCALE'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,2,'unit',decode('67726176697479','hex'),17,'UNIT'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,2,'symbol',decode('67','hex'),17,'SYMBOL'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,3,'scale',decode('696E636C696E6174696F6E2D58','hex'),17,'SCALE'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,3,'unit',decode('72616469616E','hex'),17,'UNIT'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,3,'symbol',decode('726164','hex'),17,'SYMBOL'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,4,'scale',decode('696E636C696E6174696F6E2D5A','hex'),17,'SCALE'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,4,'unit',decode('72616469616E','hex'),17,'UNIT'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,4,'symbol',decode('726164','hex'),17,'SYMBOL'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,5,'scale',decode('646973706C6163656D656E742D58','hex'),17,'SCALE'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,5,'unit',decode('6D696C6C696D65746572','hex'),17,'UNIT'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,5,'symbol',decode('6D6D','hex'),17,'SYMBOL'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,6,'scale',decode('646973706C6163656D656E742D5A','hex'),17,'SCALE'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,6,'unit',decode('6D696C6C696D65746572','hex'),17,'UNIT'),
	 ('9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid,6,'symbol',decode('6D6D','hex'),17,'SYMBOL');
INSERT INTO public.device_type (type_id,"name",description) VALUES
	 ('e0902405-9a96-497a-8fab-2deb007d8a0f'::uuid,'gateway blank','gateway with no model'),
	 ('eea82bb2-d427-4081-890d-c7c4795fd6f7'::uuid,'inclinometer array','3-axis accelerometer and inclinometer array');
INSERT INTO public.device_type_model (type_id,model_id) VALUES
	 ('eea82bb2-d427-4081-890d-c7c4795fd6f7'::uuid,'2f85c046-6851-4b80-8e6e-3698e9e707db'::uuid),
	 ('eea82bb2-d427-4081-890d-c7c4795fd6f7'::uuid,'9d93adb9-4a93-4e26-998c-26349d9932a8'::uuid);
