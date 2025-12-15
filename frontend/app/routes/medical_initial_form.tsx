import { useRef } from "react";

import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";

import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { Textarea } from "~/components/ui/textarea";


const intakeFreeTextSamples: string[] = [
    "I’ve been having a dull headache on and off for about a week. It usually starts in the afternoon and gets worse if I look at screens too long. No nausea, but I feel a bit tired lately.",
    "My throat has been sore since two days ago, and I also have a runny nose. It feels worse in the morning. I don’t have a high fever, but I feel slightly warm sometimes.",
    "I noticed some pain in my lower back after lifting heavy boxes last weekend. It’s not sharp, more like a constant ache. It hurts more when I bend or stand up after sitting for a while.",
    "I’ve been coughing a lot, mostly at night. It started maybe 10 days ago. Sometimes I feel short of breath, but it goes away after a few minutes. I’m not sure if it’s allergies or something else.",
    "For the past few months, I’ve had occasional stomach discomfort, especially after eating greasy food. It’s not very painful, just uncomfortable and bloated. No vomiting, but sometimes mild diarrhea.",
    "2週間ほど前から微熱が続いており、3日前の朝に急に下半身が痺れてしまいました。"
];


export async function clientAction({ request, params }: Route.ClientActionArgs) {
    const formData = await request.formData();
    const response = await fetch("/api/medical_interviews", {
        method: "POST",
        body: formData,
    })
    const result = await response.json()
    return redirect(`/appointment/${params.appointmentId}/medical-interview/${result.id}`)
}


export default function MedicalForm({ params }: Route.ComponentProps) {
    const textAreaRef = useRef(null);

    const insertSampleHandler = () => {
        textAreaRef.current.value = intakeFreeTextSamples[Math.floor(Math.random() * intakeFreeTextSamples.length)];
    }

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
                        <Input
                            id="appointment_id"
                            name="appointment_id"
                            type="hidden"
                            value={params.appointmentId}
                            required
                        />
                        <Textarea
                            ref={textAreaRef}
                            placeholder="Feel free to write down any concerns or worries you'd like to discuss."
                            id="initial_consult"
                            name="initial_consult"
                            className="min-h-60"
                            required
                        />
                    </Field>
                    <div className="flex justify-between">
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
                        <Button type="button" className="cursor-pointer" onClick={insertSampleHandler}>
                            Insert Sample
                        </Button>
                    </div>
                </FieldGroup>
            </Form>
        </div>
    );
}