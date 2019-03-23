BEGIN;
--
-- Create model Category
--
CREATE TABLE "catalog_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(32) NOT NULL);
--
-- Create model Item
--
CREATE TABLE "catalog_item" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(32) NOT NULL, "description" text NOT NULL, "category_id" integer NOT NULL REFERENCES "catalog_category" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "catalog_item_category_id_a5ca86ac" ON "catalog_item" ("category_id");
COMMIT;
