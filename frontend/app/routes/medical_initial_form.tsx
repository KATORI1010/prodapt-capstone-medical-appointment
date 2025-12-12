import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";

import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { Textarea } from "~/components/ui/textarea";


export async function clientAction({ request, params }: Route.ClientActionArgs) {
    const formData = await request.formData();
    // await fetch("/api/job-applications", {
    //     method: "POST",
    //     body: formData,
    // })
    alert(formData);
    return redirect(`/appointment/${params.appointmentId}/medical-interview`)
}


export default function MedicalForm({ params }: Route.ComponentProps) {
    return (
        <div className="w-full max-w-xl mx-auto m-8">
            <Form method="post" encType="multipart/form-data">
                <FieldGroup>
                    <FieldLegend>
                        <h1 className="scroll-m-20 text-center text-3xl font-bold tracking-tight text-balance">
                            What can I help you with?
                        </h1>
                    </FieldLegend>
                    <Field>
                        <Textarea
                            placeholder="Feel free to write down any concerns or worries you'd like to discuss."
                            id="consultation"
                            name="consultation"
                            className="min-h-60"
                            required
                        />
                    </Field>
                    <div className="float-right">
                        <Field orientation="horizontal">
                            <Button type="submit" className="cursor-pointer">
                                Next
                            </Button>
                            <Button variant="outline" type="button">
                                <Link to="/">Cancel</Link>
                            </Button>
                        </Field>
                    </div>
                </FieldGroup>
            </Form>
        </div>
    );
}