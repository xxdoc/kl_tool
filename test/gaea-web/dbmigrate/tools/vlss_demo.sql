/*
Navicat MySQL Data Transfer

Source Server         : test25
Source Server Version : 50548
Source Host           : 121.40.128.45:3306
Source Database       : vlss_demo

Target Server Type    : MYSQL
Target Server Version : 50548
File Encoding         : 65001

Date: 2017-06-08 18:03:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for basic_msg
-- ----------------------------
DROP TABLE IF EXISTS `basic_msg`;
CREATE TABLE `basic_msg` (
  `msg_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` int(11) NOT NULL,
  `user_id` varchar(16) NOT NULL,
  `msg_type` varchar(16) NOT NULL,
  `timestamp` int(11) DEFAULT NULL,
  PRIMARY KEY (`msg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31000 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of basic_msg
-- ----------------------------
INSERT INTO `basic_msg` VALUES ('20000', '104', '10079', 'chat_and_review', '1496914832');
INSERT INTO `basic_msg` VALUES ('20001', '105', '10022', 'chat_and_review', '1496914749');
INSERT INTO `basic_msg` VALUES ('20002', '101', '10002', 'chat_and_review', '1496913634');
INSERT INTO `basic_msg` VALUES ('20003', '105', '10018', 'chat_and_review', '1496914486');
INSERT INTO `basic_msg` VALUES ('20004', '104', '10069', 'chat_and_review', '1496913924');
INSERT INTO `basic_msg` VALUES ('20005', '102', '10009', 'chat_and_review', '1496914232');
INSERT INTO `basic_msg` VALUES ('20006', '101', '10000', 'chat_and_review', '1496914999');
INSERT INTO `basic_msg` VALUES ('20007', '102', '10008', 'chat_and_review', '1496915042');
INSERT INTO `basic_msg` VALUES ('20008', '104', '10057', 'chat_and_review', '1496913861');
INSERT INTO `basic_msg` VALUES ('20009', '105', '10078', 'chat_and_review', '1496913260');
INSERT INTO `basic_msg` VALUES ('20010', '101', '10032', 'chat_and_review', '1496913389');
INSERT INTO `basic_msg` VALUES ('20011', '104', '10080', 'chat_and_review', '1496914115');
INSERT INTO `basic_msg` VALUES ('20012', '102', '10018', 'chat_and_review', '1496914345');
INSERT INTO `basic_msg` VALUES ('20013', '105', '10036', 'chat_and_review', '1496914298');
INSERT INTO `basic_msg` VALUES ('20014', '101', '10072', 'chat_and_review', '1496913575');
INSERT INTO `basic_msg` VALUES ('20015', '105', '10040', 'chat_and_review', '1496914228');
INSERT INTO `basic_msg` VALUES ('20016', '103', '10073', 'chat_and_review', '1496913062');
INSERT INTO `basic_msg` VALUES ('20017', '103', '10065', 'chat_and_review', '1496914078');
INSERT INTO `basic_msg` VALUES ('20018', '105', '10062', 'chat_and_review', '1496915049');
INSERT INTO `basic_msg` VALUES ('20019', '105', '10027', 'chat_and_review', '1496914830');
INSERT INTO `basic_msg` VALUES ('20020', '104', '10075', 'chat_and_review', '1496914597');
INSERT INTO `basic_msg` VALUES ('20021', '103', '10056', 'chat_and_review', '1496914793');
INSERT INTO `basic_msg` VALUES ('20022', '103', '10076', 'chat_and_review', '1496913709');
INSERT INTO `basic_msg` VALUES ('20023', '102', '10011', 'chat_and_review', '1496913055');
INSERT INTO `basic_msg` VALUES ('20024', '103', '10015', 'chat_and_review', '1496915010');
INSERT INTO `basic_msg` VALUES ('20025', '104', '10022', 'chat_and_review', '1496913445');
INSERT INTO `basic_msg` VALUES ('20026', '104', '10067', 'chat_and_review', '1496914233');
INSERT INTO `basic_msg` VALUES ('20027', '104', '10025', 'chat_and_review', '1496914217');
INSERT INTO `basic_msg` VALUES ('20028', '104', '10049', 'chat_and_review', '1496913879');
INSERT INTO `basic_msg` VALUES ('20029', '101', '10004', 'chat_and_review', '1496913861');
INSERT INTO `basic_msg` VALUES ('20030', '103', '10019', 'chat_and_review', '1496913387');
INSERT INTO `basic_msg` VALUES ('20031', '101', '10074', 'chat_and_review', '1496914316');
INSERT INTO `basic_msg` VALUES ('20032', '103', '10053', 'chat_and_review', '1496914575');
INSERT INTO `basic_msg` VALUES ('20033', '103', '10018', 'chat_and_review', '1496913149');
INSERT INTO `basic_msg` VALUES ('20034', '104', '10071', 'chat_and_review', '1496914682');
INSERT INTO `basic_msg` VALUES ('20035', '104', '10036', 'chat_and_review', '1496914895');
INSERT INTO `basic_msg` VALUES ('20036', '105', '10007', 'chat_and_review', '1496914084');
INSERT INTO `basic_msg` VALUES ('20037', '101', '10033', 'chat_and_review', '1496914157');
INSERT INTO `basic_msg` VALUES ('20038', '101', '10089', 'chat_and_review', '1496913090');
INSERT INTO `basic_msg` VALUES ('20039', '101', '10048', 'chat_and_review', '1496914808');
INSERT INTO `basic_msg` VALUES ('20040', '104', '10016', 'chat_and_review', '1496914637');
INSERT INTO `basic_msg` VALUES ('20041', '104', '10009', 'chat_and_review', '1496913091');
INSERT INTO `basic_msg` VALUES ('20042', '103', '10024', 'chat_and_review', '1496913620');
INSERT INTO `basic_msg` VALUES ('20043', '105', '10040', 'chat_and_review', '1496913110');
INSERT INTO `basic_msg` VALUES ('20044', '105', '10040', 'chat_and_review', '1496914600');
INSERT INTO `basic_msg` VALUES ('20045', '101', '10035', 'chat_and_review', '1496914180');
INSERT INTO `basic_msg` VALUES ('20046', '102', '10062', 'chat_and_review', '1496913498');
INSERT INTO `basic_msg` VALUES ('20047', '102', '10065', 'chat_and_review', '1496913214');
INSERT INTO `basic_msg` VALUES ('20048', '101', '10072', 'chat_and_review', '1496913967');
INSERT INTO `basic_msg` VALUES ('20049', '104', '10018', 'chat_and_review', '1496913719');
INSERT INTO `basic_msg` VALUES ('20050', '101', '10044', 'chat_and_review', '1496913325');
INSERT INTO `basic_msg` VALUES ('20051', '105', '10002', 'chat_and_review', '1496914184');
INSERT INTO `basic_msg` VALUES ('20052', '102', '10094', 'chat_and_review', '1496913635');
INSERT INTO `basic_msg` VALUES ('20053', '103', '10009', 'chat_and_review', '1496914023');
INSERT INTO `basic_msg` VALUES ('20054', '105', '10084', 'chat_and_review', '1496914104');
INSERT INTO `basic_msg` VALUES ('20055', '101', '10021', 'chat_and_review', '1496913191');
INSERT INTO `basic_msg` VALUES ('20056', '104', '10048', 'chat_and_review', '1496913485');
INSERT INTO `basic_msg` VALUES ('20057', '103', '10044', 'chat_and_review', '1496914763');
INSERT INTO `basic_msg` VALUES ('20058', '102', '10091', 'chat_and_review', '1496913369');
INSERT INTO `basic_msg` VALUES ('20059', '103', '10094', 'chat_and_review', '1496914373');
INSERT INTO `basic_msg` VALUES ('20060', '103', '10085', 'chat_and_review', '1496913929');
INSERT INTO `basic_msg` VALUES ('20061', '104', '10092', 'chat_and_review', '1496914478');
INSERT INTO `basic_msg` VALUES ('20062', '105', '10076', 'chat_and_review', '1496914669');
INSERT INTO `basic_msg` VALUES ('20063', '101', '10011', 'chat_and_review', '1496914071');
INSERT INTO `basic_msg` VALUES ('20064', '103', '10017', 'chat_and_review', '1496913514');
INSERT INTO `basic_msg` VALUES ('20065', '105', '10030', 'chat_and_review', '1496913461');
INSERT INTO `basic_msg` VALUES ('20066', '101', '10049', 'chat_and_review', '1496913655');
INSERT INTO `basic_msg` VALUES ('20067', '104', '10025', 'chat_and_review', '1496913518');
INSERT INTO `basic_msg` VALUES ('20068', '102', '10056', 'chat_and_review', '1496914311');
INSERT INTO `basic_msg` VALUES ('20069', '101', '10063', 'chat_and_review', '1496913991');
INSERT INTO `basic_msg` VALUES ('20070', '103', '10071', 'chat_and_review', '1496914266');
INSERT INTO `basic_msg` VALUES ('20071', '105', '10089', 'chat_and_review', '1496914594');
INSERT INTO `basic_msg` VALUES ('20072', '104', '10068', 'chat_and_review', '1496914536');
INSERT INTO `basic_msg` VALUES ('20073', '104', '10049', 'chat_and_review', '1496913095');
INSERT INTO `basic_msg` VALUES ('20074', '102', '10069', 'chat_and_review', '1496913625');
INSERT INTO `basic_msg` VALUES ('20075', '104', '10025', 'chat_and_review', '1496914872');
INSERT INTO `basic_msg` VALUES ('20076', '105', '10013', 'chat_and_review', '1496913985');
INSERT INTO `basic_msg` VALUES ('20077', '105', '10056', 'chat_and_review', '1496913117');
INSERT INTO `basic_msg` VALUES ('20078', '103', '10012', 'chat_and_review', '1496914764');
INSERT INTO `basic_msg` VALUES ('20079', '103', '10096', 'chat_and_review', '1496914349');
INSERT INTO `basic_msg` VALUES ('20080', '102', '10064', 'chat_and_review', '1496913660');
INSERT INTO `basic_msg` VALUES ('20081', '101', '10073', 'chat_and_review', '1496913767');
INSERT INTO `basic_msg` VALUES ('20082', '103', '10017', 'chat_and_review', '1496913776');
INSERT INTO `basic_msg` VALUES ('20083', '102', '10056', 'chat_and_review', '1496913922');
INSERT INTO `basic_msg` VALUES ('20084', '104', '10048', 'chat_and_review', '1496913499');
INSERT INTO `basic_msg` VALUES ('20085', '105', '10097', 'chat_and_review', '1496915040');
INSERT INTO `basic_msg` VALUES ('20086', '104', '10039', 'chat_and_review', '1496913557');
INSERT INTO `basic_msg` VALUES ('20087', '103', '10035', 'chat_and_review', '1496914783');
INSERT INTO `basic_msg` VALUES ('20088', '105', '10057', 'chat_and_review', '1496913517');
INSERT INTO `basic_msg` VALUES ('20089', '103', '10081', 'chat_and_review', '1496913515');
INSERT INTO `basic_msg` VALUES ('20090', '103', '10032', 'chat_and_review', '1496914500');
INSERT INTO `basic_msg` VALUES ('20091', '104', '10055', 'chat_and_review', '1496914749');
INSERT INTO `basic_msg` VALUES ('20092', '103', '10069', 'chat_and_review', '1496914316');
INSERT INTO `basic_msg` VALUES ('20093', '102', '10083', 'chat_and_review', '1496914820');
INSERT INTO `basic_msg` VALUES ('20094', '105', '10064', 'chat_and_review', '1496914930');
INSERT INTO `basic_msg` VALUES ('20095', '101', '10047', 'chat_and_review', '1496913628');
INSERT INTO `basic_msg` VALUES ('20096', '104', '10031', 'chat_and_review', '1496913171');
INSERT INTO `basic_msg` VALUES ('20097', '105', '10097', 'chat_and_review', '1496913150');
INSERT INTO `basic_msg` VALUES ('20098', '101', '10058', 'chat_and_review', '1496913805');
INSERT INTO `basic_msg` VALUES ('20099', '103', '10083', 'chat_and_review', '1496914855');
INSERT INTO `basic_msg` VALUES ('20100', '102', '10068', 'chat_and_review', '1496914522');
INSERT INTO `basic_msg` VALUES ('20101', '105', '10020', 'chat_and_review', '1496914047');
INSERT INTO `basic_msg` VALUES ('20102', '105', '10057', 'chat_and_review', '1496913862');
INSERT INTO `basic_msg` VALUES ('20103', '103', '10030', 'chat_and_review', '1496913496');
INSERT INTO `basic_msg` VALUES ('20104', '102', '10018', 'chat_and_review', '1496914651');
INSERT INTO `basic_msg` VALUES ('20105', '102', '10009', 'chat_and_review', '1496914893');
INSERT INTO `basic_msg` VALUES ('20106', '101', '10085', 'chat_and_review', '1496914889');
INSERT INTO `basic_msg` VALUES ('20107', '103', '10031', 'chat_and_review', '1496913481');
INSERT INTO `basic_msg` VALUES ('20108', '105', '10038', 'chat_and_review', '1496914866');
INSERT INTO `basic_msg` VALUES ('20109', '104', '10035', 'chat_and_review', '1496914128');
INSERT INTO `basic_msg` VALUES ('20110', '104', '10094', 'chat_and_review', '1496913724');
INSERT INTO `basic_msg` VALUES ('20111', '103', '10003', 'chat_and_review', '1496914694');
INSERT INTO `basic_msg` VALUES ('20112', '103', '10010', 'chat_and_review', '1496914422');
INSERT INTO `basic_msg` VALUES ('20113', '105', '10078', 'chat_and_review', '1496913618');
INSERT INTO `basic_msg` VALUES ('20114', '105', '10060', 'chat_and_review', '1496914144');
INSERT INTO `basic_msg` VALUES ('20115', '102', '10097', 'chat_and_review', '1496913190');
INSERT INTO `basic_msg` VALUES ('20116', '102', '10098', 'chat_and_review', '1496913425');
INSERT INTO `basic_msg` VALUES ('20117', '102', '10028', 'chat_and_review', '1496914439');
INSERT INTO `basic_msg` VALUES ('20118', '101', '10024', 'chat_and_review', '1496914584');
INSERT INTO `basic_msg` VALUES ('20119', '103', '10096', 'chat_and_review', '1496913699');
INSERT INTO `basic_msg` VALUES ('20120', '101', '10006', 'chat_and_review', '1496913647');
INSERT INTO `basic_msg` VALUES ('20121', '102', '10051', 'chat_and_review', '1496913665');
INSERT INTO `basic_msg` VALUES ('20122', '101', '10013', 'chat_and_review', '1496913499');
INSERT INTO `basic_msg` VALUES ('20123', '103', '10032', 'chat_and_review', '1496914514');
INSERT INTO `basic_msg` VALUES ('20124', '101', '10037', 'chat_and_review', '1496913679');
INSERT INTO `basic_msg` VALUES ('20125', '105', '10095', 'chat_and_review', '1496914981');
INSERT INTO `basic_msg` VALUES ('20126', '102', '10079', 'chat_and_review', '1496913542');
INSERT INTO `basic_msg` VALUES ('20127', '104', '10009', 'chat_and_review', '1496914151');
INSERT INTO `basic_msg` VALUES ('20128', '105', '10081', 'chat_and_review', '1496913267');
INSERT INTO `basic_msg` VALUES ('20129', '102', '10083', 'chat_and_review', '1496913925');
INSERT INTO `basic_msg` VALUES ('20130', '103', '10077', 'chat_and_review', '1496913806');
INSERT INTO `basic_msg` VALUES ('20131', '103', '10093', 'chat_and_review', '1496914128');
INSERT INTO `basic_msg` VALUES ('20132', '102', '10068', 'chat_and_review', '1496913494');
INSERT INTO `basic_msg` VALUES ('20133', '104', '10035', 'chat_and_review', '1496914697');
INSERT INTO `basic_msg` VALUES ('20134', '101', '10059', 'chat_and_review', '1496914139');
INSERT INTO `basic_msg` VALUES ('20135', '101', '10002', 'chat_and_review', '1496913570');
INSERT INTO `basic_msg` VALUES ('20136', '101', '10040', 'chat_and_review', '1496913830');
INSERT INTO `basic_msg` VALUES ('20137', '105', '10070', 'chat_and_review', '1496913764');
INSERT INTO `basic_msg` VALUES ('20138', '104', '10055', 'chat_and_review', '1496913264');
INSERT INTO `basic_msg` VALUES ('20139', '103', '10061', 'chat_and_review', '1496914757');
INSERT INTO `basic_msg` VALUES ('20140', '102', '10015', 'chat_and_review', '1496913212');
INSERT INTO `basic_msg` VALUES ('20141', '102', '10082', 'chat_and_review', '1496914593');
INSERT INTO `basic_msg` VALUES ('20142', '105', '10052', 'chat_and_review', '1496913704');
INSERT INTO `basic_msg` VALUES ('20143', '101', '10071', 'chat_and_review', '1496913567');
INSERT INTO `basic_msg` VALUES ('20144', '101', '10054', 'chat_and_review', '1496914891');
INSERT INTO `basic_msg` VALUES ('20145', '102', '10049', 'chat_and_review', '1496914346');
INSERT INTO `basic_msg` VALUES ('20146', '103', '10079', 'chat_and_review', '1496913660');
INSERT INTO `basic_msg` VALUES ('20147', '104', '10056', 'chat_and_review', '1496913230');
INSERT INTO `basic_msg` VALUES ('20148', '104', '10067', 'chat_and_review', '1496914077');
INSERT INTO `basic_msg` VALUES ('20149', '101', '10002', 'chat_and_review', '1496913733');
INSERT INTO `basic_msg` VALUES ('20150', '101', '10009', 'chat_and_review', '1496914697');
INSERT INTO `basic_msg` VALUES ('20151', '104', '10088', 'chat_and_review', '1496913430');
INSERT INTO `basic_msg` VALUES ('20152', '104', '10056', 'chat_and_review', '1496913796');
INSERT INTO `basic_msg` VALUES ('20153', '102', '10080', 'chat_and_review', '1496914441');
INSERT INTO `basic_msg` VALUES ('20154', '102', '10050', 'chat_and_review', '1496913351');
INSERT INTO `basic_msg` VALUES ('20155', '103', '10035', 'chat_and_review', '1496913931');
INSERT INTO `basic_msg` VALUES ('20156', '101', '10047', 'chat_and_review', '1496914717');
INSERT INTO `basic_msg` VALUES ('20157', '103', '10051', 'chat_and_review', '1496914900');
INSERT INTO `basic_msg` VALUES ('20158', '104', '10037', 'chat_and_review', '1496913804');
INSERT INTO `basic_msg` VALUES ('20159', '104', '10045', 'chat_and_review', '1496913991');
INSERT INTO `basic_msg` VALUES ('20160', '105', '10028', 'chat_and_review', '1496914262');
INSERT INTO `basic_msg` VALUES ('20161', '102', '10045', 'chat_and_review', '1496913780');
INSERT INTO `basic_msg` VALUES ('20162', '102', '10019', 'chat_and_review', '1496914027');
INSERT INTO `basic_msg` VALUES ('20163', '101', '10002', 'chat_and_review', '1496913722');
INSERT INTO `basic_msg` VALUES ('20164', '102', '10047', 'chat_and_review', '1496914133');
INSERT INTO `basic_msg` VALUES ('20165', '102', '10010', 'chat_and_review', '1496914714');
INSERT INTO `basic_msg` VALUES ('20166', '104', '10012', 'chat_and_review', '1496913736');
INSERT INTO `basic_msg` VALUES ('20167', '104', '10029', 'chat_and_review', '1496914363');
INSERT INTO `basic_msg` VALUES ('20168', '104', '10006', 'chat_and_review', '1496913960');
INSERT INTO `basic_msg` VALUES ('20169', '103', '10065', 'chat_and_review', '1496913954');
INSERT INTO `basic_msg` VALUES ('20170', '105', '10067', 'chat_and_review', '1496914590');
INSERT INTO `basic_msg` VALUES ('20171', '102', '10088', 'chat_and_review', '1496914808');
INSERT INTO `basic_msg` VALUES ('20172', '105', '10071', 'chat_and_review', '1496914666');
INSERT INTO `basic_msg` VALUES ('20173', '103', '10018', 'chat_and_review', '1496913397');
INSERT INTO `basic_msg` VALUES ('20174', '102', '10072', 'chat_and_review', '1496913571');
INSERT INTO `basic_msg` VALUES ('20175', '103', '10005', 'chat_and_review', '1496913142');
INSERT INTO `basic_msg` VALUES ('20176', '105', '10092', 'chat_and_review', '1496913453');
INSERT INTO `basic_msg` VALUES ('20177', '104', '10000', 'chat_and_review', '1496914639');
INSERT INTO `basic_msg` VALUES ('20178', '101', '10049', 'chat_and_review', '1496913570');
INSERT INTO `basic_msg` VALUES ('20179', '101', '10010', 'chat_and_review', '1496914573');
INSERT INTO `basic_msg` VALUES ('20180', '102', '10004', 'chat_and_review', '1496913473');
INSERT INTO `basic_msg` VALUES ('20181', '103', '10031', 'chat_and_review', '1496913320');
INSERT INTO `basic_msg` VALUES ('20182', '102', '10065', 'chat_and_review', '1496914777');
INSERT INTO `basic_msg` VALUES ('20183', '104', '10039', 'chat_and_review', '1496914312');
INSERT INTO `basic_msg` VALUES ('20184', '103', '10022', 'chat_and_review', '1496914690');
INSERT INTO `basic_msg` VALUES ('20185', '102', '10016', 'chat_and_review', '1496913284');
INSERT INTO `basic_msg` VALUES ('20186', '101', '10080', 'chat_and_review', '1496914272');
INSERT INTO `basic_msg` VALUES ('20187', '103', '10056', 'chat_and_review', '1496913083');
INSERT INTO `basic_msg` VALUES ('20188', '103', '10065', 'chat_and_review', '1496914771');
INSERT INTO `basic_msg` VALUES ('20189', '103', '10039', 'chat_and_review', '1496913974');
INSERT INTO `basic_msg` VALUES ('20190', '103', '10026', 'chat_and_review', '1496914722');
INSERT INTO `basic_msg` VALUES ('20191', '105', '10018', 'chat_and_review', '1496914317');
INSERT INTO `basic_msg` VALUES ('20192', '105', '10035', 'chat_and_review', '1496913288');
INSERT INTO `basic_msg` VALUES ('20193', '105', '10014', 'chat_and_review', '1496913357');
INSERT INTO `basic_msg` VALUES ('20194', '105', '10060', 'chat_and_review', '1496913189');
INSERT INTO `basic_msg` VALUES ('20195', '102', '10069', 'chat_and_review', '1496914302');
INSERT INTO `basic_msg` VALUES ('20196', '102', '10023', 'chat_and_review', '1496913295');
INSERT INTO `basic_msg` VALUES ('20197', '101', '10015', 'chat_and_review', '1496913734');
INSERT INTO `basic_msg` VALUES ('20198', '104', '10090', 'chat_and_review', '1496914926');
INSERT INTO `basic_msg` VALUES ('20199', '103', '10046', 'chat_and_review', '1496914243');
INSERT INTO `basic_msg` VALUES ('30000', '105', '10028', 'chat_and_review', '1496914779');
INSERT INTO `basic_msg` VALUES ('30001', '102', '10014', 'chat_and_review', '1496913716');
INSERT INTO `basic_msg` VALUES ('30002', '105', '10003', 'chat_and_review', '1496913260');
INSERT INTO `basic_msg` VALUES ('30003', '105', '10053', 'chat_and_review', '1496914969');
INSERT INTO `basic_msg` VALUES ('30004', '102', '10086', 'chat_and_review', '1496914896');
INSERT INTO `basic_msg` VALUES ('30005', '105', '10033', 'chat_and_review', '1496914224');
INSERT INTO `basic_msg` VALUES ('30006', '101', '10047', 'chat_and_review', '1496914721');
INSERT INTO `basic_msg` VALUES ('30007', '103', '10049', 'chat_and_review', '1496914933');
INSERT INTO `basic_msg` VALUES ('30008', '103', '10013', 'chat_and_review', '1496914026');
INSERT INTO `basic_msg` VALUES ('30009', '104', '10067', 'chat_and_review', '1496914878');
INSERT INTO `basic_msg` VALUES ('30010', '102', '10002', 'chat_and_review', '1496915026');
INSERT INTO `basic_msg` VALUES ('30011', '102', '10037', 'chat_and_review', '1496913063');
INSERT INTO `basic_msg` VALUES ('30012', '105', '10017', 'chat_and_review', '1496913137');
INSERT INTO `basic_msg` VALUES ('30013', '102', '10040', 'chat_and_review', '1496914352');
INSERT INTO `basic_msg` VALUES ('30014', '103', '10098', 'chat_and_review', '1496914668');
INSERT INTO `basic_msg` VALUES ('30015', '101', '10077', 'chat_and_review', '1496913217');
INSERT INTO `basic_msg` VALUES ('30016', '105', '10010', 'chat_and_review', '1496913300');
INSERT INTO `basic_msg` VALUES ('30017', '103', '10057', 'chat_and_review', '1496914181');
INSERT INTO `basic_msg` VALUES ('30018', '101', '10055', 'chat_and_review', '1496913274');
INSERT INTO `basic_msg` VALUES ('30019', '101', '10024', 'chat_and_review', '1496913764');
INSERT INTO `basic_msg` VALUES ('30020', '103', '10033', 'chat_and_review', '1496914868');
INSERT INTO `basic_msg` VALUES ('30021', '101', '10033', 'chat_and_review', '1496914503');
INSERT INTO `basic_msg` VALUES ('30022', '102', '10003', 'chat_and_review', '1496913263');
INSERT INTO `basic_msg` VALUES ('30023', '103', '10045', 'chat_and_review', '1496913862');
INSERT INTO `basic_msg` VALUES ('30024', '101', '10009', 'chat_and_review', '1496914263');
INSERT INTO `basic_msg` VALUES ('30025', '101', '10091', 'chat_and_review', '1496914433');
INSERT INTO `basic_msg` VALUES ('30026', '101', '10038', 'chat_and_review', '1496913985');
INSERT INTO `basic_msg` VALUES ('30027', '102', '10052', 'chat_and_review', '1496913890');
INSERT INTO `basic_msg` VALUES ('30028', '103', '10044', 'chat_and_review', '1496914885');
INSERT INTO `basic_msg` VALUES ('30029', '104', '10043', 'chat_and_review', '1496914286');
INSERT INTO `basic_msg` VALUES ('30030', '101', '10020', 'chat_and_review', '1496913444');
INSERT INTO `basic_msg` VALUES ('30031', '102', '10052', 'chat_and_review', '1496913635');
INSERT INTO `basic_msg` VALUES ('30032', '105', '10072', 'chat_and_review', '1496913110');
INSERT INTO `basic_msg` VALUES ('30033', '105', '10073', 'chat_and_review', '1496913729');
INSERT INTO `basic_msg` VALUES ('30034', '104', '10013', 'chat_and_review', '1496913591');
INSERT INTO `basic_msg` VALUES ('30035', '101', '10067', 'chat_and_review', '1496914742');
INSERT INTO `basic_msg` VALUES ('30036', '105', '10058', 'chat_and_review', '1496914012');
INSERT INTO `basic_msg` VALUES ('30037', '105', '10065', 'chat_and_review', '1496914226');
INSERT INTO `basic_msg` VALUES ('30038', '105', '10012', 'chat_and_review', '1496913804');
INSERT INTO `basic_msg` VALUES ('30039', '102', '10093', 'chat_and_review', '1496913485');
INSERT INTO `basic_msg` VALUES ('30040', '103', '10048', 'chat_and_review', '1496913927');
INSERT INTO `basic_msg` VALUES ('30041', '105', '10076', 'chat_and_review', '1496913829');
INSERT INTO `basic_msg` VALUES ('30042', '101', '10072', 'chat_and_review', '1496913110');
INSERT INTO `basic_msg` VALUES ('30043', '101', '10013', 'chat_and_review', '1496913433');
INSERT INTO `basic_msg` VALUES ('30044', '104', '10058', 'chat_and_review', '1496913459');
INSERT INTO `basic_msg` VALUES ('30045', '105', '10062', 'chat_and_review', '1496914086');
INSERT INTO `basic_msg` VALUES ('30046', '101', '10003', 'chat_and_review', '1496914914');
INSERT INTO `basic_msg` VALUES ('30047', '103', '10025', 'chat_and_review', '1496913076');
INSERT INTO `basic_msg` VALUES ('30048', '102', '10082', 'chat_and_review', '1496913757');
INSERT INTO `basic_msg` VALUES ('30049', '101', '10096', 'chat_and_review', '1496914083');
INSERT INTO `basic_msg` VALUES ('30050', '101', '10066', 'chat_and_review', '1496914960');
INSERT INTO `basic_msg` VALUES ('30051', '104', '10094', 'chat_and_review', '1496913563');
INSERT INTO `basic_msg` VALUES ('30052', '102', '10004', 'chat_and_review', '1496913730');
INSERT INTO `basic_msg` VALUES ('30053', '104', '10081', 'chat_and_review', '1496914903');
INSERT INTO `basic_msg` VALUES ('30054', '101', '10089', 'chat_and_review', '1496913953');
INSERT INTO `basic_msg` VALUES ('30055', '101', '10075', 'chat_and_review', '1496913204');
INSERT INTO `basic_msg` VALUES ('30056', '105', '10038', 'chat_and_review', '1496913936');
INSERT INTO `basic_msg` VALUES ('30057', '101', '10048', 'chat_and_review', '1496913183');
INSERT INTO `basic_msg` VALUES ('30058', '105', '10069', 'chat_and_review', '1496913181');
INSERT INTO `basic_msg` VALUES ('30059', '104', '10087', 'chat_and_review', '1496913471');
INSERT INTO `basic_msg` VALUES ('30060', '104', '10098', 'chat_and_review', '1496914545');
INSERT INTO `basic_msg` VALUES ('30061', '105', '10018', 'chat_and_review', '1496913167');
INSERT INTO `basic_msg` VALUES ('30062', '103', '10053', 'chat_and_review', '1496914258');
INSERT INTO `basic_msg` VALUES ('30063', '101', '10047', 'chat_and_review', '1496913477');
INSERT INTO `basic_msg` VALUES ('30064', '101', '10046', 'chat_and_review', '1496914496');
INSERT INTO `basic_msg` VALUES ('30065', '104', '10033', 'chat_and_review', '1496913397');
INSERT INTO `basic_msg` VALUES ('30066', '105', '10028', 'chat_and_review', '1496914784');
INSERT INTO `basic_msg` VALUES ('30067', '105', '10049', 'chat_and_review', '1496914664');
INSERT INTO `basic_msg` VALUES ('30068', '103', '10054', 'chat_and_review', '1496913847');
INSERT INTO `basic_msg` VALUES ('30069', '105', '10008', 'chat_and_review', '1496914722');
INSERT INTO `basic_msg` VALUES ('30070', '105', '10037', 'chat_and_review', '1496913088');
INSERT INTO `basic_msg` VALUES ('30071', '101', '10004', 'chat_and_review', '1496914565');
INSERT INTO `basic_msg` VALUES ('30072', '105', '10035', 'chat_and_review', '1496914550');
INSERT INTO `basic_msg` VALUES ('30073', '103', '10040', 'chat_and_review', '1496913404');
INSERT INTO `basic_msg` VALUES ('30074', '103', '10070', 'chat_and_review', '1496914399');
INSERT INTO `basic_msg` VALUES ('30075', '102', '10090', 'chat_and_review', '1496913254');
INSERT INTO `basic_msg` VALUES ('30076', '103', '10078', 'chat_and_review', '1496915041');
INSERT INTO `basic_msg` VALUES ('30077', '102', '10087', 'chat_and_review', '1496914109');
INSERT INTO `basic_msg` VALUES ('30078', '104', '10001', 'chat_and_review', '1496913607');
INSERT INTO `basic_msg` VALUES ('30079', '101', '10069', 'chat_and_review', '1496913072');
INSERT INTO `basic_msg` VALUES ('30080', '102', '10093', 'chat_and_review', '1496913656');
INSERT INTO `basic_msg` VALUES ('30081', '102', '10056', 'chat_and_review', '1496914456');
INSERT INTO `basic_msg` VALUES ('30082', '102', '10082', 'chat_and_review', '1496913516');
INSERT INTO `basic_msg` VALUES ('30083', '103', '10013', 'chat_and_review', '1496913094');
INSERT INTO `basic_msg` VALUES ('30084', '105', '10075', 'chat_and_review', '1496913454');
INSERT INTO `basic_msg` VALUES ('30085', '103', '10067', 'chat_and_review', '1496914514');
INSERT INTO `basic_msg` VALUES ('30086', '103', '10003', 'chat_and_review', '1496914152');
INSERT INTO `basic_msg` VALUES ('30087', '101', '10057', 'chat_and_review', '1496913337');
INSERT INTO `basic_msg` VALUES ('30088', '104', '10007', 'chat_and_review', '1496913920');
INSERT INTO `basic_msg` VALUES ('30089', '105', '10066', 'chat_and_review', '1496914113');
INSERT INTO `basic_msg` VALUES ('30090', '104', '10098', 'chat_and_review', '1496914332');
INSERT INTO `basic_msg` VALUES ('30091', '101', '10029', 'chat_and_review', '1496914147');
INSERT INTO `basic_msg` VALUES ('30092', '104', '10073', 'chat_and_review', '1496914615');
INSERT INTO `basic_msg` VALUES ('30093', '102', '10091', 'chat_and_review', '1496914934');
INSERT INTO `basic_msg` VALUES ('30094', '105', '10059', 'chat_and_review', '1496913328');
INSERT INTO `basic_msg` VALUES ('30095', '101', '10020', 'chat_and_review', '1496913177');
INSERT INTO `basic_msg` VALUES ('30096', '103', '10049', 'chat_and_review', '1496914988');
INSERT INTO `basic_msg` VALUES ('30097', '104', '10018', 'chat_and_review', '1496914713');
INSERT INTO `basic_msg` VALUES ('30098', '103', '10092', 'chat_and_review', '1496914718');
INSERT INTO `basic_msg` VALUES ('30099', '105', '10014', 'chat_and_review', '1496914735');
INSERT INTO `basic_msg` VALUES ('30100', '105', '10086', 'chat_and_review', '1496914837');
INSERT INTO `basic_msg` VALUES ('30101', '102', '10050', 'chat_and_review', '1496914779');
INSERT INTO `basic_msg` VALUES ('30102', '102', '10078', 'chat_and_review', '1496913984');
INSERT INTO `basic_msg` VALUES ('30103', '104', '10093', 'chat_and_review', '1496913193');
INSERT INTO `basic_msg` VALUES ('30104', '102', '10082', 'chat_and_review', '1496913667');
INSERT INTO `basic_msg` VALUES ('30105', '105', '10039', 'chat_and_review', '1496913250');
INSERT INTO `basic_msg` VALUES ('30106', '102', '10026', 'chat_and_review', '1496913998');
INSERT INTO `basic_msg` VALUES ('30107', '102', '10065', 'chat_and_review', '1496914657');
INSERT INTO `basic_msg` VALUES ('30108', '104', '10050', 'chat_and_review', '1496914642');
INSERT INTO `basic_msg` VALUES ('30109', '104', '10038', 'chat_and_review', '1496913898');
INSERT INTO `basic_msg` VALUES ('30110', '104', '10061', 'chat_and_review', '1496914395');
INSERT INTO `basic_msg` VALUES ('30111', '102', '10092', 'chat_and_review', '1496913124');
INSERT INTO `basic_msg` VALUES ('30112', '105', '10012', 'chat_and_review', '1496913985');
INSERT INTO `basic_msg` VALUES ('30113', '103', '10055', 'chat_and_review', '1496914432');
INSERT INTO `basic_msg` VALUES ('30114', '104', '10060', 'chat_and_review', '1496914331');
INSERT INTO `basic_msg` VALUES ('30115', '101', '10087', 'chat_and_review', '1496914742');
INSERT INTO `basic_msg` VALUES ('30116', '101', '10043', 'chat_and_review', '1496913653');
INSERT INTO `basic_msg` VALUES ('30117', '104', '10071', 'chat_and_review', '1496914866');
INSERT INTO `basic_msg` VALUES ('30118', '104', '10025', 'chat_and_review', '1496914488');
INSERT INTO `basic_msg` VALUES ('30119', '102', '10032', 'chat_and_review', '1496913921');
INSERT INTO `basic_msg` VALUES ('30120', '103', '10002', 'chat_and_review', '1496913830');
INSERT INTO `basic_msg` VALUES ('30121', '101', '10045', 'chat_and_review', '1496914469');
INSERT INTO `basic_msg` VALUES ('30122', '105', '10044', 'chat_and_review', '1496914992');
INSERT INTO `basic_msg` VALUES ('30123', '103', '10098', 'chat_and_review', '1496913573');
INSERT INTO `basic_msg` VALUES ('30124', '105', '10039', 'chat_and_review', '1496913631');
INSERT INTO `basic_msg` VALUES ('30125', '105', '10030', 'chat_and_review', '1496913365');
INSERT INTO `basic_msg` VALUES ('30126', '101', '10094', 'chat_and_review', '1496913130');
INSERT INTO `basic_msg` VALUES ('30127', '104', '10082', 'chat_and_review', '1496913841');
INSERT INTO `basic_msg` VALUES ('30128', '101', '10034', 'chat_and_review', '1496913263');
INSERT INTO `basic_msg` VALUES ('30129', '105', '10024', 'chat_and_review', '1496914642');
INSERT INTO `basic_msg` VALUES ('30130', '101', '10045', 'chat_and_review', '1496914174');
INSERT INTO `basic_msg` VALUES ('30131', '101', '10014', 'chat_and_review', '1496913276');
INSERT INTO `basic_msg` VALUES ('30132', '104', '10041', 'chat_and_review', '1496914698');
INSERT INTO `basic_msg` VALUES ('30133', '105', '10048', 'chat_and_review', '1496914698');
INSERT INTO `basic_msg` VALUES ('30134', '102', '10030', 'chat_and_review', '1496914742');
INSERT INTO `basic_msg` VALUES ('30135', '103', '10004', 'chat_and_review', '1496915023');
INSERT INTO `basic_msg` VALUES ('30136', '104', '10083', 'chat_and_review', '1496914165');
INSERT INTO `basic_msg` VALUES ('30137', '104', '10058', 'chat_and_review', '1496914548');
INSERT INTO `basic_msg` VALUES ('30138', '102', '10059', 'chat_and_review', '1496913211');
INSERT INTO `basic_msg` VALUES ('30139', '101', '10021', 'chat_and_review', '1496913561');
INSERT INTO `basic_msg` VALUES ('30140', '102', '10032', 'chat_and_review', '1496914149');
INSERT INTO `basic_msg` VALUES ('30141', '102', '10001', 'chat_and_review', '1496913791');
INSERT INTO `basic_msg` VALUES ('30142', '101', '10083', 'chat_and_review', '1496913358');
INSERT INTO `basic_msg` VALUES ('30143', '103', '10076', 'chat_and_review', '1496913948');
INSERT INTO `basic_msg` VALUES ('30144', '105', '10016', 'chat_and_review', '1496913652');
INSERT INTO `basic_msg` VALUES ('30145', '101', '10064', 'chat_and_review', '1496914985');
INSERT INTO `basic_msg` VALUES ('30146', '104', '10056', 'chat_and_review', '1496913486');
INSERT INTO `basic_msg` VALUES ('30147', '105', '10004', 'chat_and_review', '1496914790');
INSERT INTO `basic_msg` VALUES ('30148', '104', '10061', 'chat_and_review', '1496914964');
INSERT INTO `basic_msg` VALUES ('30149', '101', '10024', 'chat_and_review', '1496915052');
INSERT INTO `basic_msg` VALUES ('30150', '102', '10041', 'chat_and_review', '1496914167');
INSERT INTO `basic_msg` VALUES ('30151', '101', '10099', 'chat_and_review', '1496913665');
INSERT INTO `basic_msg` VALUES ('30152', '102', '10084', 'chat_and_review', '1496914965');
INSERT INTO `basic_msg` VALUES ('30153', '104', '10071', 'chat_and_review', '1496914412');
INSERT INTO `basic_msg` VALUES ('30154', '105', '10035', 'chat_and_review', '1496914078');
INSERT INTO `basic_msg` VALUES ('30155', '104', '10075', 'chat_and_review', '1496914012');
INSERT INTO `basic_msg` VALUES ('30156', '101', '10035', 'chat_and_review', '1496913528');
INSERT INTO `basic_msg` VALUES ('30157', '101', '10033', 'chat_and_review', '1496914255');
INSERT INTO `basic_msg` VALUES ('30158', '101', '10088', 'chat_and_review', '1496913416');
INSERT INTO `basic_msg` VALUES ('30159', '101', '10095', 'chat_and_review', '1496913510');
INSERT INTO `basic_msg` VALUES ('30160', '104', '10003', 'chat_and_review', '1496913824');
INSERT INTO `basic_msg` VALUES ('30161', '104', '10092', 'chat_and_review', '1496914126');
INSERT INTO `basic_msg` VALUES ('30162', '102', '10002', 'chat_and_review', '1496913879');
INSERT INTO `basic_msg` VALUES ('30163', '105', '10002', 'chat_and_review', '1496913326');
INSERT INTO `basic_msg` VALUES ('30164', '103', '10082', 'chat_and_review', '1496913718');
INSERT INTO `basic_msg` VALUES ('30165', '102', '10012', 'chat_and_review', '1496914060');
INSERT INTO `basic_msg` VALUES ('30166', '101', '10026', 'chat_and_review', '1496913643');
INSERT INTO `basic_msg` VALUES ('30167', '103', '10041', 'chat_and_review', '1496914846');
INSERT INTO `basic_msg` VALUES ('30168', '102', '10000', 'chat_and_review', '1496914061');
INSERT INTO `basic_msg` VALUES ('30169', '102', '10097', 'chat_and_review', '1496913903');
INSERT INTO `basic_msg` VALUES ('30170', '103', '10085', 'chat_and_review', '1496913559');
INSERT INTO `basic_msg` VALUES ('30171', '105', '10013', 'chat_and_review', '1496913663');
INSERT INTO `basic_msg` VALUES ('30172', '103', '10052', 'chat_and_review', '1496914170');
INSERT INTO `basic_msg` VALUES ('30173', '105', '10049', 'chat_and_review', '1496913624');
INSERT INTO `basic_msg` VALUES ('30174', '101', '10026', 'chat_and_review', '1496913243');
INSERT INTO `basic_msg` VALUES ('30175', '104', '10064', 'chat_and_review', '1496914362');
INSERT INTO `basic_msg` VALUES ('30176', '103', '10000', 'chat_and_review', '1496914495');
INSERT INTO `basic_msg` VALUES ('30177', '105', '10061', 'chat_and_review', '1496914572');
INSERT INTO `basic_msg` VALUES ('30178', '102', '10005', 'chat_and_review', '1496914262');
INSERT INTO `basic_msg` VALUES ('30179', '104', '10038', 'chat_and_review', '1496913774');
INSERT INTO `basic_msg` VALUES ('30180', '104', '10032', 'chat_and_review', '1496913107');
INSERT INTO `basic_msg` VALUES ('30181', '102', '10044', 'chat_and_review', '1496913460');
INSERT INTO `basic_msg` VALUES ('30182', '105', '10064', 'chat_and_review', '1496913814');
INSERT INTO `basic_msg` VALUES ('30183', '105', '10054', 'chat_and_review', '1496913365');
INSERT INTO `basic_msg` VALUES ('30184', '104', '10014', 'chat_and_review', '1496914411');
INSERT INTO `basic_msg` VALUES ('30185', '101', '10043', 'chat_and_review', '1496915056');
INSERT INTO `basic_msg` VALUES ('30186', '101', '10055', 'chat_and_review', '1496914679');
INSERT INTO `basic_msg` VALUES ('30187', '104', '10022', 'chat_and_review', '1496913451');
INSERT INTO `basic_msg` VALUES ('30188', '103', '10053', 'chat_and_review', '1496914828');
INSERT INTO `basic_msg` VALUES ('30189', '104', '10064', 'chat_and_review', '1496914137');
INSERT INTO `basic_msg` VALUES ('30190', '101', '10021', 'chat_and_review', '1496913164');
INSERT INTO `basic_msg` VALUES ('30191', '103', '10057', 'chat_and_review', '1496913635');
INSERT INTO `basic_msg` VALUES ('30192', '104', '10037', 'chat_and_review', '1496913784');
INSERT INTO `basic_msg` VALUES ('30193', '105', '10057', 'chat_and_review', '1496914036');
INSERT INTO `basic_msg` VALUES ('30194', '104', '10058', 'chat_and_review', '1496913644');
INSERT INTO `basic_msg` VALUES ('30195', '101', '10009', 'chat_and_review', '1496914998');
INSERT INTO `basic_msg` VALUES ('30196', '103', '10093', 'chat_and_review', '1496914530');
INSERT INTO `basic_msg` VALUES ('30197', '104', '10090', 'chat_and_review', '1496913909');
INSERT INTO `basic_msg` VALUES ('30198', '101', '10061', 'chat_and_review', '1496913730');
INSERT INTO `basic_msg` VALUES ('30199', '105', '10053', 'chat_and_review', '1496914980');

-- ----------------------------
-- Table structure for basic_room
-- ----------------------------
DROP TABLE IF EXISTS `basic_room`;
CREATE TABLE `basic_room` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_title` varchar(32) NOT NULL,
  `chat_topic` varchar(32) NOT NULL,
  `dms_sub_key` varchar(64) NOT NULL,
  `dms_pub_key` varchar(64) NOT NULL,
  `dms_s_key` varchar(64) NOT NULL,
  `aodian_uin` int(11) NOT NULL,
  `lss_app` varchar(32) NOT NULL,
  `stream` varchar(32) NOT NULL,
  `room_status` smallint(6) NOT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of basic_room
-- ----------------------------
INSERT INTO `basic_room` VALUES ('101', 'live test 101', 'room_101', 'sub_eae37e48dab5f305516d07788eaaea60', 'pub_5bfb7a0ced7adb2ce454575747762679', 's_ceb80d29276f78653df081e5a9f0ac76', '13830', 'dyy_1736_133', 'a0c3d2dd3b4688f31da13991477980d9', '1');
INSERT INTO `basic_room` VALUES ('102', 'live test 102', 'room_102', 'sub_eae37e48dab5f305516d07788eaaea60', 'pub_5bfb7a0ced7adb2ce454575747762679', 's_ceb80d29276f78653df081e5a9f0ac76', '13830', 'dyy_1736_133', 'a0c3d2dd3b4688f31da13991477980d9', '1');
INSERT INTO `basic_room` VALUES ('103', 'live test 103', 'room_103', 'sub_eae37e48dab5f305516d07788eaaea60', 'pub_5bfb7a0ced7adb2ce454575747762679', 's_ceb80d29276f78653df081e5a9f0ac76', '13830', 'dyy_1736_133', 'a0c3d2dd3b4688f31da13991477980d9', '1');
INSERT INTO `basic_room` VALUES ('104', 'live test 104', 'room_104', 'sub_eae37e48dab5f305516d07788eaaea60', 'pub_5bfb7a0ced7adb2ce454575747762679', 's_ceb80d29276f78653df081e5a9f0ac76', '13830', 'dyy_1736_133', 'a0c3d2dd3b4688f31da13991477980d9', '1');
INSERT INTO `basic_room` VALUES ('105', 'live test 105', 'room_105', 'sub_eae37e48dab5f305516d07788eaaea60', 'pub_5bfb7a0ced7adb2ce454575747762679', 's_ceb80d29276f78653df081e5a9f0ac76', '13830', 'dyy_1736_133', 'a0c3d2dd3b4688f31da13991477980d9', '1');

-- ----------------------------
-- Table structure for basic_user
-- ----------------------------
DROP TABLE IF EXISTS `basic_user`;
CREATE TABLE `basic_user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `nick` varchar(16) NOT NULL,
  `avatar` varchar(128) NOT NULL,
  `user_type` varchar(16) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10100 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of basic_user
-- ----------------------------
INSERT INTO `basic_user` VALUES ('10000', 'Nick10000', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10001', 'Nick10001', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10002', 'Nick10002', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10003', 'Nick10003', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10004', 'Nick10004', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10005', 'Nick10005', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10006', 'Nick10006', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10007', 'Nick10007', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10008', 'Nick10008', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10009', 'Nick10009', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10010', 'Nick10010', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10011', 'Nick10011', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10012', 'Nick10012', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10013', 'Nick10013', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10014', 'Nick10014', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10015', 'Nick10015', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10016', 'Nick10016', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10017', 'Nick10017', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10018', 'Nick10018', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10019', 'Nick10019', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10020', 'Nick10020', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10021', 'Nick10021', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10022', 'Nick10022', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10023', 'Nick10023', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10024', 'Nick10024', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10025', 'Nick10025', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10026', 'Nick10026', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10027', 'Nick10027', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10028', 'Nick10028', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10029', 'Nick10029', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10030', 'Nick10030', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10031', 'Nick10031', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10032', 'Nick10032', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10033', 'Nick10033', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10034', 'Nick10034', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10035', 'Nick10035', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10036', 'Nick10036', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10037', 'Nick10037', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10038', 'Nick10038', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10039', 'Nick10039', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10040', 'Nick10040', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10041', 'Nick10041', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10042', 'Nick10042', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10043', 'Nick10043', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10044', 'Nick10044', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10045', 'Nick10045', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10046', 'Nick10046', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10047', 'Nick10047', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10048', 'Nick10048', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10049', 'Nick10049', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10050', 'Nick10050', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10051', 'Nick10051', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10052', 'Nick10052', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10053', 'Nick10053', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10054', 'Nick10054', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10055', 'Nick10055', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10056', 'Nick10056', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10057', 'Nick10057', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10058', 'Nick10058', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10059', 'Nick10059', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10060', 'Nick10060', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10061', 'Nick10061', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10062', 'Nick10062', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10063', 'Nick10063', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10064', 'Nick10064', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10065', 'Nick10065', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10066', 'Nick10066', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10067', 'Nick10067', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10068', 'Nick10068', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10069', 'Nick10069', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10070', 'Nick10070', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10071', 'Nick10071', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10072', 'Nick10072', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10073', 'Nick10073', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10074', 'Nick10074', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10075', 'Nick10075', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10076', 'Nick10076', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10077', 'Nick10077', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10078', 'Nick10078', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10079', 'Nick10079', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10080', 'Nick10080', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10081', 'Nick10081', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10082', 'Nick10082', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10083', 'Nick10083', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10084', 'Nick10084', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10085', 'Nick10085', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10086', 'Nick10086', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10087', 'Nick10087', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10088', 'Nick10088', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10089', 'Nick10089', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10090', 'Nick10090', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10091', 'Nick10091', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10092', 'Nick10092', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10093', 'Nick10093', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10094', 'Nick10094', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10095', 'Nick10095', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10096', 'Nick10096', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10097', 'Nick10097', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10098', 'Nick10098', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');
INSERT INTO `basic_user` VALUES ('10099', 'Nick10099', 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png', 'authorized');

-- ----------------------------
-- Table structure for chat_config
-- ----------------------------
DROP TABLE IF EXISTS `chat_config`;
CREATE TABLE `chat_config` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `review_type` varchar(16) NOT NULL,
  `sysmsg_type` varchar(16) NOT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of chat_config
-- ----------------------------
INSERT INTO `chat_config` VALUES ('101', 'direct_pub', 'show_all');
INSERT INTO `chat_config` VALUES ('102', 'direct_pub', 'show_all');
INSERT INTO `chat_config` VALUES ('103', 'direct_pub', 'show_all');
INSERT INTO `chat_config` VALUES ('104', 'direct_pub', 'show_all');
INSERT INTO `chat_config` VALUES ('105', 'direct_pub', 'show_all');

-- ----------------------------
-- Table structure for content_tab_config
-- ----------------------------
DROP TABLE IF EXISTS `content_tab_config`;
CREATE TABLE `content_tab_config` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `content_tab_id` int(11) NOT NULL,
  `active` varchar(16) NOT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of content_tab_config
-- ----------------------------

-- ----------------------------
-- Table structure for migrate_version
-- ----------------------------
DROP TABLE IF EXISTS `migrate_version`;
CREATE TABLE `migrate_version` (
  `repository_id` varchar(250) NOT NULL,
  `repository_path` text,
  `version` int(11) DEFAULT NULL,
  PRIMARY KEY (`repository_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of migrate_version
-- ----------------------------
INSERT INTO `migrate_version` VALUES ('database repository', 'E:\\xampp\\gaea-live\\db-migrate\\db_repository', '1');

-- ----------------------------
-- Table structure for msg_chat_and_review
-- ----------------------------
DROP TABLE IF EXISTS `msg_chat_and_review`;
CREATE TABLE `msg_chat_and_review` (
  `msg_id` int(11) NOT NULL AUTO_INCREMENT,
  `msg_type` varchar(16) NOT NULL,
  `target_user_id` varchar(16) NOT NULL,
  `target_msg_id` varchar(16) NOT NULL,
  `content_text` varchar(512) NOT NULL,
  `msg_status` varchar(16) NOT NULL,
  `operator_id` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`msg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21000 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of msg_chat_and_review
-- ----------------------------
INSERT INTO `msg_chat_and_review` VALUES ('20000', 'chat_and_review', '', '', 'CCC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20001', 'chat_and_review', '', '', 'BBB', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20002', 'chat_and_review', '', '', 'CCC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20003', 'chat_and_review', '', '', 'BBB', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20004', 'chat_and_review', '', '', 'AAA', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20005', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20006', 'chat_and_review', '', '', 'BBB', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20007', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20008', 'chat_and_review', '', '', 'ABC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20009', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20010', 'chat_and_review', '', '', 'BBB', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20011', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20012', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20013', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20014', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20015', 'chat_and_review', '', '', 'QWE', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20016', 'chat_and_review', '', '', 'BBB', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20017', 'chat_and_review', '', '', 'QWE', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20018', 'chat_and_review', '', '', 'QWE', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20019', 'chat_and_review', '', '', 'BBB', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20020', 'chat_and_review', '', '', 'ASD', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20021', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20022', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20023', 'chat_and_review', '', '', 'AAA', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20024', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20025', 'chat_and_review', '', '', 'QWE', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20026', 'chat_and_review', '', '', 'DEF', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20027', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20028', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20029', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20030', 'chat_and_review', '', '', 'QWE', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20031', 'chat_and_review', '', '', 'BBB', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20032', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20033', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20034', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20035', 'chat_and_review', '', '', 'BBB', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20036', 'chat_and_review', '', '', 'CCC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20037', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20038', 'chat_and_review', '', '', 'BBB', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20039', 'chat_and_review', '', '', 'QWE', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20040', 'chat_and_review', '', '', 'QWE', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20041', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20042', 'chat_and_review', '', '', 'AAA', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20043', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20044', 'chat_and_review', '', '', 'ABC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20045', 'chat_and_review', '', '', 'DEF', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20046', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20047', 'chat_and_review', '', '', 'ABC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20048', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20049', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20050', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20051', 'chat_and_review', '', '', 'ASD', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20052', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20053', 'chat_and_review', '', '', 'BBB', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20054', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20055', 'chat_and_review', '', '', 'BBB', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20056', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20057', 'chat_and_review', '', '', 'ABC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20058', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20059', 'chat_and_review', '', '', 'DEF', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20060', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20061', 'chat_and_review', '', '', 'QWE', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20062', 'chat_and_review', '', '', 'ASD', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20063', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20064', 'chat_and_review', '', '', 'AAA', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20065', 'chat_and_review', '', '', 'BBB', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20066', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20067', 'chat_and_review', '', '', 'QWE', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20068', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20069', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20070', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20071', 'chat_and_review', '', '', 'ASD', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20072', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20073', 'chat_and_review', '', '', 'DEF', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20074', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20075', 'chat_and_review', '', '', 'ASD', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20076', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20077', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20078', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20079', 'chat_and_review', '', '', 'BBB', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20080', 'chat_and_review', '', '', 'AAA', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20081', 'chat_and_review', '', '', 'ABC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20082', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20083', 'chat_and_review', '', '', 'QWE', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20084', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20085', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20086', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20087', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20088', 'chat_and_review', '', '', 'AAA', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20089', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20090', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20091', 'chat_and_review', '', '', 'QWE', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20092', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20093', 'chat_and_review', '', '', 'AAA', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20094', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20095', 'chat_and_review', '', '', 'DEF', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20096', 'chat_and_review', '', '', 'AAA', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20097', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20098', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20099', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20100', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20101', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20102', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20103', 'chat_and_review', '', '', 'CCC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20104', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20105', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20106', 'chat_and_review', '', '', 'AAA', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20107', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20108', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20109', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20110', 'chat_and_review', '', '', 'AAA', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20111', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20112', 'chat_and_review', '', '', 'CCC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20113', 'chat_and_review', '', '', 'AAA', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20114', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20115', 'chat_and_review', '', '', 'ASD', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20116', 'chat_and_review', '', '', 'AAA', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20117', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20118', 'chat_and_review', '', '', 'QWE', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20119', 'chat_and_review', '', '', 'ABC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20120', 'chat_and_review', '', '', 'AAA', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20121', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20122', 'chat_and_review', '', '', 'ASD', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20123', 'chat_and_review', '', '', 'CCC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20124', 'chat_and_review', '', '', 'AAA', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20125', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20126', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20127', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20128', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20129', 'chat_and_review', '', '', 'AAA', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20130', 'chat_and_review', '', '', 'BBB', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20131', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20132', 'chat_and_review', '', '', 'ABC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20133', 'chat_and_review', '', '', 'ASD', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20134', 'chat_and_review', '', '', 'CCC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20135', 'chat_and_review', '', '', 'CCC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20136', 'chat_and_review', '', '', 'DEF', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20137', 'chat_and_review', '', '', 'CCC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20138', 'chat_and_review', '', '', 'ASD', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20139', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20140', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20141', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20142', 'chat_and_review', '', '', 'ABC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20143', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20144', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20145', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20146', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20147', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20148', 'chat_and_review', '', '', 'CCC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20149', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20150', 'chat_and_review', '', '', 'QWE', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20151', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20152', 'chat_and_review', '', '', 'ASD', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20153', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20154', 'chat_and_review', '', '', 'ABC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20155', 'chat_and_review', '', '', 'DEF', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20156', 'chat_and_review', '', '', 'DEF', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20157', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20158', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20159', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20160', 'chat_and_review', '', '', 'ASD', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20161', 'chat_and_review', '', '', 'ASD', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20162', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20163', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20164', 'chat_and_review', '', '', 'AAA', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20165', 'chat_and_review', '', '', 'AAA', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20166', 'chat_and_review', '', '', 'ABC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20167', 'chat_and_review', '', '', 'ASD', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20168', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20169', 'chat_and_review', '', '', 'DEF', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20170', 'chat_and_review', '', '', 'ABC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20171', 'chat_and_review', '', '', 'CCC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20172', 'chat_and_review', '', '', 'QWE', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20173', 'chat_and_review', '', '', 'CCC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20174', 'chat_and_review', '', '', 'DEF', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20175', 'chat_and_review', '', '', 'AAA', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20176', 'chat_and_review', '', '', 'ABC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20177', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20178', 'chat_and_review', '', '', 'CCC', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20179', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20180', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20181', 'chat_and_review', '', '', 'AAA', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20182', 'chat_and_review', '', '', 'QWE', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20183', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20184', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20185', 'chat_and_review', '', '', 'ASD', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20186', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20187', 'chat_and_review', '', '', 'DEF', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20188', 'chat_and_review', '', '', 'BBB', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20189', 'chat_and_review', '', '', 'ASD', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20190', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20191', 'chat_and_review', '', '', 'CCC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20192', 'chat_and_review', '', '', 'ABC', 'publish_chat', '');
INSERT INTO `msg_chat_and_review` VALUES ('20193', 'chat_and_review', '', '', 'DEF', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20194', 'chat_and_review', '', '', 'CCC', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20195', 'chat_and_review', '', '', 'ABC', 'review_pub', '');
INSERT INTO `msg_chat_and_review` VALUES ('20196', 'chat_and_review', '', '', 'BBB', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20197', 'chat_and_review', '', '', 'ASD', 'review_del', '');
INSERT INTO `msg_chat_and_review` VALUES ('20198', 'chat_and_review', '', '', 'QWE', 'review_add', '');
INSERT INTO `msg_chat_and_review` VALUES ('20199', 'chat_and_review', '', '', 'CCC', 'review_pub', '');

-- ----------------------------
-- Table structure for msg_donate_and_gift
-- ----------------------------
DROP TABLE IF EXISTS `msg_donate_and_gift`;
CREATE TABLE `msg_donate_and_gift` (
  `msg_id` int(11) NOT NULL AUTO_INCREMENT,
  `msg_type` varchar(16) NOT NULL,
  `target_user_id` varchar(16) NOT NULL,
  `trade_type` varchar(16) NOT NULL,
  `trade_num` float NOT NULL,
  `content_text` varchar(512) NOT NULL,
  PRIMARY KEY (`msg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31000 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of msg_donate_and_gift
-- ----------------------------
INSERT INTO `msg_donate_and_gift` VALUES ('30000', 'donate_and_gift', '', 'gift_666', '687', 'gift_666 (x 687) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30001', 'donate_and_gift', '', 'gift_car', '332', 'gift_car (x 332) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30002', 'donate_and_gift', '', 'USD', '242.8', 'USD (x 242.8) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30003', 'donate_and_gift', '', 'gift_666', '974', 'gift_666 (x 974) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30004', 'donate_and_gift', '', 'gift_plane', '11', 'gift_plane (x 11) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30005', 'donate_and_gift', '', 'RMB', '312.78', 'RMB (x 312.78) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30006', 'donate_and_gift', '', 'gift_666', '231', 'gift_666 (x 231) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30007', 'donate_and_gift', '', 'gift_666', '851', 'gift_666 (x 851) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30008', 'donate_and_gift', '', 'gift_plane', '331', 'gift_plane (x 331) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30009', 'donate_and_gift', '', 'gift_plane', '393', 'gift_plane (x 393) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30010', 'donate_and_gift', '', 'gift_plane', '443', 'gift_plane (x 443) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30011', 'donate_and_gift', '', 'gift_car', '72', 'gift_car (x 72) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30012', 'donate_and_gift', '', 'gift_666', '423', 'gift_666 (x 423) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30013', 'donate_and_gift', '', 'gift_car', '739', 'gift_car (x 739) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30014', 'donate_and_gift', '', 'gift_plane', '837', 'gift_plane (x 837) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30015', 'donate_and_gift', '', 'USD', '30.88', 'USD (x 30.88) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30016', 'donate_and_gift', '', 'gift_plane', '827', 'gift_plane (x 827) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30017', 'donate_and_gift', '', 'gift_666', '252', 'gift_666 (x 252) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30018', 'donate_and_gift', '', 'RMB', '450.11', 'RMB (x 450.11) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30019', 'donate_and_gift', '', 'gift_666', '454', 'gift_666 (x 454) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30020', 'donate_and_gift', '', 'gift_car', '603', 'gift_car (x 603) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30021', 'donate_and_gift', '', 'RMB', '949.18', 'RMB (x 949.18) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30022', 'donate_and_gift', '', 'USD', '131.56', 'USD (x 131.56) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30023', 'donate_and_gift', '', 'gift_666', '845', 'gift_666 (x 845) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30024', 'donate_and_gift', '', 'USD', '944.22', 'USD (x 944.22) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30025', 'donate_and_gift', '', 'gift_car', '322', 'gift_car (x 322) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30026', 'donate_and_gift', '', 'gift_plane', '167', 'gift_plane (x 167) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30027', 'donate_and_gift', '', 'gift_car', '729', 'gift_car (x 729) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30028', 'donate_and_gift', '', 'USD', '511.35', 'USD (x 511.35) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30029', 'donate_and_gift', '', 'gift_car', '3', 'gift_car (x 3) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30030', 'donate_and_gift', '', 'gift_plane', '858', 'gift_plane (x 858) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30031', 'donate_and_gift', '', 'gift_666', '802', 'gift_666 (x 802) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30032', 'donate_and_gift', '', 'gift_plane', '779', 'gift_plane (x 779) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30033', 'donate_and_gift', '', 'gift_666', '93', 'gift_666 (x 93) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30034', 'donate_and_gift', '', 'USD', '527.66', 'USD (x 527.66) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30035', 'donate_and_gift', '', 'gift_plane', '615', 'gift_plane (x 615) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30036', 'donate_and_gift', '', 'RMB', '620.64', 'RMB (x 620.64) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30037', 'donate_and_gift', '', 'RMB', '543.63', 'RMB (x 543.63) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30038', 'donate_and_gift', '', 'gift_car', '186', 'gift_car (x 186) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30039', 'donate_and_gift', '', 'RMB', '976.49', 'RMB (x 976.49) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30040', 'donate_and_gift', '', 'gift_car', '750', 'gift_car (x 750) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30041', 'donate_and_gift', '', 'USD', '334.28', 'USD (x 334.28) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30042', 'donate_and_gift', '', 'gift_666', '340', 'gift_666 (x 340) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30043', 'donate_and_gift', '', 'USD', '523.57', 'USD (x 523.57) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30044', 'donate_and_gift', '', 'RMB', '309.61', 'RMB (x 309.61) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30045', 'donate_and_gift', '', 'gift_car', '839', 'gift_car (x 839) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30046', 'donate_and_gift', '', 'USD', '144.59', 'USD (x 144.59) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30047', 'donate_and_gift', '', 'RMB', '530.11', 'RMB (x 530.11) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30048', 'donate_and_gift', '', 'gift_car', '355', 'gift_car (x 355) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30049', 'donate_and_gift', '', 'gift_car', '691', 'gift_car (x 691) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30050', 'donate_and_gift', '', 'gift_plane', '598', 'gift_plane (x 598) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30051', 'donate_and_gift', '', 'gift_car', '418', 'gift_car (x 418) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30052', 'donate_and_gift', '', 'gift_666', '874', 'gift_666 (x 874) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30053', 'donate_and_gift', '', 'RMB', '61.03', 'RMB (x 61.03) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30054', 'donate_and_gift', '', 'USD', '358.87', 'USD (x 358.87) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30055', 'donate_and_gift', '', 'gift_plane', '302', 'gift_plane (x 302) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30056', 'donate_and_gift', '', 'gift_plane', '487', 'gift_plane (x 487) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30057', 'donate_and_gift', '', 'gift_666', '966', 'gift_666 (x 966) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30058', 'donate_and_gift', '', 'gift_plane', '560', 'gift_plane (x 560) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30059', 'donate_and_gift', '', 'USD', '715.92', 'USD (x 715.92) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30060', 'donate_and_gift', '', 'gift_666', '813', 'gift_666 (x 813) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30061', 'donate_and_gift', '', 'USD', '699.62', 'USD (x 699.62) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30062', 'donate_and_gift', '', 'RMB', '591.99', 'RMB (x 591.99) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30063', 'donate_and_gift', '', 'RMB', '447.71', 'RMB (x 447.71) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30064', 'donate_and_gift', '', 'gift_plane', '754', 'gift_plane (x 754) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30065', 'donate_and_gift', '', 'gift_666', '246', 'gift_666 (x 246) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30066', 'donate_and_gift', '', 'RMB', '986.1', 'RMB (x 986.1) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30067', 'donate_and_gift', '', 'USD', '862.48', 'USD (x 862.48) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30068', 'donate_and_gift', '', 'USD', '432.62', 'USD (x 432.62) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30069', 'donate_and_gift', '', 'gift_666', '70', 'gift_666 (x 70) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30070', 'donate_and_gift', '', 'gift_car', '857', 'gift_car (x 857) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30071', 'donate_and_gift', '', 'USD', '281.27', 'USD (x 281.27) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30072', 'donate_and_gift', '', 'gift_car', '388', 'gift_car (x 388) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30073', 'donate_and_gift', '', 'RMB', '646.35', 'RMB (x 646.35) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30074', 'donate_and_gift', '', 'gift_666', '827', 'gift_666 (x 827) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30075', 'donate_and_gift', '', 'gift_car', '64', 'gift_car (x 64) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30076', 'donate_and_gift', '', 'gift_666', '273', 'gift_666 (x 273) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30077', 'donate_and_gift', '', 'USD', '956.44', 'USD (x 956.44) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30078', 'donate_and_gift', '', 'gift_plane', '244', 'gift_plane (x 244) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30079', 'donate_and_gift', '', 'USD', '884.75', 'USD (x 884.75) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30080', 'donate_and_gift', '', 'RMB', '585.25', 'RMB (x 585.25) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30081', 'donate_and_gift', '', 'gift_plane', '548', 'gift_plane (x 548) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30082', 'donate_and_gift', '', 'gift_car', '61', 'gift_car (x 61) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30083', 'donate_and_gift', '', 'gift_plane', '950', 'gift_plane (x 950) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30084', 'donate_and_gift', '', 'gift_666', '191', 'gift_666 (x 191) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30085', 'donate_and_gift', '', 'USD', '662.96', 'USD (x 662.96) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30086', 'donate_and_gift', '', 'gift_car', '799', 'gift_car (x 799) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30087', 'donate_and_gift', '', 'gift_666', '875', 'gift_666 (x 875) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30088', 'donate_and_gift', '', 'gift_car', '772', 'gift_car (x 772) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30089', 'donate_and_gift', '', 'RMB', '956.04', 'RMB (x 956.04) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30090', 'donate_and_gift', '', 'gift_car', '43', 'gift_car (x 43) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30091', 'donate_and_gift', '', 'gift_plane', '751', 'gift_plane (x 751) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30092', 'donate_and_gift', '', 'USD', '736.59', 'USD (x 736.59) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30093', 'donate_and_gift', '', 'gift_666', '185', 'gift_666 (x 185) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30094', 'donate_and_gift', '', 'gift_car', '897', 'gift_car (x 897) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30095', 'donate_and_gift', '', 'RMB', '960.84', 'RMB (x 960.84) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30096', 'donate_and_gift', '', 'USD', '696.9', 'USD (x 696.9) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30097', 'donate_and_gift', '', 'gift_car', '264', 'gift_car (x 264) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30098', 'donate_and_gift', '', 'USD', '971.73', 'USD (x 971.73) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30099', 'donate_and_gift', '', 'gift_666', '282', 'gift_666 (x 282) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30100', 'donate_and_gift', '', 'USD', '311.33', 'USD (x 311.33) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30101', 'donate_and_gift', '', 'gift_plane', '852', 'gift_plane (x 852) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30102', 'donate_and_gift', '', 'gift_666', '544', 'gift_666 (x 544) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30103', 'donate_and_gift', '', 'RMB', '105.12', 'RMB (x 105.12) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30104', 'donate_and_gift', '', 'gift_car', '141', 'gift_car (x 141) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30105', 'donate_and_gift', '', 'USD', '515.98', 'USD (x 515.98) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30106', 'donate_and_gift', '', 'gift_666', '172', 'gift_666 (x 172) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30107', 'donate_and_gift', '', 'gift_car', '520', 'gift_car (x 520) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30108', 'donate_and_gift', '', 'gift_666', '826', 'gift_666 (x 826) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30109', 'donate_and_gift', '', 'gift_666', '907', 'gift_666 (x 907) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30110', 'donate_and_gift', '', 'gift_plane', '496', 'gift_plane (x 496) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30111', 'donate_and_gift', '', 'gift_car', '161', 'gift_car (x 161) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30112', 'donate_and_gift', '', 'gift_plane', '633', 'gift_plane (x 633) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30113', 'donate_and_gift', '', 'USD', '970.74', 'USD (x 970.74) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30114', 'donate_and_gift', '', 'gift_plane', '363', 'gift_plane (x 363) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30115', 'donate_and_gift', '', 'gift_666', '25', 'gift_666 (x 25) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30116', 'donate_and_gift', '', 'gift_car', '326', 'gift_car (x 326) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30117', 'donate_and_gift', '', 'USD', '585.23', 'USD (x 585.23) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30118', 'donate_and_gift', '', 'gift_car', '603', 'gift_car (x 603) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30119', 'donate_and_gift', '', 'gift_plane', '266', 'gift_plane (x 266) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30120', 'donate_and_gift', '', 'RMB', '407.78', 'RMB (x 407.78) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30121', 'donate_and_gift', '', 'gift_plane', '75', 'gift_plane (x 75) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30122', 'donate_and_gift', '', 'gift_plane', '864', 'gift_plane (x 864) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30123', 'donate_and_gift', '', 'gift_car', '177', 'gift_car (x 177) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30124', 'donate_and_gift', '', 'gift_plane', '826', 'gift_plane (x 826) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30125', 'donate_and_gift', '', 'gift_plane', '179', 'gift_plane (x 179) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30126', 'donate_and_gift', '', 'gift_plane', '547', 'gift_plane (x 547) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30127', 'donate_and_gift', '', 'gift_plane', '833', 'gift_plane (x 833) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30128', 'donate_and_gift', '', 'USD', '306.19', 'USD (x 306.19) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30129', 'donate_and_gift', '', 'gift_666', '635', 'gift_666 (x 635) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30130', 'donate_and_gift', '', 'gift_666', '887', 'gift_666 (x 887) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30131', 'donate_and_gift', '', 'gift_car', '820', 'gift_car (x 820) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30132', 'donate_and_gift', '', 'gift_666', '173', 'gift_666 (x 173) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30133', 'donate_and_gift', '', 'gift_plane', '866', 'gift_plane (x 866) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30134', 'donate_and_gift', '', 'gift_plane', '411', 'gift_plane (x 411) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30135', 'donate_and_gift', '', 'USD', '181.15', 'USD (x 181.15) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30136', 'donate_and_gift', '', 'gift_plane', '859', 'gift_plane (x 859) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30137', 'donate_and_gift', '', 'RMB', '430.74', 'RMB (x 430.74) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30138', 'donate_and_gift', '', 'USD', '357.88', 'USD (x 357.88) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30139', 'donate_and_gift', '', 'gift_car', '578', 'gift_car (x 578) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30140', 'donate_and_gift', '', 'USD', '766.45', 'USD (x 766.45) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30141', 'donate_and_gift', '', 'gift_car', '501', 'gift_car (x 501) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30142', 'donate_and_gift', '', 'gift_plane', '498', 'gift_plane (x 498) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30143', 'donate_and_gift', '', 'gift_plane', '822', 'gift_plane (x 822) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30144', 'donate_and_gift', '', 'gift_666', '727', 'gift_666 (x 727) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30145', 'donate_and_gift', '', 'USD', '662.48', 'USD (x 662.48) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30146', 'donate_and_gift', '', 'USD', '161.64', 'USD (x 161.64) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30147', 'donate_and_gift', '', 'RMB', '97.61', 'RMB (x 97.61) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30148', 'donate_and_gift', '', 'USD', '810.4', 'USD (x 810.4) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30149', 'donate_and_gift', '', 'RMB', '208.5', 'RMB (x 208.5) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30150', 'donate_and_gift', '', 'gift_car', '679', 'gift_car (x 679) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30151', 'donate_and_gift', '', 'gift_666', '728', 'gift_666 (x 728) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30152', 'donate_and_gift', '', 'RMB', '5.83', 'RMB (x 5.83) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30153', 'donate_and_gift', '', 'gift_car', '664', 'gift_car (x 664) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30154', 'donate_and_gift', '', 'USD', '489.72', 'USD (x 489.72) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30155', 'donate_and_gift', '', 'gift_plane', '444', 'gift_plane (x 444) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30156', 'donate_and_gift', '', 'gift_666', '476', 'gift_666 (x 476) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30157', 'donate_and_gift', '', 'RMB', '395.56', 'RMB (x 395.56) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30158', 'donate_and_gift', '', 'gift_car', '630', 'gift_car (x 630) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30159', 'donate_and_gift', '', 'gift_666', '654', 'gift_666 (x 654) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30160', 'donate_and_gift', '', 'gift_plane', '582', 'gift_plane (x 582) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30161', 'donate_and_gift', '', 'RMB', '515.27', 'RMB (x 515.27) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30162', 'donate_and_gift', '', 'gift_plane', '598', 'gift_plane (x 598) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30163', 'donate_and_gift', '', 'RMB', '455.2', 'RMB (x 455.2) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30164', 'donate_and_gift', '', 'USD', '789.47', 'USD (x 789.47) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30165', 'donate_and_gift', '', 'RMB', '654.2', 'RMB (x 654.2) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30166', 'donate_and_gift', '', 'gift_666', '231', 'gift_666 (x 231) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30167', 'donate_and_gift', '', 'gift_666', '269', 'gift_666 (x 269) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30168', 'donate_and_gift', '', 'gift_666', '31', 'gift_666 (x 31) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30169', 'donate_and_gift', '', 'gift_car', '78', 'gift_car (x 78) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30170', 'donate_and_gift', '', 'USD', '665.26', 'USD (x 665.26) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30171', 'donate_and_gift', '', 'gift_666', '44', 'gift_666 (x 44) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30172', 'donate_and_gift', '', 'RMB', '492.35', 'RMB (x 492.35) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30173', 'donate_and_gift', '', 'gift_666', '81', 'gift_666 (x 81) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30174', 'donate_and_gift', '', 'USD', '585.38', 'USD (x 585.38) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30175', 'donate_and_gift', '', 'RMB', '167.66', 'RMB (x 167.66) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30176', 'donate_and_gift', '', 'RMB', '922.27', 'RMB (x 922.27) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30177', 'donate_and_gift', '', 'gift_666', '91', 'gift_666 (x 91) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30178', 'donate_and_gift', '', 'gift_plane', '704', 'gift_plane (x 704) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30179', 'donate_and_gift', '', 'USD', '955.46', 'USD (x 955.46) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30180', 'donate_and_gift', '', 'RMB', '485.03', 'RMB (x 485.03) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30181', 'donate_and_gift', '', 'gift_666', '338', 'gift_666 (x 338) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30182', 'donate_and_gift', '', 'gift_plane', '595', 'gift_plane (x 595) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30183', 'donate_and_gift', '', 'RMB', '192.8', 'RMB (x 192.8) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30184', 'donate_and_gift', '', 'gift_car', '357', 'gift_car (x 357) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30185', 'donate_and_gift', '', 'RMB', '719.07', 'RMB (x 719.07) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30186', 'donate_and_gift', '', 'gift_666', '737', 'gift_666 (x 737) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30187', 'donate_and_gift', '', 'gift_car', '745', 'gift_car (x 745) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30188', 'donate_and_gift', '', 'RMB', '369.48', 'RMB (x 369.48) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30189', 'donate_and_gift', '', 'RMB', '733.4', 'RMB (x 733.4) ps:DEF');
INSERT INTO `msg_donate_and_gift` VALUES ('30190', 'donate_and_gift', '', 'gift_plane', '27', 'gift_plane (x 27) ps:AAA');
INSERT INTO `msg_donate_and_gift` VALUES ('30191', 'donate_and_gift', '', 'gift_666', '75', 'gift_666 (x 75) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30192', 'donate_and_gift', '', 'gift_666', '699', 'gift_666 (x 699) ps:ASD');
INSERT INTO `msg_donate_and_gift` VALUES ('30193', 'donate_and_gift', '', 'RMB', '579.46', 'RMB (x 579.46) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30194', 'donate_and_gift', '', 'USD', '203.68', 'USD (x 203.68) ps:ABC');
INSERT INTO `msg_donate_and_gift` VALUES ('30195', 'donate_and_gift', '', 'RMB', '223.26', 'RMB (x 223.26) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30196', 'donate_and_gift', '', 'RMB', '221.8', 'RMB (x 221.8) ps:BBB');
INSERT INTO `msg_donate_and_gift` VALUES ('30197', 'donate_and_gift', '', 'gift_plane', '777', 'gift_plane (x 777) ps:CCC');
INSERT INTO `msg_donate_and_gift` VALUES ('30198', 'donate_and_gift', '', 'gift_plane', '907', 'gift_plane (x 907) ps:QWE');
INSERT INTO `msg_donate_and_gift` VALUES ('30199', 'donate_and_gift', '', 'gift_666', '324', 'gift_666 (x 324) ps:QWE');

-- ----------------------------
-- Table structure for player_aodian_config
-- ----------------------------
DROP TABLE IF EXISTS `player_aodian_config`;
CREATE TABLE `player_aodian_config` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `player_type` varchar(16) NOT NULL,
  `rtmpUrl` varchar(128) NOT NULL,
  `hlsUrl` varchar(128) NOT NULL,
  `autostart` smallint(6) NOT NULL,
  `bufferlength` smallint(6) NOT NULL,
  `maxbufferlength` smallint(6) NOT NULL,
  `stretching` smallint(6) NOT NULL,
  `controlbardisplay` varchar(16) NOT NULL,
  `defvolume` smallint(6) NOT NULL,
  `adveDeAddr` varchar(128) NOT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of player_aodian_config
-- ----------------------------
INSERT INTO `player_aodian_config` VALUES ('101', 'aodianplayer', 'rtmp://13830.lssplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9', 'http://13830.hlsplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9.m3u8', '1', '1', '1', '1', 'enable', '80', 'http://static.douyalive.com/aae/dyy/assets/img/play_bj.png');
INSERT INTO `player_aodian_config` VALUES ('102', 'aodianplayer', 'rtmp://13830.lssplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9', 'http://13830.hlsplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9.m3u8', '1', '1', '1', '1', 'enable', '80', 'http://static.douyalive.com/aae/dyy/assets/img/play_bj.png');
INSERT INTO `player_aodian_config` VALUES ('103', 'aodianplayer', 'rtmp://13830.lssplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9', 'http://13830.hlsplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9.m3u8', '1', '1', '1', '1', 'enable', '80', 'http://static.douyalive.com/aae/dyy/assets/img/play_bj.png');
INSERT INTO `player_aodian_config` VALUES ('104', 'aodianplayer', 'rtmp://13830.lssplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9', 'http://13830.hlsplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9.m3u8', '1', '1', '1', '1', 'enable', '80', 'http://static.douyalive.com/aae/dyy/assets/img/play_bj.png');
INSERT INTO `player_aodian_config` VALUES ('105', 'aodianplayer', 'rtmp://13830.lssplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9', 'http://13830.hlsplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9.m3u8', '1', '1', '1', '1', 'enable', '80', 'http://static.douyalive.com/aae/dyy/assets/img/play_bj.png');

-- ----------------------------
-- Table structure for player_mps_config
-- ----------------------------
DROP TABLE IF EXISTS `player_mps_config`;
CREATE TABLE `player_mps_config` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `player_type` varchar(16) NOT NULL,
  `uin` int(11) NOT NULL,
  `appId` varchar(32) NOT NULL,
  `autostart` smallint(6) NOT NULL,
  `stretching` smallint(6) NOT NULL,
  `mobilefullscreen` smallint(6) NOT NULL,
  `controlbardisplay` varchar(16) NOT NULL,
  `isclickplay` smallint(6) NOT NULL,
  `isfullscreen` smallint(6) NOT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of player_mps_config
-- ----------------------------
INSERT INTO `player_mps_config` VALUES ('101', 'mpsplayer', '13830', 'fHNNBuuB3BbUWJiP', '1', '1', '0', 'enable', '1', '1');
INSERT INTO `player_mps_config` VALUES ('102', 'mpsplayer', '13830', 'fHNNBuuB3BbUWJiP', '1', '1', '0', 'enable', '1', '1');
INSERT INTO `player_mps_config` VALUES ('103', 'mpsplayer', '13830', 'fHNNBuuB3BbUWJiP', '1', '1', '0', 'enable', '1', '1');
INSERT INTO `player_mps_config` VALUES ('104', 'mpsplayer', '13830', 'fHNNBuuB3BbUWJiP', '1', '1', '0', 'enable', '1', '1');
INSERT INTO `player_mps_config` VALUES ('105', 'mpsplayer', '13830', 'fHNNBuuB3BbUWJiP', '1', '1', '0', 'enable', '1', '1');

-- ----------------------------
-- Table structure for tab_item_config
-- ----------------------------
DROP TABLE IF EXISTS `tab_item_config`;
CREATE TABLE `tab_item_config` (
  `content_tab_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(16) NOT NULL,
  `new_msg` smallint(6) NOT NULL,
  `component` varchar(16) NOT NULL,
  PRIMARY KEY (`content_tab_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tab_item_config
-- ----------------------------
