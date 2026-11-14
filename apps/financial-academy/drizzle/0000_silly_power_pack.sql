CREATE TABLE `readings` (
	`user_id` text NOT NULL,
	`concept_id` text NOT NULL,
	`created_at` text NOT NULL,
	PRIMARY KEY(`user_id`, `concept_id`)
);
--> statement-breakpoint
CREATE TABLE `submissions` (
	`id` text PRIMARY KEY NOT NULL,
	`user_id` text NOT NULL,
	`kind` text NOT NULL,
	`module_id` text,
	`score` integer NOT NULL,
	`passed` integer NOT NULL,
	`result_json` text NOT NULL,
	`created_at` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `submissions_user` ON `submissions` (`user_id`);