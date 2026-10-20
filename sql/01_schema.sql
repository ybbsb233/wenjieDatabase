-- Only creates this project's independent database. Does not drop existing data.
CREATE DATABASE IF NOT EXISTS learning_analysis CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE learning_analysis;
CREATE TABLE app_user (
 id BIGINT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(32) NOT NULL UNIQUE,
 real_name VARCHAR(50) NOT NULL, password_hash VARCHAR(255) NOT NULL,
 role VARCHAR(16) NOT NULL, enabled TINYINT NOT NULL DEFAULT 1,
 must_change_password TINYINT NOT NULL DEFAULT 0, token_version BIGINT NOT NULL DEFAULT 0,
 created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3), updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
 CHECK(role IN ('STUDENT','ADMIN')), CHECK(enabled IN (0,1)), CHECK(must_change_password IN (0,1)), CHECK(token_version>=0)
) ENGINE=InnoDB;
CREATE TABLE course (
 id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100) NOT NULL UNIQUE,
 description VARCHAR(500), sort_order INT NOT NULL DEFAULT 0 CHECK(sort_order>=0)
) ENGINE=InnoDB;
CREATE TABLE chapter (
 id BIGINT PRIMARY KEY AUTO_INCREMENT, course_id BIGINT NOT NULL, name VARCHAR(100) NOT NULL,
 sort_order INT NOT NULL DEFAULT 0 CHECK(sort_order>=0), is_current TINYINT NOT NULL DEFAULT 1, UNIQUE(course_id,name),
 FOREIGN KEY(course_id) REFERENCES course(id)
) ENGINE=InnoDB;
CREATE TABLE knowledge_point (
 id BIGINT PRIMARY KEY AUTO_INCREMENT, chapter_id BIGINT NOT NULL, name VARCHAR(100) NOT NULL,
 description VARCHAR(500), sort_order INT NOT NULL DEFAULT 0 CHECK(sort_order>=0), UNIQUE(chapter_id,name),
 FOREIGN KEY(chapter_id) REFERENCES chapter(id)
) ENGINE=InnoDB;
CREATE TABLE question (
 id BIGINT PRIMARY KEY AUTO_INCREMENT, chapter_id BIGINT NOT NULL, question_type VARCHAR(16) NOT NULL,
 stem TEXT NOT NULL, option_a VARCHAR(1000) NOT NULL, option_b VARCHAR(1000) NOT NULL,
 option_c VARCHAR(1000), option_d VARCHAR(1000), correct_answer VARCHAR(4) NOT NULL, explanation TEXT NOT NULL,
 FOREIGN KEY(chapter_id) REFERENCES chapter(id), INDEX idx_question_chapter(chapter_id,question_type),
 CHECK(CHAR_LENGTH(TRIM(stem))>0 AND CHAR_LENGTH(TRIM(explanation))>0),
 CHECK(CHAR_LENGTH(TRIM(option_a))>0 AND CHAR_LENGTH(TRIM(option_b))>0),
 CHECK((question_type IN ('SINGLE','MULTIPLE') AND option_c IS NOT NULL AND option_d IS NOT NULL AND CHAR_LENGTH(TRIM(option_c))>0 AND CHAR_LENGTH(TRIM(option_d))>0)
    OR (question_type='JUDGE' AND option_a='正确' AND option_b='错误' AND option_c IS NULL AND option_d IS NULL)),
 CHECK((question_type='SINGLE' AND correct_answer IN ('A','B','C','D'))
    OR (question_type='MULTIPLE' AND correct_answer IN ('AB','AC','AD','BC','BD','CD','ABC','ABD','ACD','BCD','ABCD'))
    OR (question_type='JUDGE' AND correct_answer IN ('A','B')))
) ENGINE=InnoDB;
CREATE TABLE question_knowledge (
 question_id BIGINT NOT NULL, knowledge_id BIGINT NOT NULL, PRIMARY KEY(question_id,knowledge_id),
 FOREIGN KEY(question_id) REFERENCES question(id), FOREIGN KEY(knowledge_id) REFERENCES knowledge_point(id),
 INDEX idx_knowledge_question(knowledge_id,question_id)
) ENGINE=InnoDB;
CREATE TABLE practice (
 id BIGINT PRIMARY KEY AUTO_INCREMENT, student_id BIGINT NOT NULL, course_id BIGINT NOT NULL, chapter_id BIGINT,
 archived TINYINT NOT NULL DEFAULT 0 CHECK(archived IN (0,1)),
 source_type VARCHAR(16) NOT NULL, status VARCHAR(16) NOT NULL DEFAULT 'IN_PROGRESS',
 question_count INT NOT NULL, correct_count INT, started_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3), submitted_at DATETIME(3),
 FOREIGN KEY(student_id) REFERENCES app_user(id), FOREIGN KEY(course_id) REFERENCES course(id), FOREIGN KEY(chapter_id) REFERENCES chapter(id),
 CONSTRAINT ck_practice_source CHECK(source_type IN ('NORMAL','WRONG','CHAPTER')), CHECK(question_count>0),
 CHECK((status='IN_PROGRESS' AND correct_count IS NULL AND submitted_at IS NULL)
    OR (status='SUBMITTED' AND correct_count IS NOT NULL AND correct_count BETWEEN 0 AND question_count AND submitted_at IS NOT NULL AND submitted_at>=started_at)),
 INDEX idx_student_history(student_id,status,submitted_at,id), INDEX idx_course_history(course_id,status,submitted_at,id)
) ENGINE=InnoDB;
CREATE TABLE practice_item (
 id BIGINT PRIMARY KEY AUTO_INCREMENT, practice_id BIGINT NOT NULL, question_id BIGINT NOT NULL,
 order_no INT NOT NULL CHECK(order_no>0), option_order VARCHAR(4) NOT NULL,
 selected_answer VARCHAR(4), is_correct TINYINT,
 FOREIGN KEY(practice_id) REFERENCES practice(id), FOREIGN KEY(question_id) REFERENCES question(id),
 UNIQUE(practice_id,order_no), UNIQUE(practice_id,question_id), INDEX idx_item_question(question_id),
 CHECK(option_order IN ('AB','ABCD','ABDC','ACBD','ACDB','ADBC','ADCB','BACD','BADC','BCAD','BCDA','BDAC','BDCA','CABD','CADB','CBAD','CBDA','CDAB','CDBA','DABC','DACB','DBAC','DBCA','DCAB','DCBA')),
 CHECK(is_correct IS NULL OR is_correct IN (0,1)),
 CHECK(selected_answer IS NULL OR selected_answer IN ('A','B','C','D','AB','AC','AD','BC','BD','CD','ABC','ABD','ACD','BCD','ABCD'))
) ENGINE=InnoDB;
