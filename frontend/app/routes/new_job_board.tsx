import { Form, Link, redirect, type ClientLoaderFunctionArgs } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { userContext } from "~/context";


export async function clientLoader({ context }: ClientLoaderFunctionArgs) {
    const me = context.get(userContext);
    const isAdmin = me && me.is_admin;
    return isAdmin ? {} : redirect("/job-boards");
}

export async function clientAction({ request }: Route.ClientActionArgs) {
    const formData = await request.formData();
    await fetch("/api/job-boards", {
        method: "POST",
        body: formData,
    })
    return redirect("/job-boards")
}


export default function NewJobBoardForm(_: Route.ComponentProps) {
    return (
        <div className="w-full max-w-md mx-auto m-8">
            <Form method="post" encType="multipart/form-data">
                <FieldGroup>
                    <FieldLegend>
                        <h1 className="scroll-m-20 text-center text-3xl font-bold tracking-tight text-balance">
                            New Job Board
                        </h1>
                    </FieldLegend>
                    <Field>
                        <FieldLabel htmlFor="slug">
                            Slug
                        </FieldLabel>
                        <Input
                            id="slug"
                            name="slug"
                            placeholder="acme"
                            required
                        />
                    </Field>
                    <Field>
                        <FieldLabel htmlFor="logo">
                            Logo
                        </FieldLabel>
                        <Input
                            id="logo"
                            name="logo"
                            type="file"
                            required
                        />
                    </Field>
                    <div className="float-right">
                        <Field orientation="horizontal">
                            <Button type="submit">Submit</Button>
                            <Button variant="outline" type="button">
                                <Link to="/job-boards">Cancel</Link>
                            </Button>
                        </Field>
                    </div>
                </FieldGroup>
            </Form>
        </div>
    );
}