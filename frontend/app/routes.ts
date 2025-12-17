import { layout, route, type RouteConfig } from "@react-router/dev/routes";

export default [
    layout("layouts/default.tsx", [
        route("/", "routes/home.tsx"),
        route("/appointment/:appointmentId/medical-initial-form", "routes/medical_initial_form.tsx"),
        route("/appointment/:appointmentId/medical-interview/:interviewId", "routes/medical_interview.tsx"),
    ])
] satisfies RouteConfig;