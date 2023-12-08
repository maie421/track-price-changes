create table log.products
(
    id          int auto_increment
        primary key,
    name        varchar(255)                        not null comment '상품 이름',
    product_id  bigint                             not null comment '상품 id',
    category_id bigint                             not null comment '카테고리 id',
    image       varchar(255)                        not null comment '상품 이미지',
    price       int       default 0                 not null comment '상품 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    index product_index (category_id asc, product_id asc, created_at desc)
)
    comment '상품 로그' collate = utf8mb4_unicode_ci;


create table `track_price_changes`.products_stats
(
    id          int auto_increment primary key,
    product_id  bigint                             not null comment '상품 id',
    high_price  int       default 0                 not null comment '최고가 가격',
    low_price   int       default 0                 not null comment '최저가 가격',
    avg_price   float       default 0                 not null comment '평균 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX product_detail ( product_id )
)
    comment '상품 가격 통계' collate = utf8mb4_unicode_ci;

create table `track_price_changes`.products
(
    id          int auto_increment primary key,
    product_id  bigint                             not null comment '상품 id',
    category_id bigint                             not null comment '카테고리 id',
    name        varchar(255)                        not null comment '상품 이름',
    image       varchar(255)                        not null comment '상품 이미지',
    price       int       default 0                 not null comment '상품 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX product_index  ( category_id, product_id )
)
    comment '상품' collate = utf8mb4_unicode_ci;

alter table `track_price_changes`.products
    add constraint products_pk
        unique (product_id);

# 502483 : "국/탕/전골"
# 502484 : "덮밥/비빔밥"
# 502485 : "스테이크/고기"
# 502486 : "면/파스타/감바스"
# 502487 : "분식"
# 502489 : "어린이 만들기 겸용"
# 502490 : "중식요리"
# 502491 : "기타요리"

SELECT category_id, product_id, count(*) as cnt FROM log.products group by category_id, product_id having cnt < 3;
SELECT category_id, product_id, count(*) as cnt FROM log.products group by category_id, product_id;

SELECT count(*)
FROM log.products
where category_id = '502383'
  and created_at > '2023-12-08 00:00:00'
  and created_at < '2023-12-08 23:59:59';




SELECT *
FROM log.products order by created_at desc;

SELECT count(*) FROM log.products;

SELECT SUM(data_length+index_length)/1024/1024 used_MB, SUM(data_free)/1024/1024 free_MB FROM information_schema.tables;

SELECT TABLE_NAME AS "Tables",
                     round(((data_length + index_length) / 1024 / 1024), 2) "Size in MB"
FROM information_schema.TABLES
WHERE table_schema = 'log'
ORDER BY (data_length + index_length) DESC;


    SELECT product_id, MAX(created_at) AS max_created_at
    FROM log.products
    WHERE category_id = '502383'
      AND created_at >= '2023-12-06 00:00:00'
      AND created_at <= '2023-12-06 23:59:59'
    GROUP BY product_id;


SELECT p.product_id, p.price, name, image, category_id
FROM log.products p
JOIN (
    SELECT product_id, MAX(created_at) AS max_created_at
    FROM log.products
    WHERE category_id = '502383'
      AND created_at >= '2023-12-08 00:00:00'
      AND created_at <= '2023-12-08 23:59:59'
    GROUP BY product_id
) AS max_dates
ON p.product_id = max_dates.product_id AND p.created_at = max_dates.max_created_at
WHERE p.category_id = '502383'
  AND p.created_at >= '2023-12-08 00:00:00'
  AND p.created_at <= '2023-12-08 23:59:59';



# 가격 변동이 있는 상품
SELECT product_id, count(distinct price) as cnt
FROM log.products
where created_at > '2023-12-08 00:00:00'
  and created_at < '2023-12-08 23:59:59' group by product_id having cnt >= 2;

select * from track_price_changes.products_stats where product_id in (
'156649272',
'1366404363',
'1910974154',
'2359442698',
'5293802749',
'6060763884',
'6667411234',
'6773329430',
'6908772118',
'6908778798',
'6909266222',
'7449919031',
'7704727303',
'7708582314') order by  product_id;
