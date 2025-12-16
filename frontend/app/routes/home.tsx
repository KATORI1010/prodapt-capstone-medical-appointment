import type { Route } from "../+types/root";
import { Link, useFetcher } from "react-router";

import { ClipboardPlus, RefreshCcw } from 'lucide-react';
import { Button } from "~/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";


export async function clientLoader({ request, params }: Route.ClientLoaderArgs) {
    const res = await fetch("/api/appointments");
    const appointments = await res.json();
    return { appointments }
}

export async function clientAction({ request, params }: Route.ClientActionArgs) {
    const formData = await request.formData();
    const appointment_id = formData.get("appointment_id");
    await fetch(`/api/appointments/${appointment_id}`, {
        method: "PUT",
        body: formData,
    })
}

export default function Home({ loaderData, params }: Route.ComponentProps) {
    const fetcher = useFetcher();

    return (
        <main className="w-full h-30 text-center">
            <div>
                <h1 className="mt-16 scroll-m-20 text-center text-4xl font-extrabold tracking-tight text-balance">
                    Hiroaki-san, Welcome to Tokyo Hospital
                </h1>
                <p className="leading-7 my-8">
                    Please begin the medical interview below.
                </p>
                <div className="p-4 max-w-5xl mx-auto text-left">
                    <h3 className="scroll-m-20 border-b pb-2 text-2xl font-semibold tracking-tight mt-8">
                        Medical Appointments
                    </h3>
                    <Table className="my-4">
                        <TableHeader>
                            <TableRow>
                                <TableHead className="max-w-sm">ID</TableHead>
                                <TableHead className="max-w-xs">First Name</TableHead>
                                <TableHead className="max-w-xs">Last Name</TableHead>
                                <TableHead className="max-w-xs">Date</TableHead>
                                <TableHead className="max-w-xs">Status</TableHead>
                                <TableHead className="max-w-xs">Action</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {loaderData.appointments.map(
                                (appointment) =>
                                    <TableRow key={appointment.id} className={
                                        appointment.status === "Medical interview required"
                                            ? "bg-yellow-200"
                                            : appointment.status === "Ready for medical examination"
                                                ? "bg-blue-300" : ""}>
                                        <TableCell className="max-w-md truncate">
                                            {appointment.id}
                                        </TableCell>
                                        <TableCell>
                                            {appointment.first_name}
                                        </TableCell>
                                        <TableCell>
                                            {appointment.last_name}
                                        </TableCell>
                                        <TableCell>
                                            {appointment.date}
                                        </TableCell>
                                        <TableCell>
                                            {appointment.status}
                                        </TableCell>
                                        <TableCell>
                                            {appointment.status === "Medical interview required" &&
                                                <Link to={`/appointment/${appointment.id}/medical-initial-form`}>
                                                    <Button size="sm" className="cursor-pointer">
                                                        <ClipboardPlus />
                                                        Medical Interview
                                                    </Button>
                                                </Link>
                                            }
                                            {appointment.status === "Ready for medical examination" &&
                                                <fetcher.Form method="post"
                                                    onSubmit={(event) => {
                                                        const response = confirm(
                                                            `Do you reset the appointment ID "${appointment.id}"?`,
                                                        );
                                                        if (!response) {
                                                            event.preventDefault();
                                                        }
                                                    }}
                                                >
                                                    <input name="appointment_id" type="hidden" value={appointment.id}></input>
                                                    <input name="status" type="hidden" value="Medical interview required"></input>
                                                    <Button type="submit" size="sm" className="cursor-pointer">
                                                        <RefreshCcw />
                                                        Reset for Demo
                                                    </Button>
                                                </fetcher.Form>
                                            }
                                        </TableCell>
                                    </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </div>
            </div>
        </main>
    )
}