import { Link } from "react-router";

import { ClipboardPlus } from 'lucide-react';
import { Button } from "~/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";

const appintmentData = [
    {
        id: 3,
        status: "Medical interview required",
        first_name: "Hiroaki",
        last_name: "Katori",
        date: "2025-12-19 15:30:00"
    },
    {
        id: 2,
        status: "closed",
        first_name: "Hiroaki",
        last_name: "Katori",
        date: "2025-12-02 15:30:00"
    },
    {
        id: 1,
        status: "closed",
        first_name: "Hiroaki",
        last_name: "Katori",
        date: "2025-11-02 15:30:00"
    },
]

export default function Home() {
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
                            {appintmentData.map(
                                (appointment) =>
                                    <TableRow key={appointment.id} className={appointment.status === "Medical interview required" ? "bg-yellow-200" : ""}>
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
                                        </TableCell>
                                    </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </div>
            </div>
            {/* <div className="rounded-2xl border max-w-3xl mx-auto p-8 my-8"><IntakeChat /></div> */}
        </main>
    )
}