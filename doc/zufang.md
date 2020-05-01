### create table sql


title = scrapy.Field()
rent = scrapy.Field()  # 租金
house_type = scrapy.Field() # 户型
house_type_full = scrapy.Field() # 房型(全)
house_area = scrapy.Field() # 面积
house_tier = scrapy.Field() # 楼层
house_orientation = scrapy.Field() # 朝向
house_labels = scrapy.Field() # 房屋标签 配套齐全、精装修
address = scrapy.Field()
charge_url = scrapy.Field() # detail页面
can_one = scrapy.Field() # 支持押一付一
estate_title = scrapy.Field() # 小区名字
has_balcony = scrapy.Field() # 是否有阳台
request_url = scrapy.Field() # 请求的url




```
CREATE TABLE `zufang` (
  `id` bigint(18) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(256) not null default '' comment '租房标题',
  `rent` mediumint(8) unsigned not null default '0' comment '租金(元)',
  `house_type` varchar(64) not null default '' comment '户型',
  `house_type_full` varchar(64) not null default '' comment '户型全',
  ``
  
  
  `job_title` varchar(64) NOT NULL DEFAULT '' COMMENT '岗位名称',
  `left_pay_k` mediumint(9) unsigned NOT NULL DEFAULT '0' COMMENT '薪资 月薪 左侧值',
  `right_pay_k` mediumint(9) unsigned NOT NULL DEFAULT '0' COMMENT '薪资 月薪 右侧值',
  `num_months` tinyint(4) NOT NULL COMMENT '一年多少薪 | 13薪',
  `left_pay_w` mediumint(9) NOT NULL COMMENT '薪资 年薪 左侧值',
  `right_pay_w` mediumint(9) NOT NULL COMMENT '薪资 年薪 右侧值',
  `answer_day` tinyint(4) unsigned NOT NULL DEFAULT '0' COMMENT '投递后反馈的工作日',
  `company` varchar(64) NOT NULL DEFAULT '' COMMENT '公司名称',
  `job_address` varchar(256) NOT NULL DEFAULT '' COMMENT '工作城市',
  `publish_time` date DEFAULT NULL COMMENT '发布时间',
  `education` varchar(64) NOT NULL DEFAULT '' COMMENT '学历要求',
  `experience` varchar(64) NOT NULL DEFAULT '' COMMENT '工作经验要求',
  `language` varchar(64) NOT NULL DEFAULT '' COMMENT '语言要求',
  `age` varchar(64) NOT NULL DEFAULT '' COMMENT '年龄要求',
  `job_treatment` varchar(512) NOT NULL DEFAULT '' COMMENT '工作待遇标签 [通讯津贴,午餐补助,定期体检,管理规范]',
  `job_description` text COMMENT '职位描述',
  `oth_department` varchar(64) NOT NULL DEFAULT '' COMMENT '所属部门',
  `oth_report` varchar(64) NOT NULL DEFAULT '' COMMENT '汇报对象',
  `oth_major` varchar(64) NOT NULL DEFAULT '' COMMENT '专业要求',
  `oth_underline` varchar(64) NOT NULL DEFAULT '' COMMENT '下属人数',
  `enterprise_introduce` text COMMENT '企业介绍',
  `eye_industry` varchar(64) NOT NULL DEFAULT '' COMMENT '行业',
  `eye_people` varchar(64) NOT NULL DEFAULT '' COMMENT '公司规模',
  `eye_address` varchar(64) NOT NULL DEFAULT '' COMMENT '公司地址',
  `eye_register_time` varchar(64) NOT NULL DEFAULT '' COMMENT '注册时间',
  `eye_register_fund` varchar(64) NOT NULL DEFAULT '' COMMENT '注册资金',
  `eye_deadline` varchar(64) NOT NULL DEFAULT '' COMMENT '经营期限',
  `eye_business_scope` varchar(512) NOT NULL DEFAULT '' COMMENT '经营范围',
  `detail_url` varchar(128) NOT NULL DEFAULT '' COMMENT '请求详情页面url',
  `search_category` varchar(128) NOT NULL DEFAULT '' COMMENT '搜索标签分类 | 数据分析',
  `triangle_mark` varchar(64) NOT NULL DEFAULT '' COMMENT '三角标签',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `left_pay_k` (`left_pay_k`) USING BTREE,
  KEY `right_pay_k` (`right_pay_k`) USING BTREE,
  KEY `answer_day` (`answer_day`) USING BTREE,
  KEY `publish_time` (`publish_time`) USING BTREE,
  KEY `right_pay_w` (`right_pay_w`) USING BTREE,
  KEY `left_pay_w` (`left_pay_w`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=972 DEFAULT CHARSET=utf8mb4;

```