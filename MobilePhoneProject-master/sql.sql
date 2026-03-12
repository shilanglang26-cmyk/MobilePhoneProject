CREATE TABLE `tb_user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(150) NOT NULL COMMENT '用户名',
  `password` varchar(128) NOT NULL COMMENT '加密密码',
  `phone` varchar(11) NOT NULL UNIQUE COMMENT '手机号（MD5加密存储）',
  `email` varchar(254) DEFAULT NULL COMMENT '邮箱',
  `avatar` varchar(255) DEFAULT NULL COMMENT '用户头像',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '账号状态（1-正常，0-禁用）',
  `is_staff` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为管理员（0-普通用户，1-管理员）',
  `is_superuser` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为超级管理员',
  `date_joined` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `phone` (`phone`),
  INDEX `idx_username_phone` (`username`,`phone`) COMMENT '用户名+手机号联合索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

CREATE TABLE `tb_address` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '地址ID',
  `user_id` bigint NOT NULL COMMENT '所属用户ID',
  `receiver` varchar(20) NOT NULL COMMENT '收件人',
  `phone` varchar(11) NOT NULL COMMENT '收件人电话',
  `province` varchar(20) NOT NULL COMMENT '省份',
  `city` varchar(20) NOT NULL COMMENT '城市',
  `detail_address` varchar(100) NOT NULL COMMENT '详细地址',
  `is_default` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否默认地址（1-是，0-否）',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`) COMMENT '用户ID索引',
  CONSTRAINT `fk_address_user` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收货地址表';

CREATE TABLE `tb_category` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `parent_id` bigint DEFAULT NULL COMMENT '父分类ID（0为一级分类）',
  `sort` int NOT NULL DEFAULT '0' COMMENT '排序权重（值越大越靠前）',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否启用（1-是，0-否）',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`) COMMENT '父分类ID索引',
  KEY `idx_sort` (`sort`) COMMENT '排序索引',
  CONSTRAINT `fk_category_parent` FOREIGN KEY (`parent_id`) REFERENCES `tb_category` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

CREATE TABLE `tb_product` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `name` varchar(100) NOT NULL COMMENT '商品名称',
  `category_id` bigint NOT NULL COMMENT '所属分类ID',
  `cover_image` varchar(255) NOT NULL COMMENT '商品封面图',
  `detail` longtext COMMENT '商品详情（富文本）',
  `price` decimal(10,2) NOT NULL COMMENT '参考价格',
  `sales` int NOT NULL DEFAULT '0' COMMENT '累计销量',
  `score` decimal(2,1) NOT NULL DEFAULT '5.0' COMMENT '商品评分',
  `is_hot` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否热销（1-是，0-否）',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否上架（1-是，0-否）',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`) COMMENT '分类ID索引',
  KEY `idx_hot_sales` (`is_hot`,`sales`) COMMENT '热销+销量联合索引',
  FULLTEXT KEY `ftx_product_name` (`name`) COMMENT '商品名称全文索引',
  CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) REFERENCES `tb_category` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

CREATE TABLE `tb_product_spec` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '规格ID',
  `product_id` bigint NOT NULL COMMENT '所属商品ID',
  `color` varchar(30) DEFAULT NULL COMMENT '颜色',
  `power` varchar(20) DEFAULT NULL COMMENT '功率（仅充电器类）',
  `model` varchar(50) DEFAULT NULL COMMENT '适配机型',
  `spec_price` decimal(10,2) NOT NULL COMMENT '规格售价',
  `sku` varchar(50) NOT NULL UNIQUE COMMENT '库存单位（SKU）',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`) COMMENT '商品ID索引',
  KEY `idx_sku` (`sku`) COMMENT 'SKU索引',
  CONSTRAINT `fk_spec_product` FOREIGN KEY (`product_id`) REFERENCES `tb_product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品规格表';

CREATE TABLE `tb_inventory` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '库存ID',
  `spec_id` bigint NOT NULL COMMENT '商品规格ID',
  `stock` int NOT NULL DEFAULT '0' COMMENT '当前库存',
  `warning_threshold` int NOT NULL DEFAULT '10' COMMENT '库存预警阈值',
  `locked_stock` int NOT NULL DEFAULT '0' COMMENT '锁定库存（下单未支付）',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_spec_id` (`spec_id`) COMMENT '规格ID唯一索引',
  KEY `idx_stock_warning` (`stock`,`warning_threshold`) COMMENT '库存+预警阈值联合索引',
  CONSTRAINT `fk_inventory_spec` FOREIGN KEY (`spec_id`) REFERENCES `tb_product_spec` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='库存表';

