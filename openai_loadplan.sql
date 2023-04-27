-- PRAGMA recursive_triggers=1;     --- test


BEGIN;

-- CREATE TABLE "openai_loadplan" ------------------------------
DROP TABLE IF EXISTS openai_loadplan;

CREATE TABLE openai_loadplan(
	created_at DateTime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DateTime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	page Text NOT NULL PRIMARY KEY,
	prompt Text NOT NULL DEFAULT 'a1', -- Arik's prompt 1
	answer Text NOT NULL DEFAULT '',
	status Text NOT NULL DEFAULT 'u',  -- 'u'(nprocessed), 'f'(ailed) 'd'(one) (in)'p'(rogress), 'x'(disabled)

    CONSTRAINT unique_page UNIQUE (page)
);
-- -------------------------------------------------------------

-- CREATE INDEX "index_status_updated_at" ----------------------
CREATE INDEX index_status_updated_at ON openai_loadplan(status, updated_at DESC);
-- -------------------------------------------------------------

-- CREATE INDEX "index_updated_at" -----------------------------
CREATE INDEX index_updated_at ON openai_loadplan(updated_at);
-- -------------------------------------------------------------

--DROP TRIGGER IF EXISTS after_update_updated_at;
CREATE TRIGGER after_update_updated_at AFTER UPDATE ON openai_loadplan
BEGIN
    UPDATE openai_loadplan SET updated_at=CURRENT_TIMESTAMP WHERE page=NEW.page;
END;

INSERT INTO openai_loadplan(page) VALUES('google.com');
INSERT INTO openai_loadplan(page) VALUES('facebook.com');

COMMIT;
