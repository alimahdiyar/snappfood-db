BEGIN;
--
-- Create model Address
--
CREATE TABLE "snappfood_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "x" integer NOT NULL, "y" integer NOT NULL, "street" varchar(10) NOT NULL, "alley" varchar(10) NOT NULL, "plaque" varchar(10) NOT NULL);
--
-- Create model Admin
--
CREATE TABLE "snappfood_admin" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" char(32) NOT NULL UNIQUE, "username" varchar(20) NOT NULL UNIQUE, "password" varchar(128) NOT NULL);
--
-- Create model Cart
--
CREATE TABLE "snappfood_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT);
--
-- Create model Category
--
CREATE TABLE "snappfood_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(30) NOT NULL);
--
-- Create model City
--
CREATE TABLE "snappfood_city" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(30) NOT NULL);
--
-- Create model Comment
--
CREATE TABLE "snappfood_comment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "comment" integer NOT NULL, "text" text NOT NULL);
--
-- Create model Discount
--
CREATE TABLE "snappfood_discount" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "persent" integer NOT NULL);
--
-- Create model Food
--
CREATE TABLE "snappfood_food" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "price" integer NOT NULL, "name" varchar(100) NOT NULL, "about" text NOT NULL, "discount" integer NOT NULL);
--
-- Create model Invoice
--
CREATE TABLE "snappfood_invoice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(20) NOT NULL, "address_id" integer NOT NULL REFERENCES "snappfood_address" ("id") DEFERRABLE INITIALLY DEFERRED, "discount_id" integer NULL REFERENCES "snappfood_discount" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "snappfood_invoice_items" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "invoice_id" integer NOT NULL REFERENCES "snappfood_invoice" ("id") DEFERRABLE INITIALLY DEFERRED, "food_id" integer NOT NULL REFERENCES "snappfood_food" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Shop
--
CREATE TABLE "snappfood_shop" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "about_text" text NOT NULL, "name" varchar(30) NOT NULL, "minimum_bill_value" integer NOT NULL, "address_id" integer NOT NULL UNIQUE REFERENCES "snappfood_address" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model User
--
CREATE TABLE "snappfood_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" char(32) NOT NULL UNIQUE, "first_name" varchar(20) NOT NULL, "last_name" varchar(20) NOT NULL, "phone_number" varchar(20) NOT NULL UNIQUE, "email" varchar(254) NOT NULL, "password" varchar(128) NOT NULL);
CREATE TABLE "snappfood_user_favorite" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "snappfood_user" ("id") DEFERRABLE INITIALLY DEFERRED, "food_id" integer NOT NULL REFERENCES "snappfood_food" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Wallet
--
CREATE TABLE "snappfood_wallet" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL UNIQUE REFERENCES "snappfood_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field shop to food
--
ALTER TABLE "snappfood_food" RENAME TO "snappfood_food__old";
CREATE TABLE "snappfood_food" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "price" integer NOT NULL, "name" varchar(100) NOT NULL, "about" text NOT NULL, "discount" integer NOT NULL, "shop_id" integer NOT NULL REFERENCES "snappfood_shop" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "snappfood_food" ("id", "price", "name", "about", "discount", "shop_id") SELECT "id", "price", "name", "about", "discount", NULL FROM "snappfood_food__old";
DROP TABLE "snappfood_food__old";
CREATE INDEX "snappfood_invoice_address_id_5355af61" ON "snappfood_invoice" ("address_id");
CREATE INDEX "snappfood_invoice_discount_id_ce7ad8f6" ON "snappfood_invoice" ("discount_id");
CREATE UNIQUE INDEX "snappfood_invoice_items_invoice_id_food_id_4439aa21_uniq" ON "snappfood_invoice_items" ("invoice_id", "food_id");
CREATE INDEX "snappfood_invoice_items_invoice_id_c7da4eb7" ON "snappfood_invoice_items" ("invoice_id");
CREATE INDEX "snappfood_invoice_items_food_id_b0746a01" ON "snappfood_invoice_items" ("food_id");
CREATE UNIQUE INDEX "snappfood_user_favorite_user_id_food_id_bab8eb93_uniq" ON "snappfood_user_favorite" ("user_id", "food_id");
CREATE INDEX "snappfood_user_favorite_user_id_09ea615c" ON "snappfood_user_favorite" ("user_id");
CREATE INDEX "snappfood_user_favorite_food_id_e0f8e705" ON "snappfood_user_favorite" ("food_id");
CREATE INDEX "snappfood_food_shop_id_fd33b05f" ON "snappfood_food" ("shop_id");
--
-- Add field users to discount
--
CREATE TABLE "snappfood_discount_users" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "discount_id" integer NOT NULL REFERENCES "snappfood_discount" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "snappfood_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field invoice to comment
--
ALTER TABLE "snappfood_comment" RENAME TO "snappfood_comment__old";
CREATE TABLE "snappfood_comment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "comment" integer NOT NULL, "text" text NOT NULL, "invoice_id" integer NOT NULL REFERENCES "snappfood_invoice" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "snappfood_comment" ("id", "comment", "text", "invoice_id") SELECT "id", "comment", "text", NULL FROM "snappfood_comment__old";
DROP TABLE "snappfood_comment__old";
CREATE UNIQUE INDEX "snappfood_discount_users_discount_id_user_id_52629e24_uniq" ON "snappfood_discount_users" ("discount_id", "user_id");
CREATE INDEX "snappfood_discount_users_discount_id_1e8b2601" ON "snappfood_discount_users" ("discount_id");
CREATE INDEX "snappfood_discount_users_user_id_e4f1ba46" ON "snappfood_discount_users" ("user_id");
CREATE INDEX "snappfood_comment_invoice_id_fb7e3ea0" ON "snappfood_comment" ("invoice_id");
--
-- Add field items to cart
--
CREATE TABLE "snappfood_cart_items" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cart_id" integer NOT NULL REFERENCES "snappfood_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "food_id" integer NOT NULL REFERENCES "snappfood_food" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field user to cart
--
ALTER TABLE "snappfood_cart" RENAME TO "snappfood_cart__old";
CREATE TABLE "snappfood_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL UNIQUE REFERENCES "snappfood_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "snappfood_cart" ("id", "user_id") SELECT "id", NULL FROM "snappfood_cart__old";
DROP TABLE "snappfood_cart__old";
CREATE UNIQUE INDEX "snappfood_cart_items_cart_id_food_id_4559b243_uniq" ON "snappfood_cart_items" ("cart_id", "food_id");
CREATE INDEX "snappfood_cart_items_cart_id_df7c2a50" ON "snappfood_cart_items" ("cart_id");
CREATE INDEX "snappfood_cart_items_food_id_ca47d99d" ON "snappfood_cart_items" ("food_id");
--
-- Add field shop to admin
--
ALTER TABLE "snappfood_admin" RENAME TO "snappfood_admin__old";
CREATE TABLE "snappfood_admin" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" char(32) NOT NULL UNIQUE, "username" varchar(20) NOT NULL UNIQUE, "password" varchar(128) NOT NULL, "shop_id" integer NOT NULL REFERENCES "snappfood_shop" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "snappfood_admin" ("id", "token", "username", "password", "shop_id") SELECT "id", "token", "username", "password", NULL FROM "snappfood_admin__old";
DROP TABLE "snappfood_admin__old";
CREATE INDEX "snappfood_admin_shop_id_6ea39191" ON "snappfood_admin" ("shop_id");
--
-- Add field city to address
--
ALTER TABLE "snappfood_address" RENAME TO "snappfood_address__old";
CREATE TABLE "snappfood_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "x" integer NOT NULL, "y" integer NOT NULL, "street" varchar(10) NOT NULL, "alley" varchar(10) NOT NULL, "plaque" varchar(10) NOT NULL, "city_id" integer NOT NULL REFERENCES "snappfood_city" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "snappfood_address" ("id", "x", "y", "street", "alley", "plaque", "city_id") SELECT "id", "x", "y", "street", "alley", "plaque", NULL FROM "snappfood_address__old";
DROP TABLE "snappfood_address__old";
CREATE INDEX "snappfood_address_city_id_0abd6ed4" ON "snappfood_address" ("city_id");
COMMIT;
