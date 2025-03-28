INSERT INTO public.model (model_id,name,category,description,data_type) VALUES
	 ('1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,'Generator 2 int','GENERATOR','Data generator with 2 32-bit integer',decode('0303','hex')),
	 ('820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,'Generator 2 float','GENERATOR','Data generator with 2 64-bit floating point',decode('0D0D','hex'));
INSERT INTO public.model_config (model_id,"index",name,value,"type",category) VALUES
	 ('1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,0,'name',decode('47656E657261746F722D696E74','hex'),17,'SCALE'),
	 ('1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,0,'unit',decode('756E69746C657373','hex'),17,'SCALE'),
	 ('1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,0,'symbol',decode('756C','hex'),17,'SCALE'),
	 ('1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,1,'name',decode('47656E657261746F722D696E74','hex'),17,'SCALE'),
	 ('1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,1,'unit',decode('756E69746C657373','hex'),17,'SCALE'),
	 ('1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,1,'symbol',decode('756C','hex'),17,'SCALE'),
	 ('820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,0,'name',decode('47656E657261746F722D666C6F6174','hex'),17,'SCALE'),
	 ('820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,0,'unit',decode('756E69746C657373','hex'),17,'SCALE'),
	 ('820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,0,'symbol',decode('756C','hex'),17,'SCALE'),
	 ('820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,1,'name',decode('47656E657261746F722D666C6F6174','hex'),17,'SCALE'),
	 ('820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,1,'unit',decode('756E69746C657373','hex'),17,'SCALE'),
	 ('820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,1,'symbol',decode('756C','hex'),17,'SCALE');
INSERT INTO public.device_type (type_id,name,description) VALUES
	 ('32379c0a-a849-45cf-a6e6-2b314b86545d'::uuid,'Generator 2 int','Generator data with 2 integer'),
	 ('d190ac36-ce89-42fc-ab77-7a029674278c'::uuid,'Generator 2 float','Generator data with 2 float'),
	 ('e0902405-9a96-497a-8fab-2deb007d8a0f'::uuid,'gateway blank','gateway with no model');
INSERT INTO public.device_type_model (type_id,model_id) VALUES
	 ('32379c0a-a849-45cf-a6e6-2b314b86545d'::uuid,'1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid),
	 ('d190ac36-ce89-42fc-ab77-7a029674278c'::uuid,'820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid);
