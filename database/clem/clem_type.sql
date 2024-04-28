INSERT INTO public.device_type (type_id,name,description) VALUES
	 ('590a38bf-5f01-4c37-b180-7bbc3ffea47e','gateway blank','gateway with no model'),
	 ('1d9e6f6d-62b3-45c1-a7c6-40572b0aa6d5','timestamp and counter','testing device with timestamp and counter data'),
	 ('275ca06a-a4eb-4b16-bf4c-28f5b5469a76','running hour sensor','electric energy meter used for running hour sensor'),
	 ('af95f674-994d-49b3-a2de-8f92ffd46e46','running hour sensor testing','running hour sensor for testing purpose');
INSERT INTO public.device_type_model (type_id,model_id) VALUES
	 ('1d9e6f6d-62b3-45c1-a7c6-40572b0aa6d5','05d9461d-7ac4-4822-abc5-bf4ce0d3c92b'),
	 ('1d9e6f6d-62b3-45c1-a7c6-40572b0aa6d5','8c80cf30-1af8-4b0c-a57c-e84305729a4f'),
	 ('275ca06a-a4eb-4b16-bf4c-28f5b5469a76','f4f3a383-be81-436b-af44-766791156149'),
	 ('275ca06a-a4eb-4b16-bf4c-28f5b5469a76','b9aed100-f7d0-4857-88cb-3d7c5efc4431'),
	 ('275ca06a-a4eb-4b16-bf4c-28f5b5469a76','0d1d8cf2-a947-4086-8033-93548be6dc88'),
	 ('275ca06a-a4eb-4b16-bf4c-28f5b5469a76','45d0c1ae-0738-4a19-9dc0-feeeb55d7fab'),
	 ('275ca06a-a4eb-4b16-bf4c-28f5b5469a76','a1ef4e6a-efe1-40fa-a077-04785328a460'),
	 ('275ca06a-a4eb-4b16-bf4c-28f5b5469a76','1039f8c7-dd5a-435c-82b0-41936e91c840'),
	 ('275ca06a-a4eb-4b16-bf4c-28f5b5469a76','5182f792-2903-44f5-8b36-4cdd48dd68e8'),
	 ('af95f674-994d-49b3-a2de-8f92ffd46e46','f4f3a383-be81-436b-af44-766791156149'),
	 ('af95f674-994d-49b3-a2de-8f92ffd46e46','b9aed100-f7d0-4857-88cb-3d7c5efc4431'),
	 ('af95f674-994d-49b3-a2de-8f92ffd46e46','0d1d8cf2-a947-4086-8033-93548be6dc88'),
	 ('af95f674-994d-49b3-a2de-8f92ffd46e46','45d0c1ae-0738-4a19-9dc0-feeeb55d7fab'),
	 ('af95f674-994d-49b3-a2de-8f92ffd46e46','a1ef4e6a-efe1-40fa-a077-04785328a460'),
	 ('af95f674-994d-49b3-a2de-8f92ffd46e46','1039f8c7-dd5a-435c-82b0-41936e91c840'),
	 ('af95f674-994d-49b3-a2de-8f92ffd46e46','5182f792-2903-44f5-8b36-4cdd48dd68e8');
