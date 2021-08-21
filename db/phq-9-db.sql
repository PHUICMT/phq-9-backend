CREATE TABLE `questionnaire` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `emotion` json,
  `created_at` timestamp
);

CREATE TABLE `videos` (
  `id` int PRIMARY KEY,
  `questionnaire_id` int,
  `video_name` varchar(255),
  `video_type` boolean
);

ALTER TABLE `videos` ADD FOREIGN KEY (`questionnaire_id`) REFERENCES `questionnaire` (`id`);
