-- create city
INSERT INTO "snappfood_city" ("name") VALUES ('شیراز');

-- list city
SELECT "snappfood_city"."id", "snappfood_city"."name" FROM "snappfood_city";

INSERT INTO "snappfood_address" ("city_id", "x", "y", "street", "alley", "plaque") VALUES (1, 2, 6, 'پاسداران', 'کمیل', '26'); args=[1, 2, 6, 'پاسداران', 'کمیل', '26']

INSERT INTO "snappfood_shop" ("address_id", "about_text", "name", "minimum_bill_value") VALUES (1, 'چای دنج و مناسب', 'قهوه خانه سیامکی', 10000); args=[1, 'چای دنج و مناسب', 'قهوه خانه سیامکی', 10000]
