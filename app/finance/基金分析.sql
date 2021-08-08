# noinspection NonAsciiCharactersForFile

# noinspection NonAsciiCharactersForFile @ table/"基金基础信息"

-- 算出每一年的相对涨幅

create table 基金年度涨幅
(
	基金代码 varchar(128) not null,
	净值年份 int not null,
	年初日期 int not null,
    年初净值 float null,
    年末日期 int not null,
    年末净值 float null,
	年度涨幅 float null,
	primary key (基金代码, 净值年份)
);



INSERT INTO 基金年度涨幅
    (
        SELECT
            t_g.基金代码 AS 基金代码,t_g.净值年份 AS 净值年份,
            t_g.年初日期 AS 年初日期,t_b.累计净值 AS 年初净值,
            t_g.年末日期 AS 年末日期,t_e.累计净值 AS 年末净值,
            ROUND(((CAST(t_e.累计净值 AS FLOAT) - CAST(t_b.累计净值 AS FLOAT)) / CAST(t_b.累计净值 AS FLOAT)) * 100, 2) AS 年度涨幅
        FROM
            (
                SELECT 基金代码, 净值年份, MIN(净值日期) AS 年初日期, MAX(净值日期) AS 年末日期
                FROM
                    (
                        SELECT 基金代码, (净值日期 div 10000) AS 净值年份, 净值日期, 单位净值, 累计净值 FROM fund_trend WHERE 累计净值 != '--'
                    ) AS t_1
                GROUP BY 基金代码, 净值年份
            ) AS t_g
                LEFT JOIN fund_trend AS t_b ON t_g.基金代码 = t_b.基金代码 AND t_g.年初日期 = t_b.净值日期
                LEFT JOIN fund_trend AS t_e ON t_g.基金代码 = t_e.基金代码 AND t_g.年末日期 = t_e.净值日期

    )
;

create table 基金年度涨幅——2011至2020汇总
(
    基金代码 varchar(128) not null,
    涨幅2020 float null,
    涨幅2019 float null,
    涨幅2018 float null,
    涨幅2017 float null,
    涨幅2016 float null,
    涨幅2015 float null,
    涨幅2014 float null,
    涨幅2013 float null,
    涨幅2012 float null,
    涨幅2011 float null,
    primary key (基金代码)
);

INSERT INTO 基金年度涨幅——2011至2020汇总
SELECT
    基金代码
     , COALESCE(MAX(涨幅2020),0) AS 涨幅2020
     , COALESCE(MAX(涨幅2019),0) AS 涨幅2019
     , COALESCE(MAX(涨幅2018),0) AS 涨幅2018
     , COALESCE(MAX(涨幅2017),0) AS 涨幅2017
     , COALESCE(MAX(涨幅2016),0) AS 涨幅2016
     , COALESCE(MAX(涨幅2015),0) AS 涨幅2015
     , COALESCE(MAX(涨幅2014),0) AS 涨幅2014
     , COALESCE(MAX(涨幅2013),0) AS 涨幅2013
     , COALESCE(MAX(涨幅2012),0) AS 涨幅2012
     , COALESCE(MAX(涨幅2011),0) AS 涨幅2011
