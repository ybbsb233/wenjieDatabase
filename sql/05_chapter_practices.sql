-- Upgrade statements executed against the original schema.
USE learning_analysis;
ALTER TABLE chapter ADD COLUMN is_current TINYINT NOT NULL DEFAULT 1;
ALTER TABLE practice ADD COLUMN chapter_id BIGINT NULL, ADD CONSTRAINT fk_practice_chapter FOREIGN KEY(chapter_id) REFERENCES chapter(id);
ALTER TABLE practice ADD COLUMN archived TINYINT NOT NULL DEFAULT 0 CHECK(archived IN (0,1));
ALTER TABLE practice DROP CHECK `practice_chk_1`;
ALTER TABLE practice ADD CONSTRAINT ck_practice_source CHECK(source_type IN ('NORMAL','WRONG','CHAPTER'));
