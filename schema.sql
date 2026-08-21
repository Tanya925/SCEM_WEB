-- ??????? SCEM ???? SQLite ?????????????
BEGIN TRANSACTION;
CREATE TABLE "general_info" (id INTEGER PRIMARY KEY AUTOINCREMENT, page_title_en TEXT NOT NULL, page_title_th TEXT NOT NULL, about_content_en TEXT, about_content_th TEXT, content_en TEXT, content_th TEXT);
INSERT INTO "general_info" VALUES(1,'Supply Chain and Engineering Management Research Unit: CMU','หน่วยวิจัยการจัดการโซ่อุปทานและวิศวกรรม: CMU','The Supply Chain and Engineering Management Research Unit (SCEM) focuses on research in logistics, supply chain management, and engineering management.

Its research activities cover logistics and supply chain strategy development, industrial logistics, supply chain improvement, simulation and optimization, productivity improvement, and sustainability development.','หน่วยวิจัยการจัดการโซ่อุปทานและวิศวกรรม (SCEM) มุ่งเน้นการวิจัยด้านโลจิสติกส์ การจัดการโซ่อุปทาน และการจัดการวิศวกรรม

กิจกรรมวิจัยครอบคลุมการพัฒนากลยุทธ์ด้านโลจิสติกส์และโซ่อุปทาน โลจิสติกส์อุตสาหกรรม การปรับปรุงโซ่อุปทาน การจำลองและการหาค่าที่เหมาะสม การเพิ่มผลิตภาพ และการพัฒนาความยั่งยืน','Details and Works



Logistics/ Supply Chain Strategy Development



- Roadmap design for Research and Innovation ecosystem for industries, government agencies, high-skill workforces, and university talents



- Strategy development and policy suggestion for Special Economic Corridors



- Logistics assessment for Greater Mekong Subregion (GMS) and ASEAN Economic Community (AEC)



- Feasibility study and economic impact assessment



Industrial Logistics



- Supply chain redesign for small Battery Electric Vehicle (BEV), agro and food industries, logistics industries



- Performance measurement for industrial logistics



- Logistics and supply chain improvement, simulation and optimization for industries



- Productivity improvement and engineering management for industries



- Sustainability development for industries



- Logistics and supply chain for Industry 4.0 and Industry 5.0','รายละเอียดและผลงาน



การพัฒนากลยุทธ์ด้านโลจิสติกส์และโซ่อุปทาน



- การออกแบบแผนที่นำทางสำหรับระบบนิเวศการวิจัยและนวัตกรรมสำหรับภาคอุตสาหกรรม หน่วยงานภาครัฐ บุคลากรทักษะสูง และบุคลากรที่มีศักยภาพในมหาวิทยาลัย



- การพัฒนากลยุทธ์และการเสนอแนะเชิงนโยบายสำหรับระเบียงเศรษฐกิจพิเศษ



- การประเมินด้านโลจิสติกส์สำหรับอนุภูมิภาคลุ่มแม่น้ำโขง (GMS) และประชาคมเศรษฐกิจอาเซียน (AEC)



- การศึกษาความเป็นไปได้และการประเมินผลกระทบทางเศรษฐกิจ



โลจิสติกส์อุตสาหกรรม



- การออกแบบโซ่อุปทานใหม่สำหรับอุตสาหกรรมยานยนต์ไฟฟ้าแบตเตอรี่ขนาดเล็ก (BEV) อุตสาหกรรมการเกษตรและอาหาร และอุตสาหกรรมโลจิสติกส์



- การวัดผลการดำเนินงานด้านโลจิสติกส์อุตสาหกรรม



- การปรับปรุง การจำลอง และการหาค่าที่เหมาะสมด้านโลจิสติกส์และโซ่อุปทานสำหรับภาคอุตสาหกรรม



- การปรับปรุงผลิตภาพและการจัดการวิศวกรรมสำหรับภาคอุตสาหกรรม



- การพัฒนาความยั่งยืนสำหรับภาคอุตสาหกรรม



- โลจิสติกส์และโซ่อุปทานสำหรับอุตสาหกรรม 4.0 และอุตสาหกรรม 5.0');
CREATE TABLE home_activity_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL UNIQUE
);
INSERT INTO "home_activity_images" VALUES(1,'Info1.jpg');
INSERT INTO "home_activity_images" VALUES(2,'Info2.jpg');
INSERT INTO "home_activity_images" VALUES(3,'Info3.jpg');
INSERT INTO "home_activity_images" VALUES(4,'Info4.jpg');
INSERT INTO "home_activity_images" VALUES(5,'Info5.jpg');
INSERT INTO "home_activity_images" VALUES(6,'Info6.jpg');
CREATE TABLE "publications" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_order INTEGER NOT NULL DEFAULT 0,
                title TEXT NOT NULL,
                authors TEXT NOT NULL DEFAULT '',
                journal TEXT NOT NULL DEFAULT '',
                publication_year INTEGER,
                volume TEXT NOT NULL DEFAULT '',
                issue TEXT NOT NULL DEFAULT '',
                article_number TEXT NOT NULL DEFAULT '',
                page TEXT NOT NULL DEFAULT '',
                pdf_url TEXT NOT NULL DEFAULT '',
                scopus_eid TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
