create database whatsapp_bot

use whatsapp_bot

create table content (
	 id int primary key IDENTITY(1,1)
	,mensagem		text
	,attached_image int 
	,attached_video int
	,attached_docum int
	,item_sent		int
	,send_date		datetime
	,group_whatsapp varchar(200)			
)

go 


--insert into content values('Segue anexo  exemplo dos arquivos a serem enviados  para se candidatar a vaga!!',1,1,0,0,null,'whatsapp_bot')

create table images(
	 id_content int 
	,src varchar(200)
	,FOREIGN KEY (id_content) REFERENCES content(id)
)

--insert into images values(3,'C:\myprojects\zapbot\img\item1.jpg')
DELETE images WHERE id_content = 3
SELECT * FROM images

go 

create table video(
	 id_content int 
	,src varchar(200)
	,FOREIGN KEY (id_content) REFERENCES content(id)
)

--insert into video values(3,'C:\myprojects\zapbot\video\video.mp4')

go

create table document(
	 id_content int 
	,src varchar(200)
	,FOREIGN KEY (id_content) REFERENCES content(id)
)

--insert into document values(3,'C:\myprojects\zapbot\documento\Profile.pdf')






