create table log.products
(
    id          int auto_increment
        primary key,
    market_product_id  bigint                              not null comment '상품 id',
    market_category_id bigint                              not null comment '카테고리 id',
    name        varchar(255)                        not null comment '상품 이름',
    image       varchar(255)                        not null comment '상품 이미지',
    price       decimal(10, 2) unsigned             default 0.00  not null comment '현재 상품 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at  timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
)
    comment '상품 로그' collate = utf8mb4_unicode_ci;

create index product_index
    on log.products (market_category_id asc, market_product_id asc, updated_at desc);


create table track_price_changes.products
(
    id          int auto_increment
        primary key,
    product_code       varchar(255)                        not null comment '상품 코드',
    market_product_id  bigint                              not null comment '마켓 상품 id',
    market_category_id bigint                              not null comment '마켓 카테고리 id',
    name        varchar(255)                        not null comment '상품 이름',
    image       varchar(255)                        not null comment '상품 이미지',
    price       decimal(10, 2) unsigned             default 0.00                 not null comment '현재 상품 가격',
    avg_price   decimal(10, 2) unsigned             default 0.00                               not null comment '전체 평균 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at  timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    constraint products_pk
        unique (product_code)
)
    comment '상품 정보' collate = utf8mb4_unicode_ci;

create index product_index
    on track_price_changes.products (market_category_id asc, market_product_id asc, updated_at desc);


create table track_price_changes.products_stats
(
    id         int auto_increment
        primary key,
    product_code varchar(255)                              not null comment '상품 코드',
    market_product_id bigint                              not null comment '마켓 상품 id',
    high_price decimal(10, 2) unsigned             default 0.00  not null comment '최고가 가격',
    low_price  decimal(10, 2) unsigned             default 0.00                 not null comment '최저가 가격',
    avg_price  decimal(10, 2) unsigned             default 0.00                 not null comment '평균 가격',
    created_at timestamp default CURRENT_TIMESTAMP not null,
    updated_at timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
)
    comment '일별 상품 가격 통계' collate = utf8mb4_unicode_ci;

create index product_detail
    on track_price_changes.products_stats (product_code);

create index products_stats_create
    on track_price_changes.products_stats (created_at desc);


create table category
(
    id         int auto_increment primary key,
    category_id   bigint not null comment '카테고리 id',
    category_name varchar(255) not null comment '카테고리 이름',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at  timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
)
    comment '카테고리' collate = utf8mb4_unicode_ci;

insert into track_price_changes.category (category_id, category_name)
values  (502483, '국/탕/전골'),
        (502484, '덮밥/비빔밥'),
        (502485, '스테이크/고기'),
        (502486, '면/파스타/감바스'),
        (502487, '분식'),
        (502489, '어린이 만들기 겸용'),
        (502490, '중식요리'),
        (502491, '기타요리');
