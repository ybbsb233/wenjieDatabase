-- Existing accounts keep passwords, login versions, and learning history.
USE learning_analysis;
ALTER TABLE app_user ALTER COLUMN must_change_password SET DEFAULT 0;
UPDATE app_user SET must_change_password=0 WHERE must_change_password<>0;
