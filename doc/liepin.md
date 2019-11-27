### 猎聘网数据抓取
> 流程记录

list页面 https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90

detail页面 https://www.liepin.com/job/1924386591.shtml?imscid=R000000075&ckid=1a3d8db71ded63fb&headckid=1a3d8db71ded63fb&pageNo=0&pageIdx5&totalIdx=5&sup=1&siTag=ZFDYQyfloRvvhTxLnVV_Qg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=b061131dd2ca5f9f0fd3f83473871b47&d_curPage=0&d_pageSize=40&d_headId=b061131dd2ca5f9f0fd3f83473871b47&d_posi=5


> 爬虫字段

```job_title
job_title  // 职位名称
left_pay_k // 薪资 月薪 左侧值
right_pay_k // 薪资 月薪 右侧值
num_months // 一年多少薪 | 13薪
left_pay_w // 换算成年薪 左侧值
right_pay_w // 换算成年薪 右侧值
answer_day // 投递后反馈的工作日
company // 公司名称
job_address // 工作城市
publish_time // 发布时间
education // 学历要求
experience // 工作经验要求
language // 语言要求
age // 年龄要求
job_treatment // 工作待遇标签 [通讯津贴,午餐补助,定期体检,管理规范]
job_description // 职位描述

# oth -> other 其他信息
oth_department // 所属部门
oth_report // 汇报对象
oth_major // 专业要求
oth_underline // 下属人数
enterprise_introduce // 企业介绍

# sky_eye 天眼查数据
eye_industry // 行业
eye_people // 公司规模
eye_address // 公司地址
eye_register_time // 注册时间
eye_register_fund // 注册资金
eye_deadline // 经营期限
eye_business_scope // 经营范围

detail_url // 请求详情页面url
search_category // 搜索标签分类 | 数据分析
triangle_mark // 三角标签

```

```.sql
--- create table sql

CREATE TABLE
IF
	NOT EXISTS `liepin` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `job_title` varchar(64) NOT NULL DEFAULT '' COMMENT '岗位名称',
  `left_pay_k` mediumint(9) unsigned NOT NULL DEFAULT '0' COMMENT '薪资 月薪 左侧值',
  `right_pay_k` mediumint(9) unsigned NOT NULL DEFAULT '0' COMMENT '薪资 月薪 右侧值',
  `num_months` tinyint(4) NOT NULL COMMENT '一年多少薪 | 13薪',
  `left_pay_w` mediumint(9) NOT NULL COMMENT '薪资 年薪 左侧值',
  `right_pay_w` mediumint(9) NOT NULL COMMENT '薪资 年薪 右侧值',
  `answer_day` tinyint(4) unsigned NOT NULL DEFAULT '0' COMMENT '投递后反馈的工作日',
  `company` varchar(64) NOT NULL DEFAULT '' COMMENT '公司名称',
  `job_address` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '工作城市',
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

