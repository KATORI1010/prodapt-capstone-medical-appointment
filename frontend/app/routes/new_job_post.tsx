import { useEffect, useRef, useState } from "react";

import { userContext } from "~/context";
import { Form, Link, redirect, useActionData, type ClientLoaderFunctionArgs } from "react-router";
import type { Route } from "../+types/root";

import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { Textarea } from "~/components/ui/textarea";


export async function clientLoader({ context }: ClientLoaderFunctionArgs) {
    const me = context.get(userContext);
    const isAdmin = me && me.is_admin;
    return isAdmin ? {} : redirect("/job-boards");
}

export async function clientAction({ request, params }: Route.ClientActionArgs) {
    const formData = await request.formData();
    const reviewed = formData.get("reviewed");

    if (reviewed === "false") {
        const response = await fetch("/api/review-job-description", {
            method: "POST",
            body: formData,
        })
        const result = await response.json()
        return result
    } else {
        await fetch("/api/job-posts", {
            method: "POST",
            body: formData,
        })
        return redirect(`/job-boards/${params.jobBoardId}/job-posts`)
    }
}


export default function NewJobPostForm({ params }: Route.ComponentProps) {
    const [reviewed, setReviewed] = useState(false);
    const [summary, setSummary] = useState("");
    const [revisedDescription, setRevisedDescription] = useState("");

    const descriptionRef = useRef(null);

    const actionData = useActionData();

    useEffect(() => {
        if (actionData?.overall_summary) {
            setReviewed(true);
            console.log(actionData?.overall_summary);
            setSummary(actionData?.overall_summary);
            setRevisedDescription(actionData?.revised_description)
        }
    }, [actionData])

    const handleFixButton = () => {
        descriptionRef.current.value = revisedDescription;
    };

    return (
        <div className="w-full max-w-xl mx-auto m-8">
            <Form method="post" encType="multipart/form-data">
                <FieldGroup>
                    <FieldLegend>
                        <h1 className="scroll-m-20 text-center text-3xl font-bold tracking-tight text-balance">
                            New Job
                        </h1>
                    </FieldLegend>
                    <Field>
                        <Input
                            id="job_board_id"
                            name="job_board_id"
                            type="hidden"
                            value={params.jobBoardId}
                            required
                        />
                        <Input
                            id="reviewed"
                            name="reviewed"
                            type="hidden"
                            value={reviewed.toString()}
                            required
                        />
                        <FieldLabel htmlFor="title">
                            Title
                        </FieldLabel>
                        <Input
                            id="title"
                            name="title"
                            placeholder="Azure Expert"
                            required
                        />
                    </Field>
                    <Field>
                        <FieldLabel htmlFor="description">
                            Description
                        </FieldLabel>
                        <Textarea ref={descriptionRef} placeholder="Type job description here." id="description" name="description" className="min-h-30" required />
                    </Field>
                    {reviewed &&
                        <Field>
                            <FieldLabel htmlFor="overall_summary">
                                Reviewed Summary
                            </FieldLabel>
                            <Textarea id="overall_summary" name="overall_summary" className="min-h-30" value={summary} required />
                        </Field>
                    }
                    <div className="float-right">
                        <Field orientation="horizontal">
                            <Button type="submit" className="cursor-pointer">
                                {reviewed ? "Submit" : "Review"}
                            </Button>
                            {reviewed &&
                                <Button type="button" className="cursor-pointer" onClick={handleFixButton}>
                                    Fix for me
                                </Button>
                            }
                            <Button variant="outline" type="button">
                                <Link to={`/job-boards/${params.jobBoardId}/job-posts`}>Cancel</Link>
                            </Button>
                        </Field>
                    </div>
                </FieldGroup>
            </Form>
        </div>
    );
}