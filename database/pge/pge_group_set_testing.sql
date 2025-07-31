INSERT INTO public.group_model (group_id,"name",category,description) VALUES
	 ('e0c5fedd-9272-451e-b57c-8087433d707a'::uuid,'backup raw','BACKUP',''),
	 ('96117e88-8527-4012-80f8-6e7979426bf4'::uuid,'backup data','BACKUP','');
INSERT INTO public.group_model_map (group_id,model_id) VALUES
	 ('e0c5fedd-9272-451e-b57c-8087433d707a'::uuid,'595dc8e8-0a16-4f02-8c36-18bef0e667de'),
	 ('e0c5fedd-9272-451e-b57c-8087433d707a'::uuid,'eb93788f-aa61-421c-916d-f7d6026256de'),
	 ('e0c5fedd-9272-451e-b57c-8087433d707a'::uuid,'ed66830d-ce39-4dc9-a8f2-6eac3fef461f'),
	 ('96117e88-8527-4012-80f8-6e7979426bf4'::uuid,'828feb1f-e46b-4242-b67d-20aba7c21282'),
	 ('96117e88-8527-4012-80f8-6e7979426bf4'::uuid,'cfe2c3d4-a44d-4ad9-8660-3c122e5caf89');
INSERT INTO public.group_device (group_id,"name",kind,category,description) VALUES
	 ('08bbe571-08e4-4c94-aa8c-38297e345508'::uuid,'SCL3300 inclinometer array testing',false,'ANALYSIS','SCL3300 inclinometer array for testing');
INSERT INTO public.group_device_map (group_id,device_id) VALUES
	 ('08bbe571-08e4-4c94-aa8c-38297e345508'::uuid,'1e2e02e6-45c3-4ed5-9c6c-1d082dcdeebb'::uuid),
	 ('08bbe571-08e4-4c94-aa8c-38297e345508'::uuid,'2114e19a-ad03-4e1d-a6b5-a249cd080678'::uuid),
	 ('08bbe571-08e4-4c94-aa8c-38297e345508'::uuid,'35b1b9f2-a38f-4a57-a590-d6846e98e677'::uuid),
	 ('08bbe571-08e4-4c94-aa8c-38297e345508'::uuid,'4b66ad07-06b3-482b-9dfc-c704c0e88bc5'::uuid),
	 ('08bbe571-08e4-4c94-aa8c-38297e345508'::uuid,'56abc7ca-63da-48b7-9ce6-c0f03c01ae15'::uuid);
INSERT INTO public.set_template (template_id,"name",description) VALUES
	 ('2a0a32e0-6254-481b-bf7c-6388de21e7cc'::uuid,'SCL3300 Inclinometer set 2','2 nodes YZ SCL3300 inclinometer array set'),
	 ('494578cc-096b-482c-af18-ace228b68301'::uuid,'SCL3300 Inclinometer set 4','4 nodes YZ SCL3300 inclinometer array set'),
	 ('5f02f8c0-bbe5-4516-9b5b-1b6be7312b77'::uuid,'SCL3300 Inclinometer set 5','5 nodes YZ SCL3300 inclinometer array set'),
	 ('6ece455b-0380-47d1-bd63-80863fd0172c'::uuid,'SCL3300 Inclinometer set 6','6 nodes YZ SCL3300 inclinometer array set'),
	 ('8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'SCL3300 Inclinometer set 8','8 nodes YZ SCL3300 inclinometer array set');
INSERT INTO public.set_template_map (template_id,type_id,model_id,data_index,template_index) VALUES
	 ('2a0a32e0-6254-481b-bf7c-6388de21e7cc'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),0),
	 ('2a0a32e0-6254-481b-bf7c-6388de21e7cc'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),1),
	 ('494578cc-096b-482c-af18-ace228b68301'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),0),
	 ('494578cc-096b-482c-af18-ace228b68301'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),1),
	 ('494578cc-096b-482c-af18-ace228b68301'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),2),
	 ('494578cc-096b-482c-af18-ace228b68301'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),3),
	 ('5f02f8c0-bbe5-4516-9b5b-1b6be7312b77'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),0),
	 ('5f02f8c0-bbe5-4516-9b5b-1b6be7312b77'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),1),
	 ('5f02f8c0-bbe5-4516-9b5b-1b6be7312b77'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),2),
	 ('5f02f8c0-bbe5-4516-9b5b-1b6be7312b77'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),3),
	 ('5f02f8c0-bbe5-4516-9b5b-1b6be7312b77'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),4),
	 ('6ece455b-0380-47d1-bd63-80863fd0172c'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),0),
	 ('6ece455b-0380-47d1-bd63-80863fd0172c'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),1),
	 ('6ece455b-0380-47d1-bd63-80863fd0172c'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),2),
	 ('6ece455b-0380-47d1-bd63-80863fd0172c'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),3),
	 ('6ece455b-0380-47d1-bd63-80863fd0172c'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),4),
	 ('6ece455b-0380-47d1-bd63-80863fd0172c'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),5),
	 ('8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),0),
	 ('8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),1),
	 ('8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),2),
	 ('8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),3),
	 ('8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),4),
	 ('8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),5),
	 ('8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),6),
	 ('8f213453-c1ac-4f93-9922-b07a868a0271'::uuid,'a2a8496f-3e35-495c-8631-ef85b1a0fc7e'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),7);
INSERT INTO public."set" (set_id,template_id,"name",description) VALUES
	 ('0cde1db3-d231-4163-a29a-04abb72b82e7'::uuid,'5f02f8c0-bbe5-4516-9b5b-1b6be7312b77'::uuid,'SCL3300 inclinometer set testing','SCL3300 inclinometer array set for testing');
INSERT INTO public.set_map (set_id,device_id,model_id,data_index,set_position,set_number) VALUES
	 ('0cde1db3-d231-4163-a29a-04abb72b82e7'::uuid,'1e2e02e6-45c3-4ed5-9c6c-1d082dcdeebb'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),0,20),
	 ('0cde1db3-d231-4163-a29a-04abb72b82e7'::uuid,'2114e19a-ad03-4e1d-a6b5-a249cd080678'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),4,20),
	 ('0cde1db3-d231-4163-a29a-04abb72b82e7'::uuid,'35b1b9f2-a38f-4a57-a590-d6846e98e677'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),8,20),
	 ('0cde1db3-d231-4163-a29a-04abb72b82e7'::uuid,'4b66ad07-06b3-482b-9dfc-c704c0e88bc5'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),12,20),
	 ('0cde1db3-d231-4163-a29a-04abb72b82e7'::uuid,'56abc7ca-63da-48b7-9ce6-c0f03c01ae15'::uuid,'054c454e-7cda-496a-8778-82e85b5f912e'::uuid,decode('00010203','hex'),16,20);
