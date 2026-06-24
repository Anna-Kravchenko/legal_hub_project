CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price_per_word REAL,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    service_id INTEGER,
    source_language_id INTEGER,
    target_language_id INTEGER,
    comment TEXT,
    file_path TEXT,
    status TEXT DEFAULT 'new',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (service_id) REFERENCES services(id),
    FOREIGN KEY (source_language_id) REFERENCES languages(id),
    FOREIGN KEY (target_language_id) REFERENCES languages(id)
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT,
    text TEXT,
    rating INTEGER,
    is_published INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO clients (name, email, phone)
VALUES
('Олена Коваль', 'olena@gmail.com', '+380671234567'),
('Ігор Петренко', 'igor@gmail.com', '+380661112233'),
('Марія Шевченко', 'maria@gmail.com', '+380631234123');

INSERT INTO services (name, description, price_per_word)
VALUES
('Переклад документів', 'Переклад паспортів, довідок, дипломів', 2.5),
('Юридичний переклад', 'Переклад договорів та юридичних документів', 3.5),
('Медичний переклад', 'Переклад медичних висновків та довідок', 3.8),
('Технічний переклад', 'Переклад технічної документації', 3.2),
('Нотаріальне засвідчення', 'Засвідчення перекладу нотаріусом', 250);

INSERT INTO languages (name, code)
VALUES
('Англійська', 'en'),
('Українська', 'uk'),
('Німецька', 'de'),
('Французька', 'fr'),
('Польська', 'pl'),
('Іспанська', 'es');

INSERT INTO reviews (client_name, text, rating)
VALUES
('Олена', 'Дуже швидко переклали документи. Рекомендую!', 5),
('Ігор', 'Якісний переклад та ввічливий сервіс.', 5),
('Марія', 'Замовляла переклад медичних документів, все зробили чудово.', 5),
('Андрій', 'Зручно замовляти переклад онлайн.', 4);

INSERT INTO orders
(client_id, service_id, source_language_id, target_language_id, comment, status)
VALUES
(1, 1, 1, 2, 'Переклад диплома', 'new'),
(2, 2, 2, 1, 'Переклад договору для партнера', 'in_progress'),
(3, 3, 3, 2, 'Переклад медичних документів', 'done');