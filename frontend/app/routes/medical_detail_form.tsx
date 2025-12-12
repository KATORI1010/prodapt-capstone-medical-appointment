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


export default function MedicalForm({ params }: Route.ComponentProps) {
    return (
        <div className="w-full max-w-xl mx-auto m-8">
            <Form method="post" encType="multipart/form-data">
                <FieldGroup>
                    <FieldLegend>
                        <h1 className="scroll-m-20 text-center text-3xl font-bold tracking-tight text-balance">
                            Medical Form
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
                    {/* Patient & Appointment Basics */}
                    <Field>
                        <FieldLabel htmlFor="preferred_name">Preferred Name (optional)</FieldLabel>
                        <Input id="preferred_name" name="preferred_name" placeholder="Hiro" />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="date_of_birth">Date of Birth</FieldLabel>
                        <Input id="date_of_birth" name="date_of_birth" type="date" required />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="phone">Phone Number</FieldLabel>
                        <Input id="phone" name="phone" type="tel" placeholder="+81 90 1234 5678" required />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="appointment_date">Appointment Date (optional)</FieldLabel>
                        <Input id="appointment_date" name="appointment_date" type="date" />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="visit_type">Visit Type</FieldLabel>
                        <Input
                            id="visit_type"
                            name="visit_type"
                            placeholder="New patient / Follow-up / Annual checkup"
                            required
                        />
                    </Field>

                    {/* Reason for Visit */}
                    <Field>
                        <FieldLabel htmlFor="chief_complaint">Main Reason for Visit (Chief Complaint)</FieldLabel>
                        <Input
                            id="chief_complaint"
                            name="chief_complaint"
                            placeholder="e.g., sore throat, back pain, medication refill"
                            required
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="top_concerns">Top Concerns (up to 3, optional)</FieldLabel>
                        <Input
                            id="top_concerns"
                            name="top_concerns"
                            placeholder="e.g., headache; fatigue; sleep problems"
                        />
                    </Field>

                    {/* Symptom Details (HPI-lite) */}
                    <Field>
                        <FieldLabel htmlFor="symptom_onset">When did it start?</FieldLabel>
                        <Input
                            id="symptom_onset"
                            name="symptom_onset"
                            placeholder="e.g., 3 days ago / 2025-12-01"
                            required
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="symptom_duration">How long has it been going on?</FieldLabel>
                        <Input
                            id="symptom_duration"
                            name="symptom_duration"
                            placeholder="e.g., continuous for 3 days / comes and goes"
                            required
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="symptom_location">Where is it? (Location)</FieldLabel>
                        <Input
                            id="symptom_location"
                            name="symptom_location"
                            placeholder="e.g., left lower back / chest / throat"
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="symptom_severity">Severity (0–10)</FieldLabel>
                        <Input
                            id="symptom_severity"
                            name="symptom_severity"
                            type="number"
                            min="0"
                            max="10"
                            placeholder="0"
                            required
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="symptom_triggers">What makes it better or worse? (optional)</FieldLabel>
                        <Input
                            id="symptom_triggers"
                            name="symptom_triggers"
                            placeholder="e.g., worse when walking; better with rest"
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="associated_symptoms">Other symptoms you noticed (optional)</FieldLabel>
                        <Input
                            id="associated_symptoms"
                            name="associated_symptoms"
                            placeholder="e.g., fever, cough, nausea, dizziness"
                        />
                    </Field>

                    {/* Safety / Urgency (screening) */}
                    <Field>
                        <FieldLabel htmlFor="red_flags">
                            Any severe symptoms right now? (optional)
                        </FieldLabel>
                        <Input
                            id="red_flags"
                            name="red_flags"
                            placeholder="e.g., severe chest pain, trouble breathing, fainting"
                        />
                    </Field>

                    {/* Medications & Allergies */}
                    <Field>
                        <FieldLabel htmlFor="current_medications">
                            Current Medications (include prescriptions, OTC meds, supplements)
                        </FieldLabel>
                        <Input
                            id="current_medications"
                            name="current_medications"
                            placeholder="e.g., Metformin 500mg twice daily; Ibuprofen as needed"
                            required
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="medication_adherence">
                            Are you taking them as prescribed? (optional)
                        </FieldLabel>
                        <Input
                            id="medication_adherence"
                            name="medication_adherence"
                            placeholder="Yes / No / Sometimes (and why)"
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="allergies">
                            Allergies (medications/foods/other) and reaction
                        </FieldLabel>
                        <Input
                            id="allergies"
                            name="allergies"
                            placeholder="e.g., Penicillin — rash; peanuts — swelling"
                            required
                        />
                    </Field>

                    {/* Medical History */}
                    <Field>
                        <FieldLabel htmlFor="medical_conditions">
                            Medical Conditions (optional)
                        </FieldLabel>
                        <Input
                            id="medical_conditions"
                            name="medical_conditions"
                            placeholder="e.g., asthma, high blood pressure, diabetes"
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="surgeries">
                            Past Surgeries / Hospitalizations (optional)
                        </FieldLabel>
                        <Input
                            id="surgeries"
                            name="surgeries"
                            placeholder="e.g., appendectomy in 2018"
                        />
                    </Field>

                    {/* Practical */}
                    <Field>
                        <FieldLabel htmlFor="documents">
                            Documents (optional: referral letter, test results, medication list)
                        </FieldLabel>
                        <Input
                            id="documents"
                            name="documents"
                            type="file"
                            accept=".pdf,.jpg,.jpeg,.png"
                        />
                    </Field>

                    <Field>
                        <FieldLabel htmlFor="notes_for_clinician">
                            Anything else you want the clinician to know? (optional)
                        </FieldLabel>
                        <Input
                            id="notes_for_clinician"
                            name="notes_for_clinician"
                            placeholder="e.g., concerns, questions, goals for today's visit"
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