INSERT INTO public.model (model_id,name,category,description,data_type) VALUES
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,'BME280 environment sensor','DATA','Air temperature, air pressure, and relative humidity of BME280 environment sensor',decode('0D0D0D','hex'));
INSERT INTO public.model_config (model_id,"index",name,value,"type",category) VALUES
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,0,'scale',decode('4169722054656D7065726174757265','hex'),17,'SCALE'),
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,0,'unit',decode('43656C63697573','hex'),17,'UNIT'),
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,0,'symbol',decode('B043','hex'),17,'SYMBOL'),
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,1,'scale',decode('416972205072657373757265','hex'),17,'SCALE'),
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,1,'unit',decode('686563746F2070617363616C','hex'),17,'UNIT'),
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,1,'symbol',decode('685061','hex'),17,'SYMBOL'),
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,2,'scale',decode('52656C61746976652048756D6964697479','hex'),17,'SCALE'),
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,2,'unit',decode('50657263656E74','hex'),17,'UNIT'),
	 ('828feb1f-e46b-4242-b67d-20aba7c21282'::uuid,2,'symbol',decode('25','hex'),17,'SYMBOL');
INSERT INTO public.device_type (type_id,name,description) VALUES
	 ('e0902405-9a96-497a-8fab-2deb007d8a0f'::uuid,'gateway blank','gateway with no model'),
	 ('0647b5e6-cc72-42b3-90f5-0824ff608fa5'::uuid,'BME280 environment sensor','BME280 environment sensor with air temperature, air pressure, and relative humidity data');
INSERT INTO public.device_type_model (type_id,model_id) VALUES
	 ('0647b5e6-cc72-42b3-90f5-0824ff608fa5'::uuid,'828feb1f-e46b-4242-b67d-20aba7c21282'::uuid);
