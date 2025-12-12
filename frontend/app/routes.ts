import { layout, route, type RouteConfig } from "@react-router/dev/routes";

export default [
    layout("layouts/default.tsx", [
        route("/", "routes/home.tsx"),
        route("/appointment/:appointmentId/medical-initial-form", "routes/medical_initial_form.tsx"),
        route("/appointment/:appointmentId/medical-interview", "routes/medical_interview.tsx"),
        // route("job-boards/new", "routes/new_job_board.tsx"),
        // route("job-boards/:jobBoardId/edit", "routes/edit_job_board.tsx"),
        // route("job-boards/:jobBoardId/job-posts", "routes/job_posts.tsx"),
        // route("job-boards/:jobBoardId/add-job", "routes/new_job_post.tsx"),
        // route("job-boards/:jobBoardId/job-posts/:jobPostId", "routes/job_posts_detail.tsx"),
        // route("job-boards/:jobBoardId/job-posts/:jobPostId/add-application", "routes/new_job_application.tsx"),
        // route("/admin-login", "routes/admin_login_form.tsx"),
        // route("/admin-logout", "routes/admin_logout.tsx"),
        // route("/suggest", "routes/suggest_weekend.tsx"),
    ])
] satisfies RouteConfig;