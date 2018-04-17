drop table if exists Users;

drop table if exists IssueStatus;

drop table if exists Issues;

CREATE TABLE Users (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    username    CHAR     UNIQUE
                         NOT NULL,
    email       CHAR     UNIQUE,
    phone       STRING   UNIQUE,
    password    CHAR     NOT NULL,
    createdtime DATETIME NOT NULL
);


CREATE TABLE IssueStatus (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    status      VARCHAR  NOT NULL
                         UNIQUE,
    remark      VARCHAR  NOT NULL,
    createdtime DATETIME NOT NULL,
    editedtime  DATETIME
);


CREATE TABLE Issues (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    title       VARCHAR  NOT NULL,
    intro       TEXT  NOT NULL,
    imgurl      VARCHAR,
    customer    VARCHAR  NOT NULL,
    contact     VARCHAR  NOT NULL,
    statusid    INTEGER  REFERENCES IssueStatus (id),
    reply       TEXT,
    remark      VARCHAR,
    replier     VARCHAR,
    replytime   DATETIME,
    createdtime DATETIME NOT NULL,
    replied     BOOLEAN  DEFAULT (0)
);

-- Users 用户表插入初始 admin 数据
INSERT INTO Users(username, password, createdtime) VALUES ('admin', 'admin', '2018-01-01 00:00:00');

-- IssueStatus 问题状态插入标准初始数据
INSERT INTO IssueStatus(status, remark, createdtime, editedtime) VALUES ('Open', '已打开', '2018-01-01 00:00:00', '2018-01-01 00:00:01');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('Reopen', '再打开', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('Assigned', '已指派', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('Duplicated', '重复问题', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('Postponed', '延期处理', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('In Progress', '处理中', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('Fixed', '已修复', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('Not Integrated', '未集成', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('Rejected', '已拒绝', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('No Repro', '无法复现', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('Verified', '已解决', '2018-01-01 00:00:00');
INSERT INTO IssueStatus(status, remark, createdtime) VALUES ('Closed', '已关闭', '2018-01-01 00:00:00');

-- Issues 问题表初始化数据
INSERT INTO Issues(title, intro, customer, contact, statusid, imgurl, createdtime) VALUES ('打开问题', '关联状态已打开', '柯南', 'kenan@jianghu.com', 1, 'demo.png', '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('再打开问题', '关联状态再打开', '土方', 'tufang@boyinggui.com', 2, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('指派问题', '关联状态已指派', 'saber', '15252052134', 3, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('重复问题', '关联状态重复问题', '孙悟空', '10100000000', 4, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('延期处理', '关联状态延期处理', '贝吉塔', '10200000000', 5, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('处理中问题', '关联状态处理中', '怪盗基德', 'jide@jianghu.com', 6, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('问题已修复', '关联状态已修复', '兰', 'ran@jianghu.com', 7, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('功能未集成', '关联状态未集成', '雪女', 'xuenv@huatougui.com', 8, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('问题拒不处理', '关联状态已拒绝', '卫宫切嗣', 'emiya@fate.com', 9, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('Bug 无法复现', '关联状态无法复现', '卫宫士郎', '10000000000', 10, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('问题已经解决', '关联状态已解决', '凛', '10000000001', 11, '2018-01-01 00:00:00');
INSERT INTO Issues(title, intro, customer, contact, statusid, createdtime) VALUES ('问题已关闭', '关联状态已关闭', '伊利亚', '10000000002', 12, '2018-01-01 00:00:00');
