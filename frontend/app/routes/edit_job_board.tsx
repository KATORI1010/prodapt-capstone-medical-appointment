import type { Route } from "../+types/root";
import { Form, Link, redirect } from "react-router";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";

export async function clientLoader({ request, params }: Route.ClientLoaderArgs) {
    const res = await fetch(`/api/job-boards/${params.jobBoardId}`);
    const jobBoard = await res.json();
    return { jobBoard }
}

export async function clientAction({ request }: Route.ClientActionArgs) {
    const formData = await request.formData();
    const jobBoardId = formData.get("job_board_id");
    console.log(formData.get("logo"))
    await fetch(`/api/job-boards/${jobBoardId}`, {
        method: "PUT",
        body: formData,
    })
    return redirect("/job-boards")
}


export default function EditJobBoardForm({ loaderData }: Route.ComponentProps) {
    return (
        <div className="w-full max-w-md mx-auto m-8">
            <Form method="post" encType="multipart/form-data">
                <FieldGroup>
                    <div className="flex justify-between items-center">
                        <FieldLegend>
                            <h1 className="scroll-m-20 text-3xl font-bold tracking-tight text-balance">
                                Edit Job Board
                            </h1>
                        </FieldLegend>
                        <img src={loaderData.jobBoard.logo_url} alt="Logo" className="w-30" />
                    </div>
                    <Field>
                        <FieldLabel htmlFor="slug">
                            Slug
                        </FieldLabel>
                        <Input
                            id="slug"
                            name="slug"
                            defaultValue={loaderData.jobBoard.slug}
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
                        // required
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
                <input name="job_board_id" type="hidden" value={loaderData.jobBoard.id}></input>
            </Form>
        </div>
    );
}