CREATE TABLE `tb_cart` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '购物车ID',
  `user_id` bigint NOT NULL COMMENT '所属用户ID',
  `spec_id` bigint NOT NULL COMMENT '商品规格ID',
  `quantity` int NOT NULL DEFAULT '1' COMMENT '商品数量',
  `is_selected` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否选中（1-是，0-否）',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_spec` (`user_id`,`spec_id`) COMMENT '用户+规格唯一索引（避免重复添加）',
  KEY `idx_user_id` (`user_id`) COMMENT '用户ID索引',
  CONSTRAINT `fk_cart_user` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_cart_spec` FOREIGN KEY (`spec_id`) REFERENCES `tb_product_spec` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表';

CREATE TABLE `tb_order` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_sn` varchar(30) NOT NULL UNIQUE COMMENT '订单编号（时间戳+随机数）',
  `user_id` bigint NOT NULL COMMENT '所属用户ID',
  `address_id` bigint NOT NULL COMMENT '收货地址ID',
  `total_amount` decimal(10,2) NOT NULL COMMENT '订单总金额',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '订单状态（1-待支付，2-待发货，3-待收货，4-已完成，6-已取消）',
  `payment_time` datetime DEFAULT NULL COMMENT '支付时间',
  `shipping_time` datetime DEFAULT NULL COMMENT '发货时间',
  `receive_time` datetime DEFAULT NULL COMMENT '确认收货时间',
  `cancel_time` datetime DEFAULT NULL COMMENT '取消时间',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_order_sn` (`order_sn`) COMMENT '订单编号唯一索引',
  KEY `idx_user_id` (`user_id`) COMMENT '用户ID索引',
  KEY `idx_status` (`status`) COMMENT '订单状态索引',
  KEY `idx_created_at` (`created_at`) COMMENT '创建时间索引',
  CONSTRAINT `fk_order_user` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_order_address` FOREIGN KEY (`address_id`) REFERENCES `tb_address` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

CREATE TABLE `tb_order_item` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '订单项ID',
  `order_id` bigint NOT NULL COMMENT '所属订单ID',
  `spec_id` bigint NOT NULL COMMENT '商品规格ID',
  `product_name` varchar(100) NOT NULL COMMENT '商品名称（冗余存储）',
  `spec_info` varchar(100) NOT NULL COMMENT '规格信息（颜色+型号等）',
  `price` decimal(10,2) NOT NULL COMMENT '购买单价',
  `quantity` int NOT NULL COMMENT '购买数量',
  `subtotal` decimal(10,2) NOT NULL COMMENT '小计金额',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`) COMMENT '订单ID索引',
  KEY `idx_spec_id` (`spec_id`) COMMENT '规格ID索引',
  CONSTRAINT `fk_order_item_order` FOREIGN KEY (`order_id`) REFERENCES `tb_order` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_item_spec` FOREIGN KEY (`spec_id`) REFERENCES `tb_product_spec` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单项表';

CREATE TABLE `tb_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '支付记录ID',
  `order_id` bigint NOT NULL COMMENT '所属订单ID',
  `payment_method` tinyint NOT NULL COMMENT '支付方式（1-微信支付，2-支付宝，3-银行卡）',
  `trade_no` varchar(100) DEFAULT NULL COMMENT '第三方支付流水号',
  `amount` decimal(10,2) NOT NULL COMMENT '支付金额',
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '支付状态（0-未支付，1-已支付）',
  `paid_at` datetime DEFAULT NULL COMMENT '支付时间',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_order_id` (`order_id`) COMMENT '订单ID唯一索引（一个订单对应一条支付记录）',
  KEY `idx_trade_no` (`trade_no`) COMMENT '第三方流水号索引',
  KEY `idx_status` (`status`) COMMENT '支付状态索引',
  CONSTRAINT `fk_payment_order` FOREIGN KEY (`order_id`) REFERENCES `tb_order` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付记录表';

CREATE TABLE `tb_log` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user_id` bigint DEFAULT NULL COMMENT '操作用户ID（未登录为NULL）',
  `operation` varchar(50) NOT NULL COMMENT '操作类型（登录、下单、支付等）',
  `ip_address` varchar(50) DEFAULT NULL COMMENT '操作IP地址',
  `content` text COMMENT '操作详情',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`) COMMENT '用户ID索引',
  KEY `idx_operation` (`operation`) COMMENT '操作类型索引',
  KEY `idx_created_at` (`created_at`) COMMENT '操作时间索引',
  CONSTRAINT `fk_log_user` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统日志表';