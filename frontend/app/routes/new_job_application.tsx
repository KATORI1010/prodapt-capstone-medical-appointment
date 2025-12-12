import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";

import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";


export async function clientAction({ request, params }: Route.ClientActionArgs) {
    const formData = await request.formData();
    await fetch("/api/job-applications", {
        method: "POST",
        body: formData,
    })
    return redirect(`/job-boards/${params.jobBoardId}/job-posts/${params.jobPostId}`)
}


export default function NewJobPostForm({ params }: Route.ComponentProps) {
    return (
        <div className="w-full max-w-xl mx-auto m-8">
            <Form method="post" encType="multipart/form-data">
                <FieldGroup>
                    <FieldLegend>
                        <h1 className="scroll-m-20 text-center text-3xl font-bold tracking-tight text-balance">
                            New Application
                        </h1>
                    </FieldLegend>
                    <Input
                        id="job_post_id"
                        name="job_post_id"
                        type="hidden"
                        value={params.jobPostId}
                        required
                    />
                    <Field>
                        <FieldLabel htmlFor="first_name">
                            First Name
                        </FieldLabel>
                        <Input
                            id="first_name"
                            name="first_name"
                            placeholder="Hiroaki"
                            required
                        />
                    </Field>
                    <Field>
                        <FieldLabel htmlFor="last_name">
                            Last Name
                        </FieldLabel>
                        <Input
                            id="last_name"
                            name="last_name"
                            placeholder="Katori"
                            required
                        />
                    </Field>
                    <Field>
                        <FieldLabel htmlFor="email">
                            Email
                        </FieldLabel>
                        <Input
                            id="email"
                            name="email"
                            type="email"
                            placeholder="hiroaki.katori@prodapt.com"
                            required
                        />
                    </Field>
                    <Field>
                        <FieldLabel htmlFor="resume">
                            Resume
                        </FieldLabel>
                        <Input
                            id="resume"
                            name="resume"
                            type="file"
                            accept=".pdf"
                            required
                        />
                    </Field>
                    <div className="float-right">
                        <Field orientation="horizontal">
                            <Button type="submit" className="cursor-pointer">
                                Submit
                            </Button>
                            <Button variant="outline" type="button">
                                <Link to=".." relative="path">Cancel</Link>
                            </Button>
                        </Field>
                    </div>
                </FieldGroup>
            </Form>
        </div>
    );
}