FROM
    (
        SELECT 基金代码, 年度涨幅 AS 涨幅2020,   null AS 涨幅2019,   null AS 涨幅2018,   null AS 涨幅2017,   null AS 涨幅2016,   null AS 涨幅2015,   null AS 涨幅2014,   null AS 涨幅2013 ,   null AS 涨幅2012,   null AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2020
        UNION ALL
        SELECT 基金代码,   null AS 涨幅2020, 年度涨幅 AS 涨幅2019,   null AS 涨幅2018,   null AS 涨幅2017,   null AS 涨幅2016,   null AS 涨幅2015,   null AS 涨幅2014,   null AS 涨幅2013 ,   null AS 涨幅2012,   null AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2019
        UNION ALL
        SELECT 基金代码,   null AS 涨幅2020,   null AS 涨幅2019, 年度涨幅 AS 涨幅2018,   null AS 涨幅2017,   null AS 涨幅2016,   null AS 涨幅2015,   null AS 涨幅2014,   null AS 涨幅2013 ,   null AS 涨幅2012,   null AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2018
        UNION ALL
        SELECT 基金代码,   null AS 涨幅2020,   null AS 涨幅2019,   null AS 涨幅2018, 年度涨幅 AS 涨幅2017,   null AS 涨幅2016,   null AS 涨幅2015,   null AS 涨幅2014,   null AS 涨幅2013 ,   null AS 涨幅2012,   null AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2017
        UNION ALL
        SELECT 基金代码,   null AS 涨幅2020,   null AS 涨幅2019,   null AS 涨幅2018,   null AS 涨幅2017, 年度涨幅 AS 涨幅2016,   null AS 涨幅2015,   null AS 涨幅2014,   null AS 涨幅2013 ,   null AS 涨幅2012,   null AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2016
        UNION ALL
        SELECT 基金代码,   null AS 涨幅2020,   null AS 涨幅2019,   null AS 涨幅2018,   null AS 涨幅2017,   null AS 涨幅2016, 年度涨幅 AS 涨幅2015,   null AS 涨幅2014,   null AS 涨幅2013 ,   null AS 涨幅2012,   null AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2015
        UNION ALL
        SELECT 基金代码,   null AS 涨幅2020,   null AS 涨幅2019,   null AS 涨幅2018,   null AS 涨幅2017,   null AS 涨幅2016,   null AS 涨幅2015, 年度涨幅 AS 涨幅2014,   null AS 涨幅2013 ,   null AS 涨幅2012,   null AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2014
        UNION ALL
        SELECT 基金代码,   null AS 涨幅2020,   null AS 涨幅2019,   null AS 涨幅2018,   null AS 涨幅2017,   null AS 涨幅2016,   null AS 涨幅2015,   null AS 涨幅2014, 年度涨幅 AS 涨幅2013 ,   null AS 涨幅2012,   null AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2013
        UNION ALL
        SELECT 基金代码,   null AS 涨幅2020,   null AS 涨幅2019,   null AS 涨幅2018,   null AS 涨幅2017,   null AS 涨幅2016,   null AS 涨幅2015,   null AS 涨幅2014,   null AS 涨幅2013 , 年度涨幅 AS 涨幅2012,   null AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2012
        UNION ALL
        SELECT 基金代码,   null AS 涨幅2020,   null AS 涨幅2019,   null AS 涨幅2018,   null AS 涨幅2017,   null AS 涨幅2016,   null AS 涨幅2015,   null AS 涨幅2014,   null AS 涨幅2013 ,   null AS 涨幅2012, 年度涨幅 AS 涨幅2011 FROM 基金年度涨幅 WHERE 净值年份 = 2011
    ) AS t
GROUP BY 基金代码
;



-- 打分机
CREATE TABLE 基金排序
(
    代码 varchar(128) not null,
    项目 varchar(128) not null,
    取值 float null,
    正序 int null,
    primary key (代码, 项目)
);

INSERT INTO 基金排序
SELECT
    代码,
    项目,
    取值,
    (@i:=@i+1) AS 正序
FROM
    (
        SELECT
            t.代码 AS 代码,
            '从业最大跌幅' AS 项目,
            从业最大跌幅 AS 取值
        FROM 基金基础信息 AS t
                 LEFT JOIN 基金年度涨幅——2011至2020汇总 AS t_a ON  t.代码 = t_a.基金代码
                 LEFT JOIN ( SELECT * FROM 基金经理 WHERE 经理顺位 = 1 ) t_m on t.代码 = t_m.基金代码
        ORDER BY
#             t.阶段涨幅_近6月 DESC
#          t.阶段涨幅_近1年 DESC
#          t.阶段涨幅_近2年 DESC
#          t.阶段涨幅_近3年 DESC
#          t_a.涨幅2020 DESC
#          t_a.涨幅2019 DESC
#          t_a.涨幅2018 DESC
#          t_a.涨幅2017 DESC
#          t_a.涨幅2016 DESC
#          t_a.涨幅2015 DESC
#          t.风险_年化夏普比率_1年 DESC
#          t.风险_年化夏普比率_2年 DESC
#          t.风险_年化夏普比率_3年 DESC
#         t_m.从业年均回报 DESC
#         t_m.从业最大盈利 DESC
        t_m.从业最大跌幅
    ) AS t_all, (SELECT @i:=0) as i
;


SELECT DISTINCT 项目 FROM 基金排序;

SELECT
    *
FROM 基金基础信息 AS t
LEFT JOIN 基金年度涨幅——2011至2020汇总 AS t_a ON  t.代码 = t_a.基金代码
LEFT JOIN ( SELECT * FROM 基金经理 WHERE 经理顺位 = 1 ) t_m on t.代码 = t_m.基金代码
LEFT JOIN
(
    SELECT
        *
    FROM
        (
            SELECT
                   代码,
                   SUM(正序) AS 评分
            FROM 基金排序
            WHERE 项目 not in ('涨幅2018', '涨幅2017', '涨幅2016', '涨幅2015', '阶段涨幅_近3年', '风险_年化夏普比率_3年')
            GROUP BY 代码
        ) AS t
    ORDER BY 评分
) AS t_r ON t.代码 = t_r.代码
# WHERE t_m.管理数量 <=3 AND t_m.从业最大跌幅 > -30 AND t.成立 < 20141231
WHERE t_m.从业最大跌幅 > -30 AND t.成立 < 20151231
# WHERE t_m.从业最大跌幅 > -30
ORDER BY t_r.评分
;


SELECT ROUND(10, 3);


SELECT * FROM 基金行业 WHERE 代码 = '519002';