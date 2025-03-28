INSERT INTO public.set_template (template_id,name,description) VALUES
	 ('740b6bc8-f6d2-45cf-a1ab-4e6b1d4d20d4'::uuid,'Data generator collection','Data generator collection');
INSERT INTO public.set_template_map (template_id,type_id,model_id,data_index,template_index) VALUES
	 ('740b6bc8-f6d2-45cf-a1ab-4e6b1d4d20d4'::uuid,'32379c0a-a849-45cf-a6e6-2b314b86545d'::uuid,'1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,decode('0001','hex'),0),
	 ('740b6bc8-f6d2-45cf-a1ab-4e6b1d4d20d4'::uuid,'d190ac36-ce89-42fc-ab77-7a029674278c'::uuid,'820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,decode('0001','hex'),1);
INSERT INTO public."set" (set_id,template_id,name,description) VALUES
	 ('17a3761e-742c-480a-82ee-43576fc2459f'::uuid,'740b6bc8-f6d2-45cf-a1ab-4e6b1d4d20d4'::uuid,'Data generator collection 1','Data generator collection 1'),
	 ('280877ab-5a87-41e5-aadf-4d56bbf338c1'::uuid,'740b6bc8-f6d2-45cf-a1ab-4e6b1d4d20d4'::uuid,'Data generator collection 2','Data generator collection 2');
INSERT INTO public.set_map (set_id,device_id,model_id,data_index,set_position,set_number) VALUES
	 ('17a3761e-742c-480a-82ee-43576fc2459f'::uuid,'a1c35b55-8a36-48d8-94d8-e389e9301dfe'::uuid,'1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,decode('0001','hex'),0,4),
	 ('17a3761e-742c-480a-82ee-43576fc2459f'::uuid,'b18820e1-c1df-4606-aa89-c03067bc87f5'::uuid,'820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,decode('0001','hex'),2,4),
	 ('280877ab-5a87-41e5-aadf-4d56bbf338c1'::uuid,'a23bbcce-153b-4bb5-82ae-93d939db3f0b'::uuid,'1f2d4175-a996-4680-8264-cfc5742cfbeb'::uuid,decode('0001','hex'),0,4),
	 ('280877ab-5a87-41e5-aadf-4d56bbf338c1'::uuid,'b2f5a792-7b81-4e79-b33c-f699820b7fd1'::uuid,'820648a8-5b39-4f06-a477-7cfc0ccf9060'::uuid,decode('0001','hex'),2,4);
