CREATE TABLE IF NOT EXISTS institute (
    name VARCHAR(24) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS classroom (
    code VARCHAR(24) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS classroom_user (
    id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    is_student BOOLEAN,
    is_assistant BOOLEAN,
    is_teacher BOOLEAN,
    is_administrator BOOLEAN,
    user_fk INTEGER NOT NULL,
    classroom_fk INTEGER NOT NULL,
    FOREIGN KEY(user_fk) REFERENCES users(id),
    FOREIGN KEY(classroom_fk) REFERENCES classroom(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(12) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL,
    birthday VARCHAR(10) NOT NULL,
    institute_fk INTEGER,
    FOREIGN KEY(institute_fk) REFERENCES institute(id)
);
