import { Form, Link, redirect, useFetcher, type ClientLoaderFunctionArgs } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { suggestContext } from "~/context";


// export async function clientLoader({ context }: ClientLoaderFunctionArgs) {
//     const me = context.get(userContext);
//     const isAdmin = me && me.is_admin;
//     return isAdmin ? {} : redirect("/job-boards");
// }

export async function clientAction({ request, context }: Route.ClientActionArgs) {
    const formData = await request.formData();
    const response = await fetch("/suggestion/chennai-weekend", {
        method: "POST",
        body: formData,
    })
    const suggestion = await response.json()
    return { result: suggestion };
}


export default function SeggestChennaiWeekend() {
    const fetcher = useFetcher<{ result?: any; error?: string }>();

    return (
        <div className="flex flex-col items-center">
            <div className="pt-8 pb-12">
                <h1 className="scroll-m-20 text-center text-4xl font-extrabold tracking-tight text-balance">
                    Suggest Chennai Weekend
                </h1>
            </div>
            <div className="w-full max-w-md">
                {/* <Form method="post" encType="multipart/form-data"> */}
                <fetcher.Form method="post" encType="multipart/form-data">
                    <FieldGroup>
                        <Field>
                            <FieldLabel htmlFor="target_date">
                                Target Date
                            </FieldLabel>
                            <Input
                                id="target_date"
                                name="target_date"
                                type="date"
                                placeholder=""
                                required
                            />
                        </Field>
                        <Field>
                            <FieldLabel htmlFor="user_profile">
                                User Profile
                            </FieldLabel>
                            <Input
                                id="user_profile"
                                name="user_profile"
                                type="text"
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
                {/* </Form> */}
                </fetcher.Form>
            </div>
            {fetcher.data?.result
                ? (<div>{fetcher.data?.result}Hello</div>)
                : <></>}
        </div>
    );
}