INSERT INTO public.device_type (type_id,"name",description) VALUES
	 ('e0902405-9a96-497a-8fab-2deb007d8a0f','gateway blank','gateway with no model'),
	 ('eea82bb2-d427-4081-890d-c7c4795fd6f7','soil inclinometer','3-axis accelerometer and soil inclinometer'),
	 ('3b48c722-766a-4cc4-8fe9-cf7d8a3cff69','piezometer','piezometer with fluid pressure and depth output'),
	 ('24709a09-0cf3-47e4-9080-efa7cd2860be','rain gauge','tipping bucket rain gauge with daily and hourly rain fall output'),
	 ('99f387e1-e082-4e52-9f03-f2a6fa3f3e35','environment sensor','environment sensor with air temperature, relative humidity, and  output');
INSERT INTO public.device_type_model (type_id,model_id) VALUES
	 ('eea82bb2-d427-4081-890d-c7c4795fd6f7','2f85c046-6851-4b80-8e6e-3698e9e707db'),
	 ('eea82bb2-d427-4081-890d-c7c4795fd6f7','9d93adb9-4a93-4e26-998c-26349d9932a8'),
	 ('3b48c722-766a-4cc4-8fe9-cf7d8a3cff69','eb93788f-aa61-421c-916d-f7d6026256de'),
	 ('3b48c722-766a-4cc4-8fe9-cf7d8a3cff69','91b65b70-c421-42fa-8c54-16fc8bbed445'),
	 ('24709a09-0cf3-47e4-9080-efa7cd2860be','ed66830d-ce39-4dc9-a8f2-6eac3fef461f'),
	 ('24709a09-0cf3-47e4-9080-efa7cd2860be','6a28ad85-0a32-41b8-acb5-ee92a523ec74'),
	 ('99f387e1-e082-4e52-9f03-f2a6fa3f3e35','c16908e8-cc52-49bf-9619-03c1c79edfb3'),
	 ('99f387e1-e082-4e52-9f03-f2a6fa3f3e35','939909f1-798d-4073-88eb-e80a3b846e40');
