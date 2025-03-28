INSERT INTO public.group_model (group_id,name,category,description) VALUES
	 ('9f3fa9f7-e16e-484f-b85d-554184ecd00f'::uuid,'backup','BACKUP','');
INSERT INTO public.group_model_map (group_id,model_id) VALUES
	 ('9f3fa9f7-e16e-484f-b85d-554184ecd00f'::uuid,'1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid),
	 ('9f3fa9f7-e16e-484f-b85d-554184ecd00f'::uuid,'820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid);
INSERT INTO public.group_device (group_id,name,kind,category,description) VALUES
	 ('1cf38f07-8e7a-46d8-b438-518bed60d1ab'::uuid,'Generator group 1',false,'DATA','Generator group 1'),
	 ('29005b58-4f2d-417d-8c0b-603b592fe1dd'::uuid,'Generator group 2',false,'DATA','Generator group 2');
INSERT INTO public.group_device_map (group_id,device_id) VALUES
	 ('1cf38f07-8e7a-46d8-b438-518bed60d1ab'::uuid,'a1c35b55-8a36-48d8-94d8-e389e9301dfe'::uuid),
	 ('1cf38f07-8e7a-46d8-b438-518bed60d1ab'::uuid,'b18820e1-c1df-4606-aa89-c03067bc87f5'::uuid),
	 ('29005b58-4f2d-417d-8c0b-603b592fe1dd'::uuid,'a23bbcce-153b-4bb5-82ae-93d939db3f0b'::uuid),
	 ('29005b58-4f2d-417d-8c0b-603b592fe1dd'::uuid,'b2f5a792-7b81-4e79-b33c-f699820b7fd1'::uuid);
