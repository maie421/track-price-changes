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


create table `track-price-changes`.stats
(
    id          int auto_increment primary key,
    product_id  bigint                             not null comment '상품 id',
    high_price  int       default 0                 not null comment '최고가 가격',
    low_price   int       default 0                 not null comment '최저가 가격',
    age_price   int       default 0                 not null comment '평균 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at  timestamp default CURRENT_TIMESTAMP null,
    INDEX product_detail ( product_id )
)
    comment '상품 가격 통계' collate = utf8mb4_unicode_ci;

create table `track-price-changes`.products
(
    id          int auto_increment primary key,
    product_id  bigint                             not null comment '상품 id',
    category_id bigint                             not null comment '카테고리 id',
    name        varchar(255)                        not null comment '상품 이름',
    image       varchar(255)                        not null comment '상품 이미지',
    price       int       default 0                 not null comment '상품 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at  timestamp default CURRENT_TIMESTAMP null,
    INDEX product_index  ( category_id, product_id )
)
    comment '상품' collate = utf8mb4_unicode_ci;


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

SELECT *
FROM log.products
where category_id = '502383'
  and created_at > '2023-12-06 00:00:00'
  and created_at < '2023-12-06 23:59:59';


SELECT count(*) FROM log.products;

SELECT SUM(data_length+index_length)/1024/1024 used_MB, SUM(data_free)/1024/1024 free_MB FROM information_schema.tables;

SELECT TABLE_NAME AS "Tables",
                     round(((data_length + index_length) / 1024 / 1024), 2) "Size in MB"

FROM information_schema.TABLES
WHERE table_schema = "log"
ORDER BY (data_length + index_length) DESC;
