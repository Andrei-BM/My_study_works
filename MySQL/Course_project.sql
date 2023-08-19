/* База данных транспортного предприятия. */

DROP DATABASE IF EXISTS ts;

CREATE DATABASE IF NOT EXISTS ts;
-- 1. Таблица клиентов (на мой взгляд это самое важное)

CREATE TABLE IF NOT EXISTS customers(
	id SERIAL PRIMARY KEY,
	is_company ENUM('YES', 'NO'),
	name VARCHAR(255) NOT NULL,
	phone CHAR(11) UNIQUE NOT NULL,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO customers VALUES
(DEFAULT, 'YES', 'ООО ГУК Краснодар', '78612435678', DEFAULT, DEFAULT),
(DEFAULT, 'YES', 'ТСЖ Виктория', '78612436587', DEFAULT, DEFAULT),
(DEFAULT, 'YES', 'ООО Нефтестройиндустрия-ЮГ', '78614568790', DEFAULT, DEFAULT),
(DEFAULT, 'YES', 'СНТ Мечта', '79184335568', DEFAULT, DEFAULT),
(DEFAULT, 'YES', 'МУП Комбинат питания', '78612229987', DEFAULT, DEFAULT),
(DEFAULT, 'NO', 'ИП Нестерова И. С.', '79618200905', DEFAULT, DEFAULT),
(DEFAULT, 'NO', 'Медведь П.В.', '79284312816', DEFAULT, DEFAULT);

-- 2. Данные клиентов
DROP TABLE IF EXISTS customer_profile;
CREATE TABLE IF NOT EXISTS customer_profile(
	profile_id SERIAL PRIMARY KEY,
	post VARCHAR(90), 
	first_name VARCHAR(150) NOT NULL,
	last_name VARCHAR(150) NOT NULL,
	INN CHAR(12) NOT NULL,
	city VARCHAR(150) NOT NULL,
	address VARCHAR(255) NOT NULL,
	email VARCHAR(150) UNIQUE,
	bank_account VARCHAR(255),
	FOREIGN KEY  (profile_id) REFERENCES customers(id)
);

INSERT INTO customer_profile (post, first_name, last_name, INN, city, address, email)
VALUES ('Генеральный директор', 'Людмила', 'Головченко', '2311104687', 'Краснодар', 'ул. Садовая, д.112', 'contact@gukkranodar'),
('Председатель', 'Владимир', 'Носов', '2309099638', 'Краснодар', 'ул. Стасова 178\1', 'victoria.kranodar@mail.ru'),
('Директор', 'Геннадий', 'Ушаков', '2310133597', 'Краснодар', 'ул. Каляева 1\4', 'questions.@nsi.ru'),
('Председатель', 'Игорь', 'Величко', '2311056507', 'Краснодар', 'ул. Ростовское ш. 10км', 'mechta@list.ru'),
('Директор', 'Максим', 'Царенко', '2308269022', 'Краснодар', 'ул. Длинная д. 98, п. 1,2,4', 'foodKK@yandex.ru'),
(NULL, 'Ирина', 'Нестерова', '230110573672', 'Краснодар', 'ул. Благоева д. 14, кв. 21', 'nyashka23@rambler.ru'),
(NULL, 'Петр', 'Медведь', '230809592468', 'Краснодар', 'ул. Российская д. 439', NULL);

-- 3. Виды контейнеров и тарифы
DROP TABLE IF EXISTS cargo;
CREATE TABLE IF NOT EXISTS cargo(
	id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	form VARCHAR(120) NOT NULL UNIQUE,
	description TEXT,
	price DECIMAL(9,2) NOT NULL
);

INSERT INTO cargo (form, description, price)
VALUES ('Big6', '6м контейнер для отходов', 7000.00),
('Heavy5', '5м контейнер для стройотходов', 6000.00),
('Uni4', '4м универсальный контейнер для отходов', 5000.00),
('Heavy8', '8м полуприцеп для вывоза отходов', 10000.00),
('Standart', 'Стандартный контейнер для отходов 0,75м3', 250.00),
('Pile', 'Вывоз безконтейнерных отходов', 400.00);

-- 4. Таблица сотрудников
/* По условию рабочие смены у нас 2 типов - 1 тип: 2 рабочих дня затем 2 выходных дня(обозначим их как 1ая и 2 смена),
 * второй тип: обычная 5 дневная рабочая неделя (обозначаем как 3) */
DROP TABLE IF EXISTS employees;
CREATE TABLE IF NOT EXISTS employees(
	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	post VARCHAR(50) NOT NULL,
	first_name VARCHAR(150) NOT NULL,
	last_name VARCHAR(150) NOT NULL,
	middle_name VARCHAR(150),
	phone CHAR(11) UNIQUE NOT NULL,
	shift ENUM('1', '2', '3') NOT NULL,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


INSERT employees (post, first_name, last_name, phone, shift)
VALUES ('диспетчер', 'Анастасия', 'Приходько', '79184422578', '1'),
('диспетчер', 'Светлана', 'Ромашкина', '79604411216', '2'),
('водитель', 'Вячеслав', 'Чепурных', '79604118979', '1'),
('водитель', 'Вадим', 'Бибик', '79588979112', '2'),
('водитель', 'Роман', 'Бондаренко', '79281121813', '1'),
('водитель', 'Андрей', 'Седов', '7952361819', '2'),
('водитель', 'Юрий', 'Швыдкий', '79183615319', '3'),
('водитель', 'Николай', 'Воронов', '79186153193', '1'),
('водитель', 'Михаил', 'Тихонов', '79281531963', '2');

-- 5. Таблица данных о сотрудниках
DROP TABLE IF EXISTS profiles;
CREATE TABLE IF NOT EXISTS profiles(
	emp_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	birthday DATE NOT NULL,
	gender ENUM ('f', 'm'),
	driver_license CHAR(12),
	photo BIGINT UNSIGNED,
	city VARCHAR(150) NOT NULL,
	address VARCHAR(255) NOT NULL,
	email VARCHAR(150) UNIQUE,
	INN CHAR(12) NOT NULL,
	social CHAR(11) NOT NULL,
	FOREIGN KEY (emp_id) REFERENCES employees(id)
);
SELECT e.id, e.post, e.last_name, e.first_name, p.gender, p.city, p.address, p.birthday  FROM employees AS e
INNER JOIN profiles AS p
ON e.id = p.emp_id;

INSERT profiles (emp_id, birthday, gender, city, address, INN, social)
VALUES (1, '1988-03-13', 'f', 'Краснодар', '1ый проезд Стасова, д. 14', '230908590123', '32314567813'),
(2, '1998-01-31', 'f', 'Краснодар', 'ул. Плотниченкооезд, д. 97', '230809012315', '32345678131'),
(3, '1976-09-12', 'm', 'ст. Елизаветинская', 'ул. Советская, д. 16, кв 42', '230809923151', '32456781313'),
(4, '1981-02-02', 'm', 'Краснодар', 'ул. Северная, д. 416', '230999231510', '32567813135'),
(5, '1985-06-17', 'm', 'ст. Новотитаровская', 'ул. Степная, д. 209', '231292315109', '33678131356'),
(6, '1993-12-10', 'm', 'ст. Федоровская', 'ул. Авиаторов, д. 47', '234023151099', '33181313567'),
(7, '1989-08-25', 'm', 'Краснодар', 'ул. Россинского, д. 23, кв 239', '231131510992', '32331356721'),
(8, '1997-11-06', 'm', 'Краснодар, п. Южный', 'ул. Колхозная, д. 19', '231031510992', '33361313567'),
(9, '1990-02-13', 'm', 'Краснодар', 'ул. Коммунаров, д. 4, кв 15', '231215109923', '33613135671');
-- 6. Таблица автомобилей
DROP TABLE IF EXISTS trucks;

CREATE TABLE IF NOT EXISTS trucks(
	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	reg_number CHAR(9) NOT NULL,
	form1 TINYINT UNSIGNED NOT NULL,
	form2 TINYINT UNSIGNED,
	route SMALLINT UNSIGNED,
	driver1 SMALLINT UNSIGNED NOT NULL,
	driver2	 SMALLINT UNSIGNED NOT NULL,
	active BOOL DEFAULT TRUE,
	FOREIGN KEY (form1) REFERENCES cargo(id),
	FOREIGN KEY (form2) REFERENCES cargo(id),
	FOREIGN KEY (driver1) REFERENCES employees(id),
	FOREIGN KEY (driver2) REFERENCES employees(id),
	FOREIGN KEY (route) REFERENCES routes(id),
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
truncate TABLE trucks;


INSERT trucks (reg_number, form1, form2, route, driver1, driver2)
VALUES('В212АУ123', 3, 6, 4, 3, 4),
('Р917ВС123', 5, 6, 1, 5, 6),
('M265OA123', 5, 6, 2, 8, 9),
('A030EA123', 1, 2, 5, 7, 7);

-- 7. Таблица маршрутов

DROP TABLE IF EXISTS routes;
CREATE TABLE IF NOT EXISTS routes(
	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(90) NOT NULL,
	form TINYINT UNSIGNED NOT NULL,
	description TEXT NOT NULL,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (form) REFERENCES cargo(id)
);
INSERT routes (name, form, description)
VALUES ('Ost', 5, 'Сбор стандартных контейнеров в восточной части города'),
('West', 5, 'Сбор стандартных контейнеров в западной части города'),
('KGO', 6, 'Вывоз безконтейнерных отходов'),
('Uni', 3, 'Вывоз универсальных контейнеров'),
('Big', 1, 'Крупнотонажные контейнеры');

/* 8. Таблица частота посещений
* Пришлось добавить новую таблицу, чтобы сформировать представление "План посещения на текущий день". */

DROP TABLE IF EXISTS visit;
CREATE TABLE IF NOT EXISTS visit(
	visit_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	visit_day VARCHAR(100) NOT NULL COMMENT 'День посещения',
	multi SMALLINT COMMENT 'Количество визитов',
	description TEXT COMMENT 'Описания и примечания'
);

INSERT INTO visit VALUES
(DEFAULT, 'Everyday', 2, 'Забор дважды в день'),
(DEFAULT, 'Everyday', 1, 'Забор каждый день'),
(DEFAULT, 'Monday, Thursday', 1, 'Посещение дважды в неделю'),
(DEFAULT, 'Tuesday, Friday', 1, 'Посещение дважды в неделю'),
(DEFAULT, 'Wednesday', 1, 'Посещение один раз в неделю');


-- 9. Таблица объектов посещений с адресами, типом и регулярностью посещений
DROP TABLE IF EXISTS locations;
CREATE TABLE IF NOT EXISTS locations(
	loc_id SERIAL PRIMARY KEY,
	city VARCHAR(150) NOT NULL,
	address VARCHAR(255) NOT NULL,
	form TINYINT UNSIGNED NOT NULL,
	visit SMALLINT UNSIGNED NOT NULL,
	quantity TINYINT UNSIGNED NOT NULL,
	owner BIGINT UNSIGNED NOT NULL,
	route SMALLINT UNSIGNED NOT NULL, 
	FOREIGN KEY (owner) REFERENCES customers(id),
	FOREIGN KEY (form) REFERENCES cargo(id),
	FOREIGN KEY (route) REFERENCES routes(id),
	FOREIGN KEY (visit) REFERENCES visit(visit_id),
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


INSERT INTO locations VALUES
(DEFAULT, 'Краснодар', 'ул. Тургенева 132', 5, 1, 6, 1, 2, DEFAULT),
(DEFAULT, 'Краснодар', 'ул. Атарбекова 40', 5, 1, 5, 1, 2, DEFAULT),
(DEFAULT, 'Краснодар', 'ул. Ростовское ш. 10', 5, 2, 7, 4, 2, DEFAULT),
(DEFAULT, 'Краснодар', 'ул. Мачуги 42', 5, 1, 5, 2, 1, DEFAULT),
(DEFAULT, 'Краснодар', 'ул. Селезнева 175', 5, 1, 6, 2, 1, DEFAULT),
(DEFAULT, 'Краснодар', 'ул. Ближний Западный обход 9', 1, 3, 1, 3, 5, DEFAULT),
(DEFAULT, 'Краснодар', 'ул. Благоева д. 14', 1, 5, 1, 6, 5, DEFAULT),
(DEFAULT, 'Краснодар', 'ул. Российская д. 439', 3, 5, 1, 7, 4, DEFAULT),
(DEFAULT, 'Краснодар', 'ул. Взлётная 29', 3, 4, 1, 5, 4, DEFAULT);


-- 10. Таблица начислений за услуги клиентам
DROP TABLE IF EXISTS services;
CREATE TABLE IF NOT EXISTS services(
	services_id SERIAL PRIMARY KEY,
	customer_id BIGINT UNSIGNED,
	service_date DATE,
	amount DECIMAL(9,2),
	emp_id SMALLINT UNSIGNED,
	last_update DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (customer_id) REFERENCES customers(id),
	FOREIGN KEY (emp_id) REFERENCES employees(id)
);
INSERT services VALUES
(DEFAULT, 1, '2022-06-01', 5500.00, 1, DEFAULT),
(DEFAULT, 2, '2022-06-01', 5500.00, 1, DEFAULT),
(DEFAULT, 4, '2022-06-01', 1750.00, 1, DEFAULT),
(DEFAULT, 6, '2022-06-01', 7000.00, 1, DEFAULT),
(DEFAULT, 1, '2022-06-02', 5500.00, 2, DEFAULT),
(DEFAULT, 2, '2022-06-02', 5500.00, 2, DEFAULT),
(DEFAULT, 4, '2022-06-02', 1750.00, 2, DEFAULT),
(DEFAULT, 3, '2022-06-02', 7000.00, 2, DEFAULT),
(DEFAULT, 5, '2022-06-02', 5000.00, 2, DEFAULT);


-- 11. Таблица расчётов с клиентами
DROP TABLE IF EXISTS payments;
CREATE TABLE IF NOT EXISTS payments(
	payment_id SERIAL PRIMARY KEY,
	customer_id BIGINT UNSIGNED,
	payment_date DATE NOT NULL,
	amount DECIMAL(9,2),
	emp_id SMALLINT UNSIGNED,
	last_update DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (customer_id) REFERENCES customers(id),
	FOREIGN KEY (emp_id) REFERENCES employees(id)
); 
INSERT payments VALUES
(DEFAULT, 1, '2022-06-02', 11000, 2, DEFAULT),
(DEFAULT, 2, '2022-06-02', 5500, 2, DEFAULT),
(DEFAULT, 6, '2022-06-02', 7000, 2, DEFAULT);

/* ЗАПРОСЫ */
-- Запросим клиентов у которых есть долг за услуги

SELECT c.name, c.phone, cp.city, cp.address, cp.email, (SELECT balance(c.id)) AS debt FROM customers AS c
INNER JOIN customer_profile AS cp
ON c.id = cp.profile_id 
HAVING debt > 0
ORDER BY debt DESC;

-- Запросим работников у которых день рожденья в этом месяце.

SELECT CONCAT(e.last_name, ' ', e.first_name) AS name,
CONCAT((SELECT MONTHNAME(p.birthday)), ' ', (SELECT DAYOFMONTH(p.birthday))) AS dr_day, e.post FROM employees AS e
INNER JOIN profiles AS p
ON e.id = p.emp_id
WHERE (SELECT EXTRACT(MONTH FROM p.birthday)) = (SELECT MONTH(CURDATE()));

-- Подсчитаем количество точек у наших клиентов.

SELECT c.name, COUNT(*) FROM locations AS l
INNER JOIN customers AS c
ON owner = c.id
GROUP BY owner;


-- Функция определения рабочей смены.
DELIMITER //
/* Данная функция будет определять какая сегодня работает смена 1 или 2. Точка отсчёта 2022-05-31.
 * Напоминание - смены чередуются через каждые 2 дня. */

DROP FUNCTION IF EXISTS ts.shift1 //
CREATE FUNCTION ts.shift1()
RETURNS CHAR(1) DETERMINISTIC
BEGIN
	DECLARE ONE INT;
	SET ONE = (SELECT DATEDIFF(NOW(), '2022-05-31'));
	IF ONE >= 4 THEN
		REPEAT
			SET ONE = ONE - 4;
		UNTIL ONE < 4
		END REPEAT;
	END IF;
	IF ONE = 0 OR ONE = 1 THEN 
	SET ONE = 1;
	ELSEIF ONE = 2 OR ONE = 3 THEN 
	SET ONE = 2;
	END IF;
	RETURN ONE;
END //

/* Эта функция будет определять являеется ли текущий день рабочим для 3 смены (Т.е. мы определяем
 * является ли день рабочим или нет.) Вопрос с праздничными днями пока опускаем. */

DROP FUNCTION IF EXISTS ts.shift2 //
CREATE FUNCTION ts.shift2()
RETURNS CHAR(1) DETERMINISTIC
BEGIN
	DECLARE two INT;
	DECLARE one VARCHAR(20);
	SET one = (SELECT DAYNAME(NOW()));
	IF (one = 'Sunday') OR (one = 'Saturday') THEN
		SET two = 0;
	ELSE
		SET two = 3;
	END IF;
	RETURN two;
END//

/* Создаём представление "Рабочее расписание на текующий день" 
 * Представление будет выводить список сотрудников, которые сегодня должны работать. */

DROP VIEW IF EXISTS today_work;
CREATE VIEW today_work AS SELECT post, CONCAT(last_name, ' ', first_name) AS name, phone
FROM employees WHERE shift IN ((SELECT shift1()), (SELECT shift2())) 
ORDER BY name;

SELECT * FROM today_work;

-- Представление: график сбора контейнеров на текущую дату.
DROP VIEW IF EXISTS schedule;
CREATE VIEW schedule AS 
SELECT (SELECT CURRENT_DATE()) AS 'Число', loc.owner AS id, c.name AS 'Клиент',  loc.address AS 'Адрес', loc.loc_id  
loc.quantity AS 'Количество', v.multi AS 'Визитов', r.name AS 'Маршрут', t.reg_number AS 'Автомобиль'  
FROM locations AS loc
INNER JOIN customers AS c
ON loc.owner = c.id
INNER JOIN routes AS r
ON loc.route = r.id
INNER JOIN trucks AS t
ON r.id = t.route 
INNER JOIN visit AS v 
ON loc.visit = v.visit_id 
WHERE visit IN (1, 2, (SELECT visit_id FROM visit WHERE visit_day LIKE CONCAT('%', (SELECT DAYNAME(NOW())), '%')))
ORDER BY Клиент;

SELECT * FROM schedule; 
SELECT * FROM schedule WHERE Маршрут = 'Ost';
SELECT * FROM schedule WHERE Визитов > 1;


-- Функция проверки баланса клиента по id

DROP FUNCTION IF EXISTS balance//
CREATE FUNCTION balance(f_customer_id INT)
RETURNS DECIMAL(7,2) DETERMINISTIC
BEGIN
	DECLARE charge DECIMAL(7,2);
	DECLARE payment DECIMAL(7,2);

	SELECT IFNULL(SUM(services.amount), 0) INTO charge
	FROM services WHERE customer_id = f_customer_id;
	
	SELECT IFNULL(SUM(payments.amount), 0) INTO payment
	FROM payments WHERE customer_id = f_customer_id;
	
	RETURN charge - payment;
	
END//

SELECT balance(1);


-- Процедура внесения данных в таблицу services из представления Расписание.

DROP PROCEDURE IF EXISTS fill_service//
CREATE PROCEDURE fill_service(p_customer_id BIGINT UNSIGNED, worker_id SMALLINT UNSIGNED, OUT tran_result VARCHAR(200))
BEGIN
	DECLARE amount DECIMAL(7,2);
		
	SELECT IFNULL(SUM(Количество * Визитов * (SELECT c.price FROM locations AS l INNER JOIN cargo AS c	ON l.form = c.id WHERE l.address = Адрес)), 0)
	INTO amount FROM schedule
	WHERE id = p_customer_id;
	
	START TRANSACTION;
	INSERT services VALUES(DEFAULT, p_customer_id, CURRENT_DATE(), amount, worker_id, DEFAULT);
	IF amount = 0 THEN
		SET tran_result = 'Not ok';
		ROLLBACK;
	ELSE
		SET tran_result = 'ok';
		COMMIT;
	END IF;
	SELECT tran_result;
END//

CALL fill_service(1, 1, @tran_result);

-- Вставить триггер недопустимость ввода отрицательного значения в поле amount таблицы payments.

DROP TRIGGER IF EXISTS payments_control//
CREATE TRIGGER payments_control BEFORE INSERT ON payments
FOR EACH ROW
BEGIN
	IF NEW.amount <= 0 THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такое значение недопустимо!';
	END IF;
END//

INSERT payments VALUES (DEFAULT, 2, CURRENT_DATE(), -1000, 2, DEFAULT);