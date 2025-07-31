INSERT INTO public.group_device (group_id,"name",kind,category,description) VALUES
	 ('1bd80197-9b10-4eed-b5c3-0d86dbe0178d'::uuid,'SCL3300 inclinometer array 1',false,'ANALYSIS','SCL3300 inclinometer array at point 1 of PGE soil settlement monitoring');
INSERT INTO public.group_device_map (group_id,device_id) VALUES
	 ('1bd80197-9b10-4eed-b5c3-0d86dbe0178d'::uuid,'1f81d099-4c6f-4929-8757-005f557de318'::uuid),
	 ('1bd80197-9b10-4eed-b5c3-0d86dbe0178d'::uuid,'2b682489-4a02-4bb0-80c5-458f4a20d519'::uuid),
	 ('1bd80197-9b10-4eed-b5c3-0d86dbe0178d'::uuid,'36ffe820-f54c-4f4d-b3e9-5ed4e3cab716'::uuid),
	 ('1bd80197-9b10-4eed-b5c3-0d86dbe0178d'::uuid,'4d935490-a272-4aad-a60a-8438e10416a0'::uuid),
	 ('1bd80197-9b10-4eed-b5c3-0d86dbe0178d'::uuid,'561fd4bf-d082-42be-b9d5-ffe5f121c1e4'::uuid),
	 ('1bd80197-9b10-4eed-b5c3-0d86dbe0178d'::uuid,'6b0fe48f-1e3b-4e74-9dac-79c7fe9e4778'::uuid),
	 ('1bd80197-9b10-4eed-b5c3-0d86dbe0178d'::uuid,'7aebed6a-af10-4875-82e5-b23647d58080'::uuid),
	 ('1bd80197-9b10-4eed-b5c3-0d86dbe0178d'::uuid,'83f7db09-5353-462e-8635-1f4257ab5788'::uuid);
INSERT INTO public."set" (set_id,template_id,"name",description) VALUES
	 ('10f796e8-c134-4d56-8919-b83729de7368'::uuid,'8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'SCL3300 inclinometer set 1','SCL3300 inclinometer array set at point 1 of PGE soil settlement monitoring');
INSERT INTO public.set_map (set_id,device_id,model_id,data_index,set_position,set_number) VALUES
	 ('10f796e8-c134-4d56-8919-b83729de7368'::uuid,'1f81d099-4c6f-4929-8757-005f557de318'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),0,32),
	 ('10f796e8-c134-4d56-8919-b83729de7368'::uuid,'2b682489-4a02-4bb0-80c5-458f4a20d519'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),4,32),
	 ('10f796e8-c134-4d56-8919-b83729de7368'::uuid,'36ffe820-f54c-4f4d-b3e9-5ed4e3cab716'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),8,32),
	 ('10f796e8-c134-4d56-8919-b83729de7368'::uuid,'4d935490-a272-4aad-a60a-8438e10416a0'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),12,32),
	 ('10f796e8-c134-4d56-8919-b83729de7368'::uuid,'561fd4bf-d082-42be-b9d5-ffe5f121c1e4'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),16,32),
	 ('10f796e8-c134-4d56-8919-b83729de7368'::uuid,'6b0fe48f-1e3b-4e74-9dac-79c7fe9e4778'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),20,32),
	 ('10f796e8-c134-4d56-8919-b83729de7368'::uuid,'7aebed6a-af10-4875-82e5-b23647d58080'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),24,32),
	 ('10f796e8-c134-4d56-8919-b83729de7368'::uuid,'83f7db09-5353-462e-8635-1f4257ab5788'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),28,32);