CREATE TABLE research_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_type TEXT NOT NULL CHECK (project_type IN ('ongoing', 'finished')),
    year_en TEXT,
    year_th TEXT,
    title_en TEXT NOT NULL,
    title_th TEXT NOT NULL,
    leader_en TEXT,
    leader_th TEXT,
    leader_photo_filename TEXT,
    deputy_en TEXT,
    deputy_th TEXT,
    deputy_photo_filename TEXT,
    coordinator_en TEXT,
    coordinator_th TEXT,
    coordinator_photo_filename TEXT,
    advisor_en TEXT,
    advisor_th TEXT,
    advisor_photo_filename TEXT,
    researcher_en TEXT,
    researcher_th TEXT,
    researcher_photos_json TEXT,
    engineer_en TEXT,
    engineer_th TEXT,
    engineer_photos_json TEXT,
    assistant_en TEXT,
    assistant_th TEXT,
    assistant_photos_json TEXT,
    duration_en TEXT,
    duration_th TEXT,
    lead_unit_en TEXT,
    lead_unit_th TEXT,
    partner_en TEXT,
    partner_th TEXT,
    funding_en TEXT,
    funding_th TEXT,
    budget_en TEXT,
    budget_th TEXT,
    collaboration_details_en TEXT,
    collaboration_details_th TEXT,
    custom_team_fields_json TEXT,
    custom_detail_fields_json TEXT,
    notes TEXT,
    description_en TEXT,
    description_th TEXT
);
INSERT INTO "research_projects" VALUES(76,'finished','','','Design and Development of Researcher Capacity Building Curriculum for Higher Education Institutions and a Support System for Building R&D Strategies and Action Plans for Enterprises (Talent Mobility System) to Support Personnel Mobility for Research Capacity Development in the Industrial Sector (Talent Mobility Track 2)','การออกแบบและพัฒนาหลักสูตรการพัฒนาศักยภาพนักวิจัยของสถาบันอุดมศึกษา และระบบสนับสนุนการสร้างกลยุทธ์และแผนปฏิบัติการด้านการวิจัยและพัฒนาสำหรับสถานประกอบการ (Talent Mobility System) รองรับการเคลื่อนย้ายบุคลากร เพื่อพัฒนาศักยภาพการวิจัยในภาคอุตสาหกรรม (Talent Mobility Track 2)','Prof. Apichat Sopadang, Ph.D.','ศาสตราจารย์ ดร.อภิชาต โสภาแดง',NULL,NULL,'Assoc. Prof. Sakgasem Ramingwong, Ph.D.','รองศาสตราจารย์ ดร.ศักดิ์เกษม ระมิงค์วงศ์',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Asst. Prof. Salinee Santiteerakul, Ph.D.','ผู้ช่วยศาสตราจารย์ ดร.สาลินี สันติธีรากุล',NULL,NULL,'Miss Chalisa Naroon','นางสาวชาลิสา ณรุณ',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'The first phase of the Talent Mobility System development, covering the design of a 15-hour expert training curriculum (Track 2.1) and the development of the central support system website, talentmobility.in.th, including the public relations and application system, expert database, learning assessment system, and project monitoring and reporting system.','โครงการระยะแรกของการพัฒนาระบบ Talent Mobility System ครอบคลุมการออกแบบหลักสูตรอบรมผู้เชี่ยวชาญ 15 ชั่วโมง (Track 2.1) และพัฒนาเว็บไซต์ระบบสนับสนุนกลาง talentmobility.in.th ทั้งระบบประชาสัมพันธ์-รับสมัคร ฐานข้อมูลผู้เชี่ยวชาญ ระบบประเมินผลการเรียนรู้ และระบบรายงานผลติดตามโครงการ');
INSERT INTO "research_projects" VALUES(77,'finished','','','Design and Development of Researcher Capacity Building Curriculum for Higher Education Institutions and a Support System for Building R&D Strategies and Action Plans for Enterprises (Additional Phase)','การออกแบบและพัฒนาหลักสูตรการพัฒนาศักยภาพนักวิจัยของสถาบันอุดมศึกษาและระบบสนับสนุนการสร้างกลยุทธ์และแผนปฏิบัติการด้านการวิจัยและพัฒนาสำหรับสถานประกอบการ (เพิ่มเติม)','Prof. Apichat Sopadang, Ph.D.','ศาสตราจารย์ ดร.อภิชาต โสภาแดง',NULL,NULL,'Assoc. Prof. Sakgasem Ramingwong, Ph.D.','รองศาสตราจารย์ ดร.ศักดิ์เกษม ระมิงค์วงศ์',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Asst. Prof. Salinee Santiteerakul, Ph.D.','ผู้ช่วยศาสตราจารย์ ดร.สาลินี สันติธีรากุล',NULL,NULL,'Miss Chalisa Naroon','นางสาวชาลิสา ณรุณ',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'An extension of the first phase, providing additional expert training for cohorts 4-6 (100 participants in total) and adding an "Enterprise" application and database function to the Talent Mobility System to more comprehensively support collaboration with the industrial sector.','ต่อยอดโครงการจากระยะแรก ด้วยการจัดอบรมผู้เชี่ยวชาญเพิ่มเติมรุ่นที่ 4–6 (รวม 100 คน) พร้อมทั้งเพิ่มฟังก์ชันระบบรับสมัครและฐานข้อมูล "สถานประกอบการ" เข้าสู่ระบบ Talent Mobility System เพื่อรองรับการทำงานร่วมกับภาคอุตสาหกรรมได้ครบวงจรยิ่งขึ้น');
INSERT INTO "research_projects" VALUES(78,'finished','','','Design and Development of Researcher Capacity Building Curriculum for Higher Education Institutions and a Support System for Building R&D Strategies and Action Plans for Enterprises (Additional Phase 2)','การออกแบบและพัฒนาหลักสูตรการพัฒนาศักยภาพนักวิจัยของสถาบันอุดมศึกษาและระบบสนับสนุนการสร้างกลยุทธ์และแผนปฏิบัติการด้านการวิจัยและพัฒนาสำหรับสถานประกอบการ (เพิ่มเติม) ครั้งที่ 2','Prof. Apichat Sopadang, Ph.D.','ศาสตราจารย์ ดร.อภิชาต โสภาแดง',NULL,NULL,'Assoc. Prof. Sakgasem Ramingwong, Ph.D.','รองศาสตราจารย์ ดร.ศักดิ์เกษม ระมิงค์วงศ์',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Asst. Prof. Salinee Santiteerakul, Ph.D.','ผู้ช่วยศาสตราจารย์ ดร.สาลินี สันติธีรากุล',NULL,NULL,'Miss Chalisa Naroon','นางสาวชาลิสา ณรุณ',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Expansion of the Talent Mobility System to cover Track 1 (technology deployment) and Track 3 (R&D activity stimulation), in addition to the existing Track 2 support, together with expert training for cohorts 7-10 (120 participants in total) and knowledge-sharing seminars to review the curriculum and the system with past experts.','ขยายระบบ Talent Mobility System ให้ครอบคลุม Track 1 (ติดตั้งเทคโนโลยี) และ Track 3 (กระตุ้นกิจกรรม R&D) เพิ่มเติมจากเดิมที่รองรับเฉพาะ Track 2 พร้อมจัดอบรมผู้เชี่ยวชาญรุ่นที่ 7–10 (รวม 120 คน) และจัดเวทีสัมมนาแลกเปลี่ยนเรียนรู้เพื่อทบทวนหลักสูตรและระบบร่วมกับผู้เชี่ยวชาญที่ผ่านมา');
INSERT INTO "research_projects" VALUES(79,'ongoing','','','Enhancing Personnel Mobility to Strengthen Industrial Competitiveness and Improving the Architectural Efficiency of the Supporting Information System','การยกระดับการเคลื่อนย้ายบุคลากรเพื่อพัฒนาขีดความสามารถการแข่งขันในภาคอุตสาหกรรมและการเพิ่มประสิทธิภาพเชิงสถาปัตยกรรมของระบบสารสนเทศสนับสนุน','Professor Dr. Apichat Sopadang','ศาสตราจารย์ ดร.อภิชาต โสภาแดง',NULL,NULL,'Associate Professor Dr. Sakgasem Ramingwong','รองศาสตราจารย์ ดร.ศักดิ์เกษม ระมิงค์วงศ์',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Assistant Professor Dr. Salinee Santiteerakul','ผู้ช่วยศาสตราจารย์ ดร.สาลินี สันติธีรากุล',NULL,NULL,'Miss Chalisa Naroon','นางสาวชาลิสา ณรุณ',NULL,NULL,'','',NULL,NULL,'12 months (25 June 2026 - 24 June 2027)','12 เดือน (25 มิถุนายน 2569 - 24 มิถุนายน 2570)','','','','','','',NULL,NULL,NULL,'','',NULL,NULL,NULL,'','A digital platform supporting the mobility of research personnel from higher education institutions into industry to strengthen industrial research capability (Talent Mobility), supported by the Office of the Permanent Secretary, MHESI. Developed continuously through several phases since 2023, the platform covers expert training curriculum design (Track 2.1), R&D strategy formulation for enterprises (Track 2.2), and most recently expansion to support Track 1 (technology deployment) and Track 3 (stimulation of R&D activity). Delivered through talentmobility.in.th, the system covers public relations, application intake, expert and enterprise databases, assessment, and project management and monitoring. To date more than 375 experts have registered and more than 20 projects have been undertaken with enterprises. The current phase focuses on maintaining system stability and continuous availability.','แพลตฟอร์มดิจิทัลสนับสนุนการเคลื่อนย้ายบุคลากรวิจัยจากสถาบันอุดมศึกษาไปช่วยพัฒนาศักยภาพการวิจัยให้ภาคอุตสาหกรรม (Talent Mobility) ภายใต้การสนับสนุนของ สป.อว. พัฒนาต่อเนื่องมาหลายระยะตั้งแต่ปี 2566 จนถึงปัจจุบัน ครอบคลุมทั้งการออกแบบหลักสูตรอบรมผู้เชี่ยวชาญ (Track 2.1) การสร้างกลยุทธ์วิจัยและพัฒนาให้สถานประกอบการ (Track 2.2) และล่าสุดขยายผลรองรับ Track 1 (ติดตั้งเทคโนโลยี) และ Track 3 (กระตุ้นกิจกรรม R&D) ระบบให้บริการผ่านเว็บไซต์ talentmobility.in.th ครอบคลุมงานประชาสัมพันธ์ รับสมัคร ฐานข้อมูลผู้เชี่ยวชาญและสถานประกอบการ ระบบประเมินผล และระบบติดตามบริหารโครงการ ปัจจุบันมีผู้เชี่ยวชาญขึ้นทะเบียนแล้วกว่า 375 คน และดำเนินโครงการร่วมกับสถานประกอบการไปแล้วกว่า 20 โครงการ โดยเฟสล่าสุดมุ่งเน้นการดูแลรักษาระบบให้มีเสถียรภาพและพร้อมใช้งานต่อเนื่อง');
INSERT INTO "research_projects" VALUES(80,'ongoing','','','Platform for Preparing Smart Geothermal Cooling Systems and Developing Supply Chain Resilience for Cold Storage Warehouse Infrastructure and Cold-Chain Logistics in the Thai Seafood Industry','โครงการแพลตฟอร์มเตรียมความพร้อมระบบทำความเย็นอัจฉริยะด้วยพลังงานใต้ดิน และการพัฒนาระบบ Supply Chain Resilience สำหรับโครงสร้างพื้นฐานคลังสินค้าห้องเย็นและ Cold-Chain Logistics ในอุตสาหกรรมอาหารทะเลของไทย','Associate Professor Dr. Poti Chaopaisarn','รองศาสตราจารย์ ดร. โพธิ จ้าวไพศาล',NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,'Professor of Practice Dr. Sate Sampattagul
Associate Professor Dr. Sakgasem Ramingwong
Associate Professor Dr. Thoranis Deethayat
Assistant Professor Dr. Yasinee Chakrabandhu','ศาสตราจารย์ปฏิบัติ ดร.เศรษฐ์ สัมภัตตะกุล
รองศาสตราจารย์ ดร.ศักดิ์เกษม ระมิงค์วงศ์
รองศาสตราจารย์ ดร.ธรณิศวร์ ดีทายาท
ผู้ช่วยศาสตราจารย์ ดร.ม.ล. ญาศินี จักรพันธุ์','["Sampattagul.png", "", "Deethayat.jpg", "Chakrabandhu.png"]','','','[]','Miss Chalisa Naroon','นางสาวชาลิสา ณรุณ','[""]','12 months','12 เดือน','Supply Chain and Engineering Management Research Unit, Chiang Mai University (principal grantee)','กลุ่มวิจัยการจัดการห่วงโซ่อุปทานและวิศวกรรม มหาวิทยาลัยเชียงใหม่ (ผู้รับทุนหลัก)','RT Geothermal Co., Ltd. - Technology Partner (geothermal system design and geological analysis)

U-PIN Urban Platform (UNISERV) - Data Platform Partner (dashboard and data integration development)

Participating enterprise - pilot test bed','บริษัท อาร์ที จีโอเทอร์มอล จำกัด — Technology Partner (ออกแบบระบบ Geothermal, วิเคราะห์ธรณีวิทยา)

U-PIN Urban Platform (UNISERV) — Data Platform Partner (พัฒนา Dashboard และระบบ Data Integration)

สถานประกอบการร่วมทุน — ไซต์นำร่อง (Test Bed)','Program Management Unit for Competitiveness (PMUC)','หน่วยบริหารและจัดการทุนด้านการเพิ่มความสามารถในการแข่งขันของประเทศ (บพข.)','None','None','','','[]','[]','','A 12-month pre-pilot applied research project examining the feasibility and readiness of deploying smart geothermal cooling in Thailand''s cold storage warehouse and cold-chain logistics industry, alongside the development of an assessment and strengthening framework for supply chain resilience in the seafood industry. Working with a private-sector partner in Samut Sakhon Province, the project collects field data from a pilot site, analyses technical and economic feasibility, and develops a digital platform (U-PIN Dashboard) for energy and supply chain management. Full deployment in a subsequent phase is expected to reduce energy costs by 15-25% and spoilage losses by 5-10%.','งานวิจัยเชิงประยุกต์ระยะ Pre-Pilot (12 เดือน) เพื่อศึกษาความเป็นไปได้และเตรียมความพร้อมสำหรับการนำระบบทำความเย็นด้วยพลังงานความร้อนใต้ดิน (Smart Geothermal Cooling) มาใช้ในอุตสาหกรรมคลังสินค้าห้องเย็นและ Cold-Chain Logistics ของไทย ควบคู่กับการพัฒนากรอบการประเมินและเสริมสร้างความยืดหยุ่นของห่วงโซ่อุปทาน (Supply Chain Resilience) สำหรับภาคอุตสาหกรรมอาหารทะเล โดยทำงานร่วมกับสถานประกอบการภาคเอกชนในพื้นที่ จ.สมุทรสาคร เพื่อเก็บข้อมูลจริงจากไซต์นำร่อง วิเคราะห์ความเป็นไปได้ทางเทคนิคและเศรษฐศาสตร์ และพัฒนาแพลตฟอร์มดิจิทัล (U-PIN Dashboard) สำหรับบริหารจัดการพลังงานและโซ่อุปทาน คาดว่าหากติดตั้งระบบจริงในระยะต่อไปจะช่วยลดต้นทุนพลังงานได้ 15–25% และลดการสูญเสียสินค้า (Spoilage) ได้ 5–10%');
INSERT INTO "research_projects" VALUES(81,'ongoing','','','Lancang-Mekong Cooperation Special Fund 2023: Prospect Supply Chain for Small Battery Electric Vehicle (BEV) in Lancang-Mekong Region','โครงการกองทุนพิเศษแม่โขง-ล้านช้าง ประจำปี 2566 Prospect Supply Chain for Small Battery Electric Vehicle (BEV) in Lancang-Mekong Region','Associate Professor Dr. Sakgasem Ramingwong','รองศาสตราจารย์ ดร.ศักดิ์เกษม ระมิงค์วงศ์',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Professor Dr. Apichat Sopadang
Assistant Professor Dr. Korrakot Yaibuathet Tippayawong
Assistant Professor Dr. Salinee Santiteerakul
Associate Professor Dr. Poti Chaopaisarn','ศาสตราจารย์ ดร.อภิชาต โสภาแดง, ผู้ช่วยศาสตราจารย์ ดร.กรกฎ ใยบัวเทศ ทิพยาวงศ์, ผู้ช่วยศาสตราจารย์ ดร.สาลินี สันติธีรากุล, รองศาสตราจารย์ ดร.โพธิ จ้าวไพศาล',NULL,NULL,'Miss Jidapa Chanjaroen
Miss Jurairat Rintieng','นางสาวจิดาภา ชาญเจริญ
นางสาวจุไรรัตน์ รินเที่ยง',NULL,NULL,'','',NULL,NULL,'1 January 2024 - 1 January 2027','1 มกราคม พ.ศ. 2567 – 1 มกราคม พ.ศ. 2570','Supply Chain and Engineering Management Research Unit (SCEM), Faculty of Engineering, Chiang Mai University','หน่วยวิจัยการจัดการโซ่อุปทานและวิศวกรรมการจัดการ (SCEM) คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเชียงใหม่','Shanghai Jiao Tong University, People''s Republic of China
National University of Laos, Lao PDR
Luangprabang Technical Vocational College, Lao PDR
Vietnam Institute of Agricultural Engineering and Post Harvest Technology, Socialist Republic of Viet Nam
Royal University of Phnom Penh, Kingdom of Cambodia','1) Shanghai Jiao Tong University สาธารณรัฐประชาชนจีน 2) National University of Laos สปป.ลาว 3) Luangprabang Technical Vocational College สปป.ลาว 4) Vietnam Institute of Agricultural Engineering and Post Harvest Technology สาธารณรัฐสังคมนิยมเวียดนาม 5) Royal University of Phnom Penh ราชอาณาจักรกัมพูชา','Lancang-Mekong Cooperation Special Fund, under the Ministry of Higher Education, Science, Research and Innovation','กองทุนพิเศษกรอบความร่วมมือแม่โขง-ล้านช้าง (Lancang-Mekong Cooperation Special Fund) ภายใต้กระทรวงการอุดมศึกษา วิทยาศาสตร์ วิจัยและนวัตกรรม',NULL,NULL,NULL,'In collaboration with the College of Arts, Media and Technology, Chiang Mai University - working team: Assistant Professor Dr. Jirapat Wanitwattanakosol, Assistant Professor Tisinee Surapunt, Assistant Professor Dr. Boontarika Paphawasit, Dr. Suttinee Sawadsitang','ร่วมมือกับวิทยาลัยศิลปะ สื่อ และเทคโนโลยี มหาวิทยาลัยเชียงใหม่ โดยมีคณะทำงาน ได้แก่ ผู้ช่วยศาสตราจารย์ ดร.จิรพัฒน์ วาณิชวัฒนะโกศล, ผู้ช่วยศาสตราจารย์ ธิสินี สุรพันธ์, ผู้ช่วยศาสตราจารย์ ดร.บุณฑริกา ปภาวสิทธิ์, อาจารย์ ดร.ศุทธินี สวัสดิ์ซิตัง',NULL,NULL,NULL,'','A regional research and capacity-building project studying and designing a supply chain for small battery electric vehicles (Small BEVs) for agricultural and community applications in the Lancang-Mekong subregion, covering the supply network, logistics infrastructure, information systems, and financial flows across five target countries: Thailand, Lao PDR, China, Cambodia, and Viet Nam. Field research has now been completed in all five countries, drawing on 47 expert and stakeholder interviews, and has produced the SBEV Country Readiness Assessment Framework comprising seven dimensions and sixteen indicators, together with two articles published in international journals - the World Electric Vehicle Journal and Smart Cities (May 2026). On workforce development, the project has established a four-level EV technician career pathway framework with an accompanying training curriculum, and has delivered four hands-on workshops in Vientiane, Luang Prabang, and Chiang Mai. More than 120 technicians, engineers, and educators have been trained and more than 90 have received certificates of completion. The workshops have given rise to technical exchange networks that remain active after training, and to partnerships with the National University of Laos and Luangprabang Technical Vocational College as local EV training hubs, alongside coverage in Lao print and broadcast media. A four-tier cross-border financial flow architecture has also been designed in consultation with Bangkok Bank and the Bank of Thailand. Work in progress comprises the regional logistics network design, advanced technician training, and final dissemination of project outcomes.','โครงการวิจัยและพัฒนาศักยภาพระดับภูมิภาค เพื่อศึกษาและออกแบบห่วงโซ่อุปทานยานยนต์ไฟฟ้าขนาดเล็ก (Small BEV) สำหรับการใช้งานภาคเกษตรกรรมและชุมชนในอนุภูมิภาคล้านช้าง-แม่โขง ครอบคลุมเครือข่ายอุปทาน โครงสร้างพื้นฐานด้านโลจิสติกส์ ระบบสารสนเทศ และการไหลทางการเงิน ใน 5 ประเทศเป้าหมาย ได้แก่ ไทย สปป.ลาว จีน กัมพูชา และเวียดนาม ปัจจุบันดำเนินการเก็บข้อมูลภาคสนามครบทั้ง 5 ประเทศแล้ว ผ่านการสัมภาษณ์ผู้เชี่ยวชาญและผู้มีส่วนได้ส่วนเสียรวม 47 ราย นำไปสู่การพัฒนากรอบการประเมินความพร้อม รายประเทศด้านยานยนต์ไฟฟ้าขนาดเล็ก (SBEV Country Readiness Assessment Framework) จำนวน 7 มิติ 16 ตัวชี้วัด และตีพิมพ์บทความวิจัยในวารสารวิชาการนานาชาติแล้ว 2 ฉบับ ได้แก่ World Electric Vehicle Journal และ Smart Cities (พฤษภาคม 2569) ในด้านการพัฒนากำลังคน โครงการได้จัดทำกรอบเส้นทางอาชีพ ช่างเทคนิคยานยนต์ไฟฟ้า 4 ระดับ พร้อมหลักสูตรฝึกอบรม และจัดอบรมเชิงปฏิบัติการแล้ว 4 ครั้ง ณ นครหลวงเวียงจันทน์ หลวงพระบาง และจังหวัดเชียงใหม่ มีช่างเทคนิค วิศวกร และบุคลากรทางการศึกษาเข้ารับการอบรมรวมกว่า 120 คน ได้รับประกาศนียบัตรแล้วกว่า 90 คน เกิดเครือข่ายแลกเปลี่ยนความรู้ทางเทคนิคที่ยังดำเนินต่อเนื่องหลังการอบรม และเกิดความร่วมมือกับมหาวิทยาลัยแห่งชาติลาวและวิทยาลัยเทคนิควิชาชีพหลวงพระบางในการเป็นศูนย์ฝึกอบรมยานยนต์ไฟฟ้าประจำพื้นที่ พร้อมได้รับการเผยแพร่ผ่านสื่อท้องถิ่นทั้งหนังสือพิมพ์และโทรทัศน์ใน สปป.ลาว พร้อมกันนี้ได้ออกแบบสถาปัตยกรรมการไหลทางการเงินข้ามพรมแดน 4 ระดับ ร่วมกับธนาคารกรุงเทพและธนาคารแห่งประเทศไทย งานที่อยู่ระหว่างดำเนินการ ได้แก่ การออกแบบเครือข่ายโลจิสติกส์ระดับภูมิภาค การอบรมช่างเทคนิคระดับสูง และการเผยแพร่ผลงานขั้นสุดท้าย');
INSERT INTO "research_projects" VALUES(82,'finished','','','Strategic assessment of industrial cluster development to support the special economic corridor development plan, based on the BCG economic model towards sustainable development','การประเมินเชิงยุทธศาสตร์การพัฒนาคลัสเตอร์อุตสาหกรรมเพื่อส่งเสริมแผนพัฒนาระเบียงเศรษฐกิจพิเศษ บนฐานโมเดลเศรษฐกิจสู่การพัฒนาที่ยั่งยืน BCG','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(83,'finished','','','R&D Blueprint research and development activities for enterprises','กิจกรรมการวิจัยและพัฒนา R&D Blueprint สำหรับสถานประกอบการ','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(84,'finished','','','Consultant training activities (Train the Trainer) for developing R&D plans and guidelines (R&D Blueprint)','การจัดกิจกรรมอบรมที่ปรึกษา (Train the Trainer) เพื่อจัดทำแผนและแนวทางการทำวิจัยและพัฒนา (R&D Blueprint)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(85,'finished','','','Training course for developing higher-education experts to support Talent Mobility for enhancing industrial research capacity','การอบรมหลักสูตรการพัฒนาผู้เชี่ยวชาญของสถาบันอุดมศึกษา รองรับการเคลื่อนย้ายบุคลากรเพื่อพัฒนาศักยภาพการวิจัยในภาคอุตสาหกรรม (Talent Mobility)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(86,'finished','','','Development of a strategic plan for smart transportation and traffic management on Nimmanhaemin Road for safety and economic stimulation','การพัฒนาแผนกลยุทธ์ด้านการจัดการขนส่งและจราจรอัจฉริยะในพื้นที่ถนนนิมมานเหมินทร์เพื่อความปลอดภัยและกระตุ้นเศรษฐกิจ','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(87,'finished','','','Research on developing a master plan for the Northern Economic Corridor (NEC) based on the BCG Economy concept','โครงการวิจัยการพัฒนาแผนแม่บทการพัฒนาระเบียงเศรษฐกิจพิเศษภาคเหนือ (NEC) ด้วยแนวคิด BCG Economy','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(88,'finished','','','Research and development to sustainably improve logistics management efficiency in the industrial sector','การวิจัยและพัฒนาเพื่อเพิ่มประสิทธิภาพการจัดการโลจิสติกส์ภาคอุตสาหกรรมที่มีประสิทธิภาพอย่างยั่งยืน','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(89,'finished','','','Design and development of a capacity-building curriculum for university researchers, and a support system for R&D strategy and action plans for enterprises (Talent Mobility System) to support personnel mobility for enhancing industrial research capacity','การออกแบบและพัฒนาหลักสูตรการพัฒนาศักยภาพนักวิจัยของสถาบันอุดมศึกษา และระบบสนับสนุนการสร้างกลยุทธ์และแผนปฏิบัติด้านการวิจัยและพัฒนาสำหรับสถานประกอบการ (Talent Mobility System) รองรับการเคลื่อนย้ายบุคลากร เพื่อพัฒนาศักยภาพการวิจัยในภาคอุตสาหกรรม','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(90,'finished','','','Assessment activities for logistics and supply chain management capacity development','กิจกรรมประเมินการพัฒนาศักยภาพการบริหารจัดการโลจิสติกส์และซัพพลายเชน','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(91,'finished','','','Study to upgrade the private-sector collaboration management unit in Rajabhat universities in the North and Northeast','โครงการศึกษาเพื่อยกระดับหน่วยบริหารจัดการการพัฒนาความร่วมมือกับภาคเอกชน ในมหาวิทยาลัยราชภัฏกลุ่มภาคเหนือและภาคตะวันออกเฉียงเหนือ','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(92,'finished','2022','2565','Project to enhance logistics and supply chain management capabilities in the industrial sector, fiscal year 2022, Northern Region','โครงการเพิ่มขีดความสามารถในการบริหารจัดการโลจิสติกส์และโซ่อุปทานภาคอุตสาหกรรม ประจำปีงบประมาณ พ.ศ. 2565 ภาคเหนือ','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(93,'finished','','','Industry 4.0 for SMEs - Smart Manufacturing and Logistics for SMEs in an X-to-order and Mass Customization Environment (SME 4.0)','Industry 4.0 for SMEs - Smart Manufacturing and Logistics for SMEs in an X-to-order and Mass Customization Environment (SME 4.0)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(94,'finished','','','SHYFTE 4.0 - Building Skills 4.0 through University and Enterprise Collaboration','SHYFTE 4.0 - Building Skills 4.0 through University and Enterprise Collaboration','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(95,'finished','','','Research project to upgrade process management to drive the Office of the Permanent Secretary, Ministry of Industry, towards Government 4.0 innovation','โครงการวิจัยเพื่อยกระดับการบริหารจัดการกระบวนการเพื่อขับเคลื่อนสำนักงานปลัดกระทรวงอุตสาหกรรมสู่นวัตกรรมบริหารจัดการภาครัฐ 4.0','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(96,'finished','2021','2564','Growth-level SME promotion and development project (SME Regular Level), fiscal year 2021','โครงการส่งเสริมและพัฒนาธุรกิจระดับเติบโต (SME Regular Level) ปีงบประมาณ 2564','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(97,'finished','','','Foresight research and development plan for the Northern Science Park','การวิจัยมองอนาคตและแผนพัฒนาอุทยานวิทยาศาสตร์ภาคเหนือ','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(98,'finished','2021','2564','Study on developing an innovation product certification mark by regional science parks (RSP Innovation Mark), fiscal year 2021','โครงการศึกษาแนวทางการจัดทำเครื่องหมายรับรองผลิตภัณฑ์นวัตกรรม โดยอุทยานวิทยาศาสตร์ภูมิภาค (RSP Innovation mark) ประจำงบประมาณ พ.ศ.2564','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(99,'finished','','','Growth-level SME promotion and development project (SME Regular Level)','โครงการส่งเสริมและพัฒนาธุรกิจระดับเติบโต (SME Regular Level)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(100,'finished','2020','2563','Pan Dao (Rising Star) project, fiscal year 2020','โครงการปั้นดาว ปีงบประมาณ 2563','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(101,'finished','','','Impact study and business plan development for an integrated food innovation pilot plant (Innovation Food Fabrication Pilot Plant)','การศึกษาผลกระทบและจัดทำแผนธุรกิจ (Business Plan) โรงงานต้นแบบนวัตกรรมอาหารครบวงจร (Innovation Food Fabrication Pilot Plant)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(102,'finished','','','Impact analysis of the electric vehicle (EV) supply chain to develop policy for the development and adaptation of the Thai automotive industry to support EVs','การวิเคราะห์ผลกระทบของโซ่อุปทานรถยนต์ไฟฟ้า (Electric Vehicle: EV) เพื่อพัฒนานโยบายการพัฒนาและปรับตัวของอุตสาหกรรมยานยนต์ไทยเพื่อรองรับ EV','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(103,'finished','','','Study on the research and development of the logistics system of Thailand Post Co., Ltd.','โครงการศึกษาวิจัยและพัฒนาระบบโลจิสติกส์ของบริษัท ไปรษณีย์ไทย จำกัด','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(104,'finished','2019','2562','Project to promote community enterprise networks for sustainable development, 2019','โครงการส่งเสริมเครือข่ายวิสาหกิจชุมชนเพื่อการพัฒนาที่ยั่งยืน ปี 2562','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(105,'finished','2018','2561','Project to improve logistics management efficiency to reduce costs and increase competitiveness','โครงการเพิ่มประสิทธิภาพการบริหารจัดการโลจิสติกส์ เพื่อการลดต้นทุนและเพิ่มขีดความสามารถในการแข่งขัน','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(106,'finished','2017','2560','Impact study on establishing a Northern regional office of the National Innovation Agency (Public Organization)','โครงการศึกษาผลกระทบการจัดตั้งสำนักงานภาคเหนือของสำนักงานนวัตกรรมแห่งชาติ (องค์การมหาชน)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(107,'finished','2017','2560','Thai labor productivity enhancement project, fiscal year 2017','โครงการเพิ่มผลิตภาพแรงงานไทย ประจำปีงบประมาณ พ.ศ.2560','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(108,'finished','2017','2560','Project to develop logistics and supply chain management for industrial goods businesses in border trade areas, 2017','โครงการพัฒนาการจัดการโลจิสติกส์และโซ่อุปทานธุรกิจสินค้าอุตสาหกรรมในพื้นที่การค้าชายแดน ประจําปี 2560','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(109,'finished','2017','2560','Development of a database of logistics and supply chain benchmarking indicators for the industrial sector','โครงการพัฒนาฐานข้อมูลเกณฑ์เทียบวัดประสิทธิภาพโลจิสติกส์และโซ่อุปทานภาคอุตสาหกรรม','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(110,'finished','2016','2559','Study on the innovation needs of agricultural and food industry entrepreneurs in the Northern region','โครงการการศึกษาความต้องการด้านนวัตกรรมของผู้ประกอบการอุตสาหกรรมเกษตรและอาหารในพื้นที่ภาคเหนือ','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(111,'finished','','','Pilot project for direct-sale rice, homemade rice, and customizable rice under the Innovation Road Map project for the rice industry','โครงการนำร่องข้าวส่งตรง ข้าวโฮมเมด และข้าวเลือกได้ ภายใต้โครงการจัดทำ Innovation Road Map ของอุตสาหกรรมข้าว','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(112,'finished','2016','2559','Project to develop logistics and supply chain management for industrial goods businesses in border economic zones, 2016','โครงการพัฒนาการจัดการโลจิสติกส์และโซ่อุปทานธุรกิจสินค้า อุตสาหกรรมในเขตเศรษฐกิจชายแดน ประจําปี 2559','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(113,'finished','','','Comprehensive integrated training project to promote community enterprises and Northern SMEs towards international standards through innovation, standards, and packaging (Year 2)','โครงการการฝึกอบรมบูรณาการแบบครบวงจรเพื่อส่งเสริมวิสาหกิจชุมชนและผู้ประกอบการ SMEs ภาคเหนือ สู่สากลด้วยนวัตกรรม มาตรฐาน และบรรจุภัณฑ์ (ปีที่ 2)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(114,'finished','2016','2559','Project to improve regional industrial logistics efficiency','โครงการเพิ่มประสิทธิภาพโลจิสติกส์อุตสาหกรรมภูมิภาค','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(115,'finished','2016','2559','Thai labor productivity enhancement project, fiscal year 2016','โครงการเพิ่มผลิตภาพแรงงานไทย ประจำปีงบประมาณ พ.ศ.2559','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(116,'finished','2016','2559','Ton Kla Business Challenge project, 2016','โครงการต้นกล้าท้าธุรกิจปี 2559','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(117,'finished','','','Consulting project to develop a rural road development plan for the department, Group 1','โครงการจ้างที่ปรึกษาจัดทำแผนพัฒนาทางหลวงชนบทประจำกรม กลุ่มที่ 1','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(118,'finished','2015','2558','Chiang Rai provincial cooperation project with neighboring countries in preparation for the ASEAN Community, 2015: activities supporting the development of the Chiang Rai Special Economic Zone','โครงการความร่วมมือจังหวัดเชียงรายกับประเทศเพื่อนบ้านเตรียมความพร้อมสู่ประชาคมอาเซียน 2558 กิจกรรมสนับสนุนการขับเคลื่อนเขตพัฒนาเศรษฐกิจพิเศษเชียงราย','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(119,'finished','','','Innovation Road Map project for the rice industry','โครงการจัดทำ Innovation Road Map ของอุตสาหกรรมข้าว','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(120,'finished','2015','2558','Development of information systems and in-depth economic crop data for production planning and appropriate zoning, 2015','โครงการพัฒนาข้อมูลสารสนเทศและข้อมูลพืชเศรษฐกิจเชิงลึก วางแผนการผลิตและการจัดทำ Zoning ที่เหมาะสม','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(121,'finished','2013','2556','Supply chain restructuring for the air transport industry in preparation for entry into the ASEAN Economic Community','โครงการการปรับรูปแบบโซ่อุปทานสำหรับอุตสาหกรรมการขนส่งทางอากาศเพื่อเตรียมความพร้อมในการเข้าสู่ประชาคมเศรษฐกิจอาเซียน','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(122,'finished','2014','2557','Project to improve Northern industrial logistics efficiency, 2014','โครงการเพิ่มประสิทธิภาพโลจิสติกส์อุตสาหกรรมภาคเหนือ 2557','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(123,'finished','','','Project to upgrade value chain management for manufacturing enterprise groups to increase competitiveness and serve as a production base for the AEC (textile and garment industry, and food industry)','โครงการยกระดับการจัดการห่วงโซ่คุณค่าของกลุ่มวิสาหกิจผู้ผลิตสินค้า เพื่อเพิ่มความสามารถในการแข่งขันและเป็นฐานการผลิตของAEC (อุตสาหกรรมสิ่งทอและเครื่องนุ่งห่ม และ อุตสาหกรรมอาหาร)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(124,'finished','2014','2557','Project to establish Lampang province as a land-transport logistics hub for goods and services in the North','โครงการจัดวางระบบจังหวัดลำปางให้เป็นศูนย์กลางเชื่อมโยงสินค้าและบริการทางบกของภาคเหนือ','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(125,'finished','','','Project to upgrade logistics and supply chain management capacity for manufacturing enterprise groups to serve as a production base for the AEC (automotive and auto-parts industry, and electrical appliances and electronics industry)','โครงการยกระดับศักยภาพการจัดการโลจิสติกส์และโซ่อุปทานของกลุ่มวิสาหกิจผู้ผลิตชิ้นส่วนสินค้าอุตสาหกรรมเพื่อเป็นฐานการผลิตของ AEC (อุตสาหกรรมยานยนต์และชิ้นส่วนยานยนต์และอุตสาหกรรมเครื่องใช้ไฟฟ้าและอิเล็กทรอนิกส์)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(126,'finished','2013','2556','Project to enhance labor productivity according to enterprise needs (2013 and 2014)','โครงการเพิ่มผลิตภาพแรงงานตามความต้องการสถานประกอบการกิจการ (ปี 2556 และ ปี 2557)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(127,'finished','2012','2555','Project to improve Northern industrial logistics efficiency, 2012, 2013 and 2014','โครงการเพิ่มประสิทธิภาพโลจิสติกส์อุตสาหกรรมภาคเหนือ ปี 2555, 2556 และ 2557','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(128,'finished','','','Project to improve Thai product access to the Japanese market through integration with Japanese supply chains','โครงการการปรับปรุงการเข้าถึงของสินค้าไทยสู่ตลาดญี่ปุ่น ด้วยการบูรณาการกับห่วงโซ่อุปทานของญี่ปุ่น','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(129,'finished','2011-2012','2554-2555','Project to increase off-season longan production profits by building networks and linking supply chain data among farmers','โครงการการเพิ่มกำไรการผลิตลำไยนอกฤดูด้วยสร้างเครือข่ายการรวมกลุ่มและเชื่อมโยงข้อมูลโซ่อุปทานของเกษตรกร','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(130,'finished','','','Feasibility study and master plan development for the Chiang Rai border economic zone','โครงการศึกษาความเหมาะสมและจัดทําแผนแม่บทการพัฒนาพื้นที่เศรษฐกิจชายแดนจังหวัดเชียงราย','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(131,'finished','2007','2550','Assessment of the logistics and supply chain management capacity of Thai enterprises using the SCM Logistics Scorecard','โครงการการประเมินศักยภาพด้านโลจิสติกส์และการจัดการโซ่อุปทานของผู้ประกอบการในประเทศไทย โดย SCM Logistics Scorecard','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(132,'finished','','','Project to strengthen and integrate the industrial logistics system and supply chain management for Thai SMEs','โครงการสร้างความเข้มแข็งและเชื่อมโยงของระบบโลจิสติกส์ของอุตสาหกรรม และการจัดการห่วงโซ่อุปทานให้กับ SMEs ไทย','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(133,'finished','','','Development of a database on the logistics and supply chain management capacity of Thai logistics service providers using the SCM Logistics Scorecard','โครงการการจัดทำฐานข้อมูลศักยภาพด้านโลจิสติกส์และการจัดการโซ่อุปทานของผู้ให้บริการด้านโลจิสติกส์ของไทย โดย SCM Logistics Scorecard','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(134,'finished','2011','2554','Training conference and seminar organization under the GMS-linked provincial-group logistics management system development project','โครงการจัดประชุมฝึกอบรม และสัมมนา ตามโครงการพัฒนาระบบบริหารจัดการโลจิสติกส์กลุ่มจังหวัดเชื่อมโยง GMS','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(135,'finished','2011','2554','Development of logistics efficiency improvement software for entrepreneurs under the GMS-linked provincial-group logistics management system development project','โครงการการจัดทำซอฟท์แวร์ปรับปรุงประสิทธิภาพโลจิสติกส์สำหรับผู้ประกอบการ ภายใต้โครงการพัฒนาระบบบริหารจัดการโลจิสติกส์กลุ่มจังหวัดเชื่อมโยง GMS','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(136,'finished','2011','2554','Development of a national research management strategy for the national logistics research strategy (2011-2013)','โครงการการพัฒนายุทธศาสตร์การจัดการระบบบริหารงานวิจัย ยุทธศาสตร์วิจัยด้านโลจิสติกส์ชาติ (พ.ศ.2554-2556)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(137,'finished','2010','2553','Study on developing transport and trade facilitation concepts around the Mekong River bridge along the North-South economic corridor (Chiang Khong-Houay Xai)','โครงการศึกษาแนวคิดการพัฒนาการอำนวยความสะดวกด้านการขนส่งและการค้าบริเวณสะพานข้ามแม่น้ำโขงตามแนวพัฒนาเศรษฐกิจเหนือ-ใต้ (เชียงของ-ห้วยทราย)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(138,'finished','','','Study on Thai Solar Thermal Industry Analysis','โครงการ Study on Thai Solar Thermal Industry Analysis','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(139,'finished','','','Research on enhancing the nutritional value of parboiled rice and its application in the food industry','โครงการวิจัยการเสริมคุณค่าทางโภชนาการของข้าวนึ่งและการประยุกต์ใช้ในอุตสาหกรรมอาหาร','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(140,'finished','','','System for Quality Assurance in Research and Education (SQUARE)','โครงการ System for Quality Assurance in Research and Education (SQUARE)','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(141,'finished','','','Building networks and linking data among farmers and communities: a case study of the off-season longan supply chain','โครงการการสร้างเครือข่ายการรวมกลุ่มและเชื่อมโยงข้อมูลของเกษตรกรและชุมชน กรณีศึกษา: โซ่อุปทานลำไยนอกฤดู','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(142,'finished','2009','2552','Study on the quantity and knowledge needs of Thai logistics personnel in the food processing industry','โครงการศึกษาความต้องการด้านปริมาณและองค์ความรู้ของบุคลากรด้านโลจิสติกส์ไทย ในอุตสาหกรรมแปรรูปอาหาร','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(143,'finished','2009','2552','Chiang Rai Province Logistics and Supply Chain Management Center project','โครงการศูนย์บริหารจัดการโลจิสติกส์และซัพพลายเชน จังหวัดเชียงราย','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(144,'finished','','','Feasibility study for establishing an industrial estate, environmental impact assessment, and production restructuring, Tak Province','โครงการศึกษาความเหมาะสมการจัดตั้งนิคมอุตสาหกรรม ผลกระทบสิ่งแวดล้อม และการปรับโครงสร้างการผลิต จังหวัดตาก','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(145,'finished','','','Research on enhancing the nutritional value of parboiled glutinous rice and its application in the food industry, Phase 2','โครงการวิจัยการการเพิ่มคุณค่าทางโภชนาการของข้าวเหนียวนึ่งและการประยุกต์ใช้ในอุตสาหกรรมอาหาร ระยะที่ 2','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(146,'finished','','','Preliminary data compilation for developing a research proposal on the East-West Economic Corridor within the Greater Mekong Subregion','โครงการการรวบรวมข้อมูลเบื้องต้นเพื่อพัฒนาข้อเสนอโครงการศึกษาระเบียงเศรษฐกิจตะวันออก-ตะวันตก (East-West Economic Corridor) ในกรอบกลุ่มประเทศอนุภาคลุ่มน้ำโขง','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(147,'finished','','','Research on enhancing the nutritional value of parboiled glutinous rice and its application in the food industry','โครงการวิจัยการเพิ่มคุณค่าทางโภชนาการของข้าวเหนียวนึ่งและการประยุกต์ใช้ในอุตสาหกรรมอาหาร','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(148,'finished','','','Project to build good work values and prepare for future entrepreneurship','โครงการสร้างค่านิยมในการทำงานที่ดี และเตรียมตัวให้เป็นผู้ประกอบการในอนาคต','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(149,'finished','','','Development of a short-course manual to build good work values and prepare for future entrepreneurship','โครงการจัดทำคู่มือหลักสูตรระยะสั้น เพื่อสร้างค่านิยมในการทำงานที่ดี และการเตรียมตัวเป็นผู้ประกอบการในอนาคต','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(150,'finished','','','Industrial Seedling Cultivation project, Phases 1, 2 and 3','โครงการเพาะต้นกล้าอุตสาหกรรม ระยะที่ 1, 2 และ 3','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(151,'finished','','','Study on the history of the Wat Pa Daeng Maha Wihan Buddhist tradition for its sustainable development','โครงการศึกษาประวัติพุทธศาสนาลัทธิวัดป่าแดงมหาวิหาร เพื่อพัฒนาวัดป่าแดงมหาวิหารอย่างยั่งยืน','','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','');
INSERT INTO "research_projects" VALUES(152,'ongoing','','','A Strategic Roadmap Towards the Next Level of Intelligent, Sustainable and Human-Centred SME (SME 5.0)','A Strategic Roadmap Towards the Next Level of Intelligent, Sustainable and Human-Centred SME: SME 5.0','Assistant Professor Dr. Korrakot Yaibuathet Tippayawong','ผู้ช่วยศาสตราจารย์ ดร.กรกฎ ใยบัวเทศ ทิพยาวงศ์','','Associate Professor Dr. Sakgasem Ramingwong','รองศาสตราจารย์ ดร.ศักดิ์เกษม ระมิงค์วงศ์','','Associate Professor Dr. Poti Chaopaisarn','รองศาสตราจารย์ ดร.โพธิ จ้าวไพศาล','','Professor Dr. Apichat Sopadang','ศาสตราจารย์ ดร.อภิชาต โสภาแดง','','Distinguished Professor Dr. Nakorn Tippayawong
Associate Professor Dr. Trasapong Thaiupathump
Associate Professor Dr. Rungchat Chompu-inwai
Associate Professor Dr. Warisa Nakkiew
Associate Professor Dr. Chawis Boonmee
Associate Professor Dr. Chompoonoot Kasemset
Associate Professor Dr. Pana Suttakul
Associate Professor Dr. Yuttana Mona
Assistant Professor Dr. Salinee Santiteerakul
Assistant Professor Dr. Wapee Manopiniwes
Assistant Professor Dr. Tinnakorn Phongthiya
Assistant Professor Dr. Wasawat Nakkiew
Assistant Professor Dr. Rattapol Pinnaratip
Assistant Professor Dr. Sainatee Chernbumroong
Assistant Professor Dr. Varattaya Jangkrajarng
Assistant Professor Dr. Tulaya Tulardilok
Dr. Wisuttorn Jitaree','ศาสตราจารย์เชี่ยวชาญพิเศษ ดร.นคร ทิพยาวงศ์
รองศาสตราจารย์ ดร.ตรัสพงศ์ ไทยอุปถัมภ์
รองศาสตราจารย์ ดร.รุ่งฉัตร ชมภูอินไหว
รองศาสตราจารย์ ดร.วริษา นาคเขียว
รองศาสตราจารย์ ดร.ชวิศ บุญมี
รองศาสตราจารย์ ดร.ชมพูนุท เกษมเศรษฐ์
รองศาสตราจารย์ ดร.พนา สุทธกูล
รองศาสตราจารย์ ดร.ยุทธนา โมนะ
ผู้ช่วยศาสตราจารย์ ดร.สาลินี สันติธีรากุล
ผู้ช่วยศาสตราจารย์ ดร.วาปี มโนภินิเวศ
ผู้ช่วยศาสตราจารย์ ดร.ทินกร ปงธิยา
ผู้ช่วยศาสตราจารย์ ดร.วสวัชร นาคเขียว
ผู้ช่วยศาสตราจารย์ ดร.รัฐพล ปิ่นนราทิพย์
ผู้ช่วยศาสตราจารย์ ดร.สายนที เฉินบำรุง
ผู้ช่วยศาสตราจารย์ ดร.วรัทยา แจ้งกระจ่าง
ผู้ช่วยศาสตราจารย์ ดร.ตุลยา ตุลาดิลก
อาจารย์ ดร.วิสุทธร จิตอารี','["Tippayawong.jpg", "Thaiupathump.jpg", "Rungchat.png", "", "Boonmee-0ac8ae09.png", "Kasemset.png", "Suttakul.jpg", "Mona.jpg", "", "", "Tinnakorn.png", "Nakkiew.png", "Pinnaratip.png", "", "", "", "Jitaree.jpg"]','','','[]','','','[]','1 January 2023 - 31 December 2026','1 มกราคม พ.ศ. 2566 – 31 ธันวาคม พ.ศ. 2569','Faculty of Engineering, Chiang Mai University, in collaboration with Chiang Mai University Business School','คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเชียงใหม่ ร่วมกับคณะบริหารธุรกิจ มหาวิทยาลัยเชียงใหม่','','','European Commission, under the Horizon Europe programme (international research grant)','คณะกรรมาธิการยุโรป (European Commission) ภายใต้โครงการ Horizon Europe (ทุนวิจัยจากต่างประเทศ)','Total project value EUR 1,168,400; Chiang Mai University share EUR 184,000 (THB 44,399,200)','มูลค่าโครงการรวม 1,168,400 ยูโร ในส่วนของมหาวิทยาลัยเชียงใหม่ 184,000 ยูโร (44,399,200 บาท)','','','[]','[]','','An international research project funded by the European Commission under Horizon Europe, aimed at taking small and medium-sized enterprises (SMEs) to the next level. Over the past decade, considerable effort has gone into transferring Industry 4.0 from research into practice, and recent progress has extended this to SMEs. The next major challenge is the dual (or twin) transformation: a digital transformation towards more intelligent manufacturing, combined with an accelerated sustainability transformation to deliver economically, socially, and environmentally sustainable processes, factories, and value chains. The project addresses this by developing a Strategic Roadmap that makes SMEs not only intelligent but also sustainable, resilient, and human-centric. SMEs at this next level will be data- and intelligence-driven, using available data to acquire new knowledge and applying it for optimisation purposes through artificial intelligence in a secure way.','โครงการวิจัยระดับนานาชาติภายใต้ทุน Horizon Europe ของคณะกรรมาธิการยุโรป ที่มุ่งยกระดับวิสาหกิจขนาดกลางและขนาดย่อม (SME) สู่ระดับถัดไป ในช่วงสิบปีที่ผ่านมามีความพยายามอย่างต่อเนื่องในการถ่ายทอดแนวคิด Industry 4.0 จากงานวิจัยสู่การปฏิบัติจริง และเริ่มขยายผลสู่ภาค SME ได้ในระดับหนึ่ง ความท้าทายลำดับถัดไปคือการดำเนินการเปลี่ยนผ่านคู่ขนาน (Twin Transformation) ทั้งการเปลี่ยนผ่านสู่ดิจิทัลเพื่อการผลิตที่ชาญฉลาดยิ่งขึ้น ควบคู่ไปกับการเปลี่ยนผ่านสู่ความยั่งยืน ทั้งในมิติเศรษฐกิจ สังคม และสิ่งแวดล้อม ครอบคลุมทั้งกระบวนการผลิต โรงงาน และห่วงโซ่คุณค่า โครงการจึงพัฒนาแผนที่นำทางเชิงกลยุทธ์ (Strategic Roadmap) เพื่อยกระดับ SME ให้ไม่เพียงชาญฉลาด แต่ยังยั่งยืน ยืดหยุ่นต่อการเปลี่ยนแปลง และมีมนุษย์เป็นศูนย์กลาง โดย SME ในระดับถัดไปนี้ จะขับเคลื่อนด้วยข้อมูลและปัญญาประดิษฐ์ ใช้ข้อมูลที่มีอยู่เพื่อสร้างองค์ความรู้ใหม่ และนำไปประยุกต์ใช้ในการปรับปรุงประสิทธิภาพด้วยปัญญาประดิษฐ์อย่างปลอดภัย');
CREATE TABLE staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_en TEXT NOT NULL,
    name_th TEXT NOT NULL,
    position_en TEXT,
    position_th TEXT,
    department_en TEXT,
    department_th TEXT,
    staff_group TEXT NOT NULL DEFAULT 'member' CHECK (staff_group IN ('advisor', 'member', 'cmubs', 'researcher')),
    sort_order INTEGER NOT NULL DEFAULT 0,
    photo_filename TEXT,
    profile_url TEXT NOT NULL DEFAULT '',
    scopus_author_id TEXT NOT NULL DEFAULT '',
    scopus_hindex INTEGER,
    scopus_hindex_updated_at TEXT,
    audio_en_url TEXT NOT NULL DEFAULT '',
    audio_th_url TEXT NOT NULL DEFAULT ''
);
INSERT INTO "staff" VALUES(1,'Assoc. Prof. Sakgasem Ramingwong, Ph.D.','รศ.ดร.ศักดิ์เกษม ระมิงค์วงศ์','Leader','หัวหน้า','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',1,'Sakgasem_Ramingwong.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/129','57200409458',NULL,NULL,'/static/audio/EN/EN_Sakgasem Ramingwong.mp3','/static/audio/TH/TH_Sakgasem Ramingwong.mp3');
INSERT INTO "staff" VALUES(2,'Prof. Komgrit Leksakul, D.Eng','ศ.ดร.คมกฤต เล็กสกุล','Member','สมาชิก','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',2,'Komgrit_Leksakul.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/124','36052105700',NULL,NULL,'/static/audio/EN/EN_ Komgrit Leksakul.mp3','/static/audio/TH/TH_Komgrit Leksakul.mp3');
INSERT INTO "staff" VALUES(3,'Assoc. Prof. Warisa Nakkiew, D.Eng','รศ.ดร.วริษา นาคเขียว','Member','สมาชิก','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',3,'Warisa_Nakkiew.jpeg','https://ie.eng.cmu.ac.th/people/faculty/138','59553831700',NULL,NULL,'/static/audio/EN/EN_Warisa Nakkiew.mp3','/static/audio/TH/TH_Warisa Nakkiew.mp3');
INSERT INTO "staff" VALUES(4,'Assoc. Prof. Poti Chaopaisarn, Ph.D.','รศ.ดร.โพธิ จ้าวไพศาล','Member','สมาชิก','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',4,'Poti_Chaopaisarn.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/142','57209295533',NULL,NULL,'/static/audio/EN/EN_Poti Chaopaisarn.mp3','/static/audio/TH/TH_Poti Chaopaisarn.mp3');
INSERT INTO "staff" VALUES(5,'Asst. Prof. Korrakot Yaibuathet Tippayawong, D.Eng','ผศ.ดร.กรกฎ ใยบัวเทศ ทิพยาวงศ์','Member','สมาชิก','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',5,'Korrakot_Yaibuathet_Tippayawong.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/134','54407578400',NULL,NULL,'/static/audio/EN/EN_ Korrakot Yaibuathet Tippayawong.mp3','/static/audio/TH/TH_Korrakot Yaibuathet Tippayawong.mp3');
INSERT INTO "staff" VALUES(6,'Asst. Prof. Salinee Santiteerakul, Ph.D.','ผศ.ดร.สาลินี สันติธีรากุล','Member','สมาชิก','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',6,'Salinee_Santiteerakul.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/145','56039955900',NULL,NULL,'/static/audio/EN/EN_Salinee Santiteerakul.mp3','/static/audio/TH/TH_Salinee Santiteerakul.mp3');
INSERT INTO "staff" VALUES(7,'Asst. Prof. Alonggot Limcharoen, D.Eng','ผศ.ดร.อลงกต แก้วโชติช่วงกูล','Member','สมาชิก','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',7,'Alonggot_Limcharoen.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/144','35995452600',NULL,NULL,'/static/audio/EN/EN_Alonggot Limcharoen.mp3','/static/audio/TH/TH_Alonggot Kaeochotchuangkul.mp3');
INSERT INTO "staff" VALUES(8,'Asst. Prof. Wapee Manopiniwes, Ph.D.','ผศ.ดร.วาปี มโนภินิเวศ','Member','สมาชิก','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',8,'Wapee_Manopiniwes.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/151','55867596500',NULL,NULL,'/static/audio/EN/EN_Wapee Manopiniwes.mp3','/static/audio/TH/TH_Wapee Manopiniwes.mp3');
INSERT INTO "staff" VALUES(9,'Pongsawat Premphet, Ph.D.','อ.ดร.พงษ์สวัสดิ์ เปรมเพ็ชร','Member','สมาชิก','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',9,'Pongsawat_Premphet.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/155','56576423900',NULL,NULL,'/static/audio/EN/EN_Pongsawat Premphet.mp3','/static/audio/TH/TH_Pongsawat Premphet.mp3');
INSERT INTO "staff" VALUES(10,'Prim Fongsamootr','พริม ฟองสมุทร','Member','สมาชิก','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','member',10,'Prim_Fongsamootr.png','/static/cv/CV_Prim Fongsamootr.pdf','59251106200',NULL,NULL,'/static/audio/EN/EN_Prim Fongsamootr.mp3','/static/audio/TH/TH_Prim Fongsamootr.mp3');
INSERT INTO "staff" VALUES(11,'Assoc. Prof. Sermkiat Jomjunyong','รองศาสตราจารย์ ดร.เสริมเกียรติ จอมจันทร์ยอง','Advisor','ที่ปรึกษา','Senior Retired Lecturer','อาจารย์อาวุโสเกษียณอายุ','advisor',11,'Sermkiat_Jomjunyong.jpg','','6506451345',NULL,NULL,'','');
INSERT INTO "staff" VALUES(12,'Prof. Apichat Sopadang, Ph.D.','ศ.ดร.อภิชาต โสภาแดง','Advisor','ที่ปรึกษา','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','advisor',12,'Apichat_Sopadang.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/120','13403750900',NULL,NULL,'/static/audio/EN/EN_Apichat Sopadang.mp3','/static/audio/TH/TH_Apichat Sopadang.mp3');
INSERT INTO "staff" VALUES(13,'Assoc. Prof. Nivit Charoenchai, Ph.D.','รศ.ดร.นิวิท เจริญใจ','Advisor','ที่ปรึกษา','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','advisor',13,'Nivit_Charoenchai.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/82','6505486991',NULL,NULL,'/static/audio/EN/EN_Nivit Charoenchai.mp3','/static/audio/TH/TH_Nivit Charoenchai.mp3');
INSERT INTO "staff" VALUES(14,'Asst. Prof. Tanyanuparb Anantana, D.Eng','ผศ.ดร.ธัญญานุภาพ อานันทนะ','Advisor','ที่ปรึกษา','Department of Industrial Engineering','ภาควิชาวิศวกรรมอุตสาหการ','advisor',14,'Tanyanuparb_Anantana.jpeg','https://ie.eng.cmu.ac.th/en/people/faculty/136','36141520400',NULL,NULL,'/static/audio/EN/EN_Tanyanuparb Anantana.mp3','/static/audio/TH/TH_Tanyanuparb Anantana.mp3');
INSERT INTO "staff" VALUES(15,'Miss Jurairat Rintieng','นางสาวจุไรรัตน์ รินเที่ยง','Researcher','นักวิจัย','Senior Project Manager','ผู้จัดการโครงการอาวุโส','researcher',15,'Jurairat_Rintieng.jpg','/static/cv/CV_2026 Jurairat Rintieng _TH.pdf','',NULL,NULL,'/static/audio/EN/EN_Jurairat Rintieng.mp3','/static/audio/TH/TH_Jurairat Rintieng.mp3');
INSERT INTO "staff" VALUES(16,'Miss Jidapa Chanjaroen','นางสาวจิดาภา ชาญเจริญ','Researcher','นักวิจัย','Research Assistant and Project Engineer','ผู้ช่วยวิจัยและวิศวกรโครงการ','researcher',16,'Jidapa_Chanjaroen.png','/static/cv/CV_Jidapa Chanjaroen.pdf','60610582300',NULL,NULL,'/static/audio/EN/EN_Jidapa Chanjaroen.mp3','/static/audio/TH/TH_Jidapa Chanjaroen.mp3');
INSERT INTO "staff" VALUES(17,'Miss Chalisa Naroon','นางสาวชาลิสา ณรุณ','Researcher','นักวิจัย','Research Unit Secretary','เลขานุการหน่วยวิจัย','researcher',17,'Chalisa_Naroon.jpg','/static/cv/CV Chalisa_Naroon 2026 .pdf','',NULL,NULL,'/static/audio/EN/EN_Chalisa Naroon.mp3','/static/audio/TH/TH_Chalisa Naroon.mp3');
INSERT INTO "staff" VALUES(18,'Asst. Prof. Varattaya Jangkrajarng, Ph.D.','ผู้ช่วยศาสตราจารย์ดร.วรัทยา แจ้งกระจ่าง','Member','สมาชิก','Department of Management and Entrepreneurship','ภาควิชาการจัดการและการเป็นผู้ประกอบการ คณะบริหารธุรกิจ','member',0,'Varattaya_Jangkrajarng.jpg','https://apps.cmubs.cmu.ac.th/mis/cv.php?cmu_it_account=varattaya.j@cmu.ac.th&teacher_id=66','56800842100',NULL,NULL,'/static/audio/EN/EN_Varattaya Jangkrajarng.mp3','/static/audio/TH/TH_Varattaya Jangkrajarng.mp3');
INSERT INTO "staff" VALUES(19,'Asst. Prof. Sainatee Chernbumroong, Ph.D.','ผู้ช่วยศาสตราจารย์ดร.สายนที เฉินบำรุง','Member','สมาชิก','Department of Management and Entrepreneurship','ภาควิชาการจัดการและการเป็นผู้ประกอบการ คณะบริหารธุรกิจ','member',1,'Sainatee_Chernbumroong.jpg','https://apps.cmubs.cmu.ac.th/mis/cv.php?cmu_it_account=sainatee.c@cmu.ac.th&teacher_id=62','57209832989',NULL,NULL,'/static/audio/EN/EN_Sainatee Chernbumroong.mp3','/static/audio/TH/TH_Sainatee Chernbumroong.mp3');
INSERT INTO "staff" VALUES(20,'Siravat Teerasoponpong, Ph.D.','อาจารย์ดร.ศิรวัจน์ ธีราโสภณพงศ์','Member','สมาชิก','Department of Management and Entrepreneurship','ภาควิชาการจัดการและการเป็นผู้ประกอบการ คณะบริหารธุรกิจ','member',2,'Siravat_Teerasoponpong.jpg','https://apps.cmubs.cmu.ac.th/mis/cv.php?cmu_it_account=siravat.t@cmu.ac.th&teacher_id=735','57189039232',NULL,NULL,'/static/audio/EN/EN_Siravat Teerasoponpong.mp3','/static/audio/TH/TH_Siravat Teerasoponpong.mp3');
INSERT INTO "staff" VALUES(21,'Asst. Prof. Tulaya Tulardilok, Ph.D.','ผู้ช่วยศาสตราจารย์ดร.ตุลยา ตุลาดิลก','Member','สมาชิก','Department of Accounting','ภาควิชาการบัญชี','member',3,'Tulaya_Tulardilok.jpg','https://apps.cmubs.cmu.ac.th/mis/cv.php?cmu_it_account=tulaya.t@cmu.ac.th&teacher_id=25','60151728700',NULL,NULL,'/static/audio/EN/EN_Tulaya Tulardilok.mp3','/static/audio/TH/TH_Tulaya Tulardilok.mp3');
INSERT INTO "staff" VALUES(23,'Dr. JUTAMAT JINTANA, Lecturer','อาจารย์ ดร. จุฑามาศ จินตนา','Member','สมาชิก','Faculty of Pharmacy','คณะเภสัชศาสตร์','member',4,'JUTAMAT_JINTANA.jpg','/static/cv/CV_Jutamat Jintana.pdf','57218619954',NULL,NULL,'/static/audio/EN/EN_Jutamat Jintana.mp3','/static/audio/TH/TH_Jutamat Jintana.mp3');
CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE SET NULL
            );
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('home_activity_images',7);
INSERT INTO "sqlite_sequence" VALUES('staff',23);
INSERT INTO "sqlite_sequence" VALUES('research_projects',153);
INSERT INTO "sqlite_sequence" VALUES('general_info',1);
COMMIT;

