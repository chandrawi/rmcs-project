INSERT INTO public.model (model_id,name,category,description,data_type) VALUES
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,'INA3321 power monitor','DATA','Time period and 3-channel average voltage and current result of INA3321 sensor',decode('030D0D0D0D0D0D','hex'));
INSERT INTO public.model_config (model_id,"index",name,value,"type",category) VALUES
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,0,'name',decode('506572696F64','hex'),17,'SCALE'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,0,'unit',decode('7365636F6E64','hex'),17,'UNIT'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,0,'symbol',decode('73','hex'),17,'SYMBOL'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,1,'name',decode('566F6C746167652D31','hex'),17,'SCALE'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,1,'unit',decode('566F6C74','hex'),17,'UNIT'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,1,'symbol',decode('56','hex'),17,'SYMBOL'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,2,'name',decode('43757272656e742d31','hex'),17,'SCALE'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,2,'unit',decode('416D70657265','hex'),17,'UNIT'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,2,'symbol',decode('41','hex'),17,'SYMBOL'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,3,'name',decode('566F6C746167652D32','hex'),17,'SCALE'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,3,'unit',decode('566F6C74','hex'),17,'UNIT'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,3,'symbol',decode('56','hex'),17,'SYMBOL'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,4,'name',decode('43757272656e742d32','hex'),17,'SCALE'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,4,'unit',decode('416D70657265','hex'),17,'UNIT'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,4,'symbol',decode('41','hex'),17,'SYMBOL'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,5,'name',decode('566F6C746167652D33','hex'),17,'SCALE'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,5,'unit',decode('566F6C74','hex'),17,'UNIT'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,5,'symbol',decode('56','hex'),17,'SYMBOL'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,6,'name',decode('43757272656e742d33','hex'),17,'SCALE'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,6,'unit',decode('416D70657265','hex'),17,'UNIT'),
	 ('cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid,6,'symbol',decode('41','hex'),17,'SYMBOL');
INSERT INTO public.device_type (type_id,name,description) VALUES
	 ('e0902405-9a96-497a-8fab-2deb007d8a0f'::uuid,'gateway blank','gateway with no model'),
	 ('601bda88-9279-4ba5-a6ea-6222fb92ce6a'::uuid,'INA3321 power monitor','Time period and 3-channel average voltage and current result of INA3321 sensor');
INSERT INTO public.device_type_model (type_id,model_id) VALUES
	 ('601bda88-9279-4ba5-a6ea-6222fb92ce6a'::uuid,'cfe2c3d4-a44d-4ad9-8660-3c122e5caf89'::uuid);
