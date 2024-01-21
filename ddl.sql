create table log.products
(
    id          int auto_increment
        primary key,
    product_id  bigint                              not null comment '상품 id',
    category_id bigint                              not null comment '카테고리 id',
    name        varchar(255)                        not null comment '상품 이름',
    image       varchar(255)                        not null comment '상품 이미지',
    price       int       default 0                 not null comment '현재 상품 가격',
    avg_price   float                               not null comment '평균 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at  timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    constraint products_pk
        unique (product_id)
)
    comment '상품' collate = utf8mb4_unicode_ci;

create index product_index
    on log.products (category_id asc, product_id asc, updated_at desc);


create table track_price_changes.products
(
    id          int auto_increment
        primary key,
    product_id  bigint                              not null comment '상품 id',
    category_id bigint                              not null comment '카테고리 id',
    name        varchar(255)                        not null comment '상품 이름',
    image       varchar(255)                        not null comment '상품 이미지',
    price       int       default 0                 not null comment '현재 상품 가격',
    avg_price   float                               not null comment '평균 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at  timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    constraint products_pk
        unique (product_id)
)
    comment '상품' collate = utf8mb4_unicode_ci;

create index product_index
    on track_price_changes.products (category_id asc, product_id asc, updated_at desc);


create table track_price_changes.products_stats
(
    id         int auto_increment
        primary key,
    product_id bigint                              not null comment '상품 id',
    high_price int       default 0                 not null comment '최고가 가격',
    low_price  int       default 0                 not null comment '최저가 가격',
    avg_price  float     default 0                 not null comment '평균 가격',
    created_at timestamp default CURRENT_TIMESTAMP not null,
    updated_at timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
)
    comment '상품 가격 통계' collate = utf8mb4_unicode_ci;

create index product_detail
    on track_price_changes.products_stats (product_id);

create index products_stats_create
    on track_price_changes.products_stats (created_at desc);

create table track_price_changes.products_test
(
    id          int auto_increment
        primary key,
    product_id  bigint                              not null comment '상품 id',
    category_id bigint                              not null comment '카테고리 id',
    name        varchar(255)                        not null comment '상품 이름',
    image       varchar(255)                        not null comment '상품 이미지',
    text        varchar(255)                        null comment '상품 설명',
    price       int       default 0                 not null comment '현재 상품 가격',
    avg_price   float                               not null comment '평균 가격',
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at  timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    constraint products_pk
        unique (product_id)
)
    comment '상품 인공지능 데이터 사용' collate = utf8mb4_unicode_ci;
