--
-- PostgreSQL database dump
--

-- Dumped from database version 11.6 (Debian 11.6-1.pgdg90+1)
-- Dumped by pg_dump version 11.6 (Debian 11.6-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
f384c81e6b0f
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, title_th, subtitle_th, title_en, subtitle_en, objective, abstract, introduction, method, status, approved_at, created_at, denied_at, submitted_at, updated_at) FROM stdin;
1	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.	draft	\N	2020-02-13 02:46:00+00	\N	\N	\N
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.applications (id, organization, detail, datetime, project_id) FROM stdin;
1	ตำบลคลองใหม่	นำไปให้ชาวบ้านทดลองใช้งาน ได้ผลดีมาก	2020-02-13 02:41:00+00	1
2	กรุงเทพมหานคร	นำไปให้ประชาชนในกทม.ทดลองใช้	2020-02-03 02:41:00+00	1
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, category) FROM stdin;
1	Informatics
\.


--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departments (id, name_th, name_en) FROM stdin;
1	เทคนิคการแพทย์ชุมชน	\N
\.


--
-- Data for Name: programs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.programs (id, name_th, name_en, dept_id) FROM stdin;
1	สารสนเทศทางการแพทย์	้Health informatics	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password_hash) FROM stdin;
1	likit.pre@mahidol.edu	pbkdf2:sha256:150000$cqKt1PTk$8c03aaa8c2e8b4e81b1f0d138ba1f11979489b04ab8605de461353a7f357c9c5
2	preeyanonlk@gmail.com	pbkdf2:sha256:150000$Gt2L0ivE$63c984787615f8a993c6b2c772ae5892bca31976ca9ae2641b3baa3af533ca62
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profiles (id, user_id, title_th, title_en, firstname_th, lastname_th, firstname_en, lastname_en, program_id) FROM stdin;
1	1	อาจารย์	Mr.	ลิขิต	ปรียานนท์	Likit	Preeyanon	1
2	2	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: educations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.educations (id, degree, degree_title, field, program, university, profile_id) FROM stdin;
1	doctorate	Ph.D. Microbiology and Molecular Genetics	Bioinformatics	Microbiology and Molecular Genetics	Michigan State University	1
2	bachelor	วท.บ. (เทคนิคการแพทย์)	\N	เทคนิคการแพทย์	มหาวิทยาลัยมหิดล	1
\.


--
-- Data for Name: project_members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_members (id, project_id, user_id, role) FROM stdin;
1	1	1	head
\.


--
-- Data for Name: subcategories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subcategories (id, category, parent_id, project_id) FROM stdin;
1	Health	1	1
2	Infectious diseases	1	1
\.


--
-- Name: applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.applications_id_seq', 2, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 1, true);


--
-- Name: departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.departments_id_seq', 1, true);


--
-- Name: educations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.educations_id_seq', 2, true);


--
-- Name: profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.profiles_id_seq', 2, true);


--
-- Name: programs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.programs_id_seq', 1, true);


--
-- Name: project_members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_members_id_seq', 1, true);


--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_id_seq', 1, true);


--
-- Name: subcategories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subcategories_id_seq', 2, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